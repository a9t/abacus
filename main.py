# Example file showing a circle moving on screen
import pygame

from body_manager import BodyManager
from task_generator import TaskGenerator


WIDTH = 1920
HEIGHT = 1000

# pygame setup
pygame.init()
pygame.font.init()

pygame.display.set_caption("Sume")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0

task_generator = TaskGenerator(300)
_, values = task_generator.generate_random()

body_manager = BodyManager(50, WIDTH-50, 500)
body_manager.add_immobile(values[0])
body_manager.add_mobile(values[2])


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("#AAAAAA")

    for ball in body_manager.balls:
        ball.update(event_list)

    task, values = task_generator.update(event_list)
    if task == "new":
        body_manager.clear()
        body_manager.add_immobile(values[0])
        body_manager.add_mobile(values[2])
    elif task == "clear":
        body_manager.clear()

    task_generator.draw(screen)
    body_manager.draw(screen)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        pass

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
