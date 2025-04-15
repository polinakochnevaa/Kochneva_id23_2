import pygame
import math
import json

pygame.init()

#настройки окна
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Волны и поплавки")

#цвета
background_color = (240, 240, 240)
wave_color = (255, 0, 0)
poplavok_color = (0, 0, 255)

#загрузка данных из JSON
with open("waves_data.json") as file:
    data = json.load(file)

#инициализация данных
num_waves = data["number of waves"]
wave_params = data["waves"]
poplavok_params = data["poplavki"]
poplavok_radius = data["poplavok radius"]
poplavok_positions = [height // (num_waves + 1) * (i + 1) for i in range(num_waves)]

g = 9.81 #масса свободного падения
offset_scale = 5  #коэффициент масштабирования смещения

#отрисовка волны
def draw_wave(wave_y, amplitude, period, speed, time):
    for x in range(width):
        y = wave_y + amplitude * math.sin(2 * math.pi * (x / period) - speed * time)
        pygame.draw.circle(window, wave_color, (x, int(y)), 1)  #рисуем волну

#отрисовка поплавка с учетом массы и объема
def draw_poplavok(wave_y, amplitude, period, speed, time, poplavok_x, mass, objem):
    wave_height = wave_y + amplitude * math.sin(2 * math.pi * (poplavok_x / period) - speed * time)
    offset = ((mass - objem) * g / (mass + objem)) * offset_scale  #масштабируемое смещение
    poplavok_y = wave_height + offset
    pygame.draw.circle(window, poplavok_color, (int(poplavok_x), int(poplavok_y)), poplavok_radius)  #рисуем поплавок

running = True
clock = pygame.time.Clock()

while running:
    window.fill(background_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    time = pygame.time.get_ticks() / 1000

    for i, wave in enumerate(wave_params):
        amplitude, period, speed = wave["amplitude"], wave["period"], wave["speed"]
        mass, objem = poplavok_params[i]["mass"], poplavok_params[i]["objem"]
        wave_y = poplavok_positions[i]  #вертикальная позиция волны

        draw_wave(wave_y, amplitude, period, speed, time)  #рисуем волну

        poplavok_x = (time * 100) % width  #движение поплавка по оси X
        draw_poplavok(wave_y, amplitude, period, speed, time, poplavok_x, mass, objem)  #рисуем поплавок

    pygame.display.update()
    clock.tick(120)

pygame.quit()
