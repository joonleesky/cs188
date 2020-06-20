# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        
        #Initialize
        states = self.mdp.getStates()

        self.values.incrementAll(states,0)
        
        for it in range(self.iterations):
            newValues = util.Counter()
            
            # For each State, compute expected Reward based on previous Values
            for state in states:
                Qvalues = util.Counter()
                actions = self.mdp.getPossibleActions(state)
            
                for action in actions:
                    Qvalue = self.computeQValueFromValues(state, action)
                
                    Qvalues[action] = Qvalue
                newValues[state] = Qvalues[Qvalues.argMax()]
            
            # Update the Values
            self.values = newValues
        
        
    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        Qvalue = 0
        transitions = self.mdp.getTransitionStatesAndProbs(state, action)
        
        for t in transitions:
            nextState = t[0] 
            prob  = t[1]
            reward  = self.mdp.getReward(state, action, nextState)
            value  = self.discount * self.getValue(nextState)
                    
            Qvalue += prob * (reward + value)
            
        return Qvalue

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        Qvalues = util.Counter()
        actions = self.mdp.getPossibleActions(state)

        for action in actions:
            Qvalues[action] = self.computeQValueFromValues(state, action)
        return Qvalues.argMax()

    
    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        
        #Initialize
        states = self.mdp.getStates()
        self.values.incrementAll(states,0)
        
        for it in range(self.iterations):
            newValues = util.Counter()
            tState = states[int(it % len(states))]

            # For each State, compute expected Reward based on previous Values
            for state in states:
                Qvalues = util.Counter()
                actions = self.mdp.getPossibleActions(state)
                
                if state == tState:
                    for action in actions:
                        Qvalue = self.computeQValueFromValues(state, action)
                        Qvalues[action] = Qvalue
                    self.values[state] = Qvalues[Qvalues.argMax()]

                    
class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)
        
    def computeStateValue(self,state):
        Qvalues = util.Counter()
        actions = self.mdp.getPossibleActions(state)
            
        for action in actions:
            Qvalue = self.computeQValueFromValues(state, action)
            Qvalues[action] = Qvalue
        
        return Qvalues[Qvalues.argMax()]

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"

        #Initialize
        states = self.mdp.getStates()
        predecessors = {}
        for state in states:
            predecessors[state] = set()
            
        Queue = util.PriorityQueue()
        self.values.incrementAll(states,0)
        
        # Get Predecessors for each state
        for state in states:
            actions = self.mdp.getPossibleActions(state)
            
            for action in actions:
                transitions = self.mdp.getTransitionStatesAndProbs(state, action)
                for t in transitions:
                    predecessors[t[0]].add(state)
                    
        # Push the states into Queue with initial priority
        for state in states:
            if state == 'TERMINAL_STATE':
                continue

            diff = abs(self.values[state] - self.computeStateValue(state))
            Queue.push(state, -diff)
            
    
        for it in range(self.iterations):
            if Queue.isEmpty() == True:
                break
            state = Queue.pop()            
            if state == 'TERMINAL_STATE':
                print('terminal')
                continue
            
            self.values[state] = self.computeStateValue(state)
            predecessor = predecessors[state]

            for p in predecessor:
                diff = abs(self.values[p] - self.computeStateValue(p))
                if diff > self.theta:
                    Queue.update(p, -diff)