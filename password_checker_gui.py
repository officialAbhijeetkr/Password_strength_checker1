# ============================================================
#  Password Strength Checker  (v3 — GUI Edition)
#  Cybersecurity Mini Project
#
#  Built with Python's built-in:
#    - tkinter  : graphical user interface
#    - re       : regular expressions (used inside password_checker)
#
#  Passwords are checked in memory ONLY.
#  They are NEVER stored, logged, or sent anywhere.
# ============================================================

import tkinter as tk                      # Main GUI library
from password_checker import analyse_password, get_category  # Our logic from v2


# ============================================================
#  COLOUR PALETTE  (cybersecurity / dark terminal theme)
# ============================================================
BG_DARK      = "#0d1117"   # Very dark navy — main background
BG_CARD      = "#161b22"   # Slightly lighter — card / panel background
BORDER       = "#30363d"   # Subtle grey border
TEXT_PRIMARY = "#e6edf3"   # Almost-white text
TEXT_MUTED   = "#8b949e"   # Dimmed text for labels
ACCENT_BLUE  = "#58a6ff"   # Bright blue — title, highlights
ACCENT_GREEN = "#3fb950"   # Green for Strong
ACCENT_AMBER = "#d29922"   # Amber/yellow for Medium
ACCENT_RED   = "#f85149"   # Red for Weak
BTN_BG       = "#238636"   # Button background (GitHub green)
BTN_HOVER    = "#2ea043"   # Button hover


# ============================================================
#  HELPER — build one "check row" (label + PASS/FAIL badge)
# ============================================================
def make_check_row(parent, label_text, passed):
    """
    Creates a single horizontal row showing a check name and its result.
    'passed' is True (PASS) or False (FAIL).
    Returns the row Frame so the caller can grid/pack it.
    """
    row = tk.Frame(parent, bg=BG_CARD)

    # The check name on the left
    tk.Label(
        row,
        text=label_text,
        bg=BG_CARD,
        fg=TEXT_MUTED,
        font=("Consolas", 10),
        anchor="w",
        width=26,
    ).pack(side="left")

    # The PASS / FAIL badge on the right
    badge_text  = "PASS" if passed else "FAIL"
    badge_color = ACCENT_GREEN if passed else ACCENT_RED

    tk.Label(
        row,
        text=badge_text,
        bg=BG_CARD,
        fg=badge_color,
        font=("Consolas", 10, "bold"),
    ).pack(side="left")

    return row


