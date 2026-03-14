DIFFICULTY_SETTINGS = {
    "Easy": {"range": (1, 20), "attempts": 7},
    "Normal": {"range": (1, 50), "attempts": 6},
    "Hard": {"range": (1, 100), "attempts": 6},
}


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    settings = DIFFICULTY_SETTINGS.get(difficulty, DIFFICULTY_SETTINGS["Normal"])
    return settings["range"]


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    raw = raw.strip()

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            return False, None, "Enter a whole number."

        value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int, attempt_limit: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        base_win = 50
        attempts_left = max(0, attempt_limit - attempt_number)
        win_bonus = attempts_left * 10
        return current_score + base_win + win_bonus

    penalty = 5
    if attempt_number > attempt_limit // 2:
        penalty = 8

    return max(0, current_score - penalty)
