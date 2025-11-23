import sqlite3
import random
import matplotlib.pyplot as plt
from datetime import datetime


class TaskManager:
    """A simple personal task manager using SQLite."""

    def __init__(self, db_path='tasks.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.create_table()

        # Motivational affirmations
        self.my_affirmations = [
            "You're doing great, keep going!",
            "Every small step counts!",
            "Believe in yourself!",
            "Your hard work is paying off!",
            "Stay positive and stay strong!"
        ]

    def create_table(self):
        """Creates the tasks table if it doesn't exist."""
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                description TEXT,
                priority TEXT,
                due_date TEXT,
                completed INTEGER
            )
        ''')
        self.conn.commit()

    def add_task(self, title, description, priority, due_date):
        """Adds a new task into the database."""
        self.conn.execute(
            'INSERT INTO tasks (title, description, priority, due_date, completed) VALUES (?, ?, ?, ?, ?)',
            (title, description, priority, due_date, 0)
        )
        self.conn.commit()
        print("Task added successfully!")

    def update_task(self, task_id, title, description, priority, due_date):
        """Updates an existing task."""
        self.conn.execute(
            'UPDATE tasks SET title=?, description=?, priority=?, due_date=? WHERE id=?',
            (title, description, priority, due_date, task_id)
        )
        self.conn.commit()
        print("Task updated successfully!")

    def delete_task(self, task_id):
        """Deletes a task by ID."""
        self.conn.execute('DELETE FROM tasks WHERE id=?', (task_id,))
        self.conn.commit()
        print("Task deleted successfully!")

    def complete_task(self, task_id):
        """Marks a task as completed and shows an affirmation."""
        self.conn.execute('UPDATE tasks SET completed=1 WHERE id=?', (task_id,))
        self.conn.commit()

        print("Great job! Task marked as completed!")
        print("✨ Affirmation:", random.choice(self.my_affirmations))

    def view_tasks(self):
        """Displays all tasks."""
        cursor = self.conn.execute('SELECT * FROM tasks')
        tasks = cursor.fetchall()

        if not tasks:
            print("No tasks found.")
        else:
            print("\n---- ALL TASKS ----")
            for task in tasks:
                print(task)

    def show_pie_chart(self):
        """Displays pie chart of completed vs pending tasks."""
        cursor = self.conn.execute('SELECT completed FROM tasks')
        data = cursor.fetchall()

        completed = sum(1 for d in data if d[0] == 1)
        pending = sum(1 for d in data if d[0] == 0)

        labels = ['Completed', 'Pending']
        values = [completed, pending]

        plt.pie(values, labels=labels, autopct='%1.1f%%')
        plt.title("Task Completion Status")
        plt.show()

    def show_bar_graph(self):
        """Displays a bar graph of tasks grouped by priority."""
        cursor = self.conn.execute('SELECT priority, COUNT(*) FROM tasks GROUP BY priority')
        data = cursor.fetchall()

        labels = [row[0] for row in data]
        values = [row[1] for row in data]

        plt.bar(labels, values)
        plt.title("Tasks by Priority")
        plt.xlabel("Priority")
        plt.ylabel("Number of Tasks")
        plt.show()


def menu():
    """Main menu loop by user."""
    tm = TaskManager()

    while True:
        print("\n===== PERSONAL TASK MANAGER =====")
        print("1. Add Task")
        print("2. Update Task")
        print("3. Delete Task")
        print("4. Complete Task")
        print("5. View Tasks")
        print("6. Show Pie Chart (Completed vs Pending)")
        print("7. Show Bar Graph (Priority Overview)")
        print("8. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            title = input("Title: ")
            desc = input("Description: ")
            pr = input("Priority (High/Medium/Low): ")
            date = input("Due Date (YYYY-MM-DD): ")
            tm.add_task(title, desc, pr, date)

        elif choice == "2":
            tid = int(input("Enter Task ID: "))
            title = input("New Title: ")
            desc = input("New Description: ")
            pr = input("New Priority: ")
            date = input("New Due Date: ")
            tm.update_task(tid, title, desc, pr, date)

        elif choice == "3":
            tid = int(input("Enter Task ID: "))
            tm.delete_task(tid)

        elif choice == "4":
            tid = int(input("Enter Task ID: "))
            tm.complete_task(tid)

        elif choice == "5":
            tm.view_tasks()

        elif choice == "6":
            print("Generating Pie Chart...")
            tm.show_pie_chart()

        elif choice == "7":
            print("Generating Bar Graph...")
            tm.show_bar_graph()

        elif choice == "8":
            print("Exiting... Have a productive day!")
            break

        else:
            print("Invalid choice, try again.")


menu()
