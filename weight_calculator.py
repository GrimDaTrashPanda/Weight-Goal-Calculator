#!/usr/bin/env python3
"""
Weight Goal Calculator
-----------------------
A simple, friendly tool that estimates calorie needs and a realistic
timeline for reaching a weight goal. Uses the Mifflin-St Jeor equation,
which research shows holds up better across a wide range of body sizes
than older formulas like Harris-Benedict.

DISCLAIMER: This tool is for entertainment and general informational
purposes only. It is NOT medical advice and is not a substitute for
guidance from a registered dietitian, nutritionist, or physician.
Always consult a qualified healthcare professional before making
changes to your diet, exercise, or weight management plan, especially
if you have any underlying health conditions.
"""

import tkinter as tk
from tkinter import ttk, messagebox

# ---------------------------------------------------------------------------
# Color palette - pastel, pink-primary
# ---------------------------------------------------------------------------
COLOR_BG = "#fff0f5"          # lavender blush background
COLOR_PRIMARY = "#f4a6c6"     # pastel pink
COLOR_PRIMARY_DARK = "#e87fa8"  # slightly deeper pink for hover/accents
COLOR_SECONDARY = "#c9e4de"   # pastel mint accent
COLOR_TEXT = "#5b4254"        # soft plum, readable on pastel bg
COLOR_CARD = "#ffffff"
COLOR_WARN_BG = "#fde2e2"
COLOR_WARN_TEXT = "#8a3b3b"

FONT_TITLE = ("Verdana", 16, "bold")
FONT_HEADER = ("Verdana", 11, "bold")
FONT_BODY = ("Verdana", 10)
FONT_SMALL = ("Verdana", 8)

ACTIVITY_LEVELS = {
    "Sedentary (little/no exercise)": 1.2,
    "Lightly active (1-3 days/week)": 1.375,
    "Moderately active (3-5 days/week)": 1.55,
    "Very active (6-7 days/week)": 1.725,
    "Extremely active (physical job + training)": 1.9,
}

KG_PER_LB = 0.45359237
CM_PER_IN = 2.54
CAL_PER_KG_FAT = 7700  # commonly used approximation


def lb_to_kg(lb):
    return lb * KG_PER_LB


def kg_to_lb(kg):
    return kg / KG_PER_LB


def in_to_cm(inches):
    return inches * CM_PER_IN


class WeightCalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Weight Goal Calculator")
        self.configure(bg=COLOR_BG)
        self.geometry("520x720")
        self.minsize(480, 680)
        self.resizable(True, True)

        self._build_style()
        self._build_layout()

    # ------------------------------------------------------------------
    # Styling
    # ------------------------------------------------------------------
    def _build_style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("TFrame", background=COLOR_BG)
        style.configure("Card.TFrame", background=COLOR_CARD)
        style.configure(
            "TLabel", background=COLOR_BG, foreground=COLOR_TEXT, font=FONT_BODY
        )
        style.configure(
            "Card.TLabel", background=COLOR_CARD, foreground=COLOR_TEXT, font=FONT_BODY
        )
        style.configure(
            "Header.TLabel",
            background=COLOR_BG,
            foreground=COLOR_TEXT,
            font=FONT_HEADER,
        )
        style.configure(
            "Title.TLabel",
            background=COLOR_BG,
            foreground=COLOR_PRIMARY_DARK,
            font=FONT_TITLE,
        )
        style.configure(
            "TButton",
            background=COLOR_PRIMARY,
            foreground="white",
            font=FONT_HEADER,
            padding=8,
            borderwidth=0,
        )
        style.map(
            "TButton",
            background=[("active", COLOR_PRIMARY_DARK)],
        )
        style.configure(
            "TRadiobutton",
            background=COLOR_BG,
            foreground=COLOR_TEXT,
            font=FONT_BODY,
        )
        style.configure(
            "TCombobox",
            fieldbackground="white",
            background="white",
            foreground=COLOR_TEXT,
        )
        style.configure("TEntry", fieldbackground="white", foreground=COLOR_TEXT)

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------
    def _build_layout(self):
        container = tk.Frame(self, bg=COLOR_BG)
        container.pack(fill="both", expand=True, padx=16, pady=16)

        canvas = tk.Canvas(container, bg=COLOR_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw", width=480)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        root = scroll_frame

        # Title
        ttk.Label(root, text="Weight Goal Calculator", style="Title.TLabel").pack(
            anchor="w", pady=(0, 4)
        )
        ttk.Label(
            root,
            text="Estimate your calorie needs and a realistic timeline.",
            style="TLabel",
        ).pack(anchor="w", pady=(0, 12))

        # Units toggle
        units_frame = ttk.Frame(root)
        units_frame.pack(fill="x", pady=(0, 10))
        ttk.Label(units_frame, text="Units:", style="Header.TLabel").pack(side="left")
        self.unit_var = tk.StringVar(value="imperial")
        ttk.Radiobutton(
            units_frame, text="Imperial (lb/in)", variable=self.unit_var,
            value="imperial", command=self._update_unit_labels
        ).pack(side="left", padx=8)
        ttk.Radiobutton(
            units_frame, text="Metric (kg/cm)", variable=self.unit_var,
            value="metric", command=self._update_unit_labels
        ).pack(side="left", padx=8)

        form = self._card(root)

        # Sex
        ttk.Label(form, text="Sex (for BMR formula):", style="Card.TLabel").grid(
            row=0, column=0, sticky="w", pady=6
        )
        self.sex_var = tk.StringVar(value="female")
        sex_frame = ttk.Frame(form, style="Card.TFrame")
        sex_frame.grid(row=0, column=1, sticky="w")
        ttk.Radiobutton(sex_frame, text="Female", variable=self.sex_var, value="female").pack(side="left")
        ttk.Radiobutton(sex_frame, text="Male", variable=self.sex_var, value="male").pack(side="left", padx=8)

        # Age
        ttk.Label(form, text="Age (years):", style="Card.TLabel").grid(
            row=1, column=0, sticky="w", pady=6
        )
        self.age_entry = ttk.Entry(form, width=12)
        self.age_entry.grid(row=1, column=1, sticky="w")

        # Height
        self.height_label = ttk.Label(form, text="Height (in):", style="Card.TLabel")
        self.height_label.grid(row=2, column=0, sticky="w", pady=6)
        self.height_entry = ttk.Entry(form, width=12)
        self.height_entry.grid(row=2, column=1, sticky="w")

        # Current weight
        self.weight_label = ttk.Label(form, text="Current weight (lb):", style="Card.TLabel")
        self.weight_label.grid(row=3, column=0, sticky="w", pady=6)
        self.weight_entry = ttk.Entry(form, width=12)
        self.weight_entry.grid(row=3, column=1, sticky="w")

        # Goal weight
        self.goal_label = ttk.Label(form, text="Goal weight (lb):", style="Card.TLabel")
        self.goal_label.grid(row=4, column=0, sticky="w", pady=6)
        self.goal_entry = ttk.Entry(form, width=12)
        self.goal_entry.grid(row=4, column=1, sticky="w")

        # Activity level
        ttk.Label(form, text="Activity level:", style="Card.TLabel").grid(
            row=5, column=0, sticky="w", pady=6
        )
        self.activity_var = tk.StringVar(value=list(ACTIVITY_LEVELS.keys())[0])
        activity_combo = ttk.Combobox(
            form,
            textvariable=self.activity_var,
            values=list(ACTIVITY_LEVELS.keys()),
            state="readonly",
            width=30,
        )
        activity_combo.grid(row=5, column=1, sticky="w")

        # Optional body fat %
        ttk.Label(form, text="Body fat % (optional):", style="Card.TLabel").grid(
            row=6, column=0, sticky="w", pady=6
        )
        bf_frame = ttk.Frame(form, style="Card.TFrame")
        bf_frame.grid(row=6, column=1, sticky="w")
        self.bodyfat_entry = ttk.Entry(bf_frame, width=8)
        self.bodyfat_entry.pack(side="left")
        ttk.Label(bf_frame, text=" leave blank to skip", style="Card.TLabel", font=FONT_SMALL).pack(
            side="left", padx=(6, 0)
        )
        ttk.Label(
            form,
            text="If provided, uses the Katch-McArdle formula (more accurate\nwhen lean mass is known) instead of Mifflin-St Jeor.",
            style="Card.TLabel",
            font=FONT_SMALL,
            justify="left",
        ).grid(row=7, column=0, columnspan=2, sticky="w", pady=(0, 6))

        # Weekly rate goal
        ttk.Label(form, text="Target pace:", style="Card.TLabel").grid(
            row=8, column=0, sticky="w", pady=6
        )
        self.pace_var = tk.StringVar(value="0.5 kg / 1 lb per week (moderate)")
        pace_options = [
            "0.25 kg / 0.5 lb per week (gentle)",
            "0.5 kg / 1 lb per week (moderate)",
            "0.75 kg / 1.5 lb per week (aggressive)",
            "1 kg / 2 lb per week (max recommended)",
        ]
        pace_combo = ttk.Combobox(
            form, textvariable=self.pace_var, values=pace_options, state="readonly", width=30
        )
        pace_combo.grid(row=8, column=1, sticky="w")

        # Calculate button
        calc_btn = ttk.Button(root, text="Calculate", command=self._calculate)
        calc_btn.pack(fill="x", pady=(14, 10))

        # Results card
        self.results_card = self._card(root)
        self.results_label = ttk.Label(
            self.results_card,
            text="Your results will appear here.",
            style="Card.TLabel",
            justify="left",
        )
        self.results_label.grid(row=0, column=0, sticky="w")

        # Disclaimer
        disclaimer = tk.Label(
            root,
            text=(
                "⚠ For entertainment and general informational purposes only. "
                "This is not medical advice and is not a substitute for guidance "
                "from a registered dietitian, nutritionist, or physician. Always "
                "consult a qualified healthcare professional before making changes "
                "to your diet or exercise routine, especially if you have any "
                "underlying health conditions."
            ),
            bg=COLOR_WARN_BG,
            fg=COLOR_WARN_TEXT,
            font=FONT_SMALL,
            wraplength=440,
            justify="left",
            padx=10,
            pady=10,
        )
        disclaimer.pack(fill="x", pady=(16, 0))

    def _card(self, parent):
        card = ttk.Frame(parent, style="Card.TFrame", padding=14)
        card.pack(fill="x", pady=8)
        return card

    def _update_unit_labels(self):
        if self.unit_var.get() == "imperial":
            self.height_label.config(text="Height (in):")
            self.weight_label.config(text="Current weight (lb):")
            self.goal_label.config(text="Goal weight (lb):")
        else:
            self.height_label.config(text="Height (cm):")
            self.weight_label.config(text="Current weight (kg):")
            self.goal_label.config(text="Goal weight (kg):")

    # ------------------------------------------------------------------
    # Calculation
    # ------------------------------------------------------------------
    def _calculate(self):
        try:
            age = float(self.age_entry.get())
            height_raw = float(self.height_entry.get())
            weight_raw = float(self.weight_entry.get())
            goal_raw = float(self.goal_entry.get())
        except ValueError:
            messagebox.showerror("Missing or invalid input", "Please enter valid numbers for age, height, current weight, and goal weight.")
            return

        if age <= 0 or height_raw <= 0 or weight_raw <= 0 or goal_raw <= 0:
            messagebox.showerror("Invalid input", "All values must be greater than zero.")
            return

        # Normalize to metric for the math
        if self.unit_var.get() == "imperial":
            height_cm = in_to_cm(height_raw)
            weight_kg = lb_to_kg(weight_raw)
            goal_kg = lb_to_kg(goal_raw)
            unit_label = "lb"
            display_weight = weight_raw
            display_goal = goal_raw
        else:
            height_cm = height_raw
            weight_kg = weight_raw
            goal_kg = goal_raw
            unit_label = "kg"
            display_weight = weight_raw
            display_goal = goal_raw

        # Optional body fat % -> Katch-McArdle if provided, else Mifflin-St Jeor
        bodyfat_raw = self.bodyfat_entry.get().strip()
        formula_used = "Mifflin-St Jeor"
        if bodyfat_raw:
            try:
                bodyfat_pct = float(bodyfat_raw)
            except ValueError:
                messagebox.showerror("Invalid input", "Body fat % must be a number, or leave it blank.")
                return
            if not (0 < bodyfat_pct < 75):
                messagebox.showerror("Invalid input", "Body fat % should be a realistic value between 0 and 75.")
                return
            lean_mass_kg = weight_kg * (1 - bodyfat_pct / 100)
            bmr = 370 + (21.6 * lean_mass_kg)
            formula_used = "Katch-McArdle"
        else:
            # Mifflin-St Jeor BMR
            if self.sex_var.get() == "male":
                bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
            else:
                bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161

        activity_factor = ACTIVITY_LEVELS[self.activity_var.get()]
        tdee = bmr * activity_factor

        # Weekly pace -> kg/week
        pace_map = {
            "0.25 kg / 0.5 lb per week (gentle)": 0.25,
            "0.5 kg / 1 lb per week (moderate)": 0.5,
            "0.75 kg / 1.5 lb per week (aggressive)": 0.75,
            "1 kg / 2 lb per week (max recommended)": 1.0,
        }
        kg_per_week = pace_map[self.pace_var.get()]
        daily_deficit_or_surplus = (kg_per_week * CAL_PER_KG_FAT) / 7

        weight_diff_kg = goal_kg - weight_kg  # positive = gain, negative = loss

        if abs(weight_diff_kg) < 0.01:
            target_calories = tdee
            direction = "maintain"
            weeks_needed = 0
        elif weight_diff_kg > 0:
            direction = "gain"
            target_calories = tdee + daily_deficit_or_surplus
            weeks_needed = weight_diff_kg / kg_per_week
        else:
            direction = "lose"
            target_calories = tdee - daily_deficit_or_surplus
            weeks_needed = abs(weight_diff_kg) / kg_per_week

        # Sanity floor: don't recommend below ~1200 kcal commonly cited as a
        # general floor for safe unsupervised intake (still flagged in UI).
        low_calorie_warning = target_calories < 1200

        weeks_needed_display = round(weeks_needed, 1)
        months_needed_display = round(weeks_needed / 4.345, 1) if weeks_needed else 0

        result_lines = [
            f"Formula used: {formula_used}",
            f"BMR (calories your body burns at rest): {bmr:,.0f} kcal/day",
            f"TDEE (calories burned with activity): {tdee:,.0f} kcal/day",
            "",
        ]

        if direction == "maintain":
            result_lines.append(f"You're already at your goal weight. Eat around {tdee:,.0f} kcal/day to maintain.")
        else:
            verb = "gain" if direction == "gain" else "lose"
            result_lines.append(
                f"To {verb} weight at your selected pace, aim for about "
                f"{target_calories:,.0f} kcal/day."
            )
            result_lines.append(
                f"That's a daily {'surplus' if direction == 'gain' else 'deficit'} of "
                f"~{daily_deficit_or_surplus:,.0f} kcal vs. your maintenance level."
            )
            result_lines.append("")
            result_lines.append(
                f"Estimated time to reach {display_goal:g} {unit_label} from "
                f"{display_weight:g} {unit_label}: "
                f"~{weeks_needed_display} weeks (~{months_needed_display} months)."
            )

        if low_calorie_warning:
            result_lines.append("")
            result_lines.append(
                "⚠ The calculated target falls below 1,200 kcal/day, a commonly "
                "cited general floor for unsupervised intake. Please consult a "
                "healthcare provider before pursuing a deficit this large."
            )

        self.results_label.config(text="\n".join(result_lines))


if __name__ == "__main__":
    app = WeightCalculatorApp()
    app.mainloop()
