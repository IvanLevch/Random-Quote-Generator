import tkinter as tk
from tkinter import messagebox, ttk
import random
import json
import os

# Файл для сохранения истории цитат
HISTORY_FILE = "quote_history.json"
# Файл для предопределённых цитат
PREDEFINED_QUOTES_FILE = "predefined_quotes.json"


# Список предопределённых цитат (текст, автор, тема)
PREDEFINED_QUOTES = [
    {"text": "Жизнь — это то, что происходит с тобой, пока ты строишь другие планы.", "author": "Джон Леннон", "topic": "Философия"},
    {"text": "Успех — это способность идти от неудачи к неудаче, не теряя энтузиазма.", "author": "Уинстон Черчилль", "topic": "Мотивация"},
    {"text": "Самое тёмное время перед рассветом.", "author": "Томас Фуллер", "topic": "Надежда"},
    {"text": "Знание — сила.", "author": "Фрэнсис Бэкон", "topic": "Образование"},
    {"text": "Будь изменением, которое ты хочешь видеть в мире.", "author": "Махатма Ганди", "topic": "Саморазвитие"}
]

def save_predefined_quotes():
    """Сохраняет предопределённые цитаты в файл."""
    try:
        with open(PREDEFINED_QUOTES_FILE, 'w', encoding='utf-8') as f:
            json.dump(PREDEFINED_QUOTES, f, ensure_ascii=False, indent=2)
    except IOError as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить предопределённые цитаты: {e}")

