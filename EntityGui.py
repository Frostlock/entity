import pygame
import os
import _thread
from Entity import Entity, EntityStates
from components import PygameGui
from components import HueInterface

COLORS_BG = {EntityStates.SLEEPING : (110, 110, 110),
                 EntityStates.LISTENING: (0, 200, 0),
                 EntityStates.BUSY: (200, 0, 0)}
COLOR_TEXT = (210, 210, 210)
COLOR_TEXT_BG = (40, 40, 40)
COLOR_BUTTON_BG_ON = (238, 232, 170)
COLOR_BUTTON_BG_OFF = (180, 180, 180)
COLOR_BUTTON_TEXT = (10, 10, 10)

class EntityGui(object):
    """
    GUI class for Entity.
    This class implements a Pygame GUI to manage/interact an Entity instance.
    It is based on Pygame and it can run without an X environment.
    """

    def __init__(self):
        """
        Constructor
        """
        # Initialize pygame display
        # This approach allows this to run both within an X server environment or from regular
        # terminal (using the linux framebuffer)
        #
        # Reminder: When using the framebuffer print statements wont be displayed in the console!
        # To see them you need to direct output to a file. This makes sense, the terminal is not
        # being updated while pygame is using the framebuffer.
        #
        disp_no = os.getenv('DISPLAY')
        if disp_no:
            pygame.display.init()
            print("Pygame running under X display {0}".format(disp_no))
        else:
            print("No X display available, trying the framebuffer.")
            drivers = ['fbcon', 'directfb', 'svgalib']
            found = False
            for driver in drivers:
                if not os.getenv('SDL_VIDEODRIVER'):
                    os.putenv('SDL_VIDEODRIVER', driver)
                try:
                    pygame.display.init()
                    print('Using driver: {0}.'.format(driver))
                except pygame.error:
                    print('Driver: {0} failed.'.format(driver))
                    continue
                found = True
                break
            if not found:
               raise Exception('No suitable video driver found! (Start this on the console, not via ssh)')

        # force display size to 800*480 (the size of the raspberry touchscreen)
        display_width = 800
        display_height = 480
        size = (display_width, display_height)

        # Full screen option is not required.
        # In an X server environment prefer to run this in a window.
        # In a terminal environment it will be full screen anyway.
        self.screen = pygame.display.set_mode(size)#, pygame.FULLSCREEN)

        # Mouse tracking on the touchscreen is off for some reason
        # The movement of the mouse slightly exaggerates the movement on the touchscreen
        # Effects get more profound toward the edge of the screen
        # Setting mouse starting position in the middle helps to minimize this effect
        pygame.mouse.set_pos((display_width / 2, display_height / 2))

        # Other pygame related initialization
        self.clock = pygame.time.Clock()
        pygame.font.init()

        # Start up a dedicated thread for the entity.
        self.entity = Entity()
        _thread.start_new_thread(self.entity.run, ())

        # Create Hue interface
        self.hue = HueInterface.HueInterface()

        # Main menu
        self.main_menu = PygameGui.Menu(self.screen)

        # Light toggles
        self.light_button_1 = PygameGui.Button(20, 100, 100, 100, 'Light 1',
                                               text_color=COLOR_BUTTON_TEXT,
                                               on_click=self.light_toggle_1)
        self.main_menu.add(self.light_button_1)
        self.light_button_2 = PygameGui.Button(140, 100, 100, 100, 'Light 2',
                                               text_color=COLOR_BUTTON_TEXT,
                                               on_click=self.light_toggle_2)
        self.main_menu.add(self.light_button_2)
        self.light_button_all = PygameGui.Button(20, 220, 220, 220, 'Lights',
                                               text_color=COLOR_BUTTON_TEXT,
                                               on_click=self.light_toggle_all)
        self.main_menu.add(self.light_button_all)

        # Brightness buttons
        self.Button_brightness_up = PygameGui.Button(260, 220, 100, 100, '+',
                                                 text_color=COLOR_BUTTON_TEXT,
                                                 on_click=self.light_set_brightness_up)
        self.main_menu.add(self.Button_brightness_up)
        self.Button_brightness_down = PygameGui.Button(260, 340, 100, 100, '-',
                                                 text_color=COLOR_BUTTON_TEXT,
                                                 on_click=self.light_set_brightness_down)
        self.main_menu.add(self.Button_brightness_down)

        # Color picker
        self.color_picker = PygameGui.ColorPicker(380, 40, 400, 400,
                                                  image_path='graphics/colorpicker/colorpicker.jpg',
                                                  on_click = self.light_set_color_all)
        self.main_menu.add(self.color_picker)

        # Latest recognition label
        self.latest_recognition_txt = "..."
        self.latest_recognition_button = PygameGui.Button(10, 10, display_width - 20, 20, self.latest_recognition_txt, bg_color=COLOR_TEXT_BG, text_color=COLOR_TEXT)
        self.main_menu.add(self.latest_recognition_button)

        # Main GUI loop
        self.menu_stack = []
        self.menu_stack.append(self.main_menu)

    def light_toggle_1(self):
        on = self.hue.toggle(1)
        if on:
            self.light_button_1.bg_color = COLOR_BUTTON_BG_ON
        else:
            self.light_button_1.bg_color = COLOR_BUTTON_BG_OFF

    def light_toggle_2(self):
        on = self.hue.toggle(2)
        if on:
            self.light_button_2.bg_color = COLOR_BUTTON_BG_ON
        else:
            self.light_button_2.bg_color = COLOR_BUTTON_BG_OFF

    def light_toggle_all(self):
        on = self.hue.toggle(1)
        if on:
            self.hue.turn_on(2)
            self.light_button_1.bg_color = COLOR_BUTTON_BG_ON
            self.light_button_2.bg_color = COLOR_BUTTON_BG_ON
            self.light_button_all.bg_color = COLOR_BUTTON_BG_ON
        else:
            self.hue.turn_off(2)
            self.light_button_1.bg_color = COLOR_BUTTON_BG_OFF
            self.light_button_2.bg_color = COLOR_BUTTON_BG_OFF
            self.light_button_all.bg_color = COLOR_BUTTON_BG_OFF

    def light_set_brightness_up(self):
        self.hue.set_brightness_up(1)
        self.hue.set_brightness_up(2)

    def light_set_brightness_down(self):
        self.hue.set_brightness_down(1)
        self.hue.set_brightness_down(2)

    def light_set_color_all(self, color):
        assert isinstance(color, pygame.Color)
        self.hue.set_pygame_color(1, color)
        self.hue.set_pygame_color(2, color)

    def run(self):
        try:
            running = True
            while running:
                if len(self.menu_stack) == 0: break
                current_menu = self.menu_stack[-1]

                # Check status of Entity
                # Stop GUI when entity thread has run into an exception.
                if self.entity.thread_exception is not None:
                    running = False
                    print(self.entity.thread_exception)
                    raise self.entity.thread_exception
                if not self.entity.running:
                    running = False
                # State of the entity affects current background color
                current_menu.bg_color = COLORS_BG[self.entity.state]
                # Update the latest recognized text
                if self.latest_recognition_txt != self.entity.voice_recognizer.latest_recognition:
                    self.latest_recognition_button.text = "> " + self.latest_recognition_txt

                # Draw current menu
                current_menu.draw()

                # Handle events
                for event in pygame.event.get():
                    # Pass events to current menu
                    current_menu.handle_event(event)
                    # Default event handlers
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            self.screen.fill((255, 0, 0))
                        else:
                            self.screen.fill((0, 255, 0))

                # Refresh display
                pygame.display.flip()

                # Limit frame rate to 30 FPS
                self.clock.tick(30)

        finally:
            # In case this thread crashes make sure that the thread for the entity terminates.
            self.entity.shutdown()

if __name__ == '__main__':
    GUI = EntityGui()
    GUI.run()