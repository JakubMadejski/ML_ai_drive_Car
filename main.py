import pygame
import math
import neat
import sys

WIDTH, HEIGHT = 1200, 800
CAR_SIZE_X, CAR_SIZE_Y = 30, 60

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
        self.radars = []
        self.distance = 0 # Nagroda dla AI
        self.time_alive = 0 # Czas przeżycia dla AI
    
    def move(self):
        if not self.alive: 
            return
        rad = math.radians(self.angle)
        self.x -= math.sin(rad) * self.speed
        self.y -= math.cos(rad) * self.speed
        
        self.distance += self.speed 
        self.time_alive += 1

        # Jeśli auto żyje długo (np. ponad 2 sekundy), ale mało przejechało
        if self.time_alive > 50 and self.distance < 100:
             self.alive = False # Zabijamy leniwe auto!

    def check_collision(self, screen):
        corners = self.get_corners()
        self.alive = True
        for corner in corners:
                try:
                    pixel_color = screen.get_at((int(corner[0]), int(corner[1])))[:3]
                    if pixel_color[:3] != ROAD_COLOR:
                        self.alive = False # Zabijamy samochód, jeśli którykolwiek róg jest poza drogą
                        break
                except IndexError:
                    self.reset()
                    break

    def check_radar(self, degree, screen):
        length = 0
        x = int(self.x)
        y = int(self.y)
        
        rad = math.radians(self.angle + degree)

        while length < 300:
            length += 5 # Optymalizacja (szybkość)
            x = int(self.x - math.sin(rad) * length)
            y = int(self.y - math.cos(rad) * length)

            try:
                if screen.get_at((x, y))[:3] != ROAD_COLOR:
                    break
            except IndexError:
                break

        dist = int(math.sqrt(math.pow(x - self.x, 2) + math.pow(y - self.y, 2)))
        self.radars.append(dist)

    def update(self, screen):
        self.move()
        self.check_collision(screen)
        self.radars.clear()
        if self.alive:
            for degree in [-90, -45, 0, 45, 90]:
                self.check_radar(degree, screen)

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

    def draw(self, screen):
        car_surface = pygame.Surface((CAR_SIZE_X, CAR_SIZE_Y), pygame.SRCALPHA)
        pygame.draw.rect(car_surface, CAR_COLOR, (0, 0, CAR_SIZE_X, CAR_SIZE_Y))
        pygame.draw.rect(car_surface, (0, 0, 255), (5, 5, 20, 10)) 
        
        rotated_surface = pygame.transform.rotate(car_surface, self.angle)
        rect = rotated_surface.get_rect(center=(int(self.x), int(self.y)))
        
        screen.blit(rotated_surface, rect.topleft)

        for r_len, angle in zip(self.radars, [-90, -45, 0, 45, 90]):
            rad = math.radians(self.angle + angle)
            end_x = int(self.x - math.sin(rad) * r_len)
            end_y = int(self.y - math.cos(rad) * r_len)
            pygame.draw.line(screen, (0, 255, 0), (int(self.x), int(self.y)), (end_x, end_y), 2)

def run_simulation(genomes, config):
    nets = []
    cars = []

    for i, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0
        cars.append(Car())
    
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    track_image = pygame.image.load('track.png')
    track_image = pygame.transform.scale(track_image, (WIDTH, HEIGHT))

    generation_font = pygame.font.SysFont("Arial", 30)

    running = True
    while running:
        screen.blit(track_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                exit()

        still_alive = 0

        for i, car in enumerate(cars):
            if car.alive:
                still_alive += 1
                car.update(screen)

                genomes[i][1].fitness = car.distance + car.time_alive * 0.1


                input_data = [(300 - r) / 300.0 for r in car.radars]
                if len(input_data) == 0: continue

                output = nets[i].activate(input_data)

                if output[0] > 0: # Skręt w lewo
                    car.angle += 7
                    is_turning = True
                    
                if output[1] > 0: # Skręt w prawo
                    car.angle -= 7
                    is_turning = True

        if still_alive == 0:
            break    
        
        drawn_cars = 0
        for car in cars:
            if car.alive:
                car.draw(screen)
                drawn_cars += 1
                if drawn_cars > 100: # Rysuj tylko 10 samochodów, aby nie spowalniać symulacji
                    break

        text = generation_font.render(f"Alive: {still_alive}", True, (0,0,0))
        screen.blit(text, (10, 10))

        pygame.display.flip()
        clock.tick(0)

if __name__ == "__main__":
    config_path = "config.txt"
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    p = neat.Population(config) # tworzenie populacji
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    #uruchomienie symulacji
    p.run(run_simulation, 50000)


