# 💭 Reflection: Game Glitch Investigator


## 1. What was broken when you started?

It is the game that user choose the difficulty of the game and base on that range of guess and attempts change. And user will guess number and game will give hint for next guess. 

When I play the game, following bugs detected:
-The Range and attempts are not same in sidebar and main game field
- The hints are given reversely
- attempts are starting from 1
- it accepts non-number guess as imput even it warns
- it accepts out of range numbers
- new game button is not refresh history
---

## 2. How did you use AI as a teammate?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

- I’m using Copilot to fix this game. While investigating the hint bug, it led me to discover another issue with how the code checks odd versus even attempts and how the user’s input is converted.
- the history map was not updated consistence with the attempt. And ai suggested move down the developer block. but after moving down, it behaves wrong. I had to ask with different prompt with the issue.
---

## 3. Debugging and testing your fixes


- I approve the suggested code after I review and the logic seams right. And rerun the app and test that feature on UI manually. If the it behaves supposedly, I assume it is fixed.
- Session state related bugs such as the developer block are tested mannually.
- I used the pytest for logic utils. It helped me generate test cases and I chnaged it until I understand how it works

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
Because app uses random number for secret and every time reload the app it changes the secret number.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
Session state is stored in server memory and survives reruns.
But if the browser creates a new connection or the app restarts, a new session is created and the previous session state is lost.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  Always check and brain storm the edge cases with the agents. Don't believe only one answer, ai cant debug deep logic error. Logic is always mine.
  I will always do test files in the future, usually I skip.
  Main logic and strategy is always on the developer and AI can't never decide it and cant rely on it.
