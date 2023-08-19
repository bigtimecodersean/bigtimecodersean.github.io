#-------Additional installs for D3--------

#!pip install python-igraph
#!pip install webcolors
#!pip install mplcursors
#!brew install cairo
#!brew install py3cairo
#!brew install cairo pkg-config
#!pip install pycairo

#---------------------

#-------Additional imports for D3--------
from pymdp import utils
from pymdp.agent import Agent
import copy
import statistics
import igraph as ig
from matplotlib.animation import FuncAnimation
import webcolors
import json
import subprocess
import os

#---------------------


import numpy as np
import matplotlib.pyplot as plt

class StemData:
    def __init__(self, seed_cell):
        self.msgs_from_env = []
        self.self_msgs = []
        self.min_efes = []
        self.mean_efes = []
        self.nailed_it = []
        self.nailed_it_trailing = []
        self.num_cells = []
        self.self_efficacies = {"all": {}}
        self.stemnesses = {"avg": {}}
        self.stresses = {"avg": {}}

        self.seed_cell = seed_cell

    def update(self, t, agent, all_agents, a_in, efe):
        if not agent.__repr__() in self.self_efficacies:
            self.self_efficacies[agent.__repr__()] = {}
        self.self_efficacies[agent.__repr__()][t] = agent.self_efficacy()
        if not t in self.self_efficacies["all"]:
            self.self_efficacies["all"][t] = agent.self_efficacy()
        else:
            self.self_efficacies["all"][t] += agent.self_efficacy()

        if not agent.__repr__() in self.stemnesses:
            self.stemnesses[agent.__repr__()] = {}
            self.stresses[agent.__repr__()] = {}
        self.stemnesses[agent.__repr__()][t] = agent.stemness()
        self.stresses[agent.__repr__()][t] = agent.stress
        if not t in self.stemnesses["avg"]:
            self.stemnesses["avg"][t] = agent.stemness() / len(all_agents)
            self.stresses["avg"][t] = agent.stress / len(all_agents)
        else:
            self.stemnesses["avg"][t] += agent.stemness() / len(all_agents)
            self.stresses["avg"][t] += agent.stress / len(all_agents)

        if agent == self.seed_cell:
            self.msgs_from_env.append(agent.message_from(a_in, "env"))
            self.self_msgs.append(agent.message_from(a_in, agent))
            self.mean_efes.append(np.mean(efe))
            self.min_efes.append(min(efe))
            self.num_cells.append(len(all_agents))
            # TODO: Consider having not just expected but actual FE?
            self.nailed_it.append(
                agent.message_from(a_in, "env") == agent.message_from(a_in, agent)
            )
            self.nailed_it_trailing.append(
                float(np.count_nonzero(self.nailed_it[-50:]) / len(self.nailed_it[-50:]))
            )

    def plot_msgs_from_env(self):
        plt.figure(figsize=(10, 4))
        plt.plot(self.msgs_from_env, linewidth=1, label="Message from environment")
        plt.plot(self.self_msgs, linewidth=1, label="Self-message")
        plt.title(f"Messages from environment and from seed cell for seed cell")
        plt.legend()
        plt.show()

    def plot_nailed_it(self, T):
        plt.figure(figsize=(10, 4))
        plt.plot(
            self.nailed_it,
            linewidth=0.25,
            label="Seed cell sent itself same message as environment did?",
        )
        plt.plot(self.nailed_it_trailing, linewidth=1, label="Trailing 50 turns average %")
        plt.plot([0, T], [0.5, 0.5], linewidth=1, label="Reference")
        plt.title(f"Seed cell nailed it?")
        plt.legend(loc=4)
        plt.show()

    def plot_stress(self):

        plt.figure(figsize=(10, 4))
        for ag_repr, sub_d in self.stresses.items():
            plt.plot(sub_d.keys(), sub_d.values(), linewidth=1, label=ag_repr)
        plt.title(f"Stresses")
        plt.legend()
        plt.show()

    def plot_stemness(self):
        plt.figure(figsize=(10, 4))
        for ag_repr, sub_d in self.stemnesses.items():
            plt.plot(sub_d.keys(), sub_d.values(), linewidth=1, label=ag_repr)
        plt.title(f"Stemnesses")
        plt.legend()
        plt.show()

    def plot_num_cells(self):
        plt.figure(figsize=(10, 4))
        plt.plot(self.num_cells, linewidth=2, color="r", label="Number of cells")
        plt.title(f"Number of cells")
        plt.show()

    def plot_efes(self):

        plt.figure(figsize=(10, 4))
        plt.plot(self.min_efes, linewidth=2, color="k", label="Min EFE of seed agent")
        plt.plot(
            self.mean_efes,
            linewidth=1,
            linestyle="dashed",
            color="k",
            label="Mean EFE of seed agent",
        )
        plt.title(f"Expected suffering of seed cell")
        plt.legend()
        plt.show()


