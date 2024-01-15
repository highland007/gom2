# gom/scene/scene_manager.py
# Manages user controls and scene interactions using Pygame

import pygame
from pygame.locals import *

class SceneManager:
    def __init__(self, renderer):
        self.renderer = renderer
        self.quit_requested = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.quit_requested = True
            elif event.type == KEYDOWN:
                if event.key == K_q:
                    self.quit_requested = True

    def run(self):
        while not self.quit_requested:
            self.handle_events()
            self.renderer.render()

