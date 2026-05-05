import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os

DATA_FILE = "expenses.json"

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker - Мои расходы")
        self.root.geometry("750x550")
        self.root.configure(bg="#f5f5f5")

        # хранилище расходов
        self.expenses = []
        self.load_data()

        # виджеты
        self.create_input_frame()
        self.create_table_frame()
        self.create_filter_frame()
        self.create_stats_frame()

        self.update_table()

    #    загрузка
    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.expenses = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.expenses = []

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.expenses, f, ensure_ascii=False, indent=4)

    # форма ввода
    def create_input_frame(self):
        input_frame = tk.LabelFrame(self.root, text="➕ Добавить расход", bg="#f5f5f5", font=("Arial", 10, "bold"))
        input_frame.pack(pady=10, padx=10, fill="x")

        # поле Сумма
        tk.Label(input_frame, text="Сумма (руб):", bg="#f5f5f5").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.amount_entry = tk.Entry(input_frame, width=15)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        # поле Категория
        tk.Label(input_frame, text="Категория:", bg="#f5f5f5").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.category_var = tk.StringVar()
        categories = ["Еда", "Транспорт", "Развлечения", "Здоровье", "Одежда", "Другое"]
        self.category_combo = ttk.Combobox(input_frame, textvariable=self.category_var, values=categories, width=12)
        self.category_combo.grid(row=0, column=3, padx=5, pady=5)
        self.category_combo.current(0)

        # поле Дата
        tk.Label(input_frame, text="Дата (ГГГГ-ММ-ДД):", bg="#f5f5f5").grid(row=0, column=4, sticky="w", padx=5, pady=5)
        self.date_entry = tk.Entry(input_frame, width=12)
        self.date_entry.grid(row=0, column=5, padx=5, pady=5)
        self.date_entry.insert(0, datetime.today().strftime("%Y-%m-%d"))

        # кнопка добавить
        add_btn = tk.Button(input_frame, text="Добавить", command=self.add_expense, bg="#4CAF50", fg="white")
        add_btn.grid(row=0, column=6, padx=10, pady=5)

    # таблица расходов
    def create_table_frame(self):
        table_frame = tk.LabelFrame(self.root, text="📋 Все расходы", bg="#f5f5f5", font=("Arial", 10, "bold"))
        table_frame.pack(pady=10, padx=10, fill="both", expand=True)

        columns = ("id", "amount", "category", "date")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

        self.tree.heading("id", text="№")
        self.tree.heading("amount", text="Сумма (руб)")
        self.tree.heading("category", text="Категория")
        self.tree.heading("date", text="Дата")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("amount", width=100, anchor="center")
        self.tree.column("category", width=120, anchor="center")
        self.tree.column("date", width=120, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # кнопка удалить выделенное
        del_btn = tk.Button(self.root, text="❌ Удалить выбранную запись", command=self.delete_expense, bg="#f44336", fg="white")
        del_btn.pack(pady=5)

    #  фильтрация
    def create_filter_frame(self):
        filter_frame = tk.LabelFrame(self.root, text="🔍 Фильтр", bg="#f5f5f5", font=("Arial", 10, "bold"))
        filter_frame.pack(pady=5, padx=10, fill="x")

        tk.Label(filter_frame, text="Категория:", bg="#f5f5f5").grid(row=0, column=0, padx=5, pady=5)
        self.filter_category = ttk.Combobox(filter_frame, values=["Все"] + ["Еда", "Транспорт", "Развлечения", "Здоровье", "Одежда", "Другое"], width=12)
        self.filter_category.grid(row=0, column=1, padx=5, pady=5)
        self.filter_category.current(0)

        tk.Label(filter_frame, text="Дата от (ГГГГ-ММ-ДД):", bg="#f5f5f5").grid(row=0, column=2, padx=5, pady=5)
        self.date_from = tk.Entry(filter_frame, width=12)
        self.date_from.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(filter_frame, text="Дата до (ГГГГ-ММ-ДД):", bg="#f5f5f5").grid(row=0, column=4, padx=5, pady=5)
        self.date_to = tk.Entry(filter_frame, width=12)
        self.date_to.grid(row=0, column=5, padx=5, pady=5)

        filter_btn = tk.Button(filter_frame, text="Применить фильтр", command=self.update_table, bg="#2196F3", fg="white")
        filter_btn.grid(row=0, column=6, padx=10, pady=5)

    #          статистика
    def create_stats_frame(self):
        stats_frame = tk.LabelFrame(self.root, text="💰 Статистика за период (по фильтру)", bg="#f5f5f5", font=("Arial", 10, "bold"))
        stats_frame.pack(pady=5, padx=10, fill="x")

        self.total_label = tk.Label(stats_frame, text="Общая сумма: 0 руб", bg="#f5f5f5", font=("Arial", 11, "bold"))
        self.total_label.pack(pady=5)

    #  логика добавления
    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                messagebox.showerror("Ошибка", "Сумма должна быть положительным числом.")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректную сумму (число).")
            return

        category = self.category_var.get().strip()
        if not category:
            messagebox.showerror("Ошибка", "Выберите категорию.")
            return

        date_str = self.date_entry.get().strip()
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте ГГГГ-ММ-ДД (например, 2025-04-05).")
            return

        new_id = max([e["id"] for e in self.expenses]) + 1 if self.expenses else 1
        self.expenses.append({
            "id": new_id,
            "amount": amount,
            "category": category,
            "date": date_str
        })
        self.save_data()
        self.update_table()

        self.amount_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.today().strftime("%Y-%m-%d"))

        messagebox.showinfo("Успех", "Расход добавлен!")

    #удаление записи
    def delete_expense(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите запись для удаления.")
            return

        item = self.tree.item(selected[0])
        expense_id = item["values"][0]

        for i, exp in enumerate(self.expenses):
            if exp["id"] == expense_id:
                del self.expenses[i]
                break

        self.save_data()
        self.update_table()
        messagebox.showinfo("Успех", "Запись удалена.")

    #  фильтрация и обновление таблицы
    def update_table(self):
        # Получаем значения фильтров
        filter_cat = self.filter_category.get()
        date_from_str = self.date_from.get().strip()
        date_to_str = self.date_to.get().strip()

        filtered = self.expenses[:]

        # фильтр по категории
        if filter_cat != "Все":
            filtered = [e for e in filtered if e["category"] == filter_cat]

        # фильтр по дате "от"
        if date_from_str:
            try:
                date_from = datetime.strptime(date_from_str, "%Y-%m-%d")
                filtered = [e for e in filtered if datetime.strptime(e["date"], "%Y-%m-%d") >= date_from]
            except ValueError:
                pass

        # фильтр по дате "до"
        if date_to_str:
            try:
                date_to = datetime.strptime(date_to_str, "%Y-%m-%d")
                filtered = [e for e in filtered if datetime.strptime(e["date"], "%Y-%m-%d") <= date_to]
            except ValueError:
                pass

        # сортируем по дате (новые сверху)
        filtered.sort(key=lambda x: x["date"], reverse=True)

        # обновляем таблицу
        for row in self.tree.get_children():
            self.tree.delete(row)

        for exp in filtered:
            self.tree.insert("", "end", values=(exp["id"], f"{exp['amount']:.2f}", exp["category"], exp["date"]))

        # подсчёт суммы
        total = sum(e["amount"] for e in filtered)
        self.total_label.config(text=f"📊 Общая сумма за период (по фильтру): {total:.2f} руб")

#  запуск
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()