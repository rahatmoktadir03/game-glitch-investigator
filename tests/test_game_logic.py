from logic_utils import check_guess, parse_guess, update_score

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message


def test_parse_guess_rejects_decimal_input():
    ok, value, error = parse_guess("12.5")
    assert ok is False
    assert value is None
    assert error == "Please enter a whole number."


def test_parse_guess_rejects_non_numeric_input():
    ok, value, error = parse_guess("abc")
    assert ok is False
    assert value is None
    assert error == "That is not a number."


def test_parse_guess_accepts_large_integer():
    ok, value, error = parse_guess("999999")
    assert ok is True
    assert value == 999999
    assert error is None


def test_score_penalizes_incorrect_guesses_consistently():
    score_after_high = update_score(10, "Too High", 1)
    score_after_low = update_score(10, "Too Low", 1)
    assert score_after_high == 5
    assert score_after_low == 5
