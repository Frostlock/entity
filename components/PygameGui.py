#Pygame GUI extension
import pygame

class GuiControl(pygame.Rect):
    """
    Super class for my custom pygame GUI controls.
    call draw when screen update is needed
    call handle_event when event handling is required
    typically both should be called in the main pygame loop
    """

    def __init__(self, x, y, w, h):
        super(GuiControl, self).__init__(x, y, w, h)

    def draw(self, screen):
        raise NotImplementedError()

    def handle_event(self, event):
        raise NotImplementedError()


class Button(GuiControl):
    """
    Button class
    """

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text
        self._refresh()

    @property
    def bg_color(self):
        return self._bg_color

    @bg_color.setter
    def bg_color(self, color):
        self._bg_color = color
        self._refresh()

    @property
    def text_color(self):
        return self._text_color

    @text_color.setter
    def text_color(self, color):
        self._text_color = color
        self._refresh()
        
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

    def _refresh(self):
        self._text_surface = self._font.render(self._text, True, self.text_color, self.bg_color)

    def draw(self, screen):
        # Button
        screen.fill(self.bg_color, self)
        # Text on button
        x = self.x + (self.w - self._text_surface.get_width()) // 2
        y = self.y + (self.h - self._text_surface.get_height()) // 2
        screen.blit(self._text_surface, (x, y))

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


class ColorPicker(GuiControl):
    """
    Color picker object
    """

    @property
    def on_click_function(self):
        return self._on_click_function

    @on_click_function.setter
    def on_click_function(self, function):
        self._on_click_function = function

    def __init__(self, x, y, w, h, image_path, on_click=None):
        super(ColorPicker, self).__init__(x, y, w, h)
        self.on_click_function = on_click
        #Load image
        self._image = pygame.image.load(image_path).convert()

    def draw(self, screen):
        screen.blit(self._image, self)

    def handle_event(self, event):
        if self.on_click_function is not None:
            # Can only handle mouse events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.collidepoint(*event.pos):
                    # convert mouse pposition to image coords
                    img_x = event.pos[0] - self.x
                    img_y = event.pos[1] - self.y
                    # get color at image coords
                    color = self._image.get_at((img_x, img_y))
                    # call handler
                    self.on_click_function(color)