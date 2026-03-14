from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score


def test_get_range_for_easy():
    assert get_range_for_difficulty("Easy") == (1, 20)


def test_get_range_for_normal():
    assert get_range_for_difficulty("Normal") == (1, 50)


def test_get_range_for_hard():
    assert get_range_for_difficulty("Hard") == (1, 100)


def test_get_range_defaults_to_normal_for_unknown_difficulty():
    assert get_range_for_difficulty("Impossible") == (1, 50)


def test_parse_guess_rejects_none():
    assert parse_guess(None) == (False, None, "Enter a guess.")


def test_parse_guess_rejects_blank_input():
    assert parse_guess("   ") == (False, None, "Enter a guess.")


def test_parse_guess_rejects_decimal_input():
    assert parse_guess("12.5") == (False, None, "Enter a whole number.")


def test_parse_guess_rejects_non_numeric_input():
    assert parse_guess("hello") == (False, None, "That is not a number.")


def test_parse_guess_accepts_integer_input():
    assert parse_guess("42") == (True, 42, None)


def test_check_guess_returns_win_and_message():
    assert check_guess(50, 50) == ("Win", "🎉 Correct!")


def test_check_guess_returns_too_high_and_message():
    assert check_guess(60, 50) == ("Too High", "📉 Go LOWER!")


def test_check_guess_returns_too_low_and_message():
    assert check_guess(40, 50) == ("Too Low", "📈 Go HIGHER!")


def test_update_score_rewards_early_win():
    assert update_score(10, "Win", attempt_number=2, attempt_limit=6) == 100


def test_update_score_applies_early_miss_penalty():
    assert update_score(20, "Too Low", attempt_number=2, attempt_limit=6) == 15


def test_update_score_applies_late_miss_penalty():
    assert update_score(20, "Too High", attempt_number=4, attempt_limit=6) == 12


def test_update_score_never_goes_below_zero():
    assert update_score(3, "Too High", attempt_number=6, attempt_limit=6) == 0
