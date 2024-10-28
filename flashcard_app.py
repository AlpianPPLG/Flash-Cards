import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import os
import random

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flashcard App")
        self.root.geometry("800x600")
        
        self.flashcards = []
        self.current_index = -1
        self.review_mode = False
        self.dark_mode = False

        self.load_flashcards()
        
        self.create_widgets()
        self.show_flashcard()

    def create_widgets(self):
        # Frame untuk Kontrol
        self.control_frame = tk.Frame(self.root, bd=2, relief=tk.RAISED)
        self.control_frame.pack(pady=10, padx=20, fill=tk.X)

        # Frame untuk Display
        self.display_frame = tk.Frame(self.root, bd=2, relief=tk.RAISED)
        self.display_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        # Flashcard Display
        self.flashcard_label = tk.Label(self.display_frame, text="", font=("Arial", 18), wraplength=750, pady=20)
        self.flashcard_label.pack(padx=10, pady=10)

        # Buttons
        self.show_answer_button = tk.Button(self.control_frame, text="Show Answer", font=("Arial", 14), command=self.show_answer, padx=10, pady=5)
        self.show_answer_button.pack(side=tk.LEFT, padx=10)

        self.next_button = tk.Button(self.control_frame, text="Next", font=("Arial", 14), command=self.next_flashcard, padx=10, pady=5)
        self.next_button.pack(side=tk.LEFT, padx=10)

        self.add_flashcard_button = tk.Button(self.control_frame, text="Add Flashcard", font=("Arial", 14), command=self.add_flashcard, padx=10, pady=5)
        self.add_flashcard_button.pack(side=tk.LEFT, padx=10)

        self.edit_flashcard_button = tk.Button(self.control_frame, text="Edit", font=("Arial", 14), command=self.edit_flashcard, padx=10, pady=5)
        self.edit_flashcard_button.pack(side=tk.LEFT, padx=10)

        self.delete_flashcard_button = tk.Button(self.control_frame, text="Delete", font=("Arial", 14), command=self.delete_flashcard, padx=10, pady=5)
        self.delete_flashcard_button.pack(side=tk.LEFT, padx=10)

        self.mark_review_button = tk.Button(self.control_frame, text="Mark for Review", font=("Arial", 14), command=self.mark_for_review, padx=10, pady=5)
        self.mark_review_button.pack(side=tk.LEFT, padx=10)

        self.review_mode_button = tk.Button(self.control_frame, text="Review Mode", font=("Arial", 14), command=self.toggle_review_mode, padx=10, pady=5)
        self.review_mode_button.pack(side=tk.LEFT, padx=10)

        self.dark_mode_button = tk.Button(self.control_frame, text="Dark Mode", font=("Arial", 14), command=self.toggle_dark_mode, padx=10, pady=5)
        self.dark_mode_button.pack(side=tk.LEFT, padx=10)

        self.sort_button = tk.Button(self.control_frame, text="Sort A-Z", font=("Arial", 14), command=self.sort_flashcards, padx=10, pady=5)
        self.sort_button.pack(side=tk.LEFT, padx=10)

        # Tombol Keluar
        self.exit_button = tk.Button(self.control_frame, text="Exit", font=("Arial", 14), command=self.confirm_exit, padx=10, pady=5)
        self.exit_button.pack(side=tk.RIGHT, padx=10)

        # Footer
        self.footer_label = tk.Label(self.root, text="Flashcard App by Alpian", font=("Arial", 12))
        self.footer_label.pack(side=tk.BOTTOM, pady=10)
        
        self.update_theme()

    def confirm_exit(self):
        confirm = messagebox.askyesno("Exit Confirmation", "Are you sure you want to exit?")
        if confirm:
            self.root.quit()

    def load_flashcards(self):
        if os.path.exists("flashcards.json"):
            with open("flashcards.json", "r") as file:
                self.flashcards = json.load(file)

    def save_flashcards(self):
        with open("flashcards.json", "w") as file:
            json.dump(self.flashcards, file, indent=4)

    def show_flashcard(self):
        if self.flashcards:
            if self.review_mode:
                review_cards = [fc for fc in self.flashcards if fc.get("review", False)]
                if not review_cards:
                    self.flashcard_label.config(text="No flashcards marked for review.")
                    return
                flashcard = review_cards[self.current_index % len(review_cards)]
            else:
                flashcard = self.flashcards[self.current_index % len(self.flashcards)]
            self.flashcard_label.config(text=flashcard["question"])
            self.show_answer_button.config(state=tk.NORMAL)
            self.update_mark_review_button(flashcard)
        else:
            self.flashcard_label.config(text="No flashcards available.")
            self.show_answer_button.config(state=tk.DISABLED)
            self.edit_flashcard_button.config(state=tk.DISABLED)
            self.delete_flashcard_button.config(state=tk.DISABLED)

    def show_answer(self):
        if self.flashcards:
            if self.review_mode:
                review_cards = [fc for fc in self.flashcards if fc.get("review", False)]
                flashcard = review_cards[self.current_index % len(review_cards)]
            else:
                flashcard = self.flashcards[self.current_index % len(self.flashcards)]
            self.flashcard_label.config(text=flashcard["answer"])
            self.show_answer_button.config(state=tk.DISABLED)

    def next_flashcard(self):
        self.current_index += 1
        self.show_flashcard()

    def add_flashcard(self):
        question = simpledialog.askstring("Input", "Enter the question:")
        if question:
            answer = simpledialog.askstring("Input", "Enter the answer:")
            if answer:
                self.flashcards.append({"question": question, "answer": answer, "review": False})
                self.save_flashcards()
                self.show_flashcard()
            else:
                messagebox.showwarning("Input Error", "Answer cannot be empty.")
        else:
            messagebox.showwarning("Input Error", "Question cannot be empty.")

    def edit_flashcard(self):
        if not self.flashcards:
            return

        flashcard = self.flashcards[self.current_index % len(self.flashcards)]
        new_question = simpledialog.askstring("Edit", "Edit the question:", initialvalue=flashcard["question"])
        if new_question:
            new_answer = simpledialog.askstring("Edit", "Edit the answer:", initialvalue=flashcard["answer"])
            if new_answer:
                flashcard["question"] = new_question
                flashcard["answer"] = new_answer
                self.save_flashcards()
                self.show_flashcard()
            else:
                messagebox.showwarning("Input Error", "Answer cannot be empty.")
        else:
            messagebox.showwarning("Input Error", "Question cannot be empty.")

    def delete_flashcard(self):
        if not self.flashcards:
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this flashcard?")
        if confirm:
            del self.flashcards[self.current_index % len(self.flashcards)]
            self.current_index -= 1
            self.save_flashcards()
            self.show_flashcard()

    def mark_for_review(self):
        if not self.flashcards:
            return

        flashcard = self.flashcards[self.current_index % len(self.flashcards)]
        flashcard["review"] = not flashcard.get("review", False)
        self.update_mark_review_button(flashcard)
        self.save_flashcards()

    def update_mark_review_button(self, flashcard):
        if flashcard.get("review", False):
            self.mark_review_button.config(text="Unmark Review")
        else:
            self.mark_review_button.config(text="Mark for Review")

    def toggle_review_mode(self):
        self.review_mode = not self.review_mode
        self.review_mode_button.config(text="Review Mode On" if self.review_mode else "Review Mode Off")
        self.current_index = 0
        self.show_flashcard()

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        self.update_theme()

    def update_theme(self):
        bg_color = "#333" if self.dark_mode else "#f0f0f0"
        fg_color = "#fff" if self.dark_mode else "#000"
        self.root.configure(bg=bg_color)
        self.control_frame.configure(bg=bg_color)
        self.display_frame.configure(bg=bg_color)
        self.flashcard_label.configure(bg=bg_color, fg=fg_color)
        self.footer_label.configure(bg=bg_color, fg=fg_color)

    def sort_flashcards(self):
        self.flashcards.sort(key=lambda x: x["question"])
        self.current_index = 0
        self.show_flashcard()

if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()
