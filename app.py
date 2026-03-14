import random
import streamlit as st
from logic_utils import DIFFICULTY_SETTINGS, check_guess, get_range_for_difficulty, parse_guess, update_score

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

if "difficulty" not in st.session_state:
    st.session_state.difficulty = "Normal"

if "prev_difficulty" not in st.session_state:
    st.session_state.prev_difficulty = st.session_state.difficulty

difficulty = st.sidebar.selectbox(
    "Difficulty",
    list(DIFFICULTY_SETTINGS.keys()),
    key="difficulty",
)

attempt_limit = DIFFICULTY_SETTINGS[difficulty]["attempts"]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "input_nonce" not in st.session_state:
    st.session_state.input_nonce = 0


def reset_game_state(range_low: int, range_high: int):
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(range_low, range_high)
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.input_nonce += 1


if st.session_state.prev_difficulty != difficulty:
    reset_game_state(low, high)
    st.session_state.prev_difficulty = difficulty
    st.success("Difficulty changed. New game started.")
    st.rerun()

st.subheader("Make a guess")

info_slot = st.empty()
debug_slot = st.empty()


def render_state_panels():
    with info_slot.container():
        st.info(
            f"Guess a number between {low} and {high}. "
            f"Attempts left: {attempt_limit - st.session_state.attempts}"
        )

    with debug_slot.container():
        with st.expander("Developer Debug Info"):
            st.write("Secret:", st.session_state.secret)
            st.write("Attempts:", st.session_state.attempts)
            st.write("Score:", st.session_state.score)
            st.write("Difficulty:", difficulty)
            st.write("History:", st.session_state.history)


render_state_panels()

guess_input_key = f"guess_input_{difficulty}_{st.session_state.input_nonce}"
with st.form(key="guess_form", clear_on_submit=True):
    raw_guess = st.text_input(
        "Enter your guess:",
        key=guess_input_key
    )
    submit = st.form_submit_button("Submit Guess 🚀")

col1, col2, col3 = st.columns(3)
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    reset_game_state(low, high)
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.error(err)
    elif not low <= guess_int <= high:
        st.error(f"Enter a number between {low} and {high}.")
    else:
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        outcome, message = check_guess(guess_int, st.session_state.secret)

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
            attempt_limit=attempt_limit,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Scoreboard: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Scoreboard: {st.session_state.score}"
                )

    # Refresh status panels after submit so attempts/history are not one click behind.
    render_state_panels()

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
