from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any


AMINO_ACIDS = {
    "A": {
        "name": "Alanine",
        "charge": "neutral",
        "polarity": "nonpolar",
        "aromatic": "non-aromatic",
        "hydrophobicity": "hydrophobic",
    },
    "R": {
        "name": "Arginine",
        "charge": "positive",
        "polarity": "polar",
        "aromatic": "non-aromatic",
        "hydrophobicity": "hydrophilic",
    },
    "N": {
        "name": "Asparagine",
        "charge": "neutral",
        "polarity": "polar",
        "aromatic": "non-aromatic",
        "hydrophobicity": "hydrophilic",
    },
    "D": {
        "name": "Aspartate",
        "charge": "negative",
        "polarity": "polar",
        "aromatic": "non-aromatic",
        "hydrophobicity": "hydrophilic",
    },
    "C": {
        "name": "Cysteine",
        "charge": "neutral",
        "polarity": "polar",
        "aromatic": "non-aromatic",
        "hydrophobicity": "hydrophobic",
    },
    "E": {
        "name": "Glutamate",
        "charge": "negative",
        "polarity": "polar",
        "aromatic": "non-aromatic",
        "hydrophobicity": "hydrophilic",
    },
    "Q": {
        "name": "Glutamine",
        "charge": "neutral",
        "polarity": "polar",
        "aromatic": "non-aromatic",
        "hydrophobicity": "hydrophilic",
    },
    "G": {
        "name": "Glycine",
        "charge": "neutral",
        "polarity": "nonpolar",
        "aromatic": "non-aromatic",
        "hydrophobicity": "hydrophilic",
    },
    "H": {
        "name": "Histidine",
        "charge": "positive",
        "polarity": "polar",
        "aromatic": "non-aromatic",
        "hydrophobicity": "hydrophilic",
    },
    "I": {
        "name": "Isoleucine",
        "charge": "neutral",
        "polarity": "nonpolar",
        "aromatic": "non-aromatic",
        "hydrophobicity": "hydrophobic",
    },
    "L": {
        "name": "Leucine",
        "charge": "neutral",
        "polarity": "nonpolar",
        "aromatic": "non-aromatic",
        "hydrophobicity": "hydrophobic",
    },
    "K": {
        "name": "Lysine",
        "charge": "positive",
        "polarity": "polar",
        "aromatic": "non-aromatic",
        "hydrophobicity": "hydrophilic",
    },
    "M": {
        "name": "Methionine",
        "charge": "neutral",
        "polarity": "nonpolar",
        "aromatic": "non-aromatic",
        "hydrophobicity": "hydrophobic",
    },
    "F": {
        "name": "Phenylalanine",
        "charge": "neutral",
        "polarity": "nonpolar",
        "aromatic": "aromatic",
        "hydrophobicity": "hydrophobic",
    },
    "P": {
        "name": "Proline",
        "charge": "neutral",
        "polarity": "nonpolar",
        "aromatic": "non-aromatic",
        "hydrophobicity": "hydrophilic",
    },
    "S": {
        "name": "Serine",
        "charge": "neutral",
        "polarity": "polar",
        "aromatic": "non-aromatic",
        "hydrophobicity": "hydrophilic",
    },
    "T": {
        "name": "Threonine",
        "charge": "neutral",
        "polarity": "polar",
        "aromatic": "non-aromatic",
        "hydrophobicity": "hydrophilic",
    },
    "W": {
        "name": "Tryptophan",
        "charge": "neutral",
        "polarity": "nonpolar",
        "aromatic": "aromatic",
        "hydrophobicity": "hydrophobic",
    },
    "Y": {
        "name": "Tyrosine",
        "charge": "neutral",
        "polarity": "polar",
        "aromatic": "aromatic",
        "hydrophobicity": "hydrophobic",
    },
    "V": {
        "name": "Valine",
        "charge": "neutral",
        "polarity": "nonpolar",
        "aromatic": "non-aromatic",
        "hydrophobicity": "hydrophobic",
    },
}

CATEGORY_OPTIONS = {
    "charge": ["positive", "negative", "neutral"],
    "polarity": ["polar", "nonpolar"],
    "aromatic": ["aromatic", "non-aromatic"],
    "hydrophobicity": ["hydrophobic", "hydrophilic"],
}


@dataclass
class Question:
    """
    Represents a single quiz question (logic only).

    - mode: "direct" (AA → property) or "reverse" (property → AA)
    - category: e.g. "charge", "polarity"
    - prompt: text of the question
    - options: list of option strings (for multiple choice)
    - correct_index: index into options that is correct
    - metadata: extra info (e.g. amino acid code) if the UI wants it
    """
    mode: str
    category: str
    prompt: str
    options: list[str]
    correct_index: int
    metadata: dict[str, Any] = field(default_factory=dict)


