from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox
import random

from amino_acids_logic import (
    Question,
    get_categories,
    make_direct_question,
    make_reverse_question,
)


class AminoAcidQuizApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.title("Amino Acid Classification Quiz (GUI)")
        self.geometry("700x400")

        # State
        self.mode_var = tk.StringVar(value="mixed")  # single / mixed / reverse
        self.category_var = tk.StringVar(value=get_categories()[0])
        self.current_question: Question | None = None
        self.score_correct = 0
        self.score_total = 0
        self.streak = 0
        self.rng = random.Random()

        # Build UI
        self._build_controls()
        self._build_question_area()
        self._build_status_bar()

    # ---------- UI layout ----------

    def _build_controls(self) -> None:
        """Top frame: mode selection and category selection."""
        controls = ttk.Frame(self)
        controls.pack(fill="x", padx=10, pady=10)

        # Mode selection
        ttk.Label(controls, text="Mode:").pack(side="left", padx=(0, 5))

        ttk.Radiobutton(
            controls,
            text="Single category",
            variable=self.mode_var,
            value="single",
            command=self._on_mode_change,
        ).pack(side="left")

        ttk.Radiobutton(
            controls,
            text="Mixed categories",
            variable=self.mode_var,
            value="mixed",
            command=self._on_mode_change,
        ).pack(side="left", padx=(5, 0))

        ttk.Radiobutton(
            controls,
            text="Reverse (property → AA)",
            variable=self.mode_var,
            value="reverse",
            command=self._on_mode_change,
        ).pack(side="left", padx=(5, 0))

        # Spacer
        ttk.Label(controls, text="   ").pack(side="left")

        # Category dropdown (only used in "single" mode)
        ttk.Label(controls, text="Category:").pack(side="left", padx=(0, 5))
        self.category_menu = ttk.Combobox(
            controls,
            textvariable=self.category_var,
            values=get_categories(),
            state="readonly",
            width=15,
        )
        self.category_menu.pack(side="left")

        # New question button
        ttk.Button(
            controls,
            text="New question",
            command=self.new_question,
        ).pack(side="right")

        self._on_mode_change()  # initialize enabled/disabled states

    def _build_question_area(self) -> None:
        """Middle frame: question text + options."""
        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.question_label = ttk.Label(
            frame,
            text="Click 'New question' to start.",
            wraplength=650,
            justify="left",
            font=("TkDefaultFont", 12, "bold"),
        )
        self.question_label.pack(anchor="w", pady=(0, 10))

        self.options_frame = ttk.Frame(frame)
        self.options_frame.pack(anchor="w")

        # Feedback label
        self.feedback_label = ttk.Label(
            frame,
            text="",
            foreground="blue",
            wraplength=650,
            justify="left",
        )
        self.feedback_label.pack(anchor="w", pady=(10, 0))

    def _build_status_bar(self) -> None:
        """Bottom frame: score, streak."""
        status = ttk.Frame(self, relief="groove")
        status.pack(fill="x", side="bottom")

        self.score_label = ttk.Label(status, text="Score: 0 / 0")
        self.score_label.pack(side="left", padx=10, pady=5)

        self.streak_label = ttk.Label(status, text="Streak: 0")
        self.streak_label.pack(side="left", padx=10)

    # ---------- Event handlers ----------

    def _on_mode_change(self) -> None:
        """Enable/disable category dropdown depending on mode."""
        mode = self.mode_var.get()
        if mode == "single":
            self.category_menu.configure(state="readonly")
        else:
            self.category_menu.configure(state="disabled")

    def new_question(self) -> None:
        """Generate and display a new question based on the selected mode."""
        mode = self.mode_var.get()

        if mode in ("single", "mixed"):
            category = self.category_var.get() if mode == "single" else None
            self.current_question = make_direct_question(
                category=category,
                rng=self.rng,
            )
        elif mode == "reverse":
            self.current_question = make_reverse_question(
                category=None,
                rng=self.rng,
            )
        else:
            messagebox.showerror("Error", f"Unknown mode: {mode}")
            return

        self._display_question(self.current_question)

    def _display_question(self, question: Question) -> None:
        """Render the question text and answer buttons."""
        self.question_label.configure(text=question.prompt)
        self.feedback_label.configure(text="")

        # Clear old option buttons
        for child in self.options_frame.winfo_children():
            child.destroy()

        # Create numbered buttons: 1., 2., ...
        for idx, option in enumerate(question.options, start=1):
            btn = ttk.Button(
                self.options_frame,
                text=f"{idx}. {option}",
                command=lambda i=idx - 1: self._on_answer(i),
            )
            btn.pack(anchor="w", pady=2)

    def _on_answer(self, chosen_index: int) -> None:
        """Handle the user's answer click."""
        if self.current_question is None:
            return

        self.score_total += 1

        if chosen_index == self.current_question.correct_index:
            self.score_correct += 1
            self.streak += 1
            self.feedback_label.configure(text="✅ Correct!", foreground="green")
        else:
            self.streak = 0
            correct_option = self.current_question.options[self.current_question.correct_index]
            self.feedback_label.configure(
                text=f"❌ Incorrect. The correct answer was: {correct_option}.",
                foreground="red",
            )

        self._update_status()

    def _update_status(self) -> None:
        """Update score & streak labels."""
        self.score_label.configure(text=f"Score: {self.score_correct} / {self.score_total}")
        self.streak_label.configure(text=f"Streak: {self.streak}")


if __name__ == "__main__":
    app = AminoAcidQuizApp()
    app.mainloop()
