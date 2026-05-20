import pygame #Start of game background
import random
import database
from agent import Agent
import numpy as np
pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
CELL_SIZE = 80
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
font = pygame.font.SysFont(None, 100)
win_text = font.render("You Win!", True, GREEN)
text_rect = win_text.get_rect(center=(400, 400))

time = pygame.time.Clock()
FPS = 4

display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Snake") #end of game background

class Game: #Game implementation
    def __init__(self):
        self.length = 3
        self.body = [(2,5), (1,5), (0,5)]
        self.direction = "RIGHT"
        self.apple = (6,5)
        self.attempt = 0
        self.input = 0
        self.steps = 0
        self.death = 'N'

    def reset(self):
        self.length = 3
        self.body = [(2,5), (1,5), (0,5)]
        self.direction = "RIGHT"
        self.apple = (6,5)
        self.attempt += 1
        self.input = 0
        self.steps = 0
        self.death = 'N'

    def head(self):
        return self.body[0]
    
    def tail(self):
        return self.body[-1]
    
    def collision_body_up(self):
        return (self.head()[0], self.head()[1] - 1) in self.body[1:]
    
    def collision_body_down(self):
        return (self.head()[0], self.head()[1] + 1) in self.body[1:]
    
    def collision_body_left(self):
        return (self.head()[0] - 1, self.head()[1]) in self.body[1:]
    
    def collision_body_right(self):
        return (self.head()[0] + 1, self.head()[1]) in self.body[1:]
            
    def collision_wall_up(self):    
        return (self.head()[1] - 1 < 0)
    
    def collision_wall_down(self):    
        return (self.head()[1] + 1 > 9)
    
    def collision_wall_left(self):    
        return (self.head()[0] - 1 < 0)
    
    def collision_wall_right(self):    
        return (self.head()[0] + 1 > 9)
    
    def update(self):
        if(self.direction == "LEFT"):
            new_tuple = ((self.head()[0] - 1), self.head()[1])
        elif(self.direction == "RIGHT"):
            new_tuple = ((self.head()[0] + 1), self.head()[1])
        elif(self.direction == "DOWN"):
            new_tuple = (self.head()[0], (self.head()[1] + 1))
        elif(self.direction == "UP"):
            new_tuple = (self.head()[0], (self.head()[1] - 1))

        self.body.insert(0, new_tuple)

        result = self.crash()
        if(result != "GROW"):
                self.body.pop()

        self.steps += 1
        return result

    def crash(self):
        if(self.head()[0] > 9 or self.head()[0] < 0 or self.head()[1] > 9 or self.head()[1] < 0):
            self.death = 'W'
            return "END"

        for cell in self.body[1:]:
            if(self.head() == cell):
                self.death = 'B'
                return "END"
            
        if(self.head() == self.apple):
            self.length += 1
            if(self.length == 99):
                return "WIN"
            
            while(self.apple in self.body):
                self.apple = (random.randint(0, 9), random.randint(0, 9))

            return "GROW"
        
    def draw(self):
        pixel_Ax = self.apple[0] * CELL_SIZE
        pixel_Ay = self.apple[1] * CELL_SIZE
        pygame.draw.rect(display, RED, (pixel_Ax, pixel_Ay, CELL_SIZE, CELL_SIZE))

        for cell in self.body:
            pixel_x = cell[0] * CELL_SIZE
            pixel_y = cell[1] * CELL_SIZE
            pygame.draw.rect(display, GREEN, (pixel_x, pixel_y, CELL_SIZE, CELL_SIZE))



my_snake = Game()
my_agent = Agent()
run = True

while run: #loop that checks for game state
    display.fill(BLACK)
    my_snake.draw()
    pygame.display.update()
    dt = time.tick(FPS)

    agent_state = my_agent.binary_to_int(my_snake)
    agent_move = my_agent.decide(my_snake)
    if(agent_move == 0):
        my_snake.direction = "UP"
        my_snake.input += 1
    if(agent_move == 1):
        my_snake.direction = "DOWN"
        my_snake.input += 1
    if(agent_move == 2):
        my_snake.direction = "LEFT"
        my_snake.input += 1
    if(agent_move == 3):
        my_snake.direction = "RIGHT"
        my_snake.input += 1
    state = my_snake.update()

    reward = 0
    if(state == "GROW"):
        reward = 3
    elif(state == "END"):
        reward = -10
    else:
        reward = 0
    next_state = my_agent.binary_to_int(my_snake)
    my_agent.update(agent_state, agent_move, reward, next_state)

    if state == "END":
            database.insert_attempt(my_snake)
            my_snake.reset()
            my_agent.exploration_rate = max(my_agent.min_exploration, my_agent.exploration_rate * my_agent.decay_rate)
    if state == "WIN":
        database.insert_attempt(my_snake)
        run = False
        display.blit(win_text, text_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            np.save("q_table.npy", my_agent.q_table)
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                my_snake.direction = "LEFT"
            if event.key == pygame.K_RIGHT:
                my_snake.direction = "RIGHT"
            if event.key == pygame.K_DOWN:
                my_snake.direction = "DOWN"
            if event.key == pygame.K_UP:
                my_snake.direction = "UP"
            my_snake.input += 1


if state == "WIN":
    while True:
        display.fill(BLACK)
        display.blit(win_text, text_rect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                np.save("q_table.npy", my_agent.q_table)
                pygame.quit()
                
pygame.quit()

