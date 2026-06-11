from flask import Flask, render_template, request, redirect
import sqlite3


def setup_database():
    connection = sqlite3.connect('tasks.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_name TEXT NOT NULL,
        completed INTEGER NOT NULL,
        due_date TEXT,
        priority TEXT
    )
    ''')

    connection.commit()
    connection.close()


app = Flask(__name__)


@app.route('/')
def home():
    filter_type = request.args.get('filter')
    print(filter_type)

    connection = sqlite3.connect('tasks.db')
    cursor = connection.cursor()

    if filter_type == 'completed':
        cursor.execute('SELECT * FROM tasks WHERE completed = 1')

    elif filter_type == 'incomplete':
        cursor.execute('SELECT * FROM tasks WHERE completed = 0')

    else:
        cursor.execute('SELECT * FROM tasks')

    tasks = cursor.fetchall()

    total_tasks = len(tasks)

    completed_tasks = 0

    for task in tasks:
        if task[2] == 1:
            completed_tasks += 1

    incompleted_tasks = total_tasks - completed_tasks

    connection.close()

    return render_template(
        'index.html',
        tasks=tasks,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        incompleted_tasks=incompleted_tasks
    )


@app.route('/add', methods=['POST'])
def add_task():

    task_name = request.form['task_name']

    due_date = request.form['due_date']

    priority = request.form['priority']
    
    if task_name.strip() != '':

        connection = sqlite3.connect('tasks.db')
        cursor = connection.cursor()

        cursor.execute('''
        INSERT INTO tasks (task_name, completed, due_date, priority)
        VALUES (?, 0, ?, ?)
        ''', (task_name, due_date, priority))

        connection.commit()
        connection.close()

    return redirect('/')


@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):

    connection = sqlite3.connect('tasks.db')
    cursor = connection.cursor()

    cursor.execute('''
    DELETE FROM tasks
    WHERE id = ?
    ''', (task_id,))

    connection.commit()
    connection.close()

    return redirect('/')


@app.route('/complete/<int:task_id>', methods=['POST'])
def complete_task(task_id):

    connection = sqlite3.connect('tasks.db')
    cursor = connection.cursor()

    cursor.execute('''
    UPDATE tasks
    SET completed = 1
    WHERE id = ?
    ''', (task_id,))

    connection.commit()
    connection.close()

    return redirect('/')


@app.route('/edit/<int:task_id>')
def edit_task(task_id):

    connection = sqlite3.connect('tasks.db')
    cursor = connection.cursor()

    cursor.execute(
        'SELECT * FROM tasks WHERE id = ?', (task_id,)
    )

    task = cursor.fetchone()

    connection.close()

    return render_template('edit.html', task=task)


@app.route('/update/<int:task_id>', methods=['POST'])
def update_task(task_id):
    task_name = request.form['task_name']

    if task_name.strip() != '':
        connection = sqlite3.connect('tasks.db')
        cursor = connection.cursor()

        cursor.execute('''
        UPDATE tasks
        SET task_name = ?
        WHERE id = ?
        ''', (task_name, task_id))

        connection.commit()
        connection.close()

    return redirect('/')


setup_database()

app.run(debug=True)
