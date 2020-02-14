#starts the CartPole environment web version


#  Observation: 
#        Type: Box(4)
#        Num	Observation                 Min         Max
#        0	Cart Position             -4.8            4.8
#        1	Cart Velocity             -Inf            Inf
#        2	Pole Angle                 -24°           24°
#        3	Pole Velocity At Tip      -Inf            Inf
        
#    Action:
#        Type: Discrete(2)
#        Num	Action
#        0	Push cart to the left
# 	 1	Push cart to the right

import gym
from gymWebEnvironment import start_environment

#Full documentation: https://gym.openai.com/docs/
#A: 0 (esquerda), 1 (direita)

gym.envs.register(
    id='CartPole-v100',
    entry_point='gym.envs.classic_control:CartPoleEnv',
    max_episode_steps=1000
)
env = gym.make('CartPole-v100')
env.reset()
start_environment(env)


