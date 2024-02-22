
# app.py

import tkinter as tk
from tkinter import messagebox
from database import DatabaseHandler
from auth import check_login
from visualization import plot_age_distribution


class MedicalApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Медицинский анализатор данных")
        self.geometry("600x450")  # Задаем начальный размер окна
        self.db_handler = DatabaseHandler()  # Создаем обработчик базы данных
        self.show_login_form()

    def create_widgets(self):
        self.add_patient_form = AddPatientForm(self, self.db_handler)
        self.add_patient_form.pack()

        # Добавить форму для поиска пациента
        self.search_patient_form = SearchPatientForm(self, self.db_handler)
        self.search_patient_form.pack()

        self.visualize_button = tk.Button(self, text="Показать распределение возраста пациентов",
                                        command=self.visualize_ages)
        self.visualize_button.pack()

        self.statistics_frame = StatisticsFrame(self, self.db_handler)
        self.statistics_frame.pack()

        self.export_button = tk.Button(self, text="Экспорт данных в CSV", command=self.export_data)
        self.export_button.pack()


    def show_login_form(self):
        self.login_frame = tk.Frame(self)
        self.login_frame.pack()

        tk.Label(self.login_frame, text="Логин:").grid(row=0, column=0)
        self.login_entry = tk.Entry(self.login_frame)
        self.login_entry.grid(row=0, column=1)

        tk.Label(self.login_frame, text="Пароль:").grid(row=1, column=0)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1)

        self.login_button = tk.Button(self.login_frame, text="Войти", command=self.login)
        self.login_button.grid(row=2, column=1)

    def login(self):
        # Здесь будет логика авторизации
        username = self.login_entry.get()
        password = self.password_entry.get()
        if check_login(username, password):
            messagebox.showinfo("Login", "Авторизация прошла успешно")
            self.login_frame.destroy()  # Уничтожаем виджеты формы авторизации
            self.create_widgets()  # Создаем основные виджеты приложения
        else:
            messagebox.showerror("Login", "Неправильный логин или пароль")

    def visualize_ages(self):
        # Получаем данные о возрастах пациентов
        patients = self.db_handler.get_patients()
        ages = [patient[2] for patient in patients]  # предполагается, что возраст - это второе поле в записи о пациенте
        plot_age_distribution(ages)

    def export_data(self):
        filepath = 'patients_data.csv'  # В реальном приложении можно добавить диалог для выбора файла
        self.db_handler.export_patients_to_csv(filepath)
        messagebox.showinfo("Экспорт данных", f"Данные экспортированы в файл {filepath}")


class AddPatientForm(tk.Frame):
    def __init__(self, parent, db_handler):
        super().__init__(parent)
        self.db_handler = db_handler
        # Создаем виджеты для ввода данных о пациенте
        tk.Label(self, text="Имя:").grid(row=0, column=0)
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=0, column=1)

        tk.Label(self, text="Возраст:").grid(row=1, column=0)
        self.age_entry = tk.Entry(self)
        self.age_entry.grid(row=1, column=1)

        tk.Label(self, text="Пол:").grid(row=2, column=0)
        self.gender_entry = tk.Entry(self)
        self.gender_entry.grid(row=2, column=1)

        tk.Label(self, text="Диагноз:").grid(row=3, column=0)
        self.diagnosis_entry = tk.Entry(self)
        self.diagnosis_entry.grid(row=3, column=1)

        # Кнопка для подтверждения добавления нового пациента
        self.submit_button = tk.Button(self, text="Добавить пациента", command=self.submit)
        self.submit_button.grid(row=4, column=1)

    def submit(self):
        # Логика добавления нового пациента в базу данных
        # Получаем данные из формы
        name = self.name_entry.get()
        age = int(self.age_entry.get())
        gender = self.gender_entry.get()
        diagnosis = self.diagnosis_entry.get()

        # Добавляем нового пациента в базу данных
        self.db_handler.add_patient(name, age, gender, diagnosis)

        # Очищаем поля формы после добавления
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.gender_entry.delete(0, tk.END)
        self.diagnosis_entry.delete(0, tk.END)

        messagebox.showinfo("Добавление пациента", "Пациент успешно добавлен")


class SearchPatientForm(tk.Frame):
    def __init__(self, parent, db_handler):
        super().__init__(parent)
        self.db_handler = db_handler
        # Создаем виджеты для поиска пациента
        tk.Label(self, text="Поиск пациента (имя):").grid(row=0, column=0)
        self.search_entry = tk.Entry(self)
        self.search_entry.grid(row=0, column=1)

        # Кнопка для выполнения поиска
        self.search_button = tk.Button(self, text="Поиск", command=self.search)
        self.search_button.grid(row=0, column=2)

        # Список результатов поиска
        self.search_results = tk.Listbox(self)
        self.search_results.grid(row=1, column=0, columnspan=3, sticky="nsew")

        self.edit_button = tk.Button(self, text="Редактировать", state=tk.DISABLED, command=self.edit_patient)
        self.edit_button.grid(row=2, column=1, sticky="ew")

        # Обработчик выбора пациента в списке
        self.search_results.bind('<<ListboxSelect>>', self.on_select)

    def search(self):
        search_query = self.search_entry.get()
        results = self.db_handler.search_patients(search_query)

        # Очистить предыдущие результаты поиска
        self.search_results.delete(0, tk.END)

        # Выводим результаты поиска в Listbox
        for patient in results:
            self.search_results.insert(tk.END, f"{patient[1]} (ID: {patient[0]})")

    def on_select(self, event):
        # Если выбран пациент, активировать кнопку "Редактировать"
        if self.search_results.curselection():
            self.edit_button.config(state=tk.NORMAL)
        else:
            self.edit_button.config(state=tk.DISABLED)

    def edit_patient(self):
        selection = self.search_results.curselection()
        if selection:
            selected_index = selection[0]
            patient_id = self.search_results.get(selected_index).split(" (ID: ")[1][:-1]  # Извлекаем ID
            edit_window = EditPatientWindow(self, self.db_handler, patient_id)
            edit_window.grab_set()  # Захватываем фокус на новое окно


