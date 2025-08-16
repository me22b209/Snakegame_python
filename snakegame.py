import pygame
import random
from collections import deque

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game - Player & AI Mode")
clock = pygame.time.Clock()

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.body = [(5, 5), (4, 5), (3, 5)]  # Start with length 3
        self.direction = RIGHT
        self.grow = False

    def move(self):
        head = (self.body[0][0] + self.direction[0],
                self.body[0][1] + self.direction[1])
        self.body.insert(0, head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def change_direction(self, dir):
        # Prevent reversing directly into itself
        if (dir[0] * -1, dir[1] * -1) != self.direction:
            self.direction = dir

    def collide_self(self):
        return self.body[0] in self.body[1:]

    def collide_wall(self):
        x, y = self.body[0]
        return x < 0 or y < 0 or x >= GRID_WIDTH or y >= GRID_HEIGHT

class Food:
    def __init__(self):
        self.position = (10, 10)

    def spawn(self, snake_body):
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1),
                   random.randint(0, GRID_HEIGHT - 1))
            if pos not in snake_body:
                self.position = pos
                break

def draw(snake, food, score, mode):
    screen.fill(BLACK)
    # Draw snake
    for segment in snake.body:
        pygame.draw.rect(screen, GREEN, (segment[0]*CELL_SIZE, segment[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    # Draw food
    pygame.draw.rect(screen, RED, (food.position[0]*CELL_SIZE, food.position[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    # Score
    font = pygame.font.SysFont(None, 24)
    score_text = font.render(f"Score: {score} | Mode: {mode}", True, WHITE)
    screen.blit(score_text, (10, 10))
    pygame.display.flip()

def bfs_path(start, goal, snake_body):
    """Find shortest path from start to goal avoiding snake body."""
    queue = deque([(start, [])])
    visited = set([start])
    directions = [UP, DOWN, LEFT, RIGHT]
    snake_body = set(snake_body)
    snake_body.remove(start)  # Allow head position

    while queue:
        current, path = queue.popleft()
        if current == goal:
            return path
        for d in directions:
            next_pos = (current[0] + d[0], current[1] + d[1])
            if (0 <= next_pos[0] < GRID_WIDTH and
                0 <= next_pos[1] < GRID_HEIGHT and
                next_pos not in visited and
                next_pos not in snake_body):
                queue.append((next_pos, path + [d]))
                visited.add(next_pos)
    return []

def main():
    snake = Snake()
    food = Food()
    food.spawn(snake.body)
    score = 0
    mode = "PLAYER"  # Start safe in Player mode
    running = True
    start_delay = 5  # frames before snake moves

    while running:
        clock.tick(10)  # Game speed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if mode == "PLAYER":
                    if event.key == pygame.K_UP:
                        snake.change_direction(UP)
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction(DOWN)
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction(RIGHT)
                if event.key == pygame.K_SPACE:
                    mode = "AI" if mode == "PLAYER" else "PLAYER"

        # AI mode logic
        if mode == "AI":
            path = bfs_path(snake.body[0], food.position, snake.body)
            if path:  # Only change direction if path exists
                snake.direction = path[0]

        # Start delay before first move
        if start_delay > 0:
            start_delay -= 1
            draw(snake, food, score, mode)
            continue

        snake.move()

        # Check collisions
        if snake.collide_self() or snake.collide_wall():
            print(f"Game Over! Final Score: {score}")
            running = False

        # Eat food
        if snake.body[0] == food.position:
            snake.grow = True
            score += 1
            food.spawn(snake.body)

        draw(snake, food, score, mode)

    pygame.quit()

if __name__ == "__main__":
    main()
