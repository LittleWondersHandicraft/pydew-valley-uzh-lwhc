from collections.abc import Callable

import pygame
from pygame.math import Vector2 as vector
from pygame.mouse import get_pressed as mouse_buttons

from src.enums import GameState
from src.gui.menu.components import Button
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from src.support import resource_path


class GeneralMenu:
    def __init__(
            self, title: str, options: list[str], switch: Callable[[GameState], None],
            size: tuple[int, int], center: vector = None
    ):
        if center is None:
            center = vector()

        # general setup
        self.display_surface = pygame.display.get_surface()
        self.buttons_surface = pygame.Surface(size)
        self.buttons_surface.set_colorkey('green')
        self.font = pygame.font.Font(resource_path('font/LycheeSoda.ttf'), 30)
        self.title = title

        # rect
        self.center = center
        self.size = size
        self.rect = None
        self.rect_setup()

        # buttons
        self.pressed_button = None
        self.options = options
        self.buttons = []
        self.button_setup()

        # switch
        self.switch_screen = switch

    # setup
    def rect_setup(self):
        self.rect = pygame.Rect((0, 0), self.size)
        screen_center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.rect.center = self.center or screen_center

    def button_setup(self):
        # button setup
        button_width = 400
        button_height = 50
        size = (button_width, button_height)
        space = 10
        top_margin = 20

        # generic button rect
        generic_button_rect = pygame.Rect((0, 0), size)
        generic_button_rect.top = self.rect.top + top_margin
        generic_button_rect.centerx = self.rect.centerx

        # create buttons
        for title in self.options:
            rect = generic_button_rect
            button = Button(title, self.font, rect, self.rect.topleft)
            self.buttons.append(button)
            generic_button_rect = rect.move(0, button_height + space)

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN and mouse_buttons()[0]:
            self.pressed_button = self.get_hovered_button()
            if self.pressed_button:
                self.pressed_button.start_press_animation()
                return True

        if event.type == pygame.MOUSEBUTTONUP:
            if self.pressed_button:
                self.pressed_button.start_release_animation()

                if self.pressed_button.mouse_hover():
                    self.button_action(self.pressed_button.text)
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

                self.pressed_button = None
                return True

        return False

    def get_hovered_button(self):
        for button in self.buttons:
            if button.mouse_hover():
                return button
        return None

    def mouse_hover(self):
        for button in self.buttons:
            if button.hover_active:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                return
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def button_action(self, text: str):
        if text == 'Play':
            self.switch_screen(GameState.LEVEL)
        if text == 'Quit':
            self.quit_game()

    def quit_game(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    # draw
    def draw_title(self):
        text_surf = self.font.render(self.title, False, 'Black')
        midtop = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 20)
        text_rect = text_surf.get_frect(midtop=midtop)

        bg_rect = pygame.Rect((0, 0), (200, 50))
        bg_rect.center = text_rect.center

        pygame.draw.rect(self.display_surface, 'White', bg_rect, 0, 4)
        self.display_surface.blit(text_surf, text_rect)

    def draw_buttons(self):
        self.buttons_surface.fill('green')
        for button in self.buttons:
            button.draw(self.display_surface)
        self.display_surface.blit(self.buttons_surface, self.rect.topleft)

    def draw(self):
        self.display_surface.fill('cadetblue')
        self.draw_title()
        self.draw_buttons()

    # update
    def update_buttons(self, dt: float):
        for button in self.buttons:
            button.update(dt)

    def update(self, dt: float):
        self.mouse_hover()
        self.update_buttons(dt)
        self.draw()
