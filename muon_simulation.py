import pygame
import math
import random
import numpy as np
from muon_scaterring import calculate_muon_scattering

pygame.init()

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

font = pygame.font.SysFont("arial", 28)

materials = {
    "Iron": {"X0": 1.76, "density": 7.87, "Z": 26.0},
    "Copper": {"X0": 1.43, "density": 8.96, "Z": 29.0},
    "Lead": {"X0": 0.56, "density": 11.35, "Z": 82.0},
}

material_colors = {
    "Iron": (120,120,150),
    "Copper": (200,120,70),
    "Lead": (90,90,120),
}

material_bins = {
    "Iron": 0.0000016,
    "Copper": 0.0000018,
    "Lead": 0.0000030,
}

sheet_width = 50
sheet_x = WIDTH // 2

material_list = list(materials.keys())
current_material = 2

slider_x = 200
slider_y = HEIGHT - 60
slider_w = 600
slider_h = 6
handle_radius = 10
slider_value = 0.5
dragging = False
source = False

angles = np.linspace(-0.015, 0.015, 10000)

def angle_to_color(angle):
    max_angle = 0.02
    a = min(abs(angle) / max_angle, 1.0)

    r = int(255 * a)
    g = int(255 * (1 - a))
    b = 0

    return (r, g, b)

class Particle:

    def __init__(self):
        self.x = 0
        self.y = random.randint(50, HEIGHT-50)
        self.speed = 5
        self.angle = 0
        self.deviated = False
        self.color = (0,255,0)

    def update(self):

        if not self.deviated and self.x >= sheet_x + sheet_width:

            random_muon_angle = np.random.choice(
                angles,
                p=material_prob_distributions[material_list[current_material]]
            )

            self.angle = random_muon_angle
            self.color = angle_to_color(self.angle)
            self.deviated = True

        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

    def draw(self):
        pygame.draw.circle(screen,self.color,(int(self.x),int(self.y)),3)

particles = []
running = True

while running:

    clock.tick(60)
    screen.fill((10,10,20))

    sheet_width = int(10 + slider_value * 200)

    material_prob_distributions = {
        "Iron": calculate_muon_scattering(
            angles, materials["Iron"], p=4000, v=1.0, L=sheet_width*0.01
        ) * material_bins["Iron"],

        "Copper": calculate_muon_scattering(
            angles, materials["Copper"], p=4000, v=1.0, L=sheet_width*0.01
        ) * material_bins["Copper"],

        "Lead": calculate_muon_scattering(
            angles, materials["Lead"], p=4000, v=1.0, L=sheet_width*0.01
        ) * material_bins["Lead"],
    }

    material_prob_distributions["Iron"] /= np.sum(material_prob_distributions["Iron"])
    material_prob_distributions["Copper"] /= np.sum(material_prob_distributions["Copper"])
    material_prob_distributions["Lead"] /= np.sum(material_prob_distributions["Lead"])

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                source = not source

            if event.key == pygame.K_r:
                particles = []

            if pygame.K_1 <= event.key <= pygame.K_3:
                current_material = event.key - pygame.K_1

        if event.type == pygame.MOUSEBUTTONDOWN:

            mx,my = pygame.mouse.get_pos()
            handle_x = slider_x + slider_value*slider_w

            if abs(mx-handle_x) < 15 and abs(my-slider_y) < 20:
                dragging = True

        if event.type == pygame.MOUSEBUTTONUP:
            dragging = False

        if event.type == pygame.MOUSEMOTION and dragging:

            mx,_ = pygame.mouse.get_pos()
            slider_value = (mx-slider_x)/slider_w
            slider_value = max(0,min(1,slider_value))

    if source:
        particles.append(Particle())

    material_name = material_list[current_material]
    color = material_colors[material_name]

    pygame.draw.rect(screen,color,(sheet_x,0,sheet_width,HEIGHT))

    for p in particles:
        p.update()
        p.draw()

    particles = [p for p in particles if p.x < WIDTH and 0 < p.y < HEIGHT]

    pygame.draw.rect(screen,(111,111,111),(slider_x,slider_y,slider_w,slider_h))

    handle_x = slider_x + slider_value*slider_w
    pygame.draw.circle(screen,(255,100,100),(int(handle_x),slider_y+3),handle_radius)

    text = font.render(material_name,True,(255,255,255))
    screen.blit(text,(WIDTH//2-text.get_width()//2,20))

    pygame.display.flip()

pygame.quit()