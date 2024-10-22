import numpy as np
import random
import time

class MGSCloneRL:
    def __init__(self, grid_size, learning_rate=0.1, discount_factor=0.9, epsilon=0.1):
        self.grid_size = grid_size
        self.q_table = np.zeros((grid_size, grid_size, 4))  # 4 actions: up, right, down, left
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon

    def choose_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            return random.randint(0, 3)
        else:
            return np.argmax(self.q_table[state])

    def update_q_table(self, state, action, reward, next_state):
        current_q = self.q_table[state + (action,)]
        max_next_q = np.max(self.q_table[next_state])
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_next_q - current_q)
        self.q_table[state + (action,)] = new_q

    def get_next_state(self, state, action):
        x, y = state
        if action == 0:  # up
            return (max(x - 1, 0), y)
        elif action == 1:  # right
            return (x, min(y + 1, self.grid_size - 1))
        elif action == 2:  # down
            return (min(x + 1, self.grid_size - 1), y)
        else:  # left
            return (x, max(y - 1, 0))

    def get_reward(self, state, next_state, goal):
        if next_state == goal:
            return 10  # Higher reward for reaching the goal
        elif self.manhattan_distance(next_state, goal) < self.manhattan_distance(state, goal):
            return 1  # Positive reward for moving closer to the goal
        else:
            return -1  # Negative reward for moving away from the goal or being detected

    def manhattan_distance(self, state, goal):
        return abs(state[0] - goal[0]) + abs(state[1] - goal[1])

    def train(self, start, goal, episodes):
        for _ in range(episodes):
            state = start
            while state != goal:
                action = self.choose_action(state)
                next_state = self.get_next_state(state, action)
                reward = self.get_reward(state, next_state, goal)
                self.update_q_table(state, action, reward, next_state)
                state = next_state

def visualize_game(grid_size, start, goal, path):
    grid = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]
    
    # Mark the path
    for x, y in path:
        grid[x][y] = '.'
    
    # Mark start and goal
    grid[start[0]][start[1]] = 'S'
    grid[goal[0]][goal[1]] = 'G'
    
    # Print the grid
    for row in grid:
        print('|' + '|'.join(row) + '|')
    
    print(f"\nPath length: {len(path) - 1} steps")

def play_game(agent, start, goal):
    state = start
    path = [state]
    while state != goal:
        action = agent.choose_action(state)
        state = agent.get_next_state(state, action)
        path.append(state)
    return path

# Example usage
grid_size = 10
start = (0, 0)
goal = (9, 9)

agent = MGSCloneRL(grid_size)
agent.train(start, goal, 5000)  # Train the agent

# Play the game and visualize
path = play_game(agent, start, goal)
visualize_game(grid_size, start, goal, path)