def get_random_amino_acid(rng: random.Random | None = None) -> tuple[str, dict]:
    """Return a random (code, properties_dict) pair."""
    if rng is None:
        rng = random
    code = rng.choice(list(AMINO_ACIDS.keys()))
    return code, AMINO_ACIDS[code]


def get_property(code: str, category: str) -> str:
    """Return the property (e.g. 'positive') for a given amino acid and category."""
    code = code.upper()
    if code not in AMINO_ACIDS:
        raise ValueError(f"Unknown amino acid code: {code}")
    if category not in CATEGORY_OPTIONS:
        raise ValueError(f"Unknown category: {category}")
    return AMINO_ACIDS[code][category]


def check_answer(code: str, category: str, user_answer: str) -> bool:
    """
    Convenience function for text-mode:
    Return True if the user's answer matches the true property (case-insensitive).
    """
    correct = get_property(code, category)
    return user_answer.strip().lower() == correct.lower()


def get_categories() -> list[str]:
    """Return the list of available categories."""
    return list(CATEGORY_OPTIONS.keys())


def make_direct_question(
    category: str | None = None,
    rng: random.Random | None = None,
) -> Question:
    """
    Direct question: amino acid -> property.

    Example prompt:
      "What is the charge of Lysine (K)?"
    Options are the allowed values for that category.
    """
    if rng is None:
        rng = random

    categories = get_categories()
    if category is None:
        category = rng.choice(categories)

    code, props = get_random_amino_acid(rng)
    name = props["name"]
    correct_answer = props[category]
    options = CATEGORY_OPTIONS[category][:]  # copy

    correct_index = options.index(correct_answer)

    # More natural wording:
    # "What is the polarity of Lysine (K)?"
    prompt = f"What is the {category} of {name} ({code})?"

    return Question(
        mode="direct",
        category=category,
        prompt=prompt,
        options=options,
        correct_index=correct_index,
        metadata={"code": code, "name": name},
    )


def _format_reverse_prompt(category: str, value: str) -> str:
    """Return a human-friendly prompt for a reverse question."""
    if category == "charge":
        if value == "positive":
            return "Which amino acid is positively charged?"
        if value == "negative":
            return "Which amino acid is negatively charged?"
        if value == "neutral":
            return "Which amino acid is neutral (uncharged)?"

    if category == "polarity":
        if value == "polar":
            return "Which amino acid is polar?"
        if value == "nonpolar":
            return "Which amino acid is nonpolar?"

    if category == "aromatic":
        if value == "aromatic":
            return "Which amino acid is aromatic?"
        if value == "non-aromatic":
            return "Which amino acid is non-aromatic?"

    if category == "hydrophobicity":
        if value == "hydrophobic":
            return "Which amino acid is hydrophobic?"
        if value == "hydrophilic":
            return "Which amino acid is hydrophilic?"

    # Fallback (for future categories)
    return f"Which amino acid has {category} '{value}'?"


def make_reverse_question(
    category: str | None = None,
    rng: random.Random | None = None,
) -> Question:
    """
    Reverse question: property -> amino acid.

    Example prompt:
      "Which amino acid is positively charged?"

    Options are amino acid names (with codes), one correct and several distractors.
    """
    if rng is None:
        rng = random

    categories = get_categories()
    if category is None:
        category = rng.choice(categories)

    all_codes = list(AMINO_ACIDS.keys())

    # Choose a random amino acid and use its property as the target
    correct_code = rng.choice(all_codes)
    correct_props = AMINO_ACIDS[correct_code]
    property_value = correct_props[category]

    # Distractors: amino acids that do NOT share this property in this category
    distractor_codes = [
        c for c in all_codes
        if AMINO_ACIDS[c][category] != property_value
    ]

    # Take up to 3 distractors
    num_distractors = min(3, len(distractor_codes))
    chosen_distractors = rng.sample(distractor_codes, k=num_distractors)

    option_codes = [correct_code] + chosen_distractors
    rng.shuffle(option_codes)

    options = [f"{AMINO_ACIDS[c]['name']} ({c})" for c in option_codes]
    correct_index = option_codes.index(correct_code)

    prompt = _format_reverse_prompt(category, property_value)

    return Question(
        mode="reverse",
        category=category,
        prompt=prompt,
        options=options,
        correct_index=correct_index,
        metadata={
            "correct_code": correct_code,
            "property_value": property_value,
        },
    )
