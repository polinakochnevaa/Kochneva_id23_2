import pygame
import math
import json
import os

pygame.init()

#настройки окна
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Волны и поплавки")

clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 20)

#цвета
background_color = (240, 240, 240)
wave_color = (255, 0, 0)
poplavok_color = (0, 0, 255)
ui_color = (200, 200, 200)
button_color = (180, 180, 180)
active_color = (255, 255, 255)
text_color = (0, 0, 0)

# создаем файл если нет данных
data_file = "waves_data.json"
if not os.path.exists(data_file):
    default_data = {
        "number of waves": 2,
        "waves": [
            {"amplitude": 30, "period": 150, "speed": 1.2},
            {"amplitude": 40, "period": 120, "speed": 1.5}
        ],
        "poplavki": [
            {"mass": 5, "objem": 5},
            {"mass": 6, "objem": 6}
        ],
        "poplavok radius": 15
    }
    with open(data_file, "w") as f:
        json.dump(default_data, f, indent=4)

#загрузка данных из JSON
with open(data_file) as file:
    data = json.load(file)

#инициализация данных
wave_params = data["waves"]
poplavok_params = data["poplavki"]
poplavok_radius = data["poplavok radius"]

num_waves = len(wave_params)
g = 9.81 #ускорение свободного падения
offset_scale = 5 #коэффициент масштабирования смещения

