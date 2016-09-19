import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator
import numpy as np



class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.actions = [None, 'forward', 'left', 'right']
        self.Qtable = {}
        self.epsilon = 0   # set as 1 for total random action selection
        self.gamma = 0.9
        self.learning_rate = 0.05
        self.default_Q = 4
        self.fault = 0
        self.re1 = []
        self.re2 = []
        self.re3 = []
        self.re4 = []
        self.re11 = 0
        self.re12 = 0
        self.re13 = 0
        self.re14 = 0





    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        self.prev_state = None
        self.prev_action = None
        self.prev_reward = None
        self.state = None
        self.next_waypoint = None
        self.re1.append(self.re11)
        self.re2.append(self.re12)
        self.re3.append(self.re13)
        self.re4.append(self.re14)

        self.re11 = 0
        self.re12 = 0
        self.re13 = 0
        self.re14 = 0







    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)


        # TODO: Update state
        self.state = (inputs['light'], inputs['oncoming'], inputs['right'],inputs['left'], self.next_waypoint)

        # TODO: Select action according to your policy

        for action in self.actions:
            if (self.state, action) not in self.Qtable:
                self.Qtable[(self.state, action)] = self.default_Q

        Qcurrent = [self.Qtable[(self.state, None)], self.Qtable[(self.state, 'forward')], self.Qtable[(self.state, 'left')], self.Qtable[(self.state, 'right')]]

        if random.random() < self.epsilon:
            action = self.actions[random.randint(1,3)]  #a random choice between the possible actions with None parsed out
        else:
            action = self.actions[np.argmax(Qcurrent)]


        # Execute action and get reward
        reward = self.env.act(self, action)
        if reward == -0.5:
            self.re11 = self.re11 + 1
        elif reward == -1:
            self.re12 = self.re12 + 1
        elif reward == 0:
            self.re13 = self.re13 + 1
        else:
            self.re14 = self.re14 + 1


        # TODO: Learn policy based on state, action, reward
        if self.prev_state != None:
            self.Qtable[(self.prev_state,self.prev_action)] = (1 - self.learning_rate) * self.Qtable[(self.prev_state,self.prev_action)] + self.learning_rate * (self.prev_reward + self.gamma *self.Qtable[(self.state, action)])

        # pdb.set_trace()
        self.prev_state = self.state
        self.prev_action = action
        self.prev_reward = reward

        #print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]


        if deadline == 0:
            self.fault = self.fault + 1


def run():
    """Run the agent for a finite number of trials."""
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
                # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

                # Now simulate it
    sim = Simulator(e, update_delay=0, display=False)  # create simulator (uses pygame when display=True, if available)
                # NOTE: To speed up simulation, reduce update_delay and/or set display=False
    sim.run(n_trials=100)  # run for a specified number of trials
                    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line
    QTABLE = a.Qtable;
    print type(QTABLE)
    for key in QTABLE:
        print str(key) + ':'+ str(QTABLE[key])
    print "The success rate of 100 trial is " + str(100-a.fault)
    print a.re1
    print a.re2
    print a.re3
    print a.re4


    '''
    Suss_arr = []
    for rate in [0.2,0.1,0.05]:
        for gama in [0.5,0.6,0.8,0.9]:
            for epy in [1,0.4,0.2,0.1,0.05]:
                # Set up environment and agent
                e = Environment()  # create environment (also adds some dummy traffic)
                a = e.create_agent(LearningAgent)  # create agent
                e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
                # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

                # Now simulate it
                sim = Simulator(e, update_delay=0, display=False)  # create simulator (uses pygame when display=True, if available)
                # NOTE: To speed up simulation, reduce update_delay and/or set display=False


                a.epsilon = epy
                a.gamma = gama
                a.learning_rate = rate
                sim.run(n_trials=100)  # run for a specified number of trials
                    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line
                Suss_arr.append(100-a.fault)
                a.fault = 0

    index = 0
    for rate in [0.2,0.1,0.05]:
        for gama in [0.5,0.6,0.8,0.9]:
            for epy in [1,0.4,0.2,0.1,0.05]:
                print "rate:"+str(rate)+"gama:"+str(gama)+"epy:"+str(epy)+"succcess:"+str(Suss_arr[index])
                index = index + 1
    '''









if __name__ == '__main__':
    run()
