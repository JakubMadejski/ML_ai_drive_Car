import pygame
import math

WIDTH, HEIGHT = 1200, 800
CAR_SIZE_X, CAR_SIZE_Y = 30, 60
BORDER_COLOR = (255, 255, 255)

#kolory
GRASS_CLOR = (34, 177, 76)
ROAD_COLOR = (50, 50, 50)
CAR_COLOR = (200, 0, 0)

class Car:
    def __init__(self):
        self.start_pos = (150, 200)
        self.x, self.y = self.start_pos
        self.angle = 0
        self.speed = 5
        self.alive = True
    
    def move(self):
        if not self.alive: 
            return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: self.angle += 3
        if keys[pygame.K_RIGHT]: self.angle -= 3
        if keys[pygame.K_UP]:
            rad = math.radians(self.angle)
            self.x -= math.sin(rad) * self.speed
            self.y -= math.cos(rad) * self.speed

    def check_collision(self):
        corners = self.get_corners()

        for corner in corners:
                try:
                    pixel_color = screen.get_at((int(corner[0]), int(corner[1])))[:3]
                    if pixel_color[:3] != ROAD_COLOR:
                        self.reset()
                        break
                except IndexError:
                    self.reset()
                    break
    
    def get_corners(self):
        corners = []

        rad = math.radians(self.angle)

        length = CAR_SIZE_Y / 2
        width = CAR_SIZE_X / 2

        for sx, sy in [(-width, -length), (width, -length), (width, length), (-width, length)]:
            rotated_x = self.x + (sx * math.cos(-rad) - sy * math.sin(-rad))
            rotated_y = self.y + (sx * math.sin(-rad) + sy * math.cos(-rad))
            corners.append((rotated_x, rotated_y))
        return corners

    def reset(self):
        self.x, self.y = self.start_pos
        self.angle = 0
        self.alive = True


    def draw(self, screen):
        car_surface = pygame.Surface((CAR_SIZE_X, CAR_SIZE_Y), pygame.SRCALPHA)
        
        pygame.draw.rect(car_surface, CAR_COLOR, (0, 0, CAR_SIZE_X, CAR_SIZE_Y))
        
        pygame.draw.rect(car_surface, (0, 0, 255), (5, 5, 20, 10)) 
        
        rotated_surface = pygame.transform.rotate(car_surface, self.angle)
        rect = rotated_surface.get_rect(center=(int(self.x), int(self.y)))
        
        screen.blit(rotated_surface, rect.topleft)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

try:
    track_image = pygame.image.load('track.png')
    track_image = pygame.transform.scale(track_image, (WIDTH, HEIGHT))
except:
    print("Nie można załadować obrazu trasy. Upewnij się, że 'track.png' jest w tym samym folderze co skrypt.")
    pygame.quit()
    exit()

car = Car()

running = True
while running:
    screen.blit(track_image, (0, 0)) # Rysowanie tła

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    car.move() # Logika gry
    car.check_collision() # Sprawdzenie kolizji
    car.draw(screen) #Rrysowanie samochodu 

    pygame.display.flip()
    clock.tick(60)

pygame.quit()