class EditPatientForm(tk.Frame):
    def __init__(self, parent, db_handler, patient_id):
        super().__init__(parent)
        self.db_handler = db_handler
        self.patient_id = patient_id

        # Получаем данные пациента по ID
        self.patient_data = self.db_handler.get_patient_by_id(patient_id)

        # Создаем виджеты для редактирования данных пациента
        tk.Label(self, text="Имя:").grid(row=0, column=0)
        self.name_entry = tk.Entry(self)
        self.name_entry.insert(0, self.patient_data[1])
        self.name_entry.grid(row=0, column=1)

        tk.Label(self, text="Возраст:").grid(row=1, column=0)
        self.age_entry = tk.Entry(self)
        self.age_entry.insert(0, self.patient_data[2])
        self.age_entry.grid(row=1, column=1)

        tk.Label(self, text="Пол:").grid(row=2, column=0)
        self.gender_entry = tk.Entry(self)
        self.gender_entry.insert(0, self.patient_data[3])
        self.gender_entry.grid(row=2, column=1)

        tk.Label(self, text="Диагноз:").grid(row=3, column=0)
        self.diagnosis_entry = tk.Entry(self)
        self.diagnosis_entry.insert(0, self.patient_data[4])
        self.diagnosis_entry.grid(row=3, column=1)

        # Кнопка для сохранения изменений
        self.update_button = tk.Button(self, text="Обновить", command=self.update_patient)
        self.update_button.grid(row=4, column=1)

        # Кнопка для удаления пациента
        self.delete_button = tk.Button(self, text="Удалить", command=self.delete_patient)
        self.delete_button.grid(row=4, column=2)

    def update_patient(self):
        # Логика для обновления данных пациента
        updated_name = self.name_entry.get()
        updated_age = self.age_entry.get()
        updated_gender = self.gender_entry.get()
        updated_diagnosis = self.diagnosis_entry.get()

        self.db_handler.update_patient(self.patient_id, updated_name, updated_age, updated_gender, updated_diagnosis)
        messagebox.showinfo("Обновление данных", "Данные пациента обновлены успешно")
        self.destroy()

    def delete_patient(self):
        # Логика для удаления пациента
        self.db_handler.delete_patient(self.patient_id)
        messagebox.showinfo("Удаление данных", "Данные пациента удалены успешно")
        self.destroy()


class EditPatientWindow(tk.Toplevel):
    def __init__(self, parent, db_handler, patient_id):
        super().__init__(parent)
        self.db_handler = db_handler
        self.patient_id = patient_id

        # Получаем данные пациента по ID
        self.patient_data = self.db_handler.get_patient_by_id(patient_id)

        # Создаем виджеты для редактирования данных пациента
        tk.Label(self, text="Имя:").grid(row=0, column=0)
        self.name_entry = tk.Entry(self)
        self.name_entry.insert(0, self.patient_data[1])  # Используем индекс для доступа к данным
        self.name_entry.grid(row=0, column=1)

        tk.Label(self, text="Возраст:").grid(row=1, column=0)
        self.age_entry = tk.Entry(self)
        self.age_entry.insert(0, self.patient_data[2])
        self.age_entry.grid(row=1, column=1)

        tk.Label(self, text="Пол:").grid(row=2, column=0)
        self.gender_entry = tk.Entry(self)
        self.gender_entry.insert(0, self.patient_data[3])
        self.gender_entry.grid(row=2, column=1)

        tk.Label(self, text="Диагноз:").grid(row=3, column=0)
        self.diagnosis_entry = tk.Entry(self)
        self.diagnosis_entry.insert(0, self.patient_data[4])
        self.diagnosis_entry.grid(row=3, column=1)

        # Кнопка для сохранения изменений
        self.update_button = tk.Button(self, text="Сохранить", command=self.update_patient)
        self.update_button.grid(row=4, column=0)

        # Кнопка для отмены изменений
        self.cancel_button = tk.Button(self, text="Отмена", command=self.destroy)
        self.cancel_button.grid(row=4, column=1)

    def update_patient(self):
        updated_name = self.name_entry.get()
        updated_age = self.age_entry.get()
        updated_gender = self.gender_entry.get()
        updated_diagnosis = self.diagnosis_entry.get()

        self.db_handler.update_patient(self.patient_id, updated_name, updated_age, updated_gender, updated_diagnosis)
        messagebox.showinfo("Обновление данных", "Данные пациента обновлены успешно")
        self.destroy()


class StatisticsFrame(tk.Frame):
    def __init__(self, parent, db_handler):
        super().__init__(parent)
        self.db_handler = db_handler
        self.create_widgets()

    def create_widgets(self):
        # Виджет для отображения среднего возраста
        avg_age = self.db_handler.get_age_statistics()
        tk.Label(self, text=f"Средний возраст пациентов: {avg_age:.2f}").pack()

        # Виджет для отображения распределения по полу
        gender_distribution = self.db_handler.get_gender_distribution()
        genders = ', '.join([f"{k}: {v}" for k, v in gender_distribution.items()])
        tk.Label(self, text=f"Распределение пациентов по полу: {genders}").pack()
