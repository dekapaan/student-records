import sqlite3

from flask import Flask, render_template, request, jsonify


def init_sqlite_db():
    conn = sqlite3.connect("database.db")
    print("Opened database successfully")

    conn.execute("CREATE TABLE IF NOT EXISTS students (name TEXT, addr TEXT, city TEXT, pin TEXT)")
    print("Table created successfully")
    conn.close()


init_sqlite_db()

app = Flask(__name__)


@app.route('/')
@app.route('/enter-new/')
def enter_new_student():
    return render_template('student.html')


@app.route('/add-new-record/', methods=["POST"])
def add_new_student_record():
    msg = None
    if request.method == "POST":
        try:
            name = request.form['name']
            addr = request.form['add']
            city = request.form['city']
            pin = request.form['pin']

            with sqlite3.connect('database.db') as conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO students(name, addr, city, pin) VALUES(?, ?, ?, ?)", (name, addr, city, pin))
                conn.commit()
                msg = "Record successfuly added."
        except Exception as e:
            conn.rollback()
            msg = "Error occured in insert operation: " + str(e)
        finally:
            conn.close()
            return render_template('result.html', msg=msg)


@app.route('/show-records/', methods=["GET"])
def show_records():
    records = []
    try:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM students")
            records = cur.fetchall()
    except Exception as e:
        con.rollback()
        print("There was an error fetching results from the database.")
    finally:
        con.close()
        return jsonify(records)