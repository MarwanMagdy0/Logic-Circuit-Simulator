from logic import *
screen = Screen(SURFACE)
# pygame.mouse.set_visible(0)
while True:
    # event loop and clear screen

    SURFACE.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
    # Program logic
    screen.move_screen()
    screen.draw()
    # Updating the screen
    x,y = pygame.mouse.get_pos()
    # pygame.draw.line(SURFACE, (255,255,255), (x,y-10), (x,y+10))
    # pygame.draw.line(SURFACE, (255,255,255), (x-10,y), (x+10,y))
    pygame.display.update()
    clock.tick(-1)

