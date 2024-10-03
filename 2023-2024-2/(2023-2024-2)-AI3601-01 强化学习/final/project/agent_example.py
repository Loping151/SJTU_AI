import dmc
import glob
import numpy as np

class Agent:
    # An example of the agent to be implemented.
    # Your agent must extend from this class (you may add any other functions if needed).
    def __init__(self, state_dim, action_dim):
        self.state_dim = state_dim
        self.action_dim = action_dim
    def act(self, state):
        action = np.random.uniform(-5, 5, size=(self.action_dim))
        return action
    def load(self, load_path):
        pass


def load_data(data_path):
    """
    An example function to load the episodes in the 'data_path'.
    """
    epss = sorted(glob.glob(f'{data_path}/*.npz'))
    episodes = []
    for eps in epss:
        with open(eps, 'rb') as f:
            episode = np.load(f)
            episode = {k: episode[k] for k in episode.keys()}
            episodes.append(episode)
    print(len(episodes))
    return episodes

load_data("collected_data/walker_run-td3-medium/data")
load_data("collected_data/walker_run-td3-medium-replay/data")
load_data("collected_data/walker_walk-td3-medium/data")
load_data("collected_data/walker_walk-td3-medium-replay/data")

def eval(eval_env, agent, eval_episodes):
    """
    An example function to conduct online evaluation for some agentin eval_env.
    """
    returns = []
    for episode in range(eval_episodes):
        time_step = eval_env.reset()
        cumulative_reward = 0
        while not time_step.last():
            action = agent.act(time_step.observation)
            time_step = eval_env.step(action)
            cumulative_reward += time_step.reward
        returns.append(cumulative_reward)
    return sum(returns) / eval_episodes

task_name = "walker_walk"
seed = 42
eval_env = dmc.make(task_name, seed=seed)
print(eval(eval_env=eval_env, agent=Agent(24, 6), eval_episodes=10))


task_name = "walker_run"
seed = 42
eval_env = dmc.make(task_name, seed=seed)
print(eval(eval_env=eval_env, agent=Agent(24, 6), eval_episodes=10))
