import pygame
import random

# Initialize pygame
pygame.init()

# Setup display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Brick Shooter Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Clock for controlling frame rate
clock = pygame.time.Clock()


class Paddle:
    def __init__(self):
        self.width = 100
        self.height = 20
        self.x = (width - self.width) // 2
        self.y = height - self.height - 10
        self.speed = 8

    def move(self, dx):
        self.x += dx
        # Keep paddle within the screen
        if self.x < 0:
            self.x = 0
        elif self.x > width - self.width:
            self.x = width - self.width
    
    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))

class Ball:
    def __init__(self):
        self.radius = 10
        self.x = width // 2
        self.y = height // 2
        self.x_speed = 4 * random.choice([1, -1])
        self.y_speed = -4

    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed

    def draw(self):
        pygame.draw.circle(screen, GREEN, (self.x, self.y), self.radius)

class Brick:
    def __init__(self, x, y):
        self.width = 60
        self.height = 30
        self.x = x
        self.y = y
        self.hit = False

    def draw(self):
        if not self.hit:
            pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))

def ball_paddle_collision(ball, paddle):
    if(paddle.x < ball.x < paddle.x + paddle.width) and (paddle.y < ball.y + ball.radius < paddle.y + paddle.height):
        return True
    return False

def ball_brick_collision(ball, bricks):
    for brick in bricks:
        if not brick.hit:
            if (brick.x < ball.x < brick.x + brick.width) and (brick.y < ball.y + ball.radius < brick.y + brick.height):
                brick.hit = True
                return True
    return False

def main():
    paddle = Paddle()
    ball = Ball()
    bricks = [Brick(x * 70 + 50, y * 40 + 50) for y in range(5) for x in range(10)]

    score = 0 # Initialize

    running = True
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Paddle movement (left and right)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move(-paddle.speed)
        if keys[pygame.K_RIGHT]:
            paddle.move(paddle.speed)

        # Ball movement and bouncing off walls
        ball.move()
        if ball.x - ball.radius <= 0 or ball.x + ball.radius >= width:
            ball.x_speed = - ball.x_speed
        if ball.y - ball.radius <= 0:
            ball.y_speed = - ball.y_speed
        if ball.y + ball.radius >= height:
            print("Game Over!")
            running = False

        # Check for collisions
        if ball_paddle_collision(ball, paddle):
            ball.y_speed = -ball.y_speed
        if ball_brick_collision(ball, bricks):
            ball.y_speed = -ball.y_speed
            score += 10

        # Draw game objects
        paddle.draw()
        ball.draw()
        for brick in bricks:
            brick.draw()

        # Draw the score
        font = pygame.font.SysFont("Arial", 30)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Update the display
        pygame.display.update()

        # Frame rate
        clock.tick(60)

    pygame.quit()

# Start the game
if __name__ == "__main__":
    main()