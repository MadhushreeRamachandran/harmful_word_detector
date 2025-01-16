import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import nltk
from nltk.tokenize import word_tokenize
import os

# Ensure necessary NLTK resources are available
nltk.download('punkt')

# List of harmful words (can be expanded as needed)
harmful_words = [
    "hate", "violence", "abuse", "hurt", "kill", "stupid", "disgusting", "murder"
]

# Function to tokenize and detect harmful words
def detect_harmful_words(text):
    tokens = word_tokenize(text.lower())  # Tokenizing and converting to lowercase
    harmful_found = [word for word in tokens if word in harmful_words]  # Detect harmful words
    return harmful_found

# Function to process the input file
# Function to process the input file
def process_file(file_path):
    try:
        with open(file_path, 'r') as file:
            text = file.read()

            harmful_found = detect_harmful_words(text)

            # Clear the previous result and display the new one
            output_text.delete(1.0, tk.END)

            if harmful_found:
                result = f"The content is not accepted.\nHarmful words found:\n" + ", ".join(harmful_found)
                update_status('red', "Not Accepted")
                harmful_words_tab(harmful_found)
            else:
                result = "The content is accepted."
                update_status('green', "Accepted")
                harmful_words_tab([])

            # Insert the new result
            output_text.insert(tk.END, result)

    except FileNotFoundError:
        messagebox.showerror("File Not Found", "The file was not found, please check the file path.")


# Function to handle file selection
def select_file():
    file_path = filedialog.askopenfilename(title="Select an Input File", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
    if file_path:
        process_file(file_path)

# Function to create the application window
def create_app():
    global app, output_text, signal_canvas, harmful_listbox, tab_control  # Declare 'app' globally

    # For high-DPI scaling
    try:
        app.tk.call('tk', 'scaling', 2.0)  # 2.0 scales the display, you can try changing the value for testing
    except Exception:
        pass

    # Create the main window
    app = tk.Tk()
    app.title("Harmful Word Detector")
    app.geometry("600x500")  # Set window size
    app.configure(bg="#f0f0f0")  # Set background color to light gray

    # Create the header label
    header_label = tk.Label(app, text="Harmful Word Detector", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
    header_label.pack(pady=20)

    # Create a description label
    description_label = tk.Label(app, text="Select a text file to check for harmful words.", font=("Helvetica", 12), bg="#f0f0f0")
    description_label.pack(pady=10)

    # Create the button to open file dialog
    select_button = tk.Button(app, text="Select Input File", command=select_file, font=("Helvetica", 12), relief="raised", bg="#4CAF50", fg="white")
    select_button.pack(pady=10, ipadx=10, ipady=5)

    # Create a Canvas for signal display (Green/Red circle)
    signal_canvas = tk.Canvas(app, width=50, height=50, bg="#f0f0f0", bd=0)
    signal_canvas.pack(pady=20)
    update_status('gray', "Status")

    # Create an output panel (Text widget) to show results
    output_text = tk.Text(app, height=6, width=70, font=("Arial", 12), wrap=tk.WORD, padx=10, pady=10)
    output_text.pack(padx=20, pady=20)

    # Create the tab control (Tabbed interface for harmful words)
    tab_control = ttk.Notebook(app)

    # Tab for displaying harmful words
    harmful_tab = ttk.Frame(tab_control)
    tab_control.add(harmful_tab, text="Harmful Words")

    harmful_listbox = tk.Listbox(harmful_tab, height=6, width=50, font=("Arial", 12))
    harmful_listbox.pack(padx=20, pady=20)

    # Pack the tab control
    tab_control.pack(expand=1, fill="both", padx=20, pady=10)

    # Run the main event loop
    app.mainloop()

# Function to update the signal (green or red) for 'accepted' or 'not accepted'
def update_status(color, message):
    signal_canvas.delete("all")
    signal_canvas.create_oval(10, 10, 40, 40, outline=color, width=2, fill=color)
    status_label = tk.Label(app, text=message, font=("Helvetica", 14, "bold"), bg="#f0f0f0")
    status_label.pack(pady=10)

# Function to update the harmful words in the separate tab
def harmful_words_tab(harmful_list):
    harmful_listbox.delete(0, tk.END)
    if harmful_list:
        for word in harmful_list:
            harmful_listbox.insert(tk.END, word)
    else:
        harmful_listbox.insert(tk.END, "No harmful words found.")

# Run the application
if __name__ == "__main__":
    create_app()
