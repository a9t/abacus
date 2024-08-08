import math
import pygame


class Ball:
    def __init__(self, manager, position, radius, color, movable):
        self.manager = manager
        self.color = color
        self.center = position
        self.radius = radius
        self.selected = False
        self.selected_offset = None
        self.movable = movable

    def update(self, event_list):
        if not self.movable:
            return

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.is_inside(event.pos):
                    self.selected = True
                    self.selected_offset = event.pos - self.center
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                if self.is_inside(event.pos):
                    self.manager.propose_move(self, pygame.Vector2(0, 0))
            elif event.type == pygame.MOUSEBUTTONUP:
                self.selected = False
            elif event.type == pygame.MOUSEMOTION and self.selected:
                self.manager.propose_move(self, event.pos - self.selected_offset)
                # self.center = event.pos + self.selected_offset

    def is_inside(self, pos):
        diff = pos - self.center
        dist = math.sqrt(diff[0]**2 + diff[1]**2)

        return dist < self.radius

    def move(self, position):
        if self.selected:
            self.selected_offset = pygame.mouse.get_pos() - position

        self.center = position

    def draw(self, surface):
        pygame.draw.circle(surface, "#000000", self.center, self.radius)
        pygame.draw.circle(surface, self.color, self.center, self.radius - 4)