def load_predefined_quotes():
    """Загружает предопределённые цитаты из файла или использует стандартные."""
    if os.path.exists(PREDEFINED_QUOTES_FILE):
        try:
            with open(PREDEFINED_QUOTES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return PREDEFINED_QUOTES

def load_history():
    """Загружает историю цитат из JSON-файла."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []

def save_history(history):
    """Сохраняет историю цитат в JSON-файл."""
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except IOError as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить историю: {e}")


def generate_quote():
    """Генерирует случайную цитату из предопределённого списка."""
    quotes = load_predefined_quotes()
    if not quotes:
        messagebox.showwarning("Предупреждение", "Список цитат пуст!")
        return

    selected_quote = random.choice(quotes)
    # Добавляем цитату в историю
    history = load_history()
    history.append(selected_quote)
    save_history(history)
    # Отображаем цитату
    display_quote(selected_quote)
    # Обновляем список истории
    update_history_list()

def display_quote(quote):
    """Отображает выбранную цитату в интерфейсе."""
    text_quote.delete(1.0, tk.END)
    text_quote.insert(tk.END, f"\"{quote['text']}\"\n\n")
    text_quote.insert(tk.END, f"Автор: {quote['author']}\n")
    text_quote.insert(tk.END, f"Тема: {quote['topic']}")

def update_history_list():
    """Обновляет список истории цитат."""
    listbox_history.delete(0, tk.END)
    history = load_history()
    for quote in history:
        listbox_history.insert(tk.END, f"{quote['author']} — {quote['topic']}")

def filter_by_author():
    """Фильтрует историю по автору."""
    author = entry_filterauthor.get().strip()
    if not author:
        messagebox.showwarning("Предупреждение", "Введите имя автора для фильтрации!")
        return

    history = load_history()
    filtered = [q for q in history if author.lower() in q['author'].lower()]
    update_filtered_list(filtered)

def filter_by_topic():
    """Фильтрует историю по теме."""
    topic = entry_filter_topic.get().strip()
    if not topic:
        messagebox.showwarning("Предупреждение", "Введите тему для фильтрации!")
        return

    history = load_history()
    filtered = [q for q in history if topic.lower() in q['topic'].lower()]
    update_filtered_list(filtered)

def update_filtered_list(quotes):
    """Обновляет список отфильтрованных цитат."""
    listbox_filtered.delete(0, tk.END)
    for quote in quotes:
        preview_text = quote['text'][:50] + "..." if len(quote['text']) > 50 else quote['text']
        listbox_filtered.insert(tk.END, f"{quote['author']} — {quote['topic']}: {preview_text}")

def add_new_quote():
    """Добавляет новую цитату в предопределённый список."""
    text = entry_new_text.get().strip()
    author = entry_newauthor.get().strip()
    topic = entry_new_topic.get().strip()

    # Проверка на пустые строки
    if not text or not author or not topic:
        messagebox.showwarning("Предупреждение", "Все поля должны быть заполнены!")
        return

    new_quote = {"text": text, "author": author, "topic": topic}
    quotes = load_predefined_quotes()
    quotes.append(new_quote)


    try:
        with open(PREDEFINED_QUOTES_FILE, 'w', encoding='utf-8') as f:
            json.dump(quotes, f, ensure_ascii=False, indent=2)
        messagebox.showinfo("Успех", "Новая цитата добавлена!")
        # Очищаем поля ввода
        entry_new_text.delete(0, tk.END)
        entry_newauthor.delete(0, tk.END)
        entry_new_topic.delete(0, tk.END)
    except IOError as e:
        messagebox.showerror("Ошибка", f"Не удалось добавить цитату: {e}")

def clear_filters():
    """Очищает фильтры и обновляет список отфильтрованных цитат"""
    entry_filterauthor.delete(0, tk.END)
    entry_filter_topic.delete(0, tk.END)
    listbox_filtered.delete(0, tk.END)

def on_closing():
    """Обработка закрытия окна с подтверждением"""
    if messagebox.askokcancel("Выход", "Вы уверены, что хотите выйти?"):
        root.destroy()

# Инициализация файлов при запуске
save_predefined_quotes()

# Создание главного окна
root = tk.Tk()
root.title("Random Quote Generator")
root.geometry("900x700")

# Основной фрейм
main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Фрейм для генерации цитаты
frame_generate = ttk.LabelFrame(main_frame, text="Генератор цитат", padding="10")
frame_generate.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

ttk.Button(frame_generate, text="Сгенерировать цитату", command=generate_quote).grid(row=0, column=0, padx=5)
# Отображение цитаты
text_quote = tk.Text(frame_generate, height=6, width=80, wrap=tk.WORD)
text_quote.grid(row=1, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))

# Фрейм для добавления новых цитат
frame_add = ttk.LabelFrame(main_frame, text="Добавить новую цитату", padding="10")
frame_add.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

ttk.Label(frame_add, text="Текст:").grid(row=0, column=0, sticky=tk.W)
entry_new_text = ttk.Entry(frame_add, width=50)
entry_new_text.grid(row=0, column=1, padx=5, pady=2)


ttk.Label(frame_add, text="Автор:").grid(row=1, column=0, sticky=tk.W)
entry_newauthor = ttk.Entry(frame_add, width=50)
entry_newauthor.grid(row=1, column=1, padx=5, pady=2)

ttk.Label(frame_add, text="Тема:").grid(row=2, column=0, sticky=tk.W)
entry_new_topic = ttk.Entry(frame_add, width=50)
entry_new_topic.grid(row=2, column=1, padx=5, pady=2)

ttk.Button(frame_add, text="Добавить цитату", command=add_new_quote).grid(row=3, column=0, columnspan=2, pady=5)

# Фрейм для фильтрации
frame_filter = ttk.LabelFrame(main_frame, text="Фильтрация истории", padding="10")
frame_filter.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

ttk.Label(frame_filter, text="Фильтр по автору:").grid(row=0, column=0, sticky=tk.W)
entry_filterauthor = ttk.Entry(frame_filter, width=30)
entry_filterauthor.grid(row=0, column=1, padx=5, pady=2)
ttk.Button(frame_filter, text="Применить", command=filter_by_author).grid(row=0, column=2, padx=5)

ttk.Label(frame_filter, text="Фильтр по теме:").grid(row=1, column=0, sticky=tk.W)
entry_filter_topic = ttk.Entry(frame_filter, width=30)
entry_filter_topic.grid(row=1, column=1, padx=5, pady=2)
ttk.Button(frame_filter, text="Применить", command=filter_by_topic).grid(row=1, column=2, padx=5)

# Кнопка очистки фильтров
ttk.Button(frame_filter, text="Очистить фильтры", command=clear_filters).grid(row=2, column=0, columnspan=3, pady=5)

# Фрейм для истории цитат
frame_history = ttk.LabelFrame(main_frame, text="История цитат", padding="10")
frame_history.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5, padx=(0, 5))

listbox_history = tk.Listbox(frame_history, height=8, width=40)
listbox_history.pack(fill=tk.BOTH, expand=True)


# Фрейм для отфильтрованных цитат
frame_filtered = ttk.LabelFrame(main_frame, text="Отфильтрованные цитаты", padding="10")
frame_filtered.grid(row=3, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5, padx=(5, 0))

listbox_filtered = tk.Listbox(frame_filtered, height=8, width=40)
listbox_filtered.pack(fill=tk.BOTH, expand=True)

# Настройка весов строк и столбцов для корректного растягивания
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)
main_frame.rowconfigure(3, weight=1)


# Загрузка начальной истории при запуске
update_history_list()

# Обработка закрытия окна
root.protocol("WM_DELETE_WINDOW", on_closing)

# Запуск приложения
root.mainloop()