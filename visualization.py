
# visualization.py

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from matplotlib.figure import Figure


def plot_age_distribution(ages):
    # Создаем новое окно Tkinter
    window = tk.Tk()
    window.title("Распределение возраста пациентов")

    # Создаем новый график
    fig = Figure(figsize=(6, 4), dpi=100)
    plot = fig.add_subplot(1, 1, 1)

    # Рисуем гистограмму в созданном графике
    plot.hist(ages, bins=10, alpha=0.7, color='blue')
    plot.set_title('Распределение возраста пациентов')
    plot.set_xlabel('Возраст')
    plot.set_ylabel('Количество пациентов')
    plot.grid(axis='y', alpha=0.75)

    # Добавляем график в Tkinter окно
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Запускаем основной цикл Tkinter
    window.mainloop()