# ============================================================
#  Password Strength Checker  (v2 — Scoring Edition)
#  Cybersecurity Mini Project
#  Uses Python's built-in 're' module for regular expressions
#
#  NOTE: Passwords are NEVER stored, printed to logs, or saved.
#        They are checked in memory and immediately discarded.
# ============================================================

import re  # Built-in module for pattern matching


# ------------------------------------------------------------------
# SCORING RULES
# ------------------------------------------------------------------
# Each rule that passes adds points to the total score.
# Maximum possible score = 6 points.
#
#   Rule                              Points
#   --------------------------------  ------
#   Length >= 8 characters              1
#   Length >= 12 characters             1   (bonus — rewards longer passwords)
#   Contains an uppercase letter        1
#   Contains a lowercase letter         1
#   Contains a digit (0-9)             1
#   Contains a special character        1
#
# Strength categories:
#   Score 0-2  ->  Weak
#   Score 3-4  ->  Medium
#   Score 5-6  ->  Strong
#
# HARD RULE: A password shorter than 8 characters is ALWAYS Weak,
#            no matter how many other checks it passes.
# ------------------------------------------------------------------

MAX_SCORE = 6  # Total points available


# ------------------------------------------------------------------
# STEP 1: Analyse the password — run every check, award points,
#         and collect suggestions for anything that failed.
# ------------------------------------------------------------------
def analyse_password(password):
    """
    Runs all checks on the password.
    Returns a dictionary with:
      - score       : integer (0 to 6)
      - checks      : dict of individual True/False results
      - suggestions : list of improvement tips (empty if perfect)
    """

    score = 0
    checks = {}
    suggestions = []  # Tips we'll show if a check fails

    length = len(password)

    # --- Check 1: Length >= 8 ---
    checks["length_8"] = length >= 8
    if checks["length_8"]:
        score += 1
    else:
        suggestions.append("Use at least 8 characters.")

    # --- Check 2: Length >= 12 (bonus points for extra length) ---
    checks["length_12"] = length >= 12
    if checks["length_12"]:
        score += 1
    else:
        suggestions.append("Use 12 or more characters for a stronger password.")

    # --- Check 3: Uppercase letter ---
    # [A-Z] matches any single uppercase letter anywhere in the string.
    checks["has_uppercase"] = bool(re.search(r"[A-Z]", password))
    if checks["has_uppercase"]:
        score += 1
    else:
        suggestions.append("Add at least one uppercase letter (A-Z).")

    # --- Check 4: Lowercase letter ---
    # [a-z] matches any single lowercase letter.
    checks["has_lowercase"] = bool(re.search(r"[a-z]", password))
    if checks["has_lowercase"]:
        score += 1
    else:
        suggestions.append("Add at least one lowercase letter (a-z).")

    # --- Check 5: Digit ---
    # [0-9] matches any single digit.
    checks["has_digit"] = bool(re.search(r"[0-9]", password))
    if checks["has_digit"]:
        score += 1
    else:
        suggestions.append("Add at least one number (0-9).")

    # --- Check 6: Special character ---
    # [^A-Za-z0-9] means "anything that is NOT a letter or digit".
    # Examples: ! @ # $ % ^ & * ( ) _ + - = [ ] { } ; ' : " , . < > ?
    checks["has_special"] = bool(re.search(r"[^A-Za-z0-9]", password))
    if checks["has_special"]:
        score += 1
    else:
        suggestions.append("Add at least one special character (e.g. ! @ # $ %).")

    return {
        "score": score,
        "length": length,
        "checks": checks,
        "suggestions": suggestions,
    }


# ------------------------------------------------------------------
# STEP 2: Convert the numeric score into a strength category.
#         The hard rule (< 8 chars = always Weak) is enforced here.
# ------------------------------------------------------------------
def get_category(score, length):
    """
    Returns the strength category as a string.
    Hard rule: length < 8 always produces 'Weak'.
    """

    # Hard rule — override everything if password is too short
    if length < 8:
        return "Weak"

    if score >= 5:
        return "Strong"
    elif score >= 3:
        return "Medium"
    else:
        return "Weak"


# ------------------------------------------------------------------
# STEP 3: Print the full report to the screen.
# ------------------------------------------------------------------
def display_report(result):
    """
    Prints the score, each check result, the strength category,
    and any improvement suggestions.
    """

    score    = result["score"]
    length   = result["length"]
    checks   = result["checks"]
    tips     = result["suggestions"]
    category = get_category(score, length)

    # Helper: show PASS or FAIL for a boolean value
    def mark(passed):
        return "PASS" if passed else "FAIL"

    # Choose a visual banner based on category
    banners = {
        "Strong": "[ STRONG - Great password! ]",
        "Medium": "[ MEDIUM - Getting there!  ]",
        "Weak":   "[ WEAK   - Needs work.     ]",
    }

    print("\n" + "=" * 50)
    print("        PASSWORD STRENGTH CHECKER  v2")
    print("=" * 50)
    print(f"  Length              : {length} character(s)")
    print(f"  At least  8 chars   : {mark(checks['length_8'])}")
    print(f"  At least 12 chars   : {mark(checks['length_12'])}")
    print(f"  Uppercase letter    : {mark(checks['has_uppercase'])}")
    print(f"  Lowercase letter    : {mark(checks['has_lowercase'])}")
    print(f"  Digit (0-9)         : {mark(checks['has_digit'])}")
    print(f"  Special character   : {mark(checks['has_special'])}")
    print("-" * 50)
    print(f"  Score               : {score} / {MAX_SCORE}")
    print(f"  Strength            : {category}  {banners[category]}")
    print("-" * 50)

    if tips:
        print("  Suggestions to improve:")
        for tip in tips:
            print(f"    - {tip}")
    else:
        print("  No suggestions - your password passes all checks!")

    print("=" * 50 + "\n")


# ------------------------------------------------------------------
# STEP 4: Main entry point - get input, guard against empty input,
#         run the analysis, show the report.
# ------------------------------------------------------------------
if __name__ == "__main__":
    print("\nWelcome to the Password Strength Checker  (v2)")
    print("------------------------------------------------")

    # Ask the user for a password
    password = input("Enter a password to check: ")

    # Guard: reject empty input immediately
    if not password.strip():
        print("\n[ERROR] No password entered. Please run the program again.\n")
    else:
        # Analyse and display — the password is only held in memory here
        result = analyse_password(password)
        display_report(result)
