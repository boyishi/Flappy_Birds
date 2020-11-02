import pygame, sys

pygame.init()
clock = pygame.time.Clock()

# Create the display surface
screen = pygame.display.set_mode((600, 600))
second_surface = pygame.Surface([34,24])
second_surface.fill((0,0,255))

bluebird = pygame.image.load('./assets/bluebird-downflap.png')
bluebird_rect = bluebird.get_rect(topleft = [100, 200])

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((255, 255, 255))
    screen.blit(second_surface, (100,200))
    screen.blit(bluebird, bluebird_rect)
    
    print(bluebird_rect.topleft)

    pygame.display.update()
    clock.tick(60)