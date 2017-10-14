import pygame
import os
import _thread
from Entity import Entity, EntityStates
from components import PygameGui

def light_toggle():
    print("Toggle lights!")

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
       raise Exception('No suitable video driver found!')

# force display size to 800*480 (the size of the raspberry touchscreen)
display_width = 800
display_height = 480
size = (display_width, display_height)

# Full screen option is not required.
# In an X server environment prefer to run this in a window.
# In a terminal environment it will be full screen anyway.
screen = pygame.display.set_mode(size)#, pygame.FULLSCREEN)

# Mouse tracking on the touchscreen is off for some reason
# The movement of the mouse slightly exaggerates the movement on the touchscreen
# Effects get more profound toward the edge of the screen
# Setting mouse starting position in the middle helps to minimize this effect
pygame.mouse.set_pos((display_width / 2, display_height / 2))

# Other pygame related initialization
clock = pygame.time.Clock()
pygame.font.init()

COLORS_BG = {EntityStates.SLEEPING : (110, 110, 110),
             EntityStates.LISTENING: (0, 200, 0),
             EntityStates.BUSY: (200, 0, 0)}
COLOR_TEXT = (210, 210, 210)
COLOR_TEXT_BG = (40, 40, 40)

# Start up a dedicated thread for the entity.
entity = Entity()
_thread.start_new_thread(entity.run, ())

# Main menu
main_menu = PygameGui.Menu(screen)
# Light toggle
light_button = PygameGui.Button(100, 100, 50, 50, 'Light', on_click=light_toggle)
main_menu.add(light_button)
# Latest recognition label
latest_recognition_txt = "..."
latest_recognition_button = PygameGui.Button(10, 10, display_width - 20, 20, latest_recognition_txt, bg_color=COLOR_TEXT_BG, text_color=COLOR_TEXT)
main_menu.add(latest_recognition_button)

# Main GUI loop
menu_stack = []
menu_stack.append(main_menu)

try:
    running = True
    while running:
        if len(menu_stack) == 0: break
        current_menu = menu_stack[-1]

        # Check status of Entity
        # Stop GUI when entity thread has run into an exception.
        if entity.thread_exception is not None:
            running = False
            raise entity.thread_exception
        if not entity.running:
            running = False
        # State of the entity affects current background color
        current_menu.bg_color = COLORS_BG[entity.state]
        # Update the latest recognized text
        if latest_recognition_txt != entity.voice_recognizer.latest_recognition:
            latest_recognition_button.text = "> " + latest_recognition_txt

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
                    screen.fill((255, 0, 0))
                else:
                    screen.fill((0, 255, 0))

        # Refresh display
        pygame.display.flip()

        # Limit frame rate to 30 FPS
        clock.tick(30)

    # running = True
    # while running:
    #     # set background color based on entity state
    #     screen.fill(COLORS_BG[entity.state])
    #
    #     # set latest recognition
    #     if latest_recognition_txt != entity.voice_recognizer.latest_recognition:
    #         latest_recognition_txt = entity.voice_recognizer.latest_recognition
    #         latest_recognition_label = latest_recognition_font.render("> " + latest_recognition_txt, 1, COLOR_TEXT)
    #         latest_recognition_surf = pygame.Surface((display_width - 20, 20))
    #         latest_recognition_surf.fill(COLOR_TEXT_BG)
    #         latest_recognition_surf.blit(latest_recognition_label, (4,2))
    #     screen.blit(latest_recognition_surf, (10, 10))
    #
    #     # draw button
    #     light_button.draw(screen)
    #
    #     # Check status of Entity
    #     # Stop GUI when entity thread has run into an exception.
    #     if entity.thread_exception is not None:
    #         running = False
    #         raise entity.thread_exception
    #     if not entity.running:
    #         running = False
    #
    #     for event in pygame.event.get():
    #         light_button.handle_event(event)
    #
    #         if event.type == pygame.QUIT:
    #             running = False
    #         elif event.type == pygame.KEYDOWN:
    #             if event.key == pygame.K_ESCAPE:
    #                 running = False
    #         elif event.type == pygame.MOUSEBUTTONDOWN:
    #             if event.button == 1:
    #                 screen.fill((255, 0, 0))
    #             else:
    #                 screen.fill((0, 255, 0))
    #
    #     pygame.display.flip()
    #
    #     # Limit framerate to 30 FPS
    #     clock.tick(30)
finally:
    # In case this thread crashes make sure that the thread for the entity terminates.
    entity.shutdown()