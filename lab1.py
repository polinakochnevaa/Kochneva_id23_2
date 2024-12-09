import pygame
import math

#инициализация Pygame
pygame.init()

#размеры окна
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Точка на окружности")

#цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

#центр и радиус окружности
center = (WIDTH // 2, HEIGHT // 2)
radius = 200

#переменные для движения точки
angle = 0  # Начальный угол (в радианах)
speed = 0.05  # Скорость и направление движения (изменяемая переменная)

#основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #управление скоростью и направлением через клавиши
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                speed += 0.01  #увеличить скорость
            elif event.key == pygame.K_DOWN:
                speed -= 0.01  #уменьшить скорость
            elif event.key == pygame.K_SPACE:
                speed = -speed  #изменить направление

    #очистка экрана
    screen.fill(WHITE)

    #рисуем окружность
    pygame.draw.circle(screen, BLACK, center, radius, 1)

    #вычисление координат точки на окружности
    x = center[0] + radius * math.cos(angle)
    y = center[1] + radius * math.sin(angle)

    #рисуем точку
    pygame.draw.circle(screen, RED, (int(x), int(y)), 5)

    #обновление угла
    angle += speed

    #обновление экрана
    pygame.display.flip()

    #задержка для ограничения FPS
    pygame.time.delay(30)

#завершение Pygame
pygame.quit()
