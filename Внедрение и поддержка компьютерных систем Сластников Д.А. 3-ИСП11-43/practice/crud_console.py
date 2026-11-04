import sqlite3

def get_connection():
  
    return sqlite3.connect('app.db')

def show_tasks():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, status FROM tasks")
    rows = cursor.fetchall()
    conn.close()
    
    print("\n--- СПИСОК ЗАДАЧ ---")
    if not rows:
        print("Список пуст.")
    else:
        for row in rows:
            print(f"[{row[0]}] {row[1]} (Статус: {row[2]})")
    print("--------------------\n")

def add_task():
    title = input("Введите название задачи: ")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, status) VALUES (?, 'new')", (title,))
    conn.commit()
    conn.close()
    print("Задача успешно добавлена!")

def delete_task():
    show_tasks()
    try:
        task_id = int(input("Введите ID задачи для удаления: "))
    except ValueError:
        print("Ошибка: ID должно быть числом.")
        return

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    
    if cursor.rowcount > 0:
        print(f"Задача с ID {task_id} удалена.")
    else:
        print(f"Задача с ID {task_id} не найдена.")
    conn.close()

def main():
    while True:
        print("МЕНЮ:")
        print("1. Показать все задачи")
        print("2. Добавить задачу")
        print("3. Удалить задачу")
        print("0. Выход")
        
        choice = input("Выберите действие: ")
        
        if choice == '1':
            show_tasks()
        elif choice == '2':
            add_task()
        elif choice == '3':
            delete_task()
        elif choice == '0':
            print("Выход из программы.")
            break
        else:
            print("Неверный ввод. Попробуйте снова.\n")

if __name__ == '__main__':
    main()