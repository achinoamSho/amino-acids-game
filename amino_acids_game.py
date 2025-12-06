from __future__ import annotations

import json
import random
from pathlib import Path

from amino_acids_logic import (
    Question,
    get_categories,
    make_direct_question,
    make_reverse_question,
)

STATS_FILE = Path("quiz_stats.json")

DEFAULT_STATS = {
    "total_games": 0,
    "total_questions": 0,
    "total_correct": 0,
    "best_accuracy": 0.0,   # fraction between 0 and 1
    "best_score": 0,
    "best_questions": 0,
}


def load_stats() -> dict:
    """Load quiz statistics from disk (JSON). If missing/corrupt, return defaults."""
    if not STATS_FILE.exists():
        return DEFAULT_STATS.copy()

    try:
        with STATS_FILE.open("r", encoding="utf-8") as f:
            stats = json.load(f)
    except (OSError, json.JSONDecodeError):
        return DEFAULT_STATS.copy()

    # Ensure all keys exist (in case we extend the schema later)
    for key, value in DEFAULT_STATS.items():
        stats.setdefault(key, value)

    return stats


def save_stats(stats: dict) -> None:
    """Save quiz statistics to disk (JSON)."""
    with STATS_FILE.open("w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)


def update_stats(stats: dict, score: int, num_questions: int) -> tuple[float, float]:
    """
    Update stats with the result of one game.

    Returns:
        (this_game_accuracy, overall_accuracy)
    """
    stats["total_games"] += 1
    stats["total_questions"] += num_questions
    stats["total_correct"] += score

    this_accuracy = score / num_questions if num_questions else 0.0
    overall_accuracy = (
        stats["total_correct"] / stats["total_questions"]
        if stats["total_questions"]
        else 0.0
    )

    # Update best run if this game has higher accuracy
    if this_accuracy > stats.get("best_accuracy", 0.0):
        stats["best_accuracy"] = this_accuracy
        stats["best_score"] = score
        stats["best_questions"] = num_questions

    return this_accuracy, overall_accuracy


def ask_mode_from_user() -> str:
    """
    Ask the user which game mode they want.

    Returns:
        "single"  - single category, direct questions (AA -> property)
        "mixed"   - mixed categories, direct questions
        "reverse" - mixed categories, reverse questions (property -> AA)
    """
    print("=== Choose game mode ===")
    print("1. Single category (amino acid → property)")
    print("2. Mixed categories (amino acid → property)")
    print("3. Reverse questions (property → amino acid)")

    while True:
        choice = input("Enter number (or 'q' to quit): ").strip().lower()
        if choice in ("q", "quit"):
            raise SystemExit("Goodbye!")

        if choice == "1":
            return "single"
        if choice == "2":
            return "mixed"
        if choice == "3":
            return "reverse"

        print("Invalid choice, please try again.")


def ask_category_from_user() -> str:
    """Ask the user which category they want to practice (for 'single' mode)."""
    categories = get_categories()
    print("\n=== Choose a category to practice ===")
    for i, cat in enumerate(categories, start=1):
        print(f"{i}. {cat}")

    while True:
        choice = input("Enter number (or 'q' to quit): ").strip().lower()
        if choice in ("q", "quit"):
            raise SystemExit("Goodbye!")

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(categories):
                return categories[idx]
        except ValueError:
            pass

        print("Invalid choice, please try again.")


def ask_num_questions() -> int:
    """Ask the user how many questions they want."""
    while True:
        raw = input(
            "How many questions would you like? "
            "(e.g. 5, 10, or 'q' to quit): "
        ).strip()
        if raw.lower() in ("q", "quit"):
            raise SystemExit("Goodbye!")

        try:
            n = int(raw)
            if n > 0:
                return n
        except ValueError:
            pass
        print("Please enter a positive integer.")


def play_round(question: Question) -> bool:
    """
    Play a single round using a Question object.

    Returns:
        True if the user answered correctly, False otherwise.
    """
    print("\n" + "-" * 60)
    print(question.prompt)
    print()

    # Numbered options: 1, 2, 3, ...
    for idx, option in enumerate(question.options, start=1):
        print(f"{idx}. {option}")

    # Let user answer by number only
    while True:
        ans = input("Your choice (enter a number, or 'q' to quit): ").strip()

        if not ans:
            print("Please enter a choice.")
            continue

        # quit option
        if ans.lower() in ("q", "quit"):
            raise SystemExit("Goodbye!")

        if ans.isdigit():
            num = int(ans)
            if 1 <= num <= len(question.options):
                chosen_index = num - 1
                break
            else:
                print("Number out of range, please try again.")
                continue

        print("Invalid input, please enter a number like 1, 2, or 3.")

    if chosen_index == question.correct_index:
        print("✅ Correct!")
        return True
    else:
        correct_option = question.options[question.correct_index]
        print(f"❌ Incorrect. The correct answer was: {correct_option}.")
        return False


def main() -> None:
    print("Welcome to the Amino Acid Classification Quiz!\n")

    # --- Load and show existing stats (file handling!) ---
    stats = load_stats()
    if stats["total_games"] > 0:
        overall_accuracy = (
            stats["total_correct"] / stats["total_questions"]
            if stats["total_questions"]
            else 0.0
        )
        print("=== Your overall stats so far ===")
        print(f"Games played:       {stats['total_games']}")
        print(f"Questions answered: {stats['total_questions']}")
        print(f"Overall accuracy:   {overall_accuracy * 100:.1f}%")
        if stats["best_questions"] > 0:
            print(
                f"Best run:           {stats['best_score']}/"
                f"{stats['best_questions']} "
                f"({stats['best_accuracy'] * 100:.1f}%)"
            )
        print()

    mode = ask_mode_from_user()

    fixed_category: str | None = None
    if mode == "single":
        fixed_category = ask_category_from_user()

    num_questions = ask_num_questions()

    print()
    print("=== Game settings ===")
    print(f"Mode: {mode}")
    if fixed_category is not None:
        print(f"Category: {fixed_category}")
    print(f"Number of questions: {num_questions}")
    print()

    score = 0
    rng = random.Random()

    for _ in range(num_questions):
        if mode in ("single", "mixed"):
            category_for_q = fixed_category if mode == "single" else None
            question = make_direct_question(category=category_for_q, rng=rng)
        elif mode == "reverse":
            question = make_reverse_question(category=None, rng=rng)
        else:
            raise ValueError(f"Unknown mode: {mode}")

        if play_round(question):
            score += 1

    print("\n" + "=" * 60)
    print(f"Game over! Your score: {score}/{num_questions}")

    # --- Update & save stats ---
    this_accuracy, overall_accuracy = update_stats(stats, score, num_questions)
    save_stats(stats)

    print(f"This game accuracy:  {this_accuracy * 100:.1f}%")
    print(f"Overall accuracy:    {overall_accuracy * 100:.1f}%")
    if stats["best_questions"] > 0:
        print(
            f"Best run so far:    {stats['best_score']}/"
            f"{stats['best_questions']} "
            f"({stats['best_accuracy'] * 100:.1f}%)"
        )

    if score == num_questions:
        print("Perfect! 🧬✨")
    elif score > num_questions / 2:
        print("Nice job, keep practicing!")
    else:
        print("Good effort! Try again to improve your score.")


if __name__ == "__main__":
    main()
