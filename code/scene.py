import pygame

class Scene:
    def __init__(self) -> None:
        self.widgets_grp = set()
        self.surfaces = []

    def add_widget(self, widgets):
        for widget in widgets:
            self.widgets_grp.add(widget)

    def draw(self, screen):
        for surf, pos in self.surfaces:
            screen.blit(surf, pos)