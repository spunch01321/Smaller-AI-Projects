import numpy as np
from hmmlearn import hmm
import random

class Guard:
    def __init__(self):
        # States of the Guard
        self.states = ["Patrol", "Investigate", "Alert"]
        self.n_states = len(self.states)

        # Observation of the Guard
        self.observations = ["Nothing", "Noise", "Footprint", "Glimpse"]
        self.n_observations = len(self.observations)

        # Initialize HMM
        self.model = hmm.CategoricalHMM(n_components=self.n_states, random_state=42)
        
        # Set transition probability matrix
        self.model.transmat_ = np.array([
            [0.8, 0.15, 0.05],  # Patrol
            [0.4, 0.5, 0.1],    # Investigate
            [0.2, 0.3, 0.5]     # Alert
        ])

        # Set emission probability matrix
        self.model.emissionprob_ = np.array([
            [0.7, 0.1, 0.1, 0.1],  # Patrol
            [0.2, 0.3, 0.3, 0.2],  # Investigate
            [0.1, 0.2, 0.2, 0.5]   # Alert
        ])

        # Set initial state distribution
        self.model.startprob_ = np.array([0.8, 0.15, 0.05])
        # Set # of trials
        self.model.n_trials = 4

    def update_state(self, observations):
        # Convert observations to numerical form
        obs_seq = np.array([[self.observations.index(obs)] for obs in observations]).reshape(-1,1)
        
        # Use Viterbi algorithm to find most likely state sequence
        logprob, state_sequence = self.model.decode(obs_seq, algorithm="viterbi")
    
        return self.states[state_sequence[-1]]

    def generate_observation(self, state):
        state_index = self.states.index(state)
        observation_probs = self.model.emissionprob_[state_index]
        return np.random.choice(self.observations, p=observation_probs)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_hidden = False

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.is_hidden = False

    def hide(self):
        self.is_hidden = True

class Game:
    def __init__(self):
        self.player = Player(0, 0)
        self.guard = Guard()
        self.observations = []
        self.turns = 0

    def player_action(self, action):
        if action == "move":
            direction = random.choice(["up", "down", "left", "right"])
            dx, dy = {"up": (0, 1), "down": (0, -1), "left": (-1, 0), "right": (1, 0)}[direction]
            self.player.move(dx, dy)
            self.observations.append("Footprint")
            print(f"Player moved {direction} to position ({self.player.x}, {self.player.y})")
        elif action == "hide":
            self.player.hide()
            self.observations.append("Nothing")
            print("Player is hiding")

    def update(self):
        guard_state = self.guard.update_state(self.observations)
        print(f"Guard state: {guard_state}")
        
        # Generate guard's observation based on current state
        guard_observation = self.guard.generate_observation(guard_state)
        print(f"Guard observed: {guard_observation}")
        
        self.observations = []
        self.turns += 1

        if guard_state == "Alert" and not self.player.is_hidden:
            print("Game Over! The guard caught you.")
            return False
        elif self.turns >= 10:
            print("Congratulations! You successfully infiltrated the base.")
            return False
        return True

# Example Loop
game = Game()
game_active = True

print("Welcome to Shadow Protocol!")
print("Your mission: Survive for 10 turns without getting caught.")
print("Commands: 'move' to move in a random direction, 'hide' to hide.")

while game_active:
    action = input("Enter action (move/hide): ").lower()
    if action in ["move", "hide"]:
        game.player_action(action)
        game_active = game.update()
    else:
        print("Invalid action. Please enter 'move' or 'hide'.")

print("Game ended. Thanks for playing Shadow Protocol!")