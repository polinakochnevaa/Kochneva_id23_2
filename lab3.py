import pygame
import math
import json
import os
import tkinter as tk
from tkinter import Toplevel, Label, Spinbox, Button
import threading

# инициализация Pygame
pygame.init()

# настройки окна
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("волны и поплавки")

# цвета
background_color = (240, 240, 240)
wave_color = (0, 100, 255)
poplavok_color = (255, 0, 0)

# задание пути к файлу
filename = "waves_data.json"

# значения по умолчанию
default_data = {
    "волны": [
        {"амплитуда": 30, "период": 150, "скорость": 1.2},
        {"амплитуда": 40, "период": 120, "скорость": 1.5},
    ],
    "поплавки": [
        {"масса": 50, "объем": 50},
        {"масса": 60, "объем": 70},
    ],
    "радиус поплавка": 15
}

# загрузка данных или создание файла с начальными значениями
if not os.path.exists(filename):
    with open(filename, "w") as file:
        json.dump(default_data, file, ensure_ascii=False, indent=4)

try:
    with open(filename, "r") as file:
        data = json.load(file)
        if "волны" not in data or not isinstance(data["волны"], list):
            print("ключ 'волны' отсутствует или поврежден. использую значения по умолчанию.")
            data = default_data
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"ошибка при загрузке данных: {e}. использую значения по умолчанию.")
    data = default_data

# инициализация переменных из данных
waves = data["волны"]
poplavki = data["поплавки"]
poplavok_radius = data["радиус поплавка"]

# расположение волн
def update_positions():
    global poplavok_positions
    poplavok_positions = [height // (len(waves) + 1) * (i + 1) for i in range(len(waves))]

update_positions()

# переменные для состояния анимации
paused = False
running = True
time = 0  # время для анимации
start_time = 0  # время запуска анимации
paused_time = 0  # сохранённое время на момент паузы

# список активных окон Tkinter
active_tk_windows = []

# добавление новой волны
def add_wave():
    waves.append({"амплитуда": 30, "период": 150, "скорость": 1.0})
    poplavki.append({"масса": 50, "объем": 50})
    update_positions()

# удаление последней волны
def remove_wave():
    if waves:
        waves.pop()
        poplavki.pop()
        update_positions()

# окно для изменения параметров волны или поплавка в отдельном потоке
def open_settings(index, is_wave):
    def thread_function():
        def update_values():
            try:
                if is_wave:
                    # обновление параметров волны
                    waves[index]["амплитуда"] = int(amplitude_spinbox.get())
                    waves[index]["период"] = int(period_spinbox.get())
                    waves[index]["скорость"] = float(speed_spinbox.get())
                else:
                    # обновление параметров поплавка
                    poplavki[index]["масса"] = float(mass_spinbox.get())
                    poplavki[index]["объем"] = float(volume_spinbox.get())
                settings_window.destroy()
            except ValueError:
                print("ошибка: некорректные значения")

        # создание окна Tkinter
        root = tk.Tk()
        root.withdraw()
        settings_window = Toplevel(root)
        settings_window.title("настройка параметров")

        if is_wave:
            # Параметры волны
            Label(settings_window, text="амплитуда:").pack()
            amplitude_spinbox = Spinbox(settings_window, from_=1, to=100, increment=1)
            amplitude_spinbox.delete(0, "end")
            amplitude_spinbox.insert(0, waves[index]["амплитуда"])
            amplitude_spinbox.pack()

            Label(settings_window, text="период:").pack()
            period_spinbox = Spinbox(settings_window, from_=10, to=300, increment=10)
            period_spinbox.delete(0, "end")
            period_spinbox.insert(0, waves[index]["период"])
            period_spinbox.pack()

            Label(settings_window, text="скорость:").pack()
            speed_spinbox = Spinbox(settings_window, from_=0.1, to=10.0, increment=0.1, format="%.1f")
            speed_spinbox.delete(0, "end")
            speed_spinbox.insert(0, waves[index]["скорость"])
            speed_spinbox.pack()
        else:
            # параметры поплавка
            Label(settings_window, text="масса:").pack()
            mass_spinbox = Spinbox(settings_window, from_=1, to=100, increment=1)
            mass_spinbox.delete(0, "end")
            mass_spinbox.insert(0, poplavki[index]["масса"])
            mass_spinbox.pack()

            Label(settings_window, text="объем:").pack()
            volume_spinbox = Spinbox(settings_window, from_=1, to=100, increment=1)
            volume_spinbox.delete(0, "end")
            volume_spinbox.insert(0, poplavki[index]["объем"])
            volume_spinbox.pack()

        Button(settings_window, text="сохранить", command=update_values).pack()

        root.mainloop()

    # запускаем окно Tkinter в отдельном потоке
    thread = threading.Thread(target=thread_function)
    thread.start()

# отрисовка волны
def draw_wave(wave_y, amplitude, period, speed):
    for x in range(width):
        y = wave_y + amplitude * math.sin(2 * math.pi * (x / period) - speed * time)
        pygame.draw.circle(window, wave_color, (x, int(y)), 1)

# отрисовка поплавка
def draw_poplavok(wave_y, amplitude, period, speed, poplavok_x, mass, volume):
    wave_height = wave_y + amplitude * math.sin(2 * math.pi * (poplavok_x / period) - speed * time)
    offset = ((volume - mass) * 9.81 / max(1, mass + volume)) * 5  # архимедова сила
    poplavok_y = wave_height + offset
    pygame.draw.circle(window, poplavok_color, (int(poplavok_x), int(poplavok_y)), poplavok_radius)

def handle_mouse_click(mouse_x, mouse_y):
# определяет, куда кликнул пользователь: на волну или поплавок
    for i, wave_y in enumerate(poplavok_positions):
        # позиция поплавка
        poplavok_x = (time * 100) % width
        wave_height = wave_y + waves[i]["амплитуда"] * math.sin(2 * math.pi * (poplavok_x / waves[i]["период"]) - waves[i]["скорость"] * time)
        offset = ((poplavki[i]["объем"] - poplavki[i]["масса"]) * 9.81 / max(1, poplavki[i]["масса"] + poplavki[i]["объем"])) * 5
        poplavok_y = wave_height + offset
        # проверка клика по поплавку
        if (mouse_x - poplavok_x) ** 2 + (mouse_y - poplavok_y) ** 2 <= poplavok_radius ** 2:
            open_settings(i, False)
            return
        # проверка клика по волне
        elif abs(mouse_y - wave_y) < 10:
            open_settings(i, True)
            return

# основной цикл программы
clock = pygame.time.Clock()

while running:
    window.fill(background_color)

    # обновление активных окон Tkinter
    for tk_window in active_tk_windows:
        tk_window.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
                if paused:
                    paused_time = pygame.time.get_ticks() / 1000 - start_time
                else:
                    start_time = pygame.time.get_ticks() / 1000 - paused_time
            elif event.key == pygame.K_a:  # добавить волну
                add_wave()
            elif event.key == pygame.K_d:  # удалить волну
                remove_wave()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_mouse_click(*event.pos)

    if not paused:
        time = pygame.time.get_ticks() / 1000 - start_time
        for i, wave in enumerate(waves):
            draw_wave(poplavok_positions[i], wave["амплитуда"], wave["период"], wave["скорость"])
            draw_poplavok(poplavok_positions[i], wave["амплитуда"], wave["период"], wave["скорость"], (time * 100) % width, poplavki[i]["масса"], poplavki[i]["объем"])

    pygame.display.update()
    clock.tick(60)

# сохранение состояния
with open(filename, "w") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

pygame.quit()