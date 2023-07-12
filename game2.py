import pygame
import random
import sys

# Pygame configuration
pygame.init()
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Avoid the Enemies Game")
FONT = pygame.font.Font(None, 36)

# Game states
MENU = 0
GAME = 1
GAME_OVER = 2

# Game modes
EASY = 0
MEDIUM = 1
HARD = 2

# Colors
PLAYER_COLOR = (0, 0, 255)
ENEMY_COLOR = (255, 0, 0)

ENEMY_RADIUS = 25

class Player:
    def __init__(self, radius, pos, color, speed):
        self.radius = radius
        self.pos = pos
        self.color = color
        self.speed = speed

    def draw(self):
        pygame.draw.circle(WIN, self.color, self.pos, self.radius)

    def move_left(self):
        if self.pos[0] - self.speed > self.radius:
            self.pos[0] -= self.speed

    def move_right(self):
        if self.pos[0] + self.speed < WIDTH - self.radius:
            self.pos[0] += self.speed

class Enemy:
    def __init__(self, radius, pos, color, speed):
        self.radius = radius
        self.pos = pos
        self.color = color
        self.speed = speed

    def draw(self):
        pygame.draw.circle(WIN, self.color, self.pos, self.radius)

    def update_position(self):
        self.pos[1] += self.speed
        # Check if the enemy has moved past the bottom edge of the screen
        return self.pos[1] - self.radius > HEIGHT

    def detect_collision(self, player):
        distance = ((self.pos[0] - player.pos[0]) ** 2 + (self.pos[1] - player.pos[1]) ** 2) ** 0.5
        return distance < self.radius + player.radius

class Game:
    def __init__(self, mode):
        self.mode = mode
        self.score = 0
        self.frame_count = 0
        self.enemy_list = []
        self.set_mode_parameters()

    def set_mode_parameters(self):
        if self.mode == EASY:
            self.spawn_number = 1
            self.enemy_speed = 5
            self.enemy_spawn_rate = 120
        elif self.mode == MEDIUM:
            self.spawn_number = 1
            self.enemy_speed = 10
            self.enemy_spawn_rate = 60
        elif self.mode == HARD:
            self.spawn_number = 2
            self.enemy_speed = 10
            self.enemy_spawn_rate = 30

    def update(self, player):
        self.frame_count += 1
        if self.frame_count >= self.enemy_spawn_rate:
            for _ in range(self.spawn_number):
                new_enemy_pos = [random.randrange(ENEMY_RADIUS, WIDTH - ENEMY_RADIUS), ENEMY_RADIUS]
                new_enemy = Enemy(ENEMY_RADIUS, new_enemy_pos, ENEMY_COLOR, self.enemy_speed)
                self.enemy_list.append(new_enemy)
            self.score += 100
            self.enemy_speed += 0.1
            self.frame_count = 0

        if self.mode == HARD and self.frame_count % 300 == 0:
            self.spawn_number = min(4, self.spawn_number + 1)

        # Update enemy positions and remove enemies that have moved off screen
        self.enemy_list = [enemy for enemy in self.enemy_list if not enemy.update_position()]

        # Check for collisions
        for enemy in self.enemy_list:
            if enemy.detect_collision(player):
                return True

        return False

    def draw(self):
        for enemy in self.enemy_list:
            enemy.draw()
        draw_text("Score: " + str(self.score), (80, 50))

def draw_text(text, pos):
    text_surface = FONT.render(text, True, (255, 255, 255))
    rect = text_surface.get_rect()
    rect.center = pos
    WIN.blit(text_surface, rect)
    return rect

def main():
    game_state = MENU
    game_mode = None
    player = Player(25, [WIDTH / 2, HEIGHT - 1.5 * 25], (0, 0, 255), 10)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        WIN.fill((0, 0, 0))

        if game_state == MENU:
            new_game_rect = draw_text("New Game (Easy)", (WIDTH/2, HEIGHT/2 - 60))
            medium_game_rect = draw_text("New Game (Medium)", (WIDTH/2, HEIGHT/2))
            hard_game_rect = draw_text("New Game (Hard) !Recommended!", (WIDTH/2, HEIGHT/2 + 60))
            mouse_pos = pygame.mouse.get_pos()
            if new_game_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
                game_mode = EASY
            elif medium_game_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
                game_mode = MEDIUM
            elif hard_game_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
                game_mode = HARD
            if game_mode is not None:
                game = Game(game_mode)
                game_state = GAME

        elif game_state == GAME:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player.move_left()
            if keys[pygame.K_RIGHT]:
                player.move_right()
            if game.update(player):
                game_state = GAME_OVER
            player.draw()
            game.draw()

        elif game_state == GAME_OVER:
            draw_text("Game Over", (WIDTH/2, HEIGHT/2 - 50))
            draw_text("Final Score: " + str(game.score), (WIDTH/2, HEIGHT/2))
            restart_rect = draw_text("Click here to Restart", (WIDTH/2, HEIGHT/2 + 50))
            mouse_pos = pygame.mouse.get_pos()
            if restart_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
                game_state = MENU

        pygame.display.update()
        pygame.time.Clock().tick(60)

if __name__ == "__main__":
    main()
