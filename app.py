import random
import streamlit as st
import pandas as pd
from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)

# CHALLENGE 4: Enhanced UI helpers for hot/cold feedback and visual progress
def calculate_distance(guess, secret):
    """Calculate how far the guess is from the secret (0-100 scale)."""
    if guess == secret:
        return 0
    # Return a percentage: closer to 0 = closer to secret, 100 = very far
    max_distance = max(abs(secret - 1), abs(secret - 200))
    distance = abs(guess - secret)
    return min(100, int((distance / max(max_distance, 1)) * 100))


def get_temperature_emoji(distance):
    """Return a temperature emoji based on how close the guess is."""
    if distance == 0:
        return "🔥 PERFECT!"
    elif distance <= 5:
        return "🌡️ SCORCHING"
    elif distance <= 15:
        return "🔥 HOT"
    elif distance <= 30:
        return "🌤️ WARM"
    elif distance <= 50:
        return "❄️ COOL"
    else:
        return "🧊 FREEZING"

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

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

st.subheader("Make a guess")

# FIXME: This was hard-coded to 1-100 and showed incorrect attempts left.
# FIX: Keep the prompt tied to the selected difficulty and current state.
st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    # FIXME: New game always reset secret to 1..100 and kept stale state.
    # FIX: Reset all game state and respect current difficulty range.
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.secret = random.randint(low, high)
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
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        if guess_int < low or guess_int > high:
            st.session_state.history.append(guess_int)
            st.error(f"Guess must be between {low} and {high}.")
            st.stop()

        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        # FIXME: Secret was cast to string every other attempt, causing bad comparisons.
        # FIX: Always compare numeric guess to numeric secret in shared logic.
        outcome, message = check_guess(guess_int, st.session_state.secret)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        # Enhanced feedback display
        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            # CHALLENGE 4: Prominent win feedback
            st.success(
                f"🏆 **YOU WIN!** 🏆\n\n"
                f"The secret was **{st.session_state.secret}**.\n\n"
                f"**Attempts:** {st.session_state.attempts} / {attempt_limit}\n\n"
                f"**Final Score:** {st.session_state.score} points"
            )
        else:
            # CHALLENGE 4: Color-coded feedback based on outcome
            distance = calculate_distance(guess_int, st.session_state.secret)
            temp_emoji = get_temperature_emoji(distance)
            
            if outcome == "Too High":
                st.error(f"❌ Too High! {temp_emoji}")
            else:  # Too Low
                st.error(f"❌ Too Low! {temp_emoji}")
            
            # Display hot/cold meter
            st.write(f"**Distance:** {distance}% away")
            st.progress(1 - (distance / 100), text=f"Getting warmer!" if distance < 50 else "Still looking...")
            
            if show_hint:
                st.info(message)

            # CHALLENGE 4: Guess history table
            if st.session_state.history:
                st.divider()
                st.subheader("📊 Guess History")
                
                history_data = []
                for i, guess in enumerate(st.session_state.history):
                    if isinstance(guess, int):
                        outcome_type, _ = check_guess(guess, st.session_state.secret)
                        distance = calculate_distance(guess, st.session_state.secret)
                        history_data.append({
                            "Attempt": i + 1,
                            "Guess": guess,
                            "Feedback": outcome_type,
                            "Temperature": get_temperature_emoji(distance),
                            "Distance": distance
                        })
                
                if history_data:
                    df = pd.DataFrame(history_data)
                    st.dataframe(df, use_container_width=True, hide_index=True)
            
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"💀 **GAME OVER!** 💀\n\n"
                    f"The secret was **{st.session_state.secret}**.\n\n"
                    f"**Attempts Used:** {st.session_state.attempts} / {attempt_limit}\n\n"
                    f"**Final Score:** {st.session_state.score} points"
                )

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
