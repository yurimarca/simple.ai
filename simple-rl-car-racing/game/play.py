import os
import gymnasium as gym
import pygame
from pygame.locals import *

# Set SDL_VIDEODRIVER to x11 to use XWayland
os.environ["SDL_VIDEODRIVER"] = "x11"

# Initialize Pygame and the CarRacing environment
pygame.init()
env = gym.make('CarRacing-v2', render_mode='human')

# Reset the environment to start a new episode
observation, info = env.reset()

# Initialize variables to keep track of the total reward and number of steps
total_reward = 0
steps = 0

# Create a Pygame window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("CarRacing-v2")

# Function to map keyboard inputs to actions
def get_action(keys):
    action = [0, 0, 0]
    if keys[K_LEFT]:
        action[0] = -1.0
    if keys[K_RIGHT]:
        action[0] = 1.0
    if keys[K_UP]:
        action[1] = 1.0
    if keys[K_DOWN]:
        action[2] = 0.8
    return action

# Run one episode
done = False
while not done:
    print("Running...")
    
    env.render()  # Render the environment
    
    # Get keyboard input
    keys = pygame.key.get_pressed()
    action = get_action(keys)
    
    # Step the environment forward
    observation, reward, done, truncated, info = env.step(action)
    
    # Update the total reward and steps
    total_reward += reward
    steps += 1

    # Check for Pygame events
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            done = True

    # If the episode is done, reset the environment
    if done or truncated:
        print(f"Episode finished after {steps} steps with total reward {total_reward}")
        break

# Close the environment and Pygame
env.close()
pygame.quit()
