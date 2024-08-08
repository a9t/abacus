import math
import pygame

from ball import Ball


RADIUS = 30
OFFSET_Y = 20


class BodyManager():
    def __init__(self, x_left, x_right, y_axis):
        self.x_left = x_left
        self.x_right = x_right
        self.y_axis = y_axis + RADIUS + OFFSET_Y
        self.balls = []
        self.right_hidden_ball = Ball(self, pygame.Vector2(
            self.x_right + RADIUS, self.y_axis), RADIUS, "white", False)
        self.font = pygame.font.SysFont('Comic Sans MS', 30)

    def clear(self):
        self.balls = []

    def add_immobile(self, count):
        self.__add_balls(count, self.x_left, RADIUS+RADIUS, "red", False)

    def add_mobile(self, count):
        self.__add_balls(count, self.x_right, -RADIUS-RADIUS, "blue", True)

    def __add_balls(self, count, xpos, pace, color, movable):
        temp_balls = []
        for _ in range(count):
            ball_pos = pygame.Vector2(xpos, self.y_axis)
            ball = Ball(self, ball_pos, RADIUS, color, movable)
            temp_balls.append(ball)
            xpos += pace

        if movable:
            temp_balls.reverse()

        self.balls = self.balls + temp_balls

    def draw(self, screen):
        line_color = "#333333"
        y = self.y_axis - RADIUS - OFFSET_Y
        pygame.draw.line(screen, line_color, (self.x_left -
                         RADIUS, y), (self.x_right + RADIUS, y), 4)

        x_tick = self.x_left - RADIUS
        for index in range(1, 22):
            pygame.draw.line(screen, line_color,
                             (x_tick, y), (x_tick, y - 5), 4)

            if index <= 20:
                text_count = self.font.render(f"{index}", False, line_color)
                text_width = text_count.get_width()
                screen.blit(text_count, (x_tick + RADIUS - text_width/2, y - 40))

            x_tick += RADIUS + RADIUS

        for ball in self.balls:
            ball.draw(screen)

    def propose_move(self, ball, move_to):
        move_to[1] = self.y_axis
        pos = self.balls.index(ball)

        if move_to[0] - ball.center[0] < 0:
            neighbor = self.balls[pos-1]
            mult = 1
        else:
            if pos == len(self.balls) - 1:
                neighbor = self.right_hidden_ball
            else:
                neighbor = self.balls[pos+1]
            mult = -1

        diff = move_to - neighbor.center
        move_neighbor = diff[0] * mult - RADIUS - RADIUS
        if move_neighbor < 0:
            # neighbor needs to move
            if neighbor.movable:
                neigh_pos = neighbor.center.copy()
                neigh_pos[0] += mult * move_neighbor

                neigh_center = self.propose_move(neighbor, neigh_pos)
            else:
                neigh_center = neighbor.center

            move_to[0] = neigh_center[0] + mult * (RADIUS + RADIUS)
        else:
            # neighbor does not need to move
            pass

        ball.move(move_to)
        return move_to
