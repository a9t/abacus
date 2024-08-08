import pygame
import random


class TaskGenerator:
    def __init__(self, y):
        self.y = y
        self.font = pygame.font.SysFont('Comic Sans MS', 100)
        self.state = "passive"
        self.t1 = 0
        self.t2 = 0

    def draw(self, surface):
        color = "#333333"
        if self.t1 == "":
            return

        text_count = self.font.render(f"{self.t1} + {self.t2}", False, color)
        text_width = text_count.get_width()
        surface.blit(text_count, ((surface.get_width() - text_width)/2, self.y))

    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                return self.generate_random()

            if event.type != pygame.KEYDOWN:
                continue

            if self.state == "passive":
                if event.key == pygame.K_r:
                    return self.generate_random()
                elif event.key == pygame.K_n:
                    self.state = "input_first"
                    self.t1 = ""
                    self.t2 = ""
                    return "clear", ()
            elif self.state == "input_first":
                ok, val = self.__get_digit(event)
                if not ok:
                    continue

                self.t1 = val
                self.state = "input_second"

                return "nothing", ()
            elif self.state == "input_second":
                ok, val = self.__get_digit(event)
                if not ok:
                    continue

                self.t2 = val
                self.state = "passive"

                return "new", (self.t1, "+", self.t2)

        return "nothing", ()

    def __get_digit(self, event):
        val = event.key - pygame.K_0
        if val <= 0:
            return False, val

        if val >= 10:
            return False, val

        return True, val

    def generate_random(self):
        self.t1 = random.randint(1, 9)
        self.t2 = random.randint(1, 9)
        return "new", (self.t1, "+", self.t2)