# ============================================================
#  MAIN APPLICATION CLASS
# ============================================================
class PasswordCheckerApp:
    """
    All the GUI code lives in this class.
    __init__ builds the window; check_password() runs the logic.
    """

    def __init__(self, root):
        # ---- Window setup ----
        self.root = root
        self.root.title("Password Strength Checker")
        self.root.configure(bg=BG_DARK)
        self.root.resizable(False, False)   # Fixed size — keeps layout clean

        # Centre the window on screen
        win_w, win_h = 480, 640
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = (screen_w - win_w) // 2
        y = (screen_h - win_h) // 2
        self.root.geometry(f"{win_w}x{win_h}+{x}+{y}")

        self._build_ui()

    # ----------------------------------------------------------
    # BUILD UI  — called once from __init__
    # ----------------------------------------------------------
    def _build_ui(self):
        # ---- Outer padding frame ----
        outer = tk.Frame(self.root, bg=BG_DARK, padx=24, pady=24)
        outer.pack(fill="both", expand=True)

        # ---- Title ----
        tk.Label(
            outer,
            text="Password Strength Checker",
            bg=BG_DARK,
            fg=ACCENT_BLUE,
            font=("Consolas", 16, "bold"),
        ).pack(anchor="w")

        tk.Label(
            outer,
            text="Cybersecurity Mini Project",
            bg=BG_DARK,
            fg=TEXT_MUTED,
            font=("Consolas", 10),
        ).pack(anchor="w", pady=(0, 20))

        # ---- Password input card ----
        input_card = tk.Frame(outer, bg=BG_CARD, bd=0, pady=16, padx=16,
                              highlightthickness=1, highlightbackground=BORDER)
        input_card.pack(fill="x")

        tk.Label(
            input_card,
            text="Enter your password",
            bg=BG_CARD,
            fg=TEXT_MUTED,
            font=("Consolas", 10),
            anchor="w",
        ).pack(fill="x")

        # Row: text entry + Show/Hide button side-by-side
        entry_row = tk.Frame(input_card, bg=BG_CARD)
        entry_row.pack(fill="x", pady=(6, 0))

        # The password entry field — show="*" hides characters
        self.entry = tk.Entry(
            entry_row,
            show="*",                     # Mask characters by default
            bg="#21262d",
            fg=TEXT_PRIMARY,
            insertbackground=TEXT_PRIMARY,  # Cursor colour
            relief="flat",
            font=("Consolas", 13),
            bd=0,
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=ACCENT_BLUE,
        )
        self.entry.pack(side="left", fill="x", expand=True, ipady=7)
        # Pressing Enter also triggers the check
        self.entry.bind("<Return>", lambda e: self.check_password())

        # Show / Hide toggle button
        self.toggle_btn = tk.Button(
            entry_row,
            text="Show",
            bg="#21262d",
            fg=ACCENT_BLUE,
            activebackground="#30363d",
            activeforeground=ACCENT_BLUE,
            relief="flat",
            font=("Consolas", 10),
            cursor="hand2",
            bd=0,
            padx=10,
            command=self.toggle_password,
        )
        self.toggle_btn.pack(side="left", padx=(6, 0))

        # ---- Check Strength button ----
        tk.Button(
            outer,
            text="Check Strength",
            bg=BTN_BG,
            fg="#ffffff",
            activebackground=BTN_HOVER,
            activeforeground="#ffffff",
            relief="flat",
            font=("Consolas", 12, "bold"),
            cursor="hand2",
            bd=0,
            pady=10,
            command=self.check_password,
        ).pack(fill="x", pady=(16, 0))

        # ---- Results card (hidden until first check) ----
        self.result_card = tk.Frame(
            outer,
            bg=BG_CARD,
            bd=0,
            pady=16,
            padx=16,
            highlightthickness=1,
            highlightbackground=BORDER,
        )
        # We pack this only after a successful check
        self.result_card.pack(fill="x", pady=(16, 0))
        self.result_card.pack_forget()   # Hide initially

        # Strength label (e.g. "STRONG")
        self.strength_label = tk.Label(
            self.result_card,
            text="",
            bg=BG_CARD,
            font=("Consolas", 18, "bold"),
            anchor="w",
        )
        self.strength_label.pack(fill="x")

        # Score text (e.g. "Score: 5 / 6")
        self.score_label = tk.Label(
            self.result_card,
            text="",
            bg=BG_CARD,
            fg=TEXT_MUTED,
            font=("Consolas", 10),
            anchor="w",
        )
        self.score_label.pack(fill="x", pady=(2, 10))

        # Placeholder frame — check rows are rebuilt on every check
        self.checks_frame = tk.Frame(self.result_card, bg=BG_CARD)
        self.checks_frame.pack(fill="x")

        # Separator line
        tk.Frame(self.result_card, bg=BORDER, height=1).pack(fill="x", pady=10)

        # Suggestions label
        self.suggestions_label = tk.Label(
            self.result_card,
            text="",
            bg=BG_CARD,
            fg=TEXT_MUTED,
            font=("Consolas", 10),
            anchor="w",
            justify="left",
            wraplength=400,
        )
        self.suggestions_label.pack(fill="x")

    # ----------------------------------------------------------
    # TOGGLE PASSWORD VISIBILITY
    # ----------------------------------------------------------
    def toggle_password(self):
        """Switches the password field between masked (*) and visible."""
        if self.entry["show"] == "*":
            self.entry.config(show="")          # Show plain text
            self.toggle_btn.config(text="Hide")
        else:
            self.entry.config(show="*")         # Mask again
            self.toggle_btn.config(text="Show")

    # ----------------------------------------------------------
    # CHECK PASSWORD  — runs on button click or Enter key
    # ----------------------------------------------------------
    def check_password(self):
        """
        Reads the password from the entry field, runs the analysis,
        and updates all result widgets.
        The password string is used only here and never saved.
        """
        password = self.entry.get()   # Read from the field

        # --- Guard: empty input ---
        if not password.strip():
            # Flash the entry border red to signal the error
            self.entry.config(highlightbackground=ACCENT_RED)
            self.root.after(1200, lambda: self.entry.config(
                highlightbackground=BORDER))
            self.result_card.pack_forget()  # Hide results
            return

        # --- Run analysis (logic from password_checker.py) ---
        result   = analyse_password(password)
        category = get_category(result["score"], result["length"])

        # --- Colour for this category ---
        colour_map = {
            "Strong": ACCENT_GREEN,
            "Medium": ACCENT_AMBER,
            "Weak":   ACCENT_RED,
        }
        colour = colour_map[category]

        # --- Update strength label ---
        self.strength_label.config(
            text=category.upper(),
            fg=colour,
        )

        # --- Update score label ---
        self.score_label.config(
            text=f"Score: {result['score']} / 6  |  Length: {result['length']} character(s)"
        )

        # --- Rebuild check rows (clear old ones first) ---
        for widget in self.checks_frame.winfo_children():
            widget.destroy()

        checks = result["checks"]
        rows = [
            ("Length >= 8 chars",    checks["length_8"]),
            ("Length >= 12 chars",   checks["length_12"]),
            ("Uppercase letter",     checks["has_uppercase"]),
            ("Lowercase letter",     checks["has_lowercase"]),
            ("Digit (0-9)",          checks["has_digit"]),
            ("Special character",    checks["has_special"]),
        ]
        for label, passed in rows:
            make_check_row(self.checks_frame, label, passed).pack(
                fill="x", pady=2
            )

        # --- Update suggestions ---
        tips = result["suggestions"]
        if tips:
            tip_text = "Suggestions:\n" + "\n".join(f"  - {t}" for t in tips)
        else:
            tip_text = "No suggestions - your password passes all checks!"
        self.suggestions_label.config(text=tip_text)

        # --- Show the results card ---
        self.result_card.pack(fill="x", pady=(16, 0))

        # Clear the password from memory (best practice)
        del password


# ============================================================
#  ENTRY POINT
# ============================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordCheckerApp(root)
    root.mainloop()   # Starts the GUI event loop
