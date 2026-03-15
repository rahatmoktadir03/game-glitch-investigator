def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    ranges = {
        "Easy": (1, 20),
        "Normal": (1, 100),
        "Hard": (1, 200),
    }
    return ranges.get(difficulty, (1, 100))


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    cleaned = raw.strip()
    if cleaned == "":
        return False, None, "Enter a guess."

    # Reject decimals so a guess like 12.9 is not silently converted to 12.
    if "." in cleaned:
        return False, None, "Please enter a whole number."

    try:
        value = int(cleaned)
    except ValueError:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    guess_int = int(guess)
    secret_int = int(secret)

    if guess_int == secret_int:
        return "Win", "🎉 Correct!"

    if guess_int > secret_int:
        return "Too High", "📉 Too high. Go LOWER!"

    return "Too Low", "📈 Too low. Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        # attempt_number is 1-based, so first-try win should be worth 100.
        points = 100 - 10 * (attempt_number - 1)
        return current_score + max(points, 10)

    if outcome in {"Too High", "Too Low"}:
        return current_score - 5

    return current_score
