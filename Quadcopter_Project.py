#!/usr/bin/env python
# coding: utf-8

# # Project: Train a Quadcopter How to Fly using DDOG techniques!
# 
# Design an agent to fly a quadcopter, and then train it using a reinforcement learning algorithm of your choice! 
# 
# Try to apply the techniques you have learnt, but also feel free to come up with innovative ideas and test them.

# ## Instructions
# 
# Take a look at the files in the directory to better understand the structure of the project. 
# 
# - `task.py`: Define your task (environment) in this file.
# - `agents/`: Folder containing reinforcement learning agents.
#     - `policy_search.py`: A sample agent has been provided here.
#     - `agent.py`: Develop your agent here.
# - `physics_sim.py`: This file contains the simulator for the quadcopter.  **DO NOT MODIFY THIS FILE**.
# 
# For this project, you will define your own task in `task.py`.  Although we have provided a example task to get you started, you are encouraged to change it.  Later in this notebook, you will learn more about how to amend this file.
# 
# You will also design a reinforcement learning agent in `agent.py` to complete your chosen task.  
# 
# You are welcome to create any additional files to help you to organize your code.  For instance, you may find it useful to define a `model.py` file defining any needed neural network architectures.
# 
# ## Controlling the Quadcopter
# 
# We provide a sample agent in the code cell below to show you how to use the sim to control the quadcopter.  This agent is even simpler than the sample agent that you'll examine (in `agents/policy_search.py`) later in this notebook!
# 
# The agent controls the quadcopter by setting the revolutions per second on each of its four rotors.  The provided agent in the `Basic_Agent` class below always selects a random action for each of the four rotors.  These four speeds are returned by the `act` method as a list of four floating-point numbers.  
# 
# For this project, the agent that you will implement in `agents/agent.py` will have a far more intelligent method for selecting actions!

# In[54]:


import random

class Basic_Agent():
    def __init__(self, task):
        self.task = task
    
    def act(self):
        new_thrust = random.gauss(450., 25.)
        return [new_thrust + random.gauss(0., 1.) for x in range(4)]


# Run the code cell below to have the agent select actions to control the quadcopter.  
# 
# Feel free to change the provided values of `runtime`, `init_pose`, `init_velocities`, and `init_angle_velocities` below to change the starting conditions of the quadcopter.
# 
# The `labels` list below annotates statistics that are saved while running the simulation.  All of this information is saved in a text file `data.txt` and stored in the dictionary `results`.  

# In[55]:


get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')

import csv
import numpy as np
from task import Task

# Modify the values below to give the quadcopter a different starting position.
#runtime = 5.                                     # time limit of the episode
runtime = 5000.                                  # time limit of the episode
init_pose = np.array([0., 0., 10., 0., 0., 0.])  # initial pose
init_velocities = np.array([0., 0., 0.])         # initial velocities
init_angle_velocities = np.array([0., 0., 0.])   # initial angle velocities
file_output = 'data.txt'                         # file name for saved results

# Setup
task = Task(init_pose, init_velocities, init_angle_velocities, runtime)
agent = Basic_Agent(task)
done = False
labels = ['time', 'x', 'y', 'z', 'phi', 'theta', 'psi', 'x_velocity',
          'y_velocity', 'z_velocity', 'phi_velocity', 'theta_velocity',
          'psi_velocity', 'rotor_speed1', 'rotor_speed2', 'rotor_speed3', 'rotor_speed4']
results = {x : [] for x in labels}

print("finished with setup")

