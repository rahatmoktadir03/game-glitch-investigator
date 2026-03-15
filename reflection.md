# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

When I first ran the app, it loaded and accepted guesses, but the gameplay feedback was inconsistent and confusing. The biggest bug was that high/low hints were flipped: when my guess was too high, the app told me to go higher, and vice versa. Another bug was that the app converted the secret number to a string on every even attempt, which caused wrong comparisons and made hints unreliable. I also saw state/range issues: the UI prompt was hard-coded to 1-100 even when difficulty changed, and starting a new game reset the secret using 1-100 instead of the selected difficulty range.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I used GitHub Copilot and Claude in chat-style prompts and code-edit mode to reason about bug causes and apply targeted fixes. One correct suggestion was to refactor game logic (`get_range_for_difficulty`, `parse_guess`, `check_guess`, `update_score`) into `logic_utils.py` so it could be tested separately from Streamlit UI state. I verified that suggestion by running `pytest` and confirming all logic tests passed after the refactor. One misleading AI-style approach I considered was accepting decimal input by converting `12.5` to `12`; this looked convenient but would silently change player intent and produce surprising behavior. I verified that concern by adding a test and then enforcing whole-number input with an explicit validation error.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I treated each fix as done only after both code inspection and tests matched the intended behavior. For automated verification, I ran `pytest` and added focused regression tests for high/low hint direction, decimal input rejection, non-numeric input handling, and score consistency for wrong guesses. I also manually verified Streamlit state behavior by checking the new-game reset path and confirming difficulty-aware range handling in the UI text and secret generation. AI helped me design targeted tests by turning each observed glitch into a single, explicit expected outcome.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Streamlit reruns the script from top to bottom on most interactions (button clicks, inputs, checkboxes). That means normal variables are recalculated each run, so persistent game values must be stored in `st.session_state`. I learned to initialize state keys once, then update them intentionally only when user actions occur (for example, incrementing attempts only for valid guesses). I would explain it as: your script is like a function that re-executes often, and `session_state` is the memory that survives between those executions.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

One habit I want to keep is writing small regression tests immediately after finding a bug so fixes stay locked in. Next time, I would ask AI to propose multiple alternatives first, then choose the smallest change set before applying edits, instead of accepting the first plausible suggestion. This project changed how I view AI-generated code: it is fast for scaffolding, but I should assume it can contain subtle logic and state bugs. I now trust tests and explicit validation over "looks correct" code.
