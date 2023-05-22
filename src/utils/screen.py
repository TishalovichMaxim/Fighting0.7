import pygame

class Screen:
    def __init__(self):
        self.screen = pygame.display.set_mode()
        self.drawing_items = []

    def add(self, item):
        self.drawing_items.append(item)

    def draw(self):
        for item in self.drawing_items:
            item.draw(self.screen)