# Run the simulation, and save the results.
print("run the simulation and save results")
with open(file_output, 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(labels)
    while True:
        rotor_speeds = agent.act()
        _, _, done = task.step(rotor_speeds)
        to_write = [task.sim.time] + list(task.sim.pose) + list(task.sim.v) + list(task.sim.angular_v) + list(rotor_speeds)
        for ii in range(len(labels)):
            results[labels[ii]].append(to_write[ii])
        writer.writerow(to_write)
        if done:
            break


# Run the code cell below to visualize how the position of the quadcopter evolved during the simulation.

# In[56]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

plt.plot(results['time'], results['x'], label='x')
plt.plot(results['time'], results['y'], label='y')
plt.plot(results['time'], results['z'], label='z')
plt.legend()
_ = plt.ylim()


# The next code cell visualizes the velocity of the quadcopter.

# In[57]:


plt.plot(results['time'], results['x_velocity'], label='x_hat')
plt.plot(results['time'], results['y_velocity'], label='y_hat')
plt.plot(results['time'], results['z_velocity'], label='z_hat')
plt.legend()
_ = plt.ylim()


# Next, you can plot the Euler angles (the rotation of the quadcopter over the $x$-, $y$-, and $z$-axes),

# In[58]:


plt.plot(results['time'], results['phi'], label='phi')
plt.plot(results['time'], results['theta'], label='theta')
plt.plot(results['time'], results['psi'], label='psi')
plt.legend()
_ = plt.ylim()


# before plotting the velocities (in radians per second) corresponding to each of the Euler angles.

# In[59]:


plt.plot(results['time'], results['phi_velocity'], label='phi_velocity')
plt.plot(results['time'], results['theta_velocity'], label='theta_velocity')
plt.plot(results['time'], results['psi_velocity'], label='psi_velocity')
plt.legend()
_ = plt.ylim()


# Finally, you can use the code cell below to print the agent's choice of actions.  

# In[60]:


plt.plot(results['time'], results['rotor_speed1'], label='Rotor 1 revolutions / second')
plt.plot(results['time'], results['rotor_speed2'], label='Rotor 2 revolutions / second')
plt.plot(results['time'], results['rotor_speed3'], label='Rotor 3 revolutions / second')
plt.plot(results['time'], results['rotor_speed4'], label='Rotor 4 revolutions / second')
plt.legend()
_ = plt.ylim()


# When specifying a task, you will derive the environment state from the simulator.  Run the code cell below to print the values of the following variables at the end of the simulation:
# - `task.sim.pose` (the position of the quadcopter in ($x,y,z$) dimensions and the Euler angles),
# - `task.sim.v` (the velocity of the quadcopter in ($x,y,z$) dimensions), and
# - `task.sim.angular_v` (radians/second for each of the three Euler angles).

# In[63]:


# the pose, velocity, and angular velocity of the quadcopter at the end of the episode
print(task.sim.pose)
print(task.sim.v)
print(task.sim.angular_v)


# In the sample task in `task.py`, we use the 6-dimensional pose of the quadcopter to construct the state of the environment at each timestep.  However, when amending the task for your purposes, you are welcome to expand the size of the state vector by including the velocity information.  You can use any combination of the pose, velocity, and angular velocity - feel free to tinker here, and construct the state to suit your task.
# 
# ## The Task
# 
# A sample task has been provided for you in `task.py`.  Open this file in a new window now. 
# 
# The `__init__()` method is used to initialize several variables that are needed to specify the task.  
# - The simulator is initialized as an instance of the `PhysicsSim` class (from `physics_sim.py`).  
# - Inspired by the methodology in the original DDPG paper, we make use of action repeats.  For each timestep of the agent, we step the simulation `action_repeats` timesteps.  If you are not familiar with action repeats, please read the **Results** section in [the DDPG paper](https://arxiv.org/abs/1509.02971).
# - We set the number of elements in the state vector.  For the sample task, we only work with the 6-dimensional pose information.  To set the size of the state (`state_size`), we must take action repeats into account.  
# - The environment will always have a 4-dimensional action space, with one entry for each rotor (`action_size=4`). You can set the minimum (`action_low`) and maximum (`action_high`) values of each entry here.
# - The sample task in this provided file is for the agent to reach a target position.  We specify that target position as a variable.
# 
# The `reset()` method resets the simulator.  The agent should call this method every time the episode ends.  You can see an example of this in the code cell below.
# 
# The `step()` method is perhaps the most important.  It accepts the agent's choice of action `rotor_speeds`, which is used to prepare the next state to pass on to the agent.  Then, the reward is computed from `get_reward()`.  The episode is considered done if the time limit has been exceeded, or the quadcopter has travelled outside of the bounds of the simulation.
# 
# In the next section, you will learn how to test the performance of an agent on this task.

# ## The Agent
# 
# The sample agent given in `agents/policy_search.py` uses a very simplistic linear policy to directly compute the action vector as a dot product of the state vector and a matrix of weights. Then, it randomly perturbs the parameters by adding some Gaussian noise, to produce a different policy. Based on the average reward obtained in each episode (`score`), it keeps track of the best set of parameters found so far, how the score is changing, and accordingly tweaks a scaling factor to widen or tighten the noise.
# 
# Run the code cell below to see how the agent performs on the sample task.

# In[64]:


import sys
import pandas as pd
from agents.policy_search import PolicySearch_Agent
from task import Task

num_episodes = 1000
target_pos = np.array([0., 0., 10.])
task = Task(target_pos=target_pos)
agent = PolicySearch_Agent(task) 

for i_episode in range(1, num_episodes+1):
    state = agent.reset_episode() # start a new episode
    while True:
        action = agent.act(state) 
        next_state, reward, done = task.step(action)
        agent.step(reward, done)
        state = next_state
        if done:
            print("\rEpisode = {:4d}, score = {:7.3f} (best = {:7.3f}), noise_scale = {}".format(
                i_episode, agent.score, agent.best_score, agent.noise_scale), end="")  # [debug]
            break
    sys.stdout.flush()
    
print("\nfinished running agent")


# This agent should perform very poorly on this task.  And that's where you come in!

# ## Define the Task, Design the Agent, and Train Your Agent!
# 
# Amend `task.py` to specify a task of your choosing.  If you're unsure what kind of task to specify, you may like to teach your quadcopter to takeoff, hover in place, land softly, or reach a target pose.  
# 
# After specifying your task, use the sample agent in `agents/policy_search.py` as a template to define your own agent in `agents/agent.py`.  You can borrow whatever you need from the sample agent, including ideas on how you might modularize your code (using helper methods like `act()`, `learn()`, `reset_episode()`, etc.).
# 
# Note that it is **highly unlikely** that the first agent and task that you specify will learn well.  You will likely have to tweak various hyperparameters and the reward function for your task until you arrive at reasonably good behavior.
# 
# As you develop your agent, it's important to keep an eye on how it's performing. Use the code above as inspiration to build in a mechanism to log/save the total rewards obtained in each episode to file.  If the episode rewards are gradually increasing, this is an indication that your agent is learning.

# In[65]:


## TODO: Train your agent here.
import sys
import pandas as pd
from agents.agent import DDPG
#from tasks.takeoff import Task
from task import Task
import csv

num_episodes = 500
target_pos = np.array([0., 0., 100.])
task = Task(target_pos=target_pos)
agent = DDPG(task) 
worst_score = 1000000
best_score = -1000000.
reward_log = "reward.txt"

reward_labels = ['episode', 'reward']
reward_results = {x : [] for x in reward_labels}

print("finished with setup")


# In[66]:


for i_episode in range(1, num_episodes+1):
    state = agent.reset_episode() # start a new episode
    score = 0
    while True:
        action = agent.act(state)
        #use takeoff (to) step
        next_state, reward, done = task.to_step(action)
        agent.step(action, reward, next_state, done)
        state = next_state
        score += reward
        best_score = max(best_score , score)
        worst_score = min(worst_score , score)
        if done:
            print("\rEpisode = {:4d}, score = {:7.3f} (best = {:7.3f} , worst = {:7.3f})".format(
               i_episode, score, best_score, worst_score), end="")
            break
    reward_results['episode'].append(i_episode)
    reward_results['reward'].append(score)
    sys.stdout.flush()

print("\nfinished producing results")


# ## Plot the Rewards
# 
# Once you are satisfied with your performance, plot the episode rewards, either from a single run, or averaged over multiple runs. 

# In[67]:


## TODO: Plot the rewards.
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

plt.plot(reward_results['episode'], reward_results['reward'], label='reward/episode')
plt.legend()
_ = plt.ylim()


# ## Performance Demonstration
# Lets now see how well the agent actually performs in reference to the above reward graph.
# For this, we will let the agent perform for one episode in the environment without learning anything new.

# In[69]:


get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')

import csv
#from tasks.takeoff import Task

# Modify the values below to give the quadcopter a different starting position.
runtime = 5000.                                  # time limit of the episode
init_pose = np.array([0., 0., 10., 0., 0., 0.])  # initial pose
init_velocities = np.array([0., 0., 0.])         # initial velocities
init_angle_velocities = np.array([0., 0., 0.])   # initial angle velocities
file_output = 'data.txt'                         # file name for saved results

# Setup
task = Task(init_pose, init_velocities, init_angle_velocities, runtime)
done = False
labels = ['time', 'x', 'y', 'z', 'phi', 'theta', 'psi', 'x_velocity',
          'y_velocity', 'z_velocity', 'phi_velocity', 'theta_velocity',
          'psi_velocity', 'rotor_speed1', 'rotor_speed2', 'rotor_speed3', 'rotor_speed4']
results = {x : [] for x in labels}

# Run the simulation, and save the results.
state = agent.reset_episode()
total_reward = 0
while True:
    rotor_speeds = agent.act(state)
    next_state, reward, done = task.to_step(rotor_speeds)
    to_write = [task.sim.time] + list(task.sim.pose) + list(task.sim.v) + list(task.sim.angular_v) + list(rotor_speeds)
    for ii in range(len(labels)):
        results[labels[ii]].append(to_write[ii])
    total_reward += reward
    state = next_state
    if done:
        print("Total episode reward : {}".format(total_reward))
        total_reward = 0
        break


# Run the code cell below to visualize how the position of the quadcopter evolved during the simulation.

# In[70]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

plt.plot(results['time'], results['x'], label='x')
plt.plot(results['time'], results['y'], label='y')
plt.plot(results['time'], results['z'], label='z')
plt.legend()
_ = plt.ylim()


# Run the code cell below to print the values of the following variables at the end of the simulation:
# 
# -task.sim.pose (the position of the quadcopter in ($x,y,z$) dimensions and the Euler angles),
# -task.sim.v (the velocity of the quadcopter in ($x,y,z$) dimensions), and
# -task.sim.angular_v (radians/second for each of the three Euler angles).

# In[71]:


# the pose, velocity, and angular velocity of the quadcopter at the end of the episode
print(task.sim.pose)
print(task.sim.v)
print(task.sim.angular_v)


# ## Reflections
# 
# **Question 1**: Describe the task that you specified in `task.py`.  How did you design the reward function?
# 
# **Answer**: For this project, the agent was trained using a takeoff (to) task, introducing two new functions into task.py called to_step and get_to_reward. The reward was initially set to the signed difference between the sim position and the target position (sim.pose and target.pose, respectively).  This produced very poor learning due to unbounded and very high variance.  The reward was then bounded to a range [-1,1] using a non-linear "tanh" function with some scaling to make it work for the tanh function.  The final design was a hybrid of the two approaches where the absolute difference between the sim and target positions was passed through the through the tanh function, mitigating the the gradient descent issue.
# 
# Final Reward Function: reward = np.tanh(1 - 0.003*(abs(self.sim.pose[:3] - self.target_pos))).sum()

# **Question 2**: Discuss your agent briefly, using the following questions as a guide:
# 
# - What learning algorithm(s) did you try? What worked best for you?
# - What was your final choice of hyperparameters (such as $\alpha$, $\gamma$, $\epsilon$, etc.)?
# - What neural network architecture did you use (if any)? Specify layers, sizes, activation functions, etc.
# 
# **Answer**: Given this is a continuous action space, Deep Deterministic Policy Gradients (DDPG) was used for the task, with the same initial architecture and hyperparameters.  Even using lots of tweaking hough the initial implementation didn't proved so promising for me, the agent was not learning at all . Later I found out even after so much hyperparameter tweaking, the main culprit was the inefficiency of the neural net archtecture used for both Actor and Critic.
# 
# The final selection of hyperparameters:
# -Size of minibatch from experience replay memory = 64
# -Tau (soft target update rate) = 0.001
# -Learning rate for the actor = 0.0001
# -Learning rate for the critic = 0.001
# -Gamma = 0.99
# -Capacity of experience replay memory = 1000000
# 
# The final agent uses a neural network architecture.
# 
# Actor :
# -Dense(units=400) + BatchNorm + L2 Regularization + ReLu Activation
# -Dense(units=300) + BatchNorm + L2 Regularization + ReLu Activation
# -Dense( RandomUniform Weight initialization ) + Sigmoid Activation
# 
# Critic :
# -Same as actor for the state pathway
# 
# Action Pathway:
# -Dense(units=300) + L2 Regularization + ReLu Activation
# -Combining : Add with ReLu Activation
# 
# This stripped down arch of layers with large units actually helped the agent to learn more quickly and effectively.  The training time also decreased significantly.

# **Question 3**: Using the episode rewards plot, discuss how the agent learned over time.
# 
# - Was it an easy task to learn or hard?
# - Was there a gradual learning curve, or an aha moment?
# - How good was the final performance of the agent? (e.g. mean rewards over the last 10 episodes)
# 
# **Answer**: In general, it seems like a relatively simple control task, with the agent trying all possibilities for a high reward, leading to the instability.  As it gained experience in the operating environment, it gradually became more consistent in taking actions with higher rewards, although still not completely optimized.
# 
# It was a combination, not unlike our own human experience in learning.  It started off awkwardly without much intuition, made some curious adjustments, and then matured into an agent performing with some competence.
# 
# Let's take a look at the final performance:

# In[74]:


print
plt.plot(reward_results['episode'], reward_results['reward'], label='reward/episode')
plt.legend()
_ = plt.ylim()


# In[75]:


# Final Performance 
print("Final Performance (Mean Reward over last 10 episodes): {}".format(np.sum(reward_results['reward'][-10:])/10))


# **Question 4**: Briefly summarize your experience working on this project. You can use the following prompts for ideas.
# 
# - What was the hardest part of the project? (e.g. getting started, plotting, specifying the task, etc.)
# - Did you find anything interesting in how the quadcopter or your agent behaved?
# 
# **Answer**: The most challenging part of the project for me was putting aside my 30+ years of experience I have in avionics and flight control system development.  Trusting an algorithm to zero in on the right combination of rotor speeds to get to a certain position, without my trusty flight simulation environment at work, is still something I marvel at.  As such, in terms of the coding part of the project, the continuous control task were challenging with trying to understand how to visualize the Policy Gradient.
# 
# The one thing that most surprised me was how a simple change in the reward function could have such a large impact on how the algorithm performed, and how the performance changed noticeably between one run and the next although honing in on a solution with each one.

# In[ ]:




