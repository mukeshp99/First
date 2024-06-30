from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database initialization
def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")
    conn.execute('CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER)')
    print("Table created successfully")
    conn.close()

init_sqlite_db()

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()
    conn.close()
    return render_template('index.html', students=data)

@app.route('/add/', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, age) VALUES (?, ?)", (name, age))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/update/<int:id>/', methods=['GET', 'POST'])
def update_student(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cursor.fetchone()
    conn.close()

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE students SET name=?, age=? WHERE id=?", (name, age, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('update.html', student=student)

@app.route('/delete/<int:id>/')
def delete_student(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
