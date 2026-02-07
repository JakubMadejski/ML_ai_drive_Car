import pygame
import math

WIDTH, HEIGHT = 1600, 1200
CAR_SIZE_X, CAR_SIZE_Y = 30, 60
BORDER_COLOR = (255, 255, 255)



class Car:
    def __init__(self):
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.angle = 0
        self.speed = 5
    
    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            rad = math.radians(self.angle)
            self.x -= self.speed * math.sin(rad)
            self.y -= self.speed * math.cos(rad)
        
        if keys[pygame.K_LEFT]:
            self.angle += 5
        
        if keys[pygame.K_RIGHT]:
            self.angle -= 5

        if self.x < 20: self.x = 20
        if self.x > WIDTH - 20: self.x = WIDTH - 20
        if self.y < 20: self.y = 20
        if self.y > HEIGHT - 20: self.y = HEIGHT - 20

    def draw(self, screen):
        car_surface = pygame.Surface((CAR_SIZE_X, CAR_SIZE_Y), pygame.SRCALPHA)
        
        pygame.draw.rect(car_surface, (200, 0, 0), (0, 0, CAR_SIZE_X, CAR_SIZE_Y))
        
        pygame.draw.rect(car_surface, (0, 0, 255), (5, 5, 20, 10)) 
        
        rotated_surface = pygame.transform.rotate(car_surface, self.angle)
        rect = rotated_surface.get_rect(center=(self.x, self.y))
        
        screen.blit(rotated_surface, rect.topleft)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
car = Car()

running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    car.move()
    car.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()