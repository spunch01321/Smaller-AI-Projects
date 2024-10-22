import random

class MGSClone:
    def __init__(self):
        self.stealth_levels = ['High', 'Medium', 'Low']
        self.enemy_levels = ['High', 'Medium', 'Low']
        self.actions = ['Sneak', 'Use Cardboard Box', 'Run']
        
        self.stealth_probs = {'High': 0.3, 'Medium': 0.5, 'Low': 0.2}
        self.enemy_probs = {'High': 0.4, 'Medium': 0.4, 'Low': 0.2}
        
        self.success_probs = {
            ('High', 'High', 'Sneak'): 0.7,
            ('High', 'High', 'Use Cardboard Box'): 0.6,
            ('High', 'High', 'Run'): 0.2,
            ('High', 'Medium', 'Sneak'): 0.8,
            ('High', 'Medium', 'Use Cardboard Box'): 0.7,
            ('High', 'Medium', 'Run'): 0.3,
            ('High', 'Low', 'Sneak'): 0.9,
            ('High', 'Low', 'Use Cardboard Box'): 0.8,
            ('High', 'Low', 'Run'): 0.5,
            ('Medium', 'High', 'Sneak'): 0.5,
            ('Medium', 'High', 'Use Cardboard Box'): 0.4,
            ('Medium', 'High', 'Run'): 0.1,
            ('Medium', 'Medium', 'Sneak'): 0.6,
            ('Medium', 'Medium', 'Use Cardboard Box'): 0.5,
            ('Medium', 'Medium', 'Run'): 0.2,
            ('Medium', 'Low', 'Sneak'): 0.7,
            ('Medium', 'Low', 'Use Cardboard Box'): 0.6,
            ('Medium', 'Low', 'Run'): 0.4,
            ('Low', 'High', 'Sneak'): 0.3,
            ('Low', 'High', 'Use Cardboard Box'): 0.2,
            ('Low', 'High', 'Run'): 0.1,
            ('Low', 'Medium', 'Sneak'): 0.4,
            ('Low', 'Medium', 'Use Cardboard Box'): 0.3,
            ('Low', 'Medium', 'Run'): 0.2,
            ('Low', 'Low', 'Sneak'): 0.5,
            ('Low', 'Low', 'Use Cardboard Box'): 0.4,
            ('Low', 'Low', 'Run'): 0.3
        }
        
        self.utilities = {'Success': 100, 'Failure': -50}

    def calculate_meu(self, action):
        meu = 0
        for stealth in self.stealth_levels:
            for enemy in self.enemy_levels:
                p_success = self.success_probs[(stealth, enemy, action)]
                p_failure = 1 - p_success
                meu += (self.stealth_probs[stealth] * self.enemy_probs[enemy] *
                        (p_success * self.utilities['Success'] +
                         p_failure * self.utilities['Failure']))
        return meu

    def choose_action(self):
        meus = {action: self.calculate_meu(action) for action in self.actions}
        return max(meus, key=meus.get)

    def simulate_infiltration(self):
        action = self.choose_action()
        stealth = random.choices(self.stealth_levels, weights=self.stealth_probs.values())[0]
        enemy = random.choices(self.enemy_levels, weights=self.enemy_probs.values())[0]
        success_prob = self.success_probs[(stealth, enemy, action)]
        outcome = 'Success' if random.random() < success_prob else 'Failure'
        return action, stealth, enemy, outcome

    def play_game(self):
        action, stealth, enemy, outcome = self.simulate_infiltration()
        print(f"Stealth Level: {stealth}")
        print(f"Enemy Presence: {enemy}")
        print(f"Chosen Action: {action}")
        print(f"Mission Outcome: {outcome}")

if __name__ == "__main__":
    game = MGSClone()
    game.play_game()