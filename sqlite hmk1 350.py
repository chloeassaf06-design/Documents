import sqlite3

conn = sqlite3.connect('students.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS student (
        student_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS registered_courses (
        student_id INTEGER,
        course_id TEXT,
        FOREIGN KEY (student_id) REFERENCES student (student_id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS grades (
        student_id INTEGER,
        course_id TEXT,
        grade REAL,
        FOREIGN KEY (student_id) REFERENCES student (student_id)
    )
''')

sample_students = [(101, 'Alice', 20), (102, 'Bob', 22)]
sample_grades = [
    (101, 'CS101', 85), (101, 'MATH202', 92), (101, 'PHY101', 78),
    (102, 'CS101', 88), (102, 'MATH202', 75)
]

cursor.executemany('INSERT OR IGNORE INTO student VALUES (?,?,?)', sample_students)
cursor.executemany('INSERT OR IGNORE INTO grades VALUES (?,?,?)', sample_grades)

conn.commit()

print(" Maximum Grade per Student")
query_max = '''
    SELECT student_id, course_id, MAX(grade) 
    FROM grades 
    GROUP BY student_id
'''
cursor.execute(query_max)
for row in cursor.fetchall():
    print(f"Student ID: {row[0]} | Course: {row[1]} | Max Grade: {row[2]}")

print("\n Average Grade for Student 101")
student_id = 101
cursor.execute('SELECT AVG(grade) FROM grades WHERE student_id = ?', (student_id,))
avg_grade = cursor.fetchone()[0]
print(f"The average grade for Student {student_id} is: {avg_grade:.2f}")

conn.close()