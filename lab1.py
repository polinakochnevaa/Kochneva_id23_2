import tkinter as tk
import math

# Инициализация основного окна
root = tk.Tk()
root.geometry("600x600")

# Создаем холст для рисования
canvas = tk.Canvas(root, width=600, height=600, bg="white")
canvas.pack(fill="both", expand=True)

# Определение начальных параметров
center = 300  # Центр холста по X и Y
radius = 200  # Радиус основной окружности
dot_radius = 5  # Радиус движущейся точки

# Создаем окружность в центре холста
canvas.create_oval(center - radius, center - radius,
                   center + radius, center + radius)

# Создаем движущуюся точку
dot = canvas.create_oval(center - dot_radius, center - dot_radius,
                         center + dot_radius, center + dot_radius, fill="red")

# Параметры движения точки
angle = 0  # Начальный угол
speed = 5  # Переменная скорости и направления движения

# Функция для движения точки
def move_dot():
    global angle
    # Вычисляем новые координаты точки
    x = center + radius * math.cos(math.radians(angle)) - dot_radius
    y = center + radius * math.sin(math.radians(angle)) - dot_radius
    # Обновляем положение точки
    canvas.coords(dot, x, y, x + 2 * dot_radius, y + 2 * dot_radius)
    # Изменяем угол в зависимости от скорости
    angle += speed
    if angle >= 360:
        angle = 0
    root.after(50, move_dot)  # Повторяем вызов функции через 50 мс

# Изменение скорости и направления
def increase_speed():
    global speed
    speed += 1

def decrease_speed():
    global speed
    speed -= 1

# Кнопки для управления скоростью
btn_increase = tk.Button(root, text="Увеличить скорость", command=increase_speed)
btn_increase.pack(side="left")

btn_decrease = tk.Button(root, text="Уменьшить скорость", command=decrease_speed)
btn_decrease.pack(side="left")

# Запуск анимации
move_dot()
root.mainloop()