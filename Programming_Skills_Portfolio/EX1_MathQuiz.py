import random
import tkinter as tk

# AI acknowledgement:
# Tool: ChatGPT. Prompts: "Suggest a comments for the tricky
# answer-checking and scoring parts of my code" I created the original
# game and reviewed the AI suggestions.
# Prompt: "Suggest a game-style font I can use in my Tkinter code."
# ChatGPT suggested Audiowide and showed how to use it.

# Game settings and colours
QUESTION_TOTAL = 10
BACKGROUND = "#006F0F"
PANEL = "#00c30d"
TEXT = "black"
BUTTON_COLOR = "#2E8B57"
BUTTON_TEXT = "white"
QUIT_COLOR = "#B22222"

# Game information
score = 0
question_number = 1
attempts = 0
question_finished = False
difficulty = "Easy"
number1 = 0
number2 = 0
operation = "+"
answer = 0

# Create the main window
window = tk.Tk()
window.title("Maths Quiz")
window.geometry("500x500")
window.configure(bg=BACKGROUND)


def clearWindow():
    """Remove everything from the window."""
    for item in window.winfo_children():
        item.destroy()


def displayMenu():
    """Show buttons for choosing a difficulty."""
    clearWindow()

    tk.Label(
        window, text="Maths Quiz", font=("Audiowide", 26, "bold"),
        fg=TEXT, bg=BACKGROUND
    ).pack(pady=(45, 10))

    tk.Label(
        window, text="Choose a difficulty", font=("Audiowide", 14),
        fg=TEXT, bg=BACKGROUND
    ).pack(pady=10)

    tk.Button(window, text="Easy", width=20,
              bg=BUTTON_COLOR, fg=BUTTON_TEXT,
              command=lambda: startQuiz("Easy")).pack(pady=7)
    tk.Button(window, text="Moderate", width=20,
              bg=BUTTON_COLOR, fg=BUTTON_TEXT,
              command=lambda: startQuiz("Moderate")).pack(pady=7)
    tk.Button(window, text="Advanced", width=20,
              bg=BUTTON_COLOR, fg=BUTTON_TEXT,
              command=lambda: startQuiz("Advanced")).pack(pady=7)
    tk.Button(window, text="Quit", width=20,
              bg=QUIT_COLOR, fg=BUTTON_TEXT,
              command=window.destroy).pack(pady=18)


def randomInt(level):
    """Return a random number for the chosen difficulty."""
    if level == "Easy":
        return random.randint(0, 9)
    elif level == "Moderate":
        return random.randint(10, 99)
    else:
        return random.randint(1000, 9999)


def decideOperation():
    """Randomly choose addition or subtraction."""
    return random.choice(["+", "-"])


def startQuiz(level):
    """Start a new game and reset the score and question number."""
    global difficulty, score, question_number

    difficulty = level
    score = 0
    question_number = 1
    displayProblem()


