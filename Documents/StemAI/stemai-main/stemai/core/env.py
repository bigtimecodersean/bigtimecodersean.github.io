class Env:
    def __init__(self, fn):
        self.init_state = fn(0, -1)
        self.fn = fn

    # TODO: Make it so that if multiple cells on the same turn want to divide and there's only space for
    # some of them to, that we don't just prioritize the cells earlier in the array ConnectedAgent.all_agents
    def step(self, action_id, t=None):
        if t == None:
            return self.fn(action_id)
        else:
            env_bit = self.fn(action_id, t)
            # div_bit = env_bit if action_id & 1 == env_bit else (not env_bit)
            div_bit = env_bit
            return (div_bit << 1) + env_bit

    def max_cells(self, t):
        # this could be a function of how well the agents are aligning
        if t < 50:
            return 4
        else:
            return 2
