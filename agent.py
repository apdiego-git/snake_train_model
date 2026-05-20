import numpy as np
import random

REWARD_APPLE = 3
REWARD_DEATH = -10
REWARD_NOTHING = -0.1

class Agent: #class for snake agent
    def __init__(self):
        self.learning_rate = .25
        self.discount_factor = .90
        try:
            self.exploration_rate = np.load("exploration_rate.npy")
        except:
            self.exploration_rate = 1.0
        try:
            self.q_table = np.load("q_table.npy")
        except:
            self.q_table = np.zeros((256, 4))
        self.decay_rate = .999
        self.min_exploration = .025

    def monitor(self, snake): #function that looks at game state and returns 8 binary numbers
        eight_digits = np.zeros(8)
        if(snake.collision_body_up() or snake.collision_wall_up()):
            eight_digits[0] = 1
        if(snake.collision_body_down() or snake.collision_wall_down()):
            eight_digits[1] = 1
        if(snake.collision_body_left() or snake.collision_wall_left()):
            eight_digits[2] = 1
        if(snake.collision_body_right() or snake.collision_wall_right()):
            eight_digits[3] = 1
        if(snake.apple[1] < snake.head()[1]):
            eight_digits[4] = 1
        if(snake.apple[1] > snake.head()[1]):
            eight_digits[5] = 1
        if(snake.apple[0] < snake.head()[0]):
            eight_digits[6] = 1
        if(snake.apple[0] > snake.head()[0]):
            eight_digits[7] = 1

        return eight_digits
    
    def binary_to_int(self, snake):
        binary_array = self.monitor(snake)
        exponents = np.arange(len(binary_array))[::-1]
        power = 2 ** exponents
        int_val = np.dot(binary_array, power)
        return int(int_val)
    
    def decide(self, snake):
        state = self.binary_to_int(snake)
        random_choice = random.randint(0, 3)
        if(random.random() < self.exploration_rate):
            return random_choice
        else:
            return np.argmax(self.q_table[state])
        
    def update(self, state, action, reward, next_state):
        self.q_table[state][action] = self.q_table[state][action] + (self.learning_rate * (reward + self.discount_factor * np.max(self.q_table[next_state]) - self.q_table[state][action]))



