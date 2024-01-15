# gom/scene/scene_renderer.py
# Handles graphical rendering of the scene using Pygame

import pygame
from pygame.locals import *
from scene.scene_manager import SceneManager
from scene.settings import SceneSettings

class SceneRenderer:
    def __init__(self, scene, settings=None):
        self.scene = scene
        self.settings = settings or SceneSettings()
        self.quit_requested = False
        self.scene_manager = SceneManager(self)

        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Game of Mirrors 2D")

    def render(self):
        self.scene.update()
        self.draw_elements()
        pygame.display.update()

    def draw_elements(self):
        # Create a surface to draw on
        surface = pygame.Surface((800, 600))

        # Clear the surface
        surface.fill(self.settings.background_color)

        # Render elements
        for element in self.scene.root_assembly.elements:
            x, y, angle = element.pose  # Get x coordinate, y coordinate, and angle
            width, height = element.size  # Get width and height

            # Draw rectangle on the surface
            pygame.draw.rect(surface, (255, 0, 0), (x, y, width, height))

        # Blit the surface onto the screen
        self.screen.blit(surface, (0, 0))

        pygame.display.update()

    def quit(self):
        pygame.quit()