def displayProblem():
    """Make a new question and show the answer box."""
    global number1, number2, operation, answer, attempts, question_finished

    attempts = 0
    question_finished = False
    number1 = randomInt(difficulty)
    number2 = randomInt(difficulty)
    operation = decideOperation()

    # Calculate the answer; subtraction can produce a negative result.
    if operation == "+":
        answer = number1 + number2
    else:
        answer = number1 - number2

    clearWindow()

    tk.Label(
        window, text=f"{difficulty} difficulty",
        font=("Audiowide", 12), fg=TEXT, bg=BACKGROUND
    ).pack(pady=(25, 5))

    tk.Label(
        window, text=f"Question {question_number}/{QUESTION_TOTAL}",
        font=("Audiowide", 14), fg=TEXT, bg=BACKGROUND
    ).pack(pady=5)

    tk.Label(
        window, text=f"Score: {score}",
        font=("Audiowide", 12), fg=TEXT, bg=BACKGROUND
    ).pack(pady=5)

    tk.Label(
        window, text=f"{number1} {operation} {number2} = ?",
        font=("Audiowide", 28, "bold"), fg=TEXT, bg=PANEL,
        padx=25, pady=20
    ).pack(pady=20)

    tk.Label(
        window, text="Your answer:",
        font=("Audiowide", 12), fg=TEXT, bg=BACKGROUND
    ).pack(pady=5)

    answer_box = tk.Entry(window, font=("Audiowide", 18), justify="center")
    answer_box.pack(pady=5)
    answer_box.focus_set()

    feedback = tk.Label(
        window, text="", font=("Audiowide", 12), fg=TEXT, bg=BACKGROUND
    )
    feedback.pack(pady=12)

    submit_button = tk.Button(
        window, text="Submit Answer", bg=BUTTON_COLOR, fg=BUTTON_TEXT,
    )
    submit_button.config(
        command=lambda: isCorrect(answer_box, feedback, submit_button)
    )
    submit_button.pack(pady=5)

    # Allow Enter to submit the answer.
    answer_box.bind(
        "<Return>",
        lambda event: isCorrect(answer_box, feedback, submit_button)
    )

    tk.Button(
        window, text="Quit", bg=QUIT_COLOR, fg=BUTTON_TEXT,
        command=window.destroy
    ).pack(pady=12)


def isCorrect(answer_box, feedback, submit_button):
    """Check an answer and give points or another attempt."""
    global attempts, score, question_finished

    # Prevent scoring a question twice.
    if question_finished:
        return

    try:
        player_answer = int(answer_box.get())
    except ValueError:
        feedback.config(text="Please enter a whole number.", fg="tomato")
        answer_box.focus_set()
        return

    if player_answer == answer:
        if attempts == 0:
            score = score + 10
            feedback.config(text="Correct! You earned 10 points.", fg="lightgreen")
        else:
            # Give fewer points for a second-try answer.
            score = score + 5
            feedback.config(text="Correct! You earned 5 points.", fg="lightgreen")
        question_finished = True
    else:
        attempts = attempts + 1
        if attempts == 1:
            feedback.config(text="Incorrect. Try one more time.", fg="tomato")
            answer_box.delete(0, tk.END)
            answer_box.focus_set()
            return
        else:
            feedback.config(text=f"Incorrect. The answer was {answer}.", fg="tomato")
            question_finished = True

    # Change the button after the answer is checked.
    if question_number == QUESTION_TOTAL:
        submit_button.config(text="See Results", command=displayResults)
    else:
        submit_button.config(text="Next Question", command=nextQuestion)


def nextQuestion():
    """Show the next question."""
    global question_number
    question_number = question_number + 1
    displayProblem()


def displayResults():
    """Show the final score and allow the player to play again."""
    clearWindow()

    tk.Label(
        window, text="Quiz Complete!", font=("Audiowide", 26, "bold"),
        fg=TEXT, bg=BACKGROUND
    ).pack(pady=(70, 15))

    tk.Label(
        window, text=f"Your score: {score} / 100",
        font=("Audiowide", 22), fg=TEXT, bg=BACKGROUND
    ).pack(pady=10)

    tk.Label(
        window, text=f"Grade: {getGrade(score)}",
        font=("Audiowide", 18), fg=TEXT, bg=BACKGROUND
    ).pack(pady=10)

    tk.Button(window, text="Play Again", width=20,
              bg=BUTTON_COLOR, fg=BUTTON_TEXT,
              command=displayMenu).pack(pady=(30, 10))
    tk.Button(window, text="Quit", width=20,
              bg=QUIT_COLOR, fg=BUTTON_TEXT,
              command=window.destroy).pack(pady=5)


def getGrade(final_score):
    """Choose a grade based on the final score."""
    if final_score > 90:
        return "A+"
    elif final_score >= 80:
        return "A"
    elif final_score >= 70:
        return "B"
    elif final_score >= 60:
        return "C"
    elif final_score >= 50:
        return "D"
    else:
        return "Keep practising"


displayMenu()
window.mainloop()
