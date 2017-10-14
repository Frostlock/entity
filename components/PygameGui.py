#Pygame GUI extension
import pygame

class Button(pygame.Rect):
    """
    Button class
    Instantiate
    call draw when screen update is needed
    call handle_event when event handling is required
    typically both should be called in the main pygame loop
    """

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text
        self._text_surface = self._font.render(self._text, True, self._text_color, self._bg_color)

    @property
    def on_click_function(self):
        return self._on_click_function

    @on_click_function.setter
    def on_click_function(self, function):
        self._on_click_function = function

    def __init__(self, x, y, w, h, text="", bg_color=(150,150,150), text_color=(255, 255, 255), on_click=None):
        super(Button, self).__init__(x, y, w, h)
        self._font = pygame.font.Font(None, 20)
        self._bg_color = bg_color
        self._text_color = text_color
        self.text = text
        self.on_click_function = on_click

    def center(self):
        x = self.x + (self.w - self._text_surface.get_width()) // 2
        y = self.y + (self.h - self._text_surface.get_height()) // 2
        return (x, y)

    def draw(self, screen):
        # Button
        screen.fill(self._bg_color, self)
        # Text on button
        screen.blit(self._text_surface, self.center())

    def handle_event(self, event):
        if self.on_click_function is not None:
            # Can only handle mouse events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.collidepoint(*event.pos):
                    self.on_click_function()


class Menu(object):
    """
    Menu screen built-up out of multiple pygame components.
    """

    @property
    def components(self):
        """
        Children components of this Menu.
        :return: List of children components
        """
        return self._components

    @property
    def bg_color(self):
        return self._bg_color

    @bg_color.setter
    def bg_color(self, color):
        self._bg_color = color

    def __init__(self, screen):
        self._components = []
        self._bg_color = (0, 0, 0)
        self._screen = screen

    def add(self, component):
        self._components.append(component)

    def draw(self):
        """
        Draws this menu on the screen
        :return:
        """
        # Fill with background color
        self._screen.fill(self.bg_color)

        # draw components
        for component in self.components:
            component.draw(self._screen)

    def handle_event(self, event):
        # Pass all events to children components
        for component in self.components:
            component.handle_event(event)