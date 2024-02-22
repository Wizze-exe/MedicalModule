
# database.py

import sqlite3
import numpy as np
import csv


class DatabaseHandler:
    def __init__(self):
        self.conn = sqlite3.connect('medical_data.db')
        self.cur = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Создаем таблицы в базе данных
        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            diagnosis TEXT
        )
        ''')
        self.conn.commit()

    def add_patient(self, name, age, gender, diagnosis):
        # Добавляем запись о новом пациенте
        self.cur.execute('''
        INSERT INTO patients (name, age, gender, diagnosis) VALUES (?, ?, ?, ?)
        ''', (name, age, gender, diagnosis))
        self.conn.commit()

    def __del__(self):
        # Закрываем соединение с базой данных при удалении объекта
        self.conn.close()

    def get_patients(self):
        # Получаем всех пациентов из базы данных
        self.cur.execute('SELECT * FROM patients')
        return self.cur.fetchall()

    def get_patient_by_id(self, patient_id):
        self.cur.execute('SELECT * FROM patients WHERE id = ?', (patient_id,))
        return self.cur.fetchone()

    def search_patients(self, search_query):
        # Ищем пациентов, чье имя содержит search_query
        self.cur.execute('SELECT * FROM patients WHERE name LIKE ?', ('%' + search_query + '%',))
        return self.cur.fetchall()

    def update_patient(self, patient_id, name, age, gender, diagnosis):
        # Обновляем данные пациента по его ID
        self.cur.execute('''
        UPDATE patients SET name = ?, age = ?, gender = ?, diagnosis = ? WHERE id = ?
        ''', (name, age, gender, diagnosis, patient_id))
        self.conn.commit()

    def delete_patient(self, patient_id):
        # Удаляем пациента по его ID
        self.cur.execute('DELETE FROM patients WHERE id = ?', (patient_id,))
        self.conn.commit()

    def get_age_statistics(self):
        self.cur.execute('SELECT age FROM patients')
        ages = [age[0] for age in self.cur.fetchall()]
        avg_age = np.mean(ages)
        return avg_age

    def get_gender_distribution(self):
        self.cur.execute('SELECT gender, COUNT(*) FROM patients GROUP BY gender')
        distribution = {row[0]: row[1] for row in self.cur.fetchall()}
        return distribution

    def export_patients_to_csv(self, filepath):
        self.cur.execute('SELECT * FROM patients')
        patients_data = self.cur.fetchall()
        with open(filepath, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['ID', 'Имя', 'Возраст', 'Пол', 'Диагноз'])
            csvwriter.writerows(patients_data)
