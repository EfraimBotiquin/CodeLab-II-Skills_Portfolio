from pathlib import Path
import random
import tkinter as tk

# AI acknowledgement: I created this app and used OpenAI ChatGPT for help with
# loading jokes safely and splitting each joke at its first question mark.
# Prompts used: "How can I handle a missing or empty joke file?"
# "How can I split a joke at its first question mark in Python?"
# Prompt: "Suggest a game-style font I can use in my Tkinter code."
# AI suggested "Audiowide" and showed how to download and use it.

# Keep randomJokes.txt in the same folder as this program.
JOKES_FILE = Path(__file__).resolve().parent / "randomJokes.txt"


def load_jokes():
    """Load valid setup and punchline pairs from the text file."""
    jokes = []

    try:
        with JOKES_FILE.open("r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                # Split only at the first question mark, preserving any later ones.
                if "?" in line:
                    setup, punchline = line.split("?", 1)
                    setup = setup.strip()
                    punchline = punchline.strip()

                    if setup and punchline:
                        jokes.append((setup + "?", punchline))
    except OSError:
        # Leave the list empty so the app can show a helpful message.
        pass

    return jokes


def show_random_joke():
    """Choose a joke and show its setup, keeping the punchline hidden."""
    global current_joke, previous_joke_index

    if not jokes:
        current_joke = None
        setup_label.config(text="No jokes found. Check that randomJokes.txt is beside this program.")
        punchline_label.config(text="")
        return

    choices = list(range(len(jokes)))

    # Avoid showing the same joke twice in a row when possible.
    if len(choices) > 1 and previous_joke_index is not None:
        choices.remove(previous_joke_index)

    selected_index = random.choice(choices)
    previous_joke_index = selected_index
    current_joke = jokes[selected_index]

    setup_label.config(text=current_joke[0])
    punchline_label.config(text="")


def show_punchline():
    """Display the punchline after the user presses its button."""
    if current_joke is None:
        punchline_label.config(text="Please load a joke first.")
    else:
        punchline_label.config(text=current_joke[1])


# Load the jokes before creating the window.
jokes = load_jokes()
current_joke = None
previous_joke_index = None

# Create the main application window.
root = tk.Tk()
root.title("Alexa Tell Me a Joke")
root.geometry("680x410")
root.minsize(520, 350)
root.configure(bg="#253858")

# Heading
heading = tk.Label(
    root,
    text="Alexa Tell Me a Joke",
    font=("Audiowide", 22, "bold"),
    bg="#253858",
    fg="white",
    pady=16,
)
heading.pack(fill="x")

# Joke setup display
setup_label = tk.Label(
    root,
    text="Press the button below to hear a joke!",
    font=("Audiowide", 14),
    wraplength=600,
    justify="center",
    bg="white",
    fg="#172b4d",
    padx=20,
    pady=24,
    relief="groove",
)
setup_label.pack(fill="x", padx=28, pady=(28, 10))

# The punchline starts blank and appears only when requested.
punchline_label = tk.Label(
    root,
    text="",
    font=("Audiowide", 14, "italic"),
    wraplength=600,
    justify="center",
    bg="#deebff",
    fg="#0747A6",
    padx=20,
    pady=18,
)
punchline_label.pack(fill="x", padx=28, pady=8)

# Required joke controls
button_frame = tk.Frame(root, bg="#253858")
button_frame.pack(pady=18)

button_style = {
    "font": ("Audiowide", 10, "bold"),
    "bg": "#0052CC",
    "fg": "white",
    "padx": 12,
    "pady": 9,
}

tk.Button(
    button_frame,
    text="Alexa tell me a Joke",
    command=show_random_joke,
    **button_style,
).pack(side="left", padx=6)

tk.Button(
    button_frame,
    text="Show Punchline",
    command=show_punchline,
    **button_style,
).pack(side="left", padx=6)

tk.Button(
    button_frame,
    text="Next Joke",
    command=show_random_joke,
    **button_style,
).pack(side="left", padx=6)

tk.Button(
    root,
    text="Quit",
    command=root.destroy,
    font=("Audiowide", 10, "bold"),
    bg="#B22222",
    fg="white",
    padx=22,
    pady=8,
).pack(pady=(2, 14))

root.mainloop()

