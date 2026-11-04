from flask import Flask, render_template, request, redirect 
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    conn.close()
    return render_template('index.html', tasks=rows)

@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    conn = sqlite3.connect('app.db')
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при работе с БД: {e}")
        conn.rollback() 
    finally:    
        conn.close()   
    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete(task_id):
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/complete/<int:task_id>')
def complete(task_id):
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    # Меняем статус на 'done' (выполнено)
    cursor.execute("UPDATE tasks SET status = 'done' WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect('/')
    
if __name__ == '__main__':
    app.run(debug=True)