#обновляем вертикальные позиции поплавков
def update_poplavok_positions():
    global poplavok_positions
    if num_waves > 0:
        poplavok_positions = [height // (num_waves + 1) * (i + 1) for i in range(num_waves)]
    else:
        poplavok_positions = []

update_poplavok_positions()

#рисуем волну
def draw_wave(surface, wave_y, amplitude, period, speed, time):
    for x in range(width):
        #вычисляем синусоиду для волны
        y = wave_y + amplitude * math.sin(2 * math.pi * (x / period) - speed * time)
        if 0 <= y < height:
            surface.set_at((x, int(y)), wave_color)

#рисуем поплавок
def draw_poplavok(surface, wave_y, amplitude, period, speed, time, poplavok_x, mass, objem):
    #вычисляем высоту волны для поплавка
    wave_height = wave_y + amplitude * math.sin(2 * math.pi * (poplavok_x / period) - speed * time)
    #вычисляем смещение поплавка
    offset = ((mass - objem) * g / (mass + objem)) * offset_scale
    poplavok_y = wave_height + offset
    pygame.draw.circle(surface, poplavok_color, (int(poplavok_x), int(poplavok_y)), poplavok_radius)
    return (int(poplavok_x), int(poplavok_y))

#прямоугольники кнопок сверху
add_wave_button_rect = pygame.Rect(10, 10, 100, 30)
remove_wave_button_rect = pygame.Rect(120, 10, 100, 30)
next_wave_button_rect = pygame.Rect(230, 10, 100, 30)
prev_wave_button_rect = pygame.Rect(340, 10, 100, 30)
pause_button_rect = pygame.Rect(450, 10, 100, 30)

selected_wave_index = 0
wave_amplitude_rect = pygame.Rect(10, 50, 100, 30)
wave_period_rect = pygame.Rect(120, 50, 100, 30)
apply_wave_button_rect = pygame.Rect(230, 50, 100, 30)

#инициализация текстовых полей для волны
if len(wave_params) > 0:
    wave_amplitude_text = str(wave_params[selected_wave_index]["amplitude"])
    wave_period_text = str(wave_params[selected_wave_index]["period"])
else:
    wave_amplitude_text = ""
    wave_period_text = ""

poplavok_edit_index = None
poplavok_window_open = False

#окно настройки поплавка
poplavok_window_rect = pygame.Rect(200, 200, 200, 150)
offset_x = poplavok_window_rect.x
offset_y = poplavok_window_rect.y

mass_label_pos = (offset_x + 10, offset_y + 10)
mass_field_rect = pygame.Rect(offset_x + 70, offset_y + 10, 80, 30)
objem_label_pos = (offset_x + 10, offset_y + 60)
objem_field_rect = pygame.Rect(offset_x + 70, offset_y + 60, 80, 30)
apply_poplavok_rect = pygame.Rect(offset_x + 10, offset_y + 110, 80, 30)

poplavok_mass_text = ""
poplavok_objem_text = ""

active_field = None
paused = False #флаг паузы анимации
animation_time = 0.0 #таймер анимации

#функция отрисовки кнопки
def draw_button(surface, rect, text_str):
    #рисуем прямоугольник кнопки
    pygame.draw.rect(surface, button_color, rect)
    #рисуем текст по центру
    text_surf = font.render(text_str, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)

#функция отрисовки текстового поля
def draw_text_field(surface, rect, text_str, active=False):
    #цвет поля зависит от активности
    color = active_color if active else (255,255,255)
    pygame.draw.rect(surface, color, rect)
    pygame.draw.rect(surface, (0,0,0), rect, 1)
    #если активно, добавляем курсор
    display_text = text_str
    if active:
        display_text += "|"
    text_surf = font.render(display_text, True, text_color)
    surface.blit(text_surf, (rect.x + 5, rect.y + 5))

#открываем окно настройки параметров поплавка
def open_poplavok_editor(i):
    global poplavok_edit_index, poplavok_window_open, poplavok_mass_text, poplavok_objem_text
    #запоминаем индекс поплавка
    poplavok_edit_index = i
    poplavok_window_open = True
    #заполняем поля текущими значениями
    poplavok_mass_text = str(poplavok_params[i]["mass"])
    poplavok_objem_text = str(poplavok_params[i]["objem"])

#выбираем текущую волну по индексу
def select_wave(index):
    global selected_wave_index, wave_amplitude_text, wave_period_text
    if len(wave_params) == 0:
        selected_wave_index = 0
        wave_amplitude_text = ""
        wave_period_text = ""
        return
    #берем волну по индексу по модулю количества волн
    selected_wave_index = index % len(wave_params)
    #обновляем текстовые поля амплитуды и периода
    wave_amplitude_text = str(wave_params[selected_wave_index]["amplitude"])
    wave_period_text = str(wave_params[selected_wave_index]["period"])

running = True

while running:
    dt = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #при выходе не сохраняем файл
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            #проверяем попадание в поплавок
            clicked_on_poplavok = False
            for i in range(len(wave_params)):
                if i < len(poplavok_positions):
                    w = wave_params[i]
                    amplitude, period, speed = w["amplitude"], w["period"], w["speed"]
                    mass, objem = poplavok_params[i]["mass"], poplavok_params[i]["objem"]
                    wave_y = poplavok_positions[i]
                    #вычисляем положение поплавка
                    pop_x = (animation_time * 100) % width
                    wave_height = wave_y + amplitude * math.sin(2 * math.pi * (pop_x / period) - speed * animation_time)
                    offset = ((mass - objem) * g / (mass + objem)) * offset_scale
                    pop_y = wave_height + offset
                    #проверяем клик на поплавке
                    if (mouse_pos[0] - pop_x)**2 + (mouse_pos[1] - pop_y)**2 <= poplavok_radius**2:
                        #открываем окно редактирования поплавка
                        open_poplavok_editor(i)
                        clicked_on_poplavok = True
                        break
            #если не в поплавок, проверяем ui
            if not clicked_on_poplavok:
                if add_wave_button_rect.collidepoint(mouse_pos):
                    #добавляем волну и поплавок
                    wave_params.append({"amplitude":30,"period":150,"speed":1.0})
                    poplavok_params.append({"mass":5,"objem":5})
                    num_waves = len(wave_params)
                    update_poplavok_positions()
                    if num_waves == 1:
                        select_wave(0)
                elif remove_wave_button_rect.collidepoint(mouse_pos):
                    #удаляем последнюю волну и поплавок
                    if len(wave_params) > 0:
                        wave_params.pop()
                        poplavok_params.pop()
                        num_waves = len(wave_params)
                        update_poplavok_positions()
                        if num_waves > 0:
                            select_wave(selected_wave_index)
                        else:
                            wave_amplitude_text = ""
                            wave_period_text = ""
                elif next_wave_button_rect.collidepoint(mouse_pos):
                    #переход к следующей волне
                    if len(wave_params) > 0:
                        select_wave(selected_wave_index+1)
                elif prev_wave_button_rect.collidepoint(mouse_pos):
                    #переход к предыдущей волне
                    if len(wave_params) > 0:
                        select_wave(selected_wave_index-1)
                elif pause_button_rect.collidepoint(mouse_pos):
                    #ставим паузу или снимаем
                    paused = not paused
                elif wave_amplitude_rect.collidepoint(mouse_pos):
                    #выбираем поле амплитуды для ввода
                    active_field = 'wave_amplitude'
                elif wave_period_rect.collidepoint(mouse_pos):
                    #выбираем поле периода для ввода
                    active_field = 'wave_period'
                elif apply_wave_button_rect.collidepoint(mouse_pos):
                    #применяем параметры волны
                    if len(wave_params) > 0:
                        try:
                            new_amp = float(wave_amplitude_text)
                            new_period = float(wave_period_text)
                            wave_params[selected_wave_index]["amplitude"] = new_amp
                            wave_params[selected_wave_index]["period"] = new_period
                        except ValueError:
                            pass
                if poplavok_window_open:
                    #проверяем клики внутри окна поплавка
                    if mass_field_rect.collidepoint(mouse_pos):
                        active_field = 'poplavok_mass'
                    elif objem_field_rect.collidepoint(mouse_pos):
                        active_field = 'poplavok_objem'
                    elif apply_poplavok_rect.collidepoint(mouse_pos):
                        #применяем новые параметры поплавка
                        if poplavok_edit_index is not None:
                            try:
                                new_mass = float(poplavok_mass_text)
                                new_objem = float(poplavok_objem_text)
                                poplavok_params[poplavok_edit_index]["mass"] = new_mass
                                poplavok_params[poplavok_edit_index]["objem"] = new_objem
                                poplavok_window_open = False
                                poplavok_edit_index = None
                                active_field = None
                            except ValueError:
                                pass
        elif event.type == pygame.KEYDOWN:
            #обработка ввода текста в поля
            if active_field is not None:
                if event.key == pygame.K_BACKSPACE:
                    #удаляем последний символ
                    if active_field == 'wave_amplitude':
                        wave_amplitude_text = wave_amplitude_text[:-1]
                    elif active_field == 'wave_period':
                        wave_period_text = wave_period_text[:-1]
                    elif active_field == 'poplavok_mass':
                        poplavok_mass_text = poplavok_mass_text[:-1]
                    elif active_field == 'poplavok_objem':
                        poplavok_objem_text = poplavok_objem_text[:-1]
                elif event.key == pygame.K_RETURN:
                    #завершаем ввод по enter
                    active_field = None
                else:
                    char = event.unicode
                    #разрешаем цифры, точку, минус
                    if char.isdigit() or char in ['.', '-']:
                        if active_field == 'wave_amplitude':
                            wave_amplitude_text += char
                        elif active_field == 'wave_period':
                            wave_period_text += char
                        elif active_field == 'poplavok_mass':
                            poplavok_mass_text += char
                        elif active_field == 'poplavok_objem':
                            poplavok_objem_text += char

    if not paused:
        #обновляем время анимации только если не на паузе
        animation_time += dt

    #очищаем экран
    window.fill(background_color)

    #отрисовываем волны и поплавки
    for i, wave in enumerate(wave_params):
        a, pp, sp = wave["amplitude"], wave["period"], wave["speed"]
        m, o = poplavok_params[i]["mass"], poplavok_params[i]["objem"]
        if i < len(poplavok_positions):
            wy = poplavok_positions[i]
            draw_wave(window, wy, a, pp, sp, animation_time)
            px = (animation_time * 100) % width
            draw_poplavok(window, wy, a, pp, sp, animation_time, px, m, o)

    #кнопки управления волнами и паузой
    draw_button(window, add_wave_button_rect, "Add Wave")
    draw_button(window, remove_wave_button_rect, "Rem Wave")
    draw_button(window, next_wave_button_rect, "Next Wave")
    draw_button(window, prev_wave_button_rect, "Prev Wave")

    #кнопка паузы
    pause_text = "Resume" if paused else "Pause"
    draw_button(window, pause_button_rect, pause_text)

    #поля ввода параметров волны
    draw_text_field(window, wave_amplitude_rect, wave_amplitude_text, active=(active_field=='wave_amplitude'))
    draw_text_field(window, wave_period_rect, wave_period_text, active=(active_field=='wave_period'))
    draw_button(window, apply_wave_button_rect, "Apply Wave")

    #отображаем текущую волну
    if len(wave_params) > 0:
        info_str = f"Editing wave {selected_wave_index+1} of {len(wave_params)}"
    else:
        info_str = "No waves"
    info_surf = font.render(info_str, True, (0,0,0))
    info_x = width - info_surf.get_width() - 10
    info_y = 10
    window.blit(info_surf, (info_x, info_y))

    #если открыто окно поплавка
    if poplavok_window_open:
        #рисуем окно и элементы
        pygame.draw.rect(window, ui_color, poplavok_window_rect)
        pygame.draw.rect(window, (0,0,0), poplavok_window_rect, 2)
        mass_label_surf = font.render("Mass:", True, text_color)
        objem_label_surf = font.render("Objem:", True, text_color)
        window.blit(mass_label_surf, mass_label_pos)
        draw_text_field(window, mass_field_rect, poplavok_mass_text, active=(active_field=='poplavok_mass'))
        window.blit(objem_label_surf, objem_label_pos)
        draw_text_field(window, objem_field_rect, poplavok_objem_text, active=(active_field=='poplavok_objem'))
        draw_button(window, apply_poplavok_rect, "Apply")

    pygame.display.update()

pygame.quit()
