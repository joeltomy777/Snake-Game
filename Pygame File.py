import time
import random
import pygame
from pygame.locals import *

SIZE = 20
Background_Colour = (92, 25, 84)
starting_length=1

class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load('resources/apple.jpg').convert()
        self.parent_screen = parent_screen
        self.x = random.randint(0, 24) * SIZE
        self.y = random.randint(0, 19) * SIZE

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0, 24)*SIZE
        self.y = random.randint(0, 19)*SIZE


class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load('resources/block.jpg').convert()
        self.direction = random.choice(['up', 'down', 'left', 'right'])

        self.x, self.y = [500] * length, [400] * length

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        self.parent_screen.fill(Background_Colour)
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def walk(self):
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        self.draw()


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Snake and Apple Game')

        pygame.mixer.init()
        self.background_music()

        self.surface = pygame.display.set_mode((1000, 800))
        self.surface.fill(Background_Colour)
        self.snake = Snake(self.surface,starting_length)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collision(self, x2, y2, x1, y1):
        if x2>=x1 and x2<x1+SIZE:
            if y2 >= y1 and y2 < y1 + SIZE:
                return True
        return False

    def background_music(self):
        pygame.mixer.music.load('resources/bg.mp3')
        pygame.mixer.music.play(loops=-1)

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f'resources/{sound}.mp3')
        pygame.mixer.Sound.play(sound)

    def render_background(self):
        bg = pygame.image.load('resources/bgpic.jpg')
        self.surface.blit(bg, (0, 0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # snake eating apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound('ding')
            self.snake.increase_length()
            self.apple.move()

        # snake biting itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')
                raise 'Game over'

        # snake hitting walls
        if self.snake.x[0]<0 or self.snake.x[0]>=1000 or self.snake.y[0]<0 or self.snake.y[0]>=800:
            self.play_sound('crash')
            raise 'Game over'

    def display_score(self):
        font=pygame.font.SysFont('arial', 30)
        score=font.render(f"Score: {self.snake.length-1}", True, (255, 255, 255))
        self.surface.blit(score, (800, 10))

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Game is over!! Your score is  {self.snake.length - 1}", True, (255, 255, 255))
        self.surface.blit(score, (200, 300))
        msg = font.render('To play again press ENTER, to exit press ESC!', True, (255, 255, 255))
        self.surface.blit(msg, (200, 350))
        pygame.display.flip()
        pygame.mixer.music.pause()

    def reset(self):
        self.snake = Snake(self.surface, starting_length)
        self.apple = Apple(self.surface)

    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False
                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            if self.snake.length < 5:
                time.sleep(0.2)
            elif self.snake.length >= 5 and self.snake.length < 10:
                time.sleep(0.15)
            elif self.snake.length >= 10 and self.snake.length < 20:
                time.sleep(0.1)
            elif self.snake.length >= 20 and self.snake.length < 30:
                time.sleep(0.075)
            elif self.snake.length >= 30 and self.snake.length < 40:
                time.sleep(0.05)
            elif self.snake.length >= 40:
                time.sleep(0.025)

if __name__ == '__main__':
    game = Game()
    game.run()
