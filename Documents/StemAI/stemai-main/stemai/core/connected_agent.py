import numpy as np
from pymdp import utils
from pymdp.agent import Agent
import copy
from .params import *

class ConnectedAgent(Agent):
    def __init__(
        self,
        penpals=[],
        is_seed_cell=False,
        stem_dim=2,
        logging=False,
        initial_action=0,
        stress_increment=SELF_STRESS_INCREMENT,
        max_stress=MAX_STRESS,
        penpal_stress_increment=ALL_PENPAL_STRESS_INCREMENT,
        stress_relief=STRESS_RELIEF,
        min_stress=MIN_STRESS,
        *args,
        **kwargs,
    ):
        """
        ConnectedAgent class.
        If the agent is_seed_cell, then the agent wants to align with the environment
        Otherwise, the agent wants to align with its parent.

        The agent is initialized with A matrix of shape (env_dim, env_dim)
        Then we do self.add_bilteral_penpal() for each penpal, and the agent itself, which scales the number of states
        to be all combinations of environment, self and penpals."""

        self.is_seed_cell = is_seed_cell
        self.stress_increment = stress_increment
        self.max_stress = max_stress
        self.penpal_stress_increment = penpal_stress_increment
        self.stress_relief = stress_relief
        self.min_stress = min_stress

        A = utils.initialize_empty_A([stem_dim], [stem_dim])
        A[0] = np.eye(stem_dim)
        B = utils.obj_array(1)
        B[0] = np.full((stem_dim, stem_dim, stem_dim), 1.0 / stem_dim)
        pB = utils.dirichlet_like(B, scale=0.1)
        C = utils.obj_array_zeros([stem_dim])
        D = utils.obj_array_uniform([stem_dim])  # TODO: Add learning for D?

        super().__init__(
            A=A,
            B=B,
            pB=pB,
            lr_pB=1.0,
            C=C,
            D=D,
            action_selection="deterministic",
            save_belief_hist=True,
            *args,
            **kwargs,
        )

        self.stem_factor = 1
        self.logging = logging

        self.penpals = []
        self.action = np.array([initial_action])
        [self.add_bilateral_penpal(p) for p in penpals]
        self.add_bilateral_penpal(self)
        self.stress = 0

    def __repr__(self):
        """returns a string representation of the ConnectedAgent object.
        Generates a string that includes the class name (CA) followed by the hexadecimal ID of the object."""
        return f"CA{hex(id(self))[-4:]}"

    def stemness(self):
        """Calculates the stemness, which is the minimum entry
        in the B matrix, divided by the maximum possible entry"""
        max_possible_entry = 1.0 / len(self.B[0])
        min_actual_entry = np.min(self.B[0])
        return min_actual_entry / max_possible_entry

    def adjust_to_stress(self):
        if self.stress > 0:
            self.pB[0] = (
                self.pB[0] * (100 - self.stress) + (np.average(self.pB[0]) * self.stress)
            ) / 100  # Make it stemmier
            self.action_selection = "deterministic"
        else:
            self.pB[0] -= np.average(self.pB[0]) / 10
            self.action_selection = "deterministic"

    def adjust_to_B_mass(self):
        cur_sum_pB = np.sum(self.pB[0])
        if cur_sum_pB >= B_MASS:
            target_sum_pB = B_MASS
            pB_reweight_coefficient = target_sum_pB / cur_sum_pB
            self.pB[0] *= pB_reweight_coefficient
            if self.logging:
                print(f"Mass of pB: {np.sum(self.pB[0])}")

    def determinize_B_cols(self):
        new_B = copy.deepcopy(self.B)
        dim = len(new_B[0])
        # TODO: consider npappply_over_axes to simplify other logic elsewhere

        def sample_f(col):
            if max(col) > 0.9:
                return utils.onehot(np.argmax(col), dim)
            else:
                return col

        new_B[0] = np.apply_along_axis(sample_f, 0, new_B[0])
        self.B = new_B

    def update_B(self, stress_update=True, mass_update=True, onehot_B=True):
        """Updates the agent's B matrix based on the observed outcomes (qs_hist)
        and the learning rate (lr_pB).
        Adjusts the probabilities in the pB matrix by incorporating the observed outcomes
        and applies a smoothing technique to prevent probabilities from becoming too small.

        If stress_update is true, then update pB based on the stress of the agent"""

        # Re-compute B first so I'm not using the binarized version from a previous turn:
        self.B = utils.norm_dist_obj_arr(self.pB)
        dim = len(self.pB[0][:, :, 0])

        if stress_update:
            self.adjust_to_stress()

        if mass_update:
            self.adjust_to_B_mass()

        self.pB[0] = np.maximum(self.pB[0], np.full((dim, dim, dim), 0.05))

        if len(self.qs_hist) > 2:
            super().update_B(self.qs_hist[-2])  # general actinf B update

        if onehot_B and self.stress == 0:
            self.determinize_B_cols()

        return self.pB

    def update_C(self, obs=None, add_noise=0):
        """Updates the agent's C matrix, which represents the agent's preferences or biases.
        Currently, the always aligns with its "parent," whether that's the env or an environment

        """
        if self.is_seed_cell:
            parent_index = 0
        else:
            parent_index = 2

        for i in range(len(self.C[0])):
            if (i & 2 > 0) == (i & int(2**parent_index) > 0):
                self.C[0][i] = 1000
            else:
                self.C[0][i] = 0
        if self.logging:
            print(f"C: {self.C[0]}")

    def _interacts_with_environment(self):
        # if u dont interact w the enviornnment then there is a differnet relationship between # of penpals and size of A
        return len(self.A[0]) > 2 ** len(self.penpals)

    # TODO: Figure out how to check if the penpals have already been added so I don't double-add them!
    def add_bilateral_penpal(self, p):
        """adds a bilateral penpal (connected agent) to the agent's penpal list.
        Updates the agent's A, B, pB, C, D, E, qs, and action matrices accordingly.

        This is done such that the agent maintains what it has learned about its existing penpals"""

        if p in self.penpals:
            return  # For now don't allow a penpal to be added more than once
        # TODO: Delete an old penpal if there are too many, or return True or False?
        for x, y in [[self, p], [p, self]]:
            x.penpals.append(y)

            x.A[0] = np.eye(len(x.A[0]) * 2)
            # increase the dimensionality of A by factor of two (OR ADD A NEW MODALITY)

            for tensor in [x.B, x.pB, x.C, x.D, x.qs]:
                for method in [np.hstack, np.vstack, np.dstack][: len(tensor[0].shape)]:
                    tensor[0] = method([tensor[0], tensor[0]])
                if tensor is not x.pB:
                    tensor /= 2  # TODO: Should this occur for x.pB also?
            x.E = np.hstack([x.E, x.E]) / 2
            x._update_nums()
            if y == self:  # If I'm connecting to myself, don't add another-nother penpal
                break

    def bilateral_disconnect_from(self, p):
        # TODO: Test the heck out of this
        for x, y in [[self, p], [p, self]]:
            s_index = x.penpals.index(y) + x._interacts_with_environment()
            dim = int(len(x.B[0][:, :, 0]) / 2)
            indices = np.arange(dim * 2)
            and_arg = int(dim / (2**s_index))
            first_indices = indices[indices & and_arg == 0]
            second_indices = indices[indices & and_arg != 0]
            x.A[0] = np.eye(dim)
            for tensor in [x.B, x.pB, x.C, x.D, x.qs]:
                first_ix_in = [first_indices] * len(tensor[0].shape)
                second_ix_in = [second_indices] * len(tensor[0].shape)
                first_ix_specific = np.ix_(*first_ix_in)
                # e.g. if tensor shape is 2, first_ix_specific is [first_indices, first_indices]
                second_ix_specific = np.ix_(*second_ix_in)
                tensor[0] = tensor[0][first_ix_specific] + tensor[0][second_ix_specific]
                tensor /= 2 ** (len(tensor[0].shape) - 1)  # TODO: Should this occur for x.pB also?
            x.E = sum(np.hsplit(x.E, 2)) / 2
            x._update_nums()
            cur_action = int(x.action[0])
            new_action = 0
            masks = x._bit_loc_masks("all")
            y_pos = x._bit_locs(y)[0]
            masks = np.delete(masks, y_pos)
            for i, mask in enumerate(masks):
                res = (mask & cur_action > 0) << i
                new_action += res
            x.action[0] = new_action
            x.penpals.remove(y)
            if y == self:  # If I'm disconnecting from myself, don't do it again
                break
        # TODO: See what happens when disconnected cells remain connected to themselves; does it get cancer?

    def _update_nums(self):
        """Updates the dimensions and attributes of the agent,
        such as num_states, num_factors, num_controls, and policies"""
        self.num_states = [self.B[f].shape[0] for f in range(len(self.B))]
        self.num_factors = len(self.num_states)
        self.num_controls = [self.B[f].shape[2] for f in range(self.num_factors)]
        self.policies = self._construct_policies()
        self.num_modalities = len(self.A)
        self.num_obs = [self.A[i].shape[0] for i in range(self.num_modalities)]

    # TODO: Implement a max number of penpals per cell, and remove connections to make space for new ones?
    def asymmetric_divide(self):
        """Creates a new agent with the current agent as its penpal and returns both the current agent and the new agent."""

        # TODO: If there's a maximum number of penpals per cell, delete the least efficacious channel
        new_agent = ConnectedAgent(penpals=[self])
        return [self, new_agent]

    def symmetric_divide(self):
        """Performs symmetric cell division, creating a new ConnectedAgent object.
        Creates a new agent with the same penpals as the current agent and returns both the current agent and the new agent."""

        # Copy over the old penpals:
        new_agent = ConnectedAgent(is_seed_cell=False, penpals=self.penpals)
        # Swap me to position 0 per usual convention:
        my_pos = new_agent.penpals.index(new_agent)
        new_agent.penpals[0], new_agent.penpals[my_pos] = (
            new_agent.penpals[my_pos],
            new_agent.penpals[0],
        )
        # print(f"CHECKING {new_agent.penpals}, {self.penpals}")
        # Copy over my generative model:
        for nat, st in zip(
            [
                new_agent.A,
                new_agent.B,
                new_agent.pB,
                new_agent.C,
                new_agent.D,
                new_agent.E,
                new_agent.qs,
                new_agent.action,
            ],
            [self.A, self.B, self.pB, self.C, self.D, self.E, self.qs, self.action],
        ):
            nat[0] = copy.copy(st[0])
        new_agent.stem_factor = self.stem_factor

        return [self, new_agent]

    def wants_to_divide(self):
        # TODO: Make this a function of stress rather than number of penpals?
        return True
        # return np.random.random() < (1.0 / len(self.penpals))

    # Convention if the cell interacts with the environment:
    # Message: 1   0   0
    #          ^   ^   ^
    # Meaning: p1  p0  env

    # wrt can be:
    # * 'env': my message for the environment
    # * a penpal
    # * an index, representing the index of a penpal
    # TODO: Get rid of 'env' altogether; just have an environment agent which is a subclass of ConnectedAgent?
    def message_for(self, wrt="env"):
        return int(self.action[0]) & self._bit_loc_masks(wrt)[0] > 0

    # Same input types as above: this one mainly for debugging to make sure messages are received intact
    def message_from(self, a_in, wrt="env"):
        return a_in & self._bit_loc_masks(wrt)[0] > 0

    def self_efficacy(self, wrt=None):
        """Calculates the self-efficacy of the agent with respect to a specific source or set of sources.
        It measures the discrepancy between the agent's beliefs and the outcomes.
        The self-efficacy can be calculated for the environment, a penpal, or a list of penpals.
        The function returns the self-efficacy value(s)."""

        # TODO: Consider a self-efficacy metric w.r.t. a given penpal which considers how what I do in
        # *all* channels--not just with that penpal--affects what I receive from that penpal
        masks = self._bit_loc_masks(wrt)
        dim = self.B[0].shape[-1]
        slice_indices = np.arange(dim)
        results = []
        for m in masks:
            first_indices = np.nonzero(slice_indices & m == 0)
            second_indices = np.nonzero(slice_indices & m != 0)
            first_slices = self.B[0][:, :, first_indices]
            second_slices = self.B[0][:, :, second_indices]
            mean_abs_dif = np.mean(np.abs(first_slices - second_slices) * (dim / 2))
            results.append(mean_abs_dif)
        if hasattr(wrt, "__iter__") or isinstance(wrt, str):
            return np.array(results)
        else:
            return np.sum(results)  # Why is self-efficacy going down when a cell divides?
        # Should there be a self-efficacy that is independent of the size of B so it doesn't shrink/grow by a factor of 8 when penpals are added/removed?

    # wrt can be:
    # * 'env': just the index of the environment bit
    # * a penpal
    # * a list of penpals
    # * an index, representing the index of a penpal
    # * a list of indices, representing the indices of penpals
    # * 'all', meaning the indices of everything that exists among env, penpals
    # * None, which is like all but returns the average instead of a list
    def _bit_locs(self, wrt=None):
        if hasattr(wrt, "__iter__") and not isinstance(wrt, str):
            iterable_wrt = wrt
        else:
            iterable_wrt = [wrt]
        iwe = self._interacts_with_environment()
        indices = []
        for w in iterable_wrt:
            if w == "env":
                assert iwe, "Asked for env bit but agent doesn't interact with env"
                indices.append(0)
            elif isinstance(w, int):  # By convention, an integer w means the penpal of index w
                indices.append(iwe + w)
            elif isinstance(w, ConnectedAgent):
                indices.append(iwe + self.penpals.index(w))
            else:  # Meaning w == None or w == 'all':
                indices = range(iwe + len(self.penpals))
                break  # If any w in wrt is None or 'all', we include all indices always
        return np.array(indices).astype(int)

    def _bit_loc_masks(self, wrt=None):
        bit_locs = self._bit_locs(wrt)
        return np.array([1 << b for b in bit_locs]).astype(int)

    def compute_input(self, non_penpal_input):
        tmp = 0
        if self._interacts_with_environment():
            tmp += non_penpal_input & 1
        for p in self.penpals:
            tmp += p.message_for(self) * self._bit_loc_masks(p)[0]
        return tmp
