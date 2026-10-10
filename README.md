# 🔐 Password Strength Checker
A beginner Cybersecurity Mini Project written in Python.

---

## How to Run

```
python password_checker.py
```

---

## What It Does — Step by Step

| Step | What happens |
|------|-------------|
| 1 | You type a password |
| 2 | The program checks its **length** (good if ≥ 8 characters) |
| 3 | It checks for **uppercase** letters (A–Z) |
| 4 | It checks for **lowercase** letters (a–z) |
| 5 | It checks for **digits** (0–9) |
| 6 | It checks for **special characters** (!, @, #, $ …) |
| 7 | It shows a clear report and an overall strength label |

---

## Strength Labels

| Label    | Meaning                              |
|----------|--------------------------------------|
| Strong   | All 5 checks passed                  |
| Moderate | 3 or 4 checks passed                 |
| Weak     | Fewer than 3 checks passed           |

---

## Example Output

```
Welcome to the Password Strength Checker!
------------------------------------------
Enter a password to check: Hello@123

=============================================
       PASSWORD STRENGTH CHECKER RESULTS
=============================================
  Password entered  : Hello@123
  Length            : 9 characters  ✓ Yes (min 8)
  Uppercase letter  : ✓ Yes
  Lowercase letter  : ✓ Yes
  Digit (0-9)       : ✓ Yes
  Special character : ✓ Yes
---------------------------------------------
  Overall Strength  : Strong 💪
=============================================
```

---

## Project Structure

```
password_strength_checker/
├── password_checker.py   ← main program
└── README.md             ← this file
```

---

## What You Will Learn
- Using Python's built-in **`re` module** for pattern matching
- Writing **functions** to organise code
- Using **`if __name__ == "__main__"`** — the standard Python entry point
