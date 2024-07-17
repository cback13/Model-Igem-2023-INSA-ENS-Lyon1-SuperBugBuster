import pygame
import random
import math
import imageio

# Initialize Pygame
pygame.init()

# Window parameters
width, height = 400, 300
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("2D Ball Simulation")

# Define colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
DARK_GREEN = (0, 128, 0)
LIGHT_GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)

# Class to represent a ball
class Ball:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.reproduction_rate = {
            DARK_GREEN: 2.3,  # Reproduction rate for dark green balls
            LIGHT_GREEN: 2.3,  # Reproduction rate for light green balls
            RED: 1.39,  # Reproduction rate for red balls
            ORANGE: 1.39,  # Reproduction rate for orange balls
        }
        self.mortality_rate = {
            BLUE: 0.02,  # Mortality rate for blue balls
        }

    def reproduce(self):
        if self.color in self.reproduction_rate:
            if random.random() < self.reproduction_rate[self.color] * dt:
                return Ball(self.x, self.y, self.color)
        return None

    def die(self):
        if self.color in self.mortality_rate:
            if random.random() < self.mortality_rate[self.color] * dt:
                return True
        return False

    def move(self):
        # Calculate the new displacement
        dx = random.uniform(-10, 10)
        dy = random.uniform(-10, 10)

        # Update coordinates
        self.x += dx
        self.y += dy

        # Check if the ball reaches the window borders
        if self.x < 0 or self.x > width:
            self.x = max(0, min(self.x, width))
        if self.y < 0 or self.y > height:
            self.y = max(0, min(self.y, height))

    def collision(self, other_ball):
        distance = math.sqrt((self.x - other_ball.x)**2 + (self.y - other_ball.y)**2)
        return distance < 10  # Collision radius

    def change_color(self, other_ball):
        if self.color == BLUE:
            if other_ball.color == RED:
                if random.random() < 0.52:
                    other_ball.color = ORANGE
            elif other_ball.color == DARK_GREEN:
                if random.random() < 0.52:
                    other_ball.color = LIGHT_GREEN
        elif self.color == RED:
            if other_ball.color == DARK_GREEN:
                if random.random() < 0.8:
                    other_ball.color = RED
            elif other_ball.color == LIGHT_GREEN:
                if random.random() < 0.8:
                    other_ball.color = RED
        elif self.color == ORANGE:
            if other_ball.color == LIGHT_GREEN:
                if random.random() < 0.8:
                    other_ball.color = ORANGE
            elif other_ball.color == DARK_GREEN:
                if random.random() < 0.8:
                    other_ball.color = ORANGE
        elif self.color == LIGHT_GREEN:
            if random.random() < 0.3:
                self.color = DARK_GREEN

# List of balls
balls = [Ball(random.randint(0, width), random.randint(0, height), BLUE) for _ in range(10)]
balls += [Ball(random.randint(0, width), random.randint(0, height), RED) for _ in range(5)]
balls += [Ball(random.randint(0, width), random.randint(0, height), DARK_GREEN) for _ in range(5)]

# Video parameters
fps = 30
video_duration = 30 / 3600  # 30 seconds

# Create a list to store video frames
frames = []

# Time between each frame
time_between_frames = 1 / fps

# Total simulation time in hours
total_simulation_time = 15  # 15 hours
dt = time_between_frames / total_simulation_time

# Variables for displaying "Induction"
induction_displayed = False
induction_display_duration = 0.5  # Duration of "Induction" display in hours

# Initial time
time = 0

# Main loop
running = True
video_completed = False

while running and time <= total_simulation_time:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill((0, 0, 0))  # Black background

    if not induction_displayed and time >= 2.0:
        # Check the percentage of red and orange balls
        font = pygame.font.Font(None, 36)
        text = font.render("Induction", True, (255, 255, 255))
        text_rect = text.get_rect(center=(width // 2, height // 2))
        window.blit(text, text_rect)
        induction_displayed = True
        # During induction, change all balls except red ones to dark green
        for ball in balls:
            if ball.color != RED:
                ball.color = DARK_GREEN
        red_percentage = sum(1 for ball in balls if ball.color == RED) / len(balls)
        if red_percentage < 0.2:
            # If less than 10% red and orange balls, remove them
            balls = [ball for ball in balls if ball.color != RED]

    elif any(ball.color != DARK_GREEN for ball in balls):
        for ball in balls:
            ball.move()
            new_ball = ball.reproduce()
            if new_ball:
                balls.append(new_ball)
            if ball.die():
                balls.remove(ball)

        for ball1 in balls:
            for ball2 in balls:
                if ball1 != ball2 and ball1.collision(ball2):
                    ball1.change_color(ball2)

        for ball in balls:
            pygame.draw.circle(window, ball.color, (int(ball.x), int(ball.y)), 10)

        # Capture the current frame for the video
        image = pygame.surfarray.array3d(window)
        image = image.swapaxes(0, 1)  # Correct orientation
        frames.append(image)

        # Update time
        time += dt

        pygame.display.flip()

        pygame.time.delay(int(1000 / fps))  # Delay in milliseconds

    else:
        # Remaining time for dark green ball multiplication phase
        remaining_time = total_simulation_time - time
        if remaining_time > 0:
            red_percentage = sum(1 for ball in balls if ball.color == RED) / len(balls)
            if red_percentage < 0.2:
                # If less than 10% red and orange balls, remove them
                balls = [ball for ball in balls if ball.color not in (RED)]
            # Allow dark green balls to multiply during the remaining time
            for ball in balls:
                if ball.color == DARK_GREEN:
                    new_ball = ball.reproduce()
                    if new_ball:
                        balls.append(new_ball)

            for ball1 in balls:
                for ball2 in balls:
                    if ball1 != ball2 and ball1.collision(ball2):
                        ball1.change_color(ball2)

            for ball in balls:
                pygame.draw.circle(window, ball.color, (int(ball.x), int(ball.y)), 10)

            # Capture the current frame for the video
            image = pygame.surfarray.array3d(window)
            image = image.swapaxes(0, 1)  # Correct orientation
            frames.append(image)

            pygame.display.flip()

            pygame.time.delay(int(1000 / fps))  # Delay in milliseconds
            time += dt

# Save the video as a GIF
imageio.mimsave('simulation.gif', frames, duration=1 / fps)

pygame.quit()
