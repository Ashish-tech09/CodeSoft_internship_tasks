import random
import tkinter as tk
from tkinter import messagebox


class RockPaperScissorsApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Retro Arena: RPS")
        self.root.geometry("450x550")
        self.root.configure(bg="#1e1e2e")  # Dark modern palette
        self.root.resizable(False, False)

        # Game State Variables
        self.user_score = 0
        self.computer_score = 0
        self.ties = 0

        # ---- 1. DIGITAL SCOREBOARD DISPLAY ----
        self.display_frame = tk.Frame(root, bg="#11111b", bd=2, relief="solid")
        self.display_frame.pack(fill="x", padx=20, pady=20)

        # Main Matchup Readout Banner
        self.matchup_label = tk.Label(
            self.display_frame,
            text="CHOOSE YOUR WEAPON",
            font=("Consolas", 16, "bold"),
            fg="#fab387",  # Vibrant amber
            bg="#11111b",
            pady=10,
        )
        self.matchup_label.pack(fill="x")

        # Live Telemetry Stats Sub-bar
        self.stats_label = tk.Label(
            self.display_frame,
            text="WINS: 0  |  LOSSES: 0  |  TIES: 0",
            font=("Consolas", 11),
            fg="#a6e3a1",  # Digital matrix green
            bg="#11111b",
            pady=8,
        )
        self.stats_label.pack(fill="x")

        # ---- 2. GAME VISUALIZER AREA ----
        self.arena_frame = tk.Frame(root, bg="#1e1e2e")
        self.arena_frame.pack(fill="x", padx=20, pady=10)

        self.vs_label = tk.Label(
            self.arena_frame,
            text="YOU  vs  CPU",
            font=("Segoe UI Black", 14),
            fg="#585b70",
            bg="#1e1e2e",
        )
        self.vs_label.pack()

        self.battle_label = tk.Label(
            self.arena_frame,
            text="🤖 Ready to Match 🤖",
            font=("Segoe UI", 12, "italic"),
            fg="#cdd6f4",
            bg="#1e1e2e",
            pady=10,
        )
        self.battle_label.pack()

        # ---- 3. INTERACTIVE GRID OF KEYS ----
        # 2x2 layout housing choices and reset matrix triggers
        self.grid_frame = tk.Frame(root, bg="#1e1e2e")
        self.grid_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        # Enforce symmetrical scaling for 2 columns and 2 rows
        self.grid_frame.columnconfigure(0, weight=1)
        self.grid_frame.columnconfigure(1, weight=1)
        self.grid_frame.rowconfigure(0, weight=1)
        self.grid_frame.rowconfigure(1, weight=1)

        # Core input choices configuration
        # Text, BG, Move identifier
        moves = [
            ("🪨 ROCK", "#89b4fa", "Rock"),  # Row 0, Col 0
            ("📜 PAPER", "#a6e3a1", "Paper"),  # Row 0, Col 1
            ("✂️ SCISSORS", "#f9e2af", "Scissors"),  # Row 1, Col 0
        ]

        for i, (text, bg, move) in enumerate(moves):
            row = i // 2
            col = i % 2
            btn = tk.Button(
                self.grid_frame,
                text=text,
                font=("Segoe UI Black", 12),
                bg=bg,
                fg="#11111b",
                activebackground="#11111b",
                activeforeground=bg,
                bd=0,
                cursor="hand2",
                command=lambda m=move: self.play_round(m),
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

        # Global Control System Key (Reset Button occupies bottom right square)
        self.btn_reset = tk.Button(
            self.grid_frame,
            text="🧹 RESET\nSTATS",
            font=("Segoe UI Black", 10),
            bg="#f38ba8",  # Alert crimson
            fg="#11111b",
            activebackground="#11111b",
            activeforeground="#f38ba8",
            bd=0,
            cursor="hand2",
            command=self.reset_game,
        )
        self.btn_reset.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

    # ---- GAME MECHANICS LOGIC ----

    def play_round(self, user_choice):
        choices = ["Rock", "Paper", "Scissors"]
        computer_choice = random.choice(choices)

        # Emoji representations for high-fidelity telemetry readout
        emoji_map = {"Rock": "🪨", "Paper": "📜", "Scissors": "✂️"}

        # Logic Matrix evaluations
        if user_choice == computer_choice:
            result_text = "IT'S A TIE FIGHT!"
            self.ties += 1
            text_color = "#f9e2af"  # Yellow for a draw
        elif (
            (user_choice == "Rock" and computer_choice == "Scissors")
            or (user_choice == "Paper" and computer_choice == "Rock")
            or (user_choice == "Scissors" and computer_choice == "Paper")
        ):
            result_text = "YOU WIN THIS ROUND!"
            self.user_score += 1
            text_color = "#a6e3a1"  # Mint green for victory
        else:
            result_text = "COMPUTER OVERRIDE: YOU LOSE!"
            self.computer_score += 1
            text_color = "#f38ba8"  # Crimson red for loss

        # Push updates back to display elements
        self.matchup_label.config(text=result_text, fg=text_color)
        self.battle_label.config(
            text=f"You chose {emoji_map[user_choice]}  |  CPU chose {emoji_map[computer_choice]}"
        )
        self.update_scoreboard()

    def update_scoreboard(self):
        self.stats_label.config(
            text=f"WINS: {self.user_score}  |  LOSSES: {self.computer_score}  |  TIES: {self.ties}"
        )

    def reset_game(self):
        if self.user_score > 0 or self.computer_score > 0 or self.ties > 0:
            if messagebox.askyesno(
                "Reset System", "Are you sure you want to clear scoreboard logs?"
            ):
                self.user_score = 0
                self.computer_score = 0
                self.ties = 0
                self.update_scoreboard()
                self.matchup_label.config(
                    text="CHOOSE YOUR WEAPON", fg="#fab387"
                )
                self.battle_label.config(text="🤖 Ready to Match 🤖")


if __name__ == "__main__":
    root = tk.Tk()
    app = RockPaperScissorsApp(root)
    root.mainloop()