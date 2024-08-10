import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import os

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flashcard App")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        self.flashcards = []
        self.current_index = -1
        
        self.load_flashcards()
        
        self.create_widgets()
        self.show_flashcard()

    def create_widgets(self):
        # Frame untuk Kontrol
        control_frame = tk.Frame(self.root, bg='#ffffff', bd=2, relief=tk.RAISED)
        control_frame.pack(pady=10, padx=20, fill=tk.X)

        # Frame untuk Display
        display_frame = tk.Frame(self.root, bg='#ffffff', bd=2, relief=tk.RAISED)
        display_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        # Flashcard Display
        self.flashcard_label = tk.Label(display_frame, text="", font=("Arial", 18), wraplength=750, bg='#ffffff', pady=20)
        self.flashcard_label.pack(padx=10, pady=10)

        # Buttons
        self.show_answer_button = tk.Button(control_frame, text="Show Answer", font=("Arial", 14), command=self.show_answer, bg='#4CAF50', fg='white', padx=10, pady=5)
        self.show_answer_button.pack(side=tk.LEFT, padx=10)

        self.next_button = tk.Button(control_frame, text="Next", font=("Arial", 14), command=self.next_flashcard, bg='#2196F3', fg='white', padx=10, pady=5)
        self.next_button.pack(side=tk.LEFT, padx=10)

        self.add_flashcard_button = tk.Button(control_frame, text="Add Flashcard", font=("Arial", 14), command=self.add_flashcard, bg='#FF5722', fg='white', padx=10, pady=5)
        self.add_flashcard_button.pack(side=tk.LEFT, padx=10)

        # New Buttons for Edit and Delete
        self.edit_flashcard_button = tk.Button(control_frame, text="Edit Flashcard", font=("Arial", 14), command=self.edit_flashcard, bg='#FFC107', fg='white', padx=10, pady=5)
        self.edit_flashcard_button.pack(side=tk.LEFT, padx=10)

        self.delete_flashcard_button = tk.Button(control_frame, text="Delete Flashcard", font=("Arial", 14), command=self.delete_flashcard, bg='#F44336', fg='white', padx=10, pady=5)
        self.delete_flashcard_button.pack(side=tk.LEFT, padx=10)

        # Footer
        footer_frame = tk.Frame(self.root, bg='#ffffff', bd=2, relief=tk.RAISED)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.footer_label = tk.Label(footer_frame, text="Flashcard App by Alpian", font=("Arial", 12), bg='#ffffff')
        self.footer_label.pack(pady=10)

    def load_flashcards(self):
        if os.path.exists("flashcards.json"):
            with open("flashcards.json", "r") as file:
                self.flashcards = json.load(file)

    def save_flashcards(self):
        with open("flashcards.json", "w") as file:
            json.dump(self.flashcards, file, indent=4)

    def show_flashcard(self):
        if self.flashcards:
            self.current_index = (self.current_index + 1) % len(self.flashcards)
            flashcard = self.flashcards[self.current_index]
            self.flashcard_label.config(text=flashcard["question"])
            self.show_answer_button.config(state=tk.NORMAL)
        else:
            self.flashcard_label.config(text="No flashcards available.")
            self.show_answer_button.config(state=tk.DISABLED)
            self.edit_flashcard_button.config(state=tk.DISABLED)
            self.delete_flashcard_button.config(state=tk.DISABLED)

    def show_answer(self):
        if self.flashcards:
            flashcard = self.flashcards[self.current_index]
            self.flashcard_label.config(text=flashcard["answer"])
            self.show_answer_button.config(state=tk.DISABLED)
            self.edit_flashcard_button.config(state=tk.NORMAL)
            self.delete_flashcard_button.config(state=tk.NORMAL)

    def next_flashcard(self):
        self.show_flashcard()

    def add_flashcard(self):
        question = simpledialog.askstring("Input", "Enter the question:")
        if question:
            answer = simpledialog.askstring("Input", "Enter the answer:")
            if answer:
                self.flashcards.append({"question": question, "answer": answer})
                self.save_flashcards()
                self.show_flashcard()
            else:
                messagebox.showwarning("Input Error", "Answer cannot be empty.")
        else:
            messagebox.showwarning("Input Error", "Question cannot be empty.")

    def edit_flashcard(self):
        if not self.flashcards:
            return

        flashcard = self.flashcards[self.current_index]
        new_question = simpledialog.askstring("Edit", "Edit the question:", initialvalue=flashcard["question"])
        if new_question:
            new_answer = simpledialog.askstring("Edit", "Edit the answer:", initialvalue=flashcard["answer"])
            if new_answer:
                self.flashcards[self.current_index] = {"question": new_question, "answer": new_answer}
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
            del self.flashcards[self.current_index]
            if self.flashcards:
                self.current_index = self.current_index % len(self.flashcards)
            else:
                self.current_index = -1
            self.save_flashcards()
            self.show_flashcard()

if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()