class GenModelData:
    def __init__(self):
        self.all_qs = []
        self.all_obs = []
        self.all_qpi = []
        self.all_efe = []
        self.num_agents = {}
        self.all_Bs = []
        self.all_Cs = []

    def check(self, t, all_agents):
        self.num_agents[t] = len(all_agents)
        while len(self.all_qs) < len(all_agents):
            self.all_qs.append({})
        while len(self.all_obs) < len(all_agents):
            self.all_obs.append({})
        while len(self.all_qpi) < len(all_agents):
            self.all_qpi.append({})
        while len(self.all_efe) < len(all_agents):
            self.all_efe.append({})
        while len(self.all_Bs) < len(all_agents):
            self.all_Bs.append({})
        while len(self.all_Cs) < len(all_agents):
            self.all_Cs.append({})

    def update(self, agent_idx, t, B, C, qs, q_pi, efe, a_in):
        self.all_Bs[agent_idx][t] = B
        self.all_Cs[agent_idx][t] = C

        self.all_qs[agent_idx][t] = qs[0]
        self.all_qpi[agent_idx][t] = q_pi
        self.all_efe[agent_idx][t] = efe
        self.all_obs[agent_idx][t] = a_in

#----------------------------------
    def create_d3_JSON(seed_cell, all_agents_before_death, all_inputs_before_death, did_die, did_divide, timestamp):
    
        data_single_timestamp = {
            "nodes": [
            ],
            
            "links": [
            ]
        } 
    
        seed_cell_id = seed_cell.__repr__()
        
        #create a new Env node as a dictionary 
    #     env_node = {
    #         "id": "env",
    #         "class": "env",
    #         "will_die": 0,
    #         "will_divide": 0,
    #         "self_efficacy": 0, 
    #         "self_signal": 0,
    #         "timestamp": timestamp
    #     }

        #append the new node to the "nodes" list in "data_Final"
    #     data_single_timestamp["nodes"].append(env_node)

        agents_dict = {} 
        
        #Add a vertex for every agent: 
        for index, agent in enumerate(all_agents_before_death):
            agents_dict.update({repr(agent): (index, agent)})
            agent_id = agent.__repr__() 
            
            #-----------ADD A NEW NODE TO THE JSON------------
            new_node = {
            "id": agent_id, 
            "class": None, 
            "will_die": None, 
            "will_divide": None, 
            "self_efficacy": None, 
            "self_signal": None,
            "timestamp": timestamp  
            }
            
            #---------------------
            
            new_node["self_efficacy"] = round(agent.self_efficacy(), 2)

            if agent_id in did_die: 
                new_node["will_die"] = 1
                
            else: 
                new_node["will_die"] = 0

            if agent_id in did_divide:     
                new_node["will_divide"] = 1
            else: 
                new_node["will_divide"] = 0 
            
            if agent_id == seed_cell_id: 
                new_node["class"] = "seed" 

            else: 
                new_node["class"] = "non-seed" 
            
            data_single_timestamp["nodes"].append(new_node)
        
        #ADDING EDGES TO THE GRAPH 
        
        #go through every agent in all_agents_before_death OR in data_Final["nodes"] that we just created 
        for agent_index, agent in enumerate(all_agents_before_death):
            
            print(f"id: {agent['id']}")
            print(f"class: {agent['class']}")
            print(f"will die: {agent['will_die']}")
            print(f"will divide: {agent['will_divide']}")
            print(f"self signal: {agent['self_signal']}")
            print(f"timestamp: {agent['timestamp']}")
            
            agent_id = agent.__repr__() 
            
            #check if the node interacts with the environmemnt 
            if agent._interacts_with_environment(): 
                
                #check if the node receives a signal from the environment OR NOT 
                if agent.message_from(all_inputs_before_death[agent_index], 'env'):
                    
                    #add a link between the node and the environment with 1 signal 
                    env_link = {
                            "source": "env",
                            "target": agent_id,
                            "signal": 1, 
                            "timestamp": timestamp
                        }
                        
                    data_single_timestamp["links"].append(env_link) 
                    
                else:  #add a link between the node and the environment with 1 signal 
                    
                    env_link = {
                            "source": "env",
                            "target": agent_id,
                            "signal": 0, 
                            "timestamp": timestamp
                        }
                        
                    data_single_timestamp["links"].append(env_link) 
                                    
            #Loop through all the nodes ("penpals") in agent.penpals
            for penpal_index, penpal in enumerate(agent.penpals):
                
                penpal_id = penpal.__repr__()

                if penpal not in all_agents_before_death:
                    continue 
                
            #check if the agent received a message from penpal 

                if agent.message_from(all_inputs_before_death[agent_index], penpal):
                                    
                    #add a link between the agent and the penpal with 1 signal 
                    new_link = {
                            "source": penpal_id,
                            "target": agent_id,
                            "signal": 1, 
                            "timestamp": timestamp
                        }
                        
                    data_single_timestamp["links"].append(new_link) 
                    
                    if penpal_id == agent_id: 
                        data_single_timestamp["nodes"][agent_index+1]["self_signal"] = 1 

                else:  #add a link between the agent and the penpal with 0 signal 

                    new_link = {
                            "source": penpal_id,
                            "target": agent_id,
                            "signal": 0, 
                            "timestamp": timestamp
                        
                        }
                        
                    data_single_timestamp["links"].append(new_link) 
                    
                    if penpal_id == agent_id: 
                        data_single_timestamp["nodes"][agent_index+1]["self_signal"] = 0 
        
        # (in act inf loop) save JSON output as stemai.d3_visualization.input.json

        return data_single_timestamp
    
    def add_to_d3_visualization_final(d3_visualization_data_final, msgs_from_env, self_msgs, nailed_it, nailed_it_trailing, num_cells, min_efes, mean_efes, self_efficacies, stemnesses, stresses ): 

        modified_msgs_from_env = [1 if item else 0 for item in msgs_from_env]
        modified_self_msgs = [1 if item else 0 for item in self_msgs]
        modified_nailed_it = [1 if item else 0 for item in nailed_it]
        
        #Adding an index 
        modified_msgs_from_env = [{"time": index, "value": value} for index, value in enumerate(modified_msgs_from_env)]
        modified_self_msgs = [{"time": index, "value": value} for index, value in enumerate(modified_self_msgs)]
        modified_nailed_it = [{"time": index, "value": value} for index, value in enumerate(modified_nailed_it)]
        modified_nailed_it_trailing = [{"time": index, "value": value} for index, value in enumerate(nailed_it_trailing)]
        modified_num_cells = [{"time": index, "value": value} for index, value in enumerate(num_cells)]
        modified_min_efes = [{"time": index, "value": value} for index, value in enumerate(min_efes)]
        modified_mean_efes = [{"time": index, "value": value} for index, value in enumerate(mean_efes)]

        d3_visualization_data_final["msgs_from_env"].extend(modified_msgs_from_env)
        d3_visualization_data_final["self_msgs"].extend(modified_self_msgs)
        d3_visualization_data_final["nailed_it"].extend(modified_nailed_it)
        d3_visualization_data_final["nailed_it_trailing"].extend(modified_nailed_it_trailing)
        d3_visualization_data_final["num_cells"].extend(modified_num_cells)
        d3_visualization_data_final["min_efes"].extend(modified_min_efes)
        d3_visualization_data_final["mean_efes"].extend(modified_mean_efes)
        
        d3_visualization_data_final["self_efficacies"] = self_efficacies 
        d3_visualization_data_final["stemnesses"] = stemnesses 
        d3_visualization_data_final["stresses"] = stresses 

    def export_JSON_data(d3_visualization_data_final_JSON): 

        # Get the path to the current directory
        current_directory = os.path.dirname(__file__)

        # Define the path to the output JSON file
        output_folder = os.path.join(current_directory, "..", "..", "d3_visualization") #two folders up? 
        output_file = os.path.join(output_folder, "input.json")

        # Create the output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Write the JSON data to the output JSON file
        with open(output_file, "w") as f:
            json.dump(d3_visualization_data_final_JSON, f, indent=4)
        
    def visualize_d3(): 

        current_directory = os.path.dirname(__file__)
        
        # Navigate to the desired folder
        folder_path = os.path.join(current_directory, "..", "..", "d3_visualization", "demo")
        os.chdir(folder_path)

        # Run the yarn dev command
        command = "yarn dev"
        subprocess.run(command, shell=True)


