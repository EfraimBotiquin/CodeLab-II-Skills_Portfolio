import tkinter as tk
from tkinter import messagebox, simpledialog
from pathlib import Path

# AI acknowledgement:
# Prompts used:
# - What is the difference between total marks and percentage?
# - How does updating a text file work?
# - How can I compare two student totals?

DATA_FILE = Path(__file__).parent / "studentMarks.txt"


def load_students():
    """Read the count on line one, then read each student's comma-separated data."""
    students = []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            lines = file.readlines()

        # The first line is the stated number of records; each later line is a record.
        for line in lines[1:]:
            parts = line.strip().split(",")
            if len(parts) == 6:
                students.append({
                    "code": parts[0].strip(),
                    "name": parts[1].strip(),
                    "course1": int(parts[2]),
                    "course2": int(parts[3]),
                    "course3": int(parts[4]),
                    "exam": int(parts[5]),
                })
    except FileNotFoundError:
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        save_students(students)
    except (ValueError, OSError) as error:
        messagebox.showerror("File problem", f"Could not read the student file:\n{error}")
    return students


def save_students(students):
    """Write the current count and all records back to the text file."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        file.write(str(len(students)) + "\n")
        for student in students:
            file.write(
                f"{student['code']},{student['name']},{student['course1']},"
                f"{student['course2']},{student['course3']},{student['exam']}\n"
            )


def total_mark(student):
    return student["course1"] + student["course2"] + student["course3"] + student["exam"]


def percentage(student):
    return total_mark(student) / 160 * 100


def grade(student):
    mark = percentage(student)
    if mark >= 70:
        return "A"
    if mark >= 60:
        return "B"
    if mark >= 50:
        return "C"
    if mark >= 40:
        return "D"
    return "F"


class StudentManager:
    def __init__(self, window):
        self.window = window
        self.window.title("Student Manager")
        self.window.geometry("780x570")
        self.students = load_students()

        tk.Label(window, text="Student Manager", font=("Arial", 18, "bold")).pack(pady=8)

        buttons = tk.Frame(window)
        buttons.pack(pady=5)
        options = [
            ("View all", self.view_all),
            ("View one", self.view_one),
            ("Highest", self.show_highest),
            ("Lowest", self.show_lowest),
            ("Sort", self.sort_students),
            ("Add", self.add_student),
            ("Delete", self.delete_student),
            ("Update", self.update_student),
        ]
        for number, (label, action) in enumerate(options):
            tk.Button(buttons, text=label, width=13, command=action).grid(
                row=number // 4, column=number % 4, padx=4, pady=4
            )

        self.output = tk.Text(window, width=94, height=26, wrap="none", font=("Consolas", 10))
        self.output.pack(padx=10, pady=8, fill="both", expand=True)
        self.write("Choose an option above.\n")

    def write(self, text):
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, text)

    def student_text(self, student):
        course_total = student["course1"] + student["course2"] + student["course3"]
        return (
            f"Name: {student['name']}\n"
            f"Student number: {student['code']}\n"
            f"Coursework total: {course_total}/60\n"
            f"Exam mark: {student['exam']}/100\n"
            f"Overall: {total_mark(student)}/160 ({percentage(student):.2f}%)\n"
            f"Grade: {grade(student)}\n"
        )

    def view_students(self, students, summary=True):
        if not students:
            self.write("No student records found. Add a student or check the data file.\n")
            return
        text = ""
        for student in students:
            text += self.student_text(student) + "\n" + "-" * 38 + "\n"
        if summary:
            average = sum(percentage(s) for s in students) / len(students)
            text += f"\nClass size: {len(students)}\nAverage percentage: {average:.2f}%\n"
        self.write(text)

    def view_all(self):
        self.view_students(self.students)

    def find_student(self):
        search = simpledialog.askstring("Find student", "Enter student number or name:")
        if not search:
            return None
        for student in self.students:
            if student["code"] == search.strip() or student["name"].lower() == search.strip().lower():
                return student
        messagebox.showinfo("Not found", "No student matched that name or number.")
        return None

    def view_one(self):
        student = self.find_student()
        if student:
            self.view_students([student], summary=False)

    def show_highest(self):
        if self.students:
            self.view_students([max(self.students, key=total_mark)], summary=False)
        else:
            self.view_students([])

    def show_lowest(self):
        if self.students:
            self.view_students([min(self.students, key=total_mark)], summary=False)
        else:
            self.view_students([])

    def sort_students(self):
        direction = simpledialog.askstring("Sort", "Type A for ascending or D for descending:")
        if direction and direction.upper() in ("A", "D"):
            self.students.sort(key=total_mark, reverse=(direction.upper() == "D"))
            self.view_students(self.students)

    def get_mark(self, question, maximum):
        value = simpledialog.askinteger("Student mark", question, minvalue=0, maxvalue=maximum)
        return value

    def add_student(self):
        code = simpledialog.askstring("Add student", "Student number (4 digits):")
        if code is None:
            return
        code = code.strip()
        if not code.isdigit() or len(code) != 4:
            messagebox.showerror("Invalid number", "Student number must contain 4 digits.")
            return
        if any(s["code"] == code for s in self.students):
            messagebox.showerror("Already used", "That student number is already in use.")
            return
        name = simpledialog.askstring("Add student", "Student name (no commas):")
        if not name or "," in name:
            messagebox.showerror("Invalid name", "Enter a name without commas.")
            return
        marks = []
        for label, maximum in (("Course mark 1 (out of 20)", 20), ("Course mark 2 (out of 20)", 20),
                               ("Course mark 3 (out of 20)", 20), ("Exam mark (out of 100)", 100)):
            mark = self.get_mark(label, maximum)
            if mark is None:
                return
            marks.append(mark)
        self.students.append({"code": code, "name": name.strip(), "course1": marks[0],
                              "course2": marks[1], "course3": marks[2], "exam": marks[3]})
        save_students(self.students)
        self.view_all()

    def delete_student(self):
        student = self.find_student()
        if student and messagebox.askyesno("Delete student", f"Delete {student['name']}?"):
            self.students.remove(student)
            save_students(self.students)
            self.view_all()

    def update_student(self):
        student = self.find_student()
        if not student:
            return
        name = simpledialog.askstring("Update", "New name (leave blank to keep current):")
        if name:
            if "," in name:
                messagebox.showerror("Invalid name", "Names cannot contain commas.")
                return
            student["name"] = name.strip()
        for field, label, maximum in (
            ("course1", "Course mark 1 /20 (Cancel to keep current)", 20),
            ("course2", "Course mark 2 /20 (Cancel to keep current)", 20),
            ("course3", "Course mark 3 /20 (Cancel to keep current)", 20),
            ("exam", "Exam mark /100 (Cancel to keep current)", 100),
        ):
            value = simpledialog.askinteger("Update", label, minvalue=0, maxvalue=maximum)
            if value is not None:
                student[field] = value
        save_students(self.students)
        self.view_all()


window = tk.Tk()
app = StudentManager(window)
window.mainloop()
