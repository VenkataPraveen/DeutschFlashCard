# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox, filedialog
import random
import json
import os


class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flashcard App")

        # Flashcard storage
        self.flashcards = []
        self.flashcard_views = {}  # To track the number of views
        self.load_flashcards()  # Load flashcards from memory

        # GUI Elements
        self.term_label = tk.Label(root, text="German Term:", font=("Arial", 14))
        self.term_label.pack(pady=5)

        self.term_entry = tk.Entry(root, font=("Arial", 14))
        self.term_entry.pack(pady=5)

        self.translation_label = tk.Label(
            root, text="English Translation:", font=("Arial", 14)
        )
        self.translation_label.pack(pady=5)

        self.translation_entry = tk.Entry(root, font=("Arial", 14))
        self.translation_entry.pack(pady=5)

        self.explanation_label = tk.Label(
            root, text="German Explanation:", font=("Arial", 14)
        )
        self.explanation_label.pack(pady=5)

        self.explanation_entry = tk.Entry(root, font=("Arial", 14))
        self.explanation_entry.pack(pady=5)

        self.example_label = tk.Label(root, text="German Example:", font=("Arial", 14))
        self.example_label.pack(pady=5)

        self.example_entry = tk.Entry(root, font=("Arial", 14))
        self.example_entry.pack(pady=5)

        self.example_translation_label = tk.Label(
            root, text="English Example Translation:", font=("Arial", 14)
        )
        self.example_translation_label.pack(pady=5)

        self.example_translation_entry = tk.Entry(root, font=("Arial", 14))
        self.example_translation_entry.pack(pady=5)

        self.add_button = tk.Button(
            root, text="Add Flashcard", font=("Arial", 14), command=self.add_flashcard
        )
        self.add_button.pack(pady=10)

        self.import_button = tk.Button(
            root,
            text="Import from File",
            font=("Arial", 14),
            command=self.import_flashcards,
        )
        self.import_button.pack(pady=10)

        self.export_button = tk.Button(
            root,
            text="Export to File",
            font=("Arial", 14),
            command=self.export_flashcards,
        )
        self.export_button.pack(pady=10)

        self.view_all_button = tk.Button(
            root,
            text="View All Flashcards",
            font=("Arial", 14),
            command=self.view_all_flashcards,
        )
        self.view_all_button.pack(pady=10)

        self.quiz_button = tk.Button(
            root, text="Quiz Mode", font=("Arial", 14), command=self.start_quiz
        )
        self.quiz_button.pack(pady=10)

    def add_flashcard(self):
        term = self.term_entry.get().strip()
        translation = self.translation_entry.get().strip()
        explanation = self.explanation_entry.get().strip()
        example = self.example_entry.get().strip()
        example_translation = self.example_translation_entry.get().strip()

        if (
            not term
            or not translation
            or not explanation
            or not example
            or not example_translation
        ):
            messagebox.showwarning(
                "Input Error", "Please fill in all fields to add a flashcard."
            )
            return

        self.flashcards.append(
            {
                "term": term,
                "translation": translation,
                "explanation": explanation,
                "example": example,
                "example_translation": example_translation,
            }
        )
        self.flashcard_views[term] = 0  # Initialize view count
        self.save_flashcards()
        messagebox.showinfo("Success", f"Flashcard '{term}' added successfully!")

        # Clear input fields
        self.term_entry.delete(0, tk.END)
        self.translation_entry.delete(0, tk.END)
        self.explanation_entry.delete(0, tk.END)
        self.example_entry.delete(0, tk.END)
        self.example_translation_entry.delete(0, tk.END)

    def save_flashcards(self):
        with open("flashcards.json", "w", encoding="utf-8") as file:
            json.dump(
                {"flashcards": self.flashcards, "views": self.flashcard_views}, file
            )

    def load_flashcards(self):
        if os.path.exists("flashcards.json"):
            with open("flashcards.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                self.flashcards = data.get("flashcards", [])
                self.flashcard_views = data.get("views", {})

    def import_flashcards(self):
        file_path = filedialog.askopenfilename(
            title="Select Flashcards File",
            filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")),
        )

        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                for line in file:
                    parts = line.strip().split("|")
                    if len(parts) == 5:
                        term = parts[0]
                        self.flashcards.append(
                            {
                                "term": term,
                                "translation": parts[1],
                                "explanation": parts[2],
                                "example": parts[3],
                                "example_translation": parts[4],
                            }
                        )
                        self.flashcard_views[term] = self.flashcard_views.get(term, 0)
                self.save_flashcards()
            messagebox.showinfo("Success", "Flashcards imported successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not import flashcards: {str(e)}")

    def export_flashcards(self):
        file_path = filedialog.asksaveasfilename(
            title="Save Flashcards File",
            defaultextension=".txt",
            filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")),
        )

        if not file_path:
            return

        try:
            with open(file_path, "w", encoding="utf-8") as file:
                for flashcard in self.flashcards:
                    line = "|".join(
                        [
                            flashcard["term"],
                            flashcard["translation"],
                            flashcard["explanation"],
                            flashcard["example"],
                            flashcard["example_translation"],
                        ]
                    )
                    file.write(line + "\n")
            messagebox.showinfo("Success", "Flashcards exported successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not export flashcards: {str(e)}")

    def view_all_flashcards(self):
        if not self.flashcards:
            messagebox.showwarning("No Flashcards", "No flashcards available to view.")
            return

        # Initialize pagination variables
        self.current_page = 0
        self.flashcards_per_page = 5
        self.total_pages = (
            len(self.flashcards) + self.flashcards_per_page - 1
        ) // self.flashcards_per_page

        # Create a new Toplevel window
        self.view_window = tk.Toplevel(self.root)
        self.view_window.title("All Flashcards")
        self.view_window.geometry("400x400")

        # Frame for displaying flashcards
        self.flashcard_frame = tk.Frame(self.view_window)
        self.flashcard_frame.pack(fill=tk.BOTH, expand=True)

        # Navigation frame
        self.navigation_frame = tk.Frame(self.view_window)
        self.navigation_frame.pack(fill=tk.X)

        self.prev_button = tk.Button(
            self.navigation_frame, text="Previous", command=self.show_previous_page
        )
        self.prev_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.next_button = tk.Button(
            self.navigation_frame, text="Next", command=self.show_next_page
        )
        self.next_button.pack(side=tk.RIGHT, padx=10, pady=5)

        self.page_label = tk.Label(
            self.navigation_frame,
            text=f"Page {self.current_page + 1} of {self.total_pages}",
            font=("Arial", 12),
        )
        self.page_label.pack(side=tk.LEFT, padx=10, pady=5)

        # Display the first page of flashcards
        self.show_flashcards_page()

    def show_flashcards_page(self):
        # Clear previous flashcards
        for widget in self.flashcard_frame.winfo_children():
            widget.destroy()

        # Determine the start and end indices for the current page
        start_index = self.current_page * self.flashcards_per_page
        end_index = start_index + self.flashcards_per_page

        # Display flashcards for the current page
        for i in range(start_index, min(end_index, len(self.flashcards))):
            flashcard = self.flashcards[i]
            term = flashcard["term"]

            # Increment the view count
            self.flashcard_views[term] = self.flashcard_views.get(term, 0)

            # Determine the button color based on view count
            button_color = (
                "green" if self.flashcard_views[term] >= 5 else "SystemButtonFace"
            )

            button_text = f"{term} (Seen: {self.flashcard_views[term]} times)"
            button = tk.Button(
                self.flashcard_frame,
                text=button_text,
                font=("Arial", 12),
                bg=button_color,
                command=lambda f=flashcard: self.show_flashcard_popup(f),
            )
            button.pack(fill=tk.X, padx=10, pady=5)

        # Update the page label
        self.page_label.config(
            text=f"Page {self.current_page + 1} of {self.total_pages}"
        )

    def show_previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_flashcards_page()

    def show_next_page(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.show_flashcards_page()

    def show_flashcard_popup(self, flashcard):
        term = flashcard["term"]
        self.flashcard_views[term] = self.flashcard_views.get(term, 0) + 1
        self.save_flashcards()

        # Create a popup window
        popup = tk.Toplevel(self.root)
        popup.title("Flashcard")
        popup.geometry("400x400")

        # Flashcard term label
        flashcard_label = tk.Label(popup, text=flashcard["term"], font=("Arial", 16))
        flashcard_label.pack(expand=True, fill=tk.BOTH)

        # Toggle between term and details
        showing_back = False

        def flip_flashcard():
            nonlocal showing_back
            if showing_back:
                flashcard_label.config(text=flashcard["term"])
            else:
                flashcard_label.config(
                    text=(
                        f"Translation: {flashcard['translation']}\n\n"
                        f"Explanation: {flashcard['explanation']}\n\n"
                        f"Example: {flashcard['example']}\n\n"
                        f"Example Translation: {flashcard['example_translation']}"
                    )
                )
            showing_back = not showing_back

        flashcard_label.bind("<Button-1>", lambda event: flip_flashcard())
        # Update the flashcard color in the main view if viewed >= 5 times
        if self.flashcard_views[term] >= 5:
            self.show_flashcards_page()

    def start_quiz(self):
        if not self.flashcards:
            messagebox.showwarning(
                "No Flashcards", "No flashcards available for a quiz."
            )
            return

        # Shuffle the flashcards
        random.shuffle(self.flashcards)

        # Create a new Toplevel window
        self.quiz_window = tk.Toplevel(self.root)
        self.quiz_window.title("Quiz Mode")
        self.quiz_window.geometry("500x500")

        # Initialize quiz state variables
        self.quiz_index = 0
        self.correct_answers = 0
        self.wrong_answers = 0

        def show_next_question():
            if self.quiz_index >= len(self.flashcards):
                # End the quiz
                self.quiz_window.destroy()
                messagebox.showinfo(
                    "Quiz Completed",
                    f"Correct: {self.correct_answers}, Wrong: {self.wrong_answers}",
                )
                return

            flashcard = self.flashcards[self.quiz_index]
            term = flashcard["term"]
            correct_translation = flashcard["translation"]

            # Generate random options
            options = [correct_translation]
            while len(options) < 4:
                random_card = random.choice(self.flashcards)
                if random_card["translation"] not in options:
                    options.append(random_card["translation"])
            random.shuffle(options)  # Shuffle options

            # Update the question and options
            self.quiz_label.config(text=f"Term: {term}", bg="white")

            for i, option in enumerate(self.option_buttons):
                option.config(
                    text=options[i],
                    bg="SystemButtonFace",
                    command=lambda opt=options[i]: validate_answer(
                        opt, correct_translation
                    ),
                )

            self.quiz_index += 1

        def validate_answer(selected_option, correct_option):
            if selected_option == correct_option:
                self.correct_answers += 1
                for button in self.option_buttons:
                    if button["text"] == correct_option:
                        button.config(bg="green")
            else:
                self.wrong_answers += 1
                for button in self.option_buttons:
                    if button["text"] == correct_option:
                        button.config(bg="green")  # Highlight correct answer
                    elif button["text"] == selected_option:
                        button.config(bg="red")  # Highlight incorrect answer

            self.root.after(
                1000, show_next_question
            )  # Move to the next question after 1 second

        # Create quiz UI elements
        self.quiz_label = tk.Label(
            self.quiz_window, text="", font=("Arial", 16), bg="white"
        )
        self.quiz_label.pack(expand=True, fill=tk.BOTH, pady=20)

        self.option_buttons = []
        for _ in range(4):
            button = tk.Button(self.quiz_window, text="", font=("Arial", 14))
            button.pack(fill=tk.X, padx=20, pady=10)
            self.option_buttons.append(button)

        # Start the quiz with the first question
        show_next_question()


if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.geometry("500x700")
    root.mainloop()
