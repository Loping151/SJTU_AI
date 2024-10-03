## Offline Dataset

The offline dataset in `collected_data` consists of offline samples in two tasks (walker_run and walker_walk), each having two levels of data qualities (medium and medium-replay), where the medium data has higher overall quality than medium-replay. The data was collected in the replay buffer when training a TD3 agent in the walker_walk and walker_run environment. The folder `custom_dmc_tasks` contains the environment specifications for the tasks. In the example given in `agent_example.py`, you mey refer to the `load_data` function for offline data loading and the `eval` function for testing in these environments.

## Agent

In this project, we are training an agent to learn from the offline datasets for a policy that could perform well in both walker_walk and walker_run tasks. The agent you implement should follow the interface in the `Agent` class in `agent_example.py`. Please note that the training of the agent could only use the given offline data, and the online environment can only be used for agent evaluation. You need to submit your code implementation of the agent that follows the given interface, alongside with an agent checkpoint and an instruction to load and test the checkpoint for evaluation.

## Package Specifications

- `dm_control==1.0.14`
- `gym==0.21.0`