import copy
from stemai.core.connected_agent import ConnectedAgent
from stemai.core.dataclass import GenModelData, StemData

COLLAPSE_OUTPUTS = False


def kill_excess_cells(all_agents: list[ConnectedAgent], max_cells: int, seed_cell: ConnectedAgent, did_die: list):
    """kills cells with low efficacy

    If update seed is True, and the seed cell gets killed off, replaces the seed cell with the most
    efficacious cell."""

    sorted_by_efficacy = sorted(all_agents, key=lambda a: -a.self_efficacy())
    sorted_by_efficacy.remove(seed_cell)

    excess_cells = sorted_by_efficacy[
        -len(all_agents) + max_cells :
    ]  # Keep only the most efficacious max_cell cells
    for ec in excess_cells:
        # The following works whereas a list iterator doesn't because we're removing items from the list as it operates
        while len(ec.penpals) > 0:
            ec.bilateral_disconnect_from(ec.penpals[0])
        all_agents.remove(ec)

        #---------------
        #ADD THIS AGENT'S ID TO THE LIST OF DID_DIE 
        did_die.append(ec.__repr__())
        #---------------


    return all_agents, seed_cell


def remove_orphaned_cells(all_agents, seed_cell, did_die: list):
    # print("Removing orphaned cells")
    # Perform autophagy on any orphaned cells which are only connected to themselves or to nobody
    internal_agents = [a for a in all_agents if a != seed_cell]
    while True:
        to_delete = [a for a in internal_agents if len(a.penpals) == 0 or a.penpals == [a]]
        if not to_delete:
            break
        for td in to_delete:
            # print(f"Autophagy! {td}")
            if td.penpals:
                td.bilateral_disconnect_from(td)
            internal_agents.remove(td)
            all_agents.remove(td)

            #------ADD THIS AGENT'S ID TO THE LIST OF DID_DIE---------
            
            did_die.append(td.__repr__())

            #---------------

    return all_agents


def actinf_loop(agent, a_in):
    # print(f"{agent} Received input: {a_in}")

    qs = agent.infer_states([a_in])  # Note this assumes all observations are in obs[0]
    q_pi, efe = agent.infer_policies()
    # agent.unbinarize_B(bb)
    # TODO: Compute an "actual suffering" metric in addition to a predicted one?
    noise = abs((max(agent.C[0]) - agent.C[0][a_in]) / max(agent.C[0]))
    agent.update_B(add_noise=noise)
    chosen_action_id = agent.sample_action()
    agent.update_C(obs=a_in, add_noise=noise)

    return agent, qs, efe


def update_self_efficacies(agent: ConnectedAgent, self_efficacies: dict, t: int):
    if not agent.__repr__() in self_efficacies:
        self_efficacies[agent.__repr__()] = {}
    self_efficacies[agent.__repr__()][t] = agent.self_efficacy()
    if not t in self_efficacies["all"]:
        self_efficacies["all"][t] = agent.self_efficacy()
    else:
        self_efficacies["all"][t] += agent.self_efficacy()

    return self_efficacies


def run_active_inference_loop(all_agents, env, T, d3_visualization_data_final):
    env_obs = env.init_state
    # TODO: Make the initial observation fort the seed cell random
    # TODO: Allow multiple cells, not just the seed cell, to interact with the environment?
    seed_cell = all_agents[0]

    genmodel_data = GenModelData()

    stem_data = StemData(seed_cell)

    for t in range(T):

        #---------------
        #INITIALIZE DID DIE + DID_DIVIDE LISTS AND COPY ALL_AGENTS & ALL_INPUTS 
        
        all_agents_BEFORE_DEATH = copy.copy(all_agents) 
#         all_inputs_BEFORE_DEATH = [a.compute_input(env_obs) for a in all_agents] 
        all_inputs_BEFORE_DEATH = [a.compute_input() for a in all_agents] 

        did_die = []
        did_divide = []
        #----------------

        genmodel_data.check(t, all_agents)

        # Kill excess cells:
        if len(all_agents) > env.max_cells(t):
            all_agents, seed_cell = kill_excess_cells(
                all_agents, env.max_cells(t), seed_cell, did_die
            )
            #---------------


        all_agents = remove_orphaned_cells(all_agents, seed_cell, did_die)

        all_inputs = [a.compute_input(env_obs) for a in all_agents]

        agent_idx = 0
        # Note it's important to copy all_agents since we're modifying all_agents along the way
        for agent, a_in in zip(copy.copy(all_agents), all_inputs):

            # bb = agent.binarize_B()
            qs = agent.infer_states([a_in])  # Note this assumes all observations are in obs[0]

            q_pi, efe = agent.infer_policies()

            genmodel_data.update(agent_idx, t, agent.B, agent.C, qs, q_pi, efe, a_in)

            agent_idx += 1

            nailed_it_this_turn = max(agent.C[0]) == agent.C[0][a_in]

            # update stress
            if not nailed_it_this_turn:
                agent.stress = min(agent.stress + agent.stress_increment, agent.max_stress)
                for p in agent.penpals:
                    if p != agent:
                        p.stress = min(
                            p.stress + (agent.penpal_stress_increment / len(agent.penpals)),
                            agent.max_stress,
                        )

            agent.update_B()

            agent.sample_action()

            agent.update_C()

            agent.stress = max(agent.stress * (1 - agent.stress_relief), agent.min_stress)

            stem_data.update(t, agent, all_agents, a_in, efe)

            if agent == seed_cell:
                env_obs = env.step(agent.message_for("env"), t=t)
            if agent.wants_to_divide() and len(all_agents) < env.max_cells(t):
                # TODO: Make sure it passes the right number to the environment!
                all_agents.insert(0, agent.symmetric_divide()[1])
                assert (p in all_agents for p in agent.penpals)

                #------ADD THIS AGENT"S ID TO LIST OF DID_DIVIDE---------
                did_divide.append(agent.__repr__())
                #---------------

        #-------Adding data for single timestamp to overall data object--------
        data_single_timestamp = stem_data.create_d3_JSON(seed_cell, all_agents_BEFORE_DEATH, all_inputs_BEFORE_DEATH, did_die, did_divide, t)
        d3_visualization_data_final["nodes"].extend(data_single_timestamp["nodes"])
        d3_visualization_data_final["links"].extend(data_single_timestamp["links"])
        #-------------------------------------------------------------------

    return stem_data, genmodel_data, d3_visualization_data_final
