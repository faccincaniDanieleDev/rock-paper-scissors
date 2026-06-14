"""gameGUI.py — Main GUI for the Rock Paper Scissors game."""

import os
import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from .moveType import MoveType
from .gameMatch import GameMatch

# Absolute path of this file's directory, used to resolve image assets
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class GUI(ctk.CTk):
    """Main application window for the Rock Paper Scissors game.

    Builds the full UI, manages the match lifecycle and handles
    all user interactions. Inherits from CTk (customtkinter root window).
    """

    BG_COLOR = "#141721"

    # Round result messages and colors
    _MSG_TIE  = "ROUND TIE! The CPU also chose {move}."
    _MSG_WIN  = "YOU WON THE ROUND! The CPU chose {move}."
    _MSG_LOSS = "YOU LOST THIS ROUND... The CPU had {move}."

    _COLOR_TIE  = "#00FFFF"
    _COLOR_WIN  = "#39FF14"
    _COLOR_LOSS = "#FF003F"

    # Match end verdicts
    _VERDICT_WIN  = "🏆 CONGRATULATIONS, YOU WON THE MATCH! 🏆"
    _VERDICT_LOSS = "🏆 GAME OVER, THE CPU WON THE MATCH! 🏆"
    _VERDICT_DRAW = "🏆 THE MATCH ENDED IN A DRAW! 🏆"

    # UI text constants
    _ROUND_END_TEXT    = "END"
    _ROUND_INITIAL_TEXT = "ROUND\n1/3"
    _ROUND_TEXT        = "ROUND\n{round}/3"
    _STATUS_INITIAL    = "YOUR MOVE"
    _STATUS_INITIAL_COLOR = "#4caf50"

    # Button configuration: image path, glow color, move type, badge key
    _BUTTON_CONFIGS: list[dict] = [
        {"image_path": os.path.join(BASE_DIR, "assets", "rockImage.png"),    "glow_color": "#00FFFF", "move_type": MoveType.ROCK,    "bind_key": "0"},
        {"image_path": os.path.join(BASE_DIR, "assets", "paperImage.png"),   "glow_color": "#39FF14", "move_type": MoveType.PAPER,   "bind_key": "1"},
        {"image_path": os.path.join(BASE_DIR, "assets", "scissorImage.png"), "glow_color": "#FF003F", "move_type": MoveType.SCISSOR, "bind_key": "2"},
    ]

    # Scoreboard player configuration: column, key, name, color, icon, bg
    _PLAYER_CONFIGS: list[tuple] = [
        (0, "player", "Player",   "#1f75fe", "👤", "#28354a"),
        (2, "cpu",    "Computer", "#e53935", "🤖", "#3d242b"),
    ]

    def __init__(self) -> None:
        """Initializes the window, builds the UI and starts a new match."""
        super().__init__()
        self._setup_window()
        self._build_header()
        self._build_scoreboard()
        self._build_status_label()
        self._build_game_buttons()
        self._build_footer()
        self._build_restart_button()
        self._new_match()

    # ── window setup ───────────────────────────────────────────────────

    def _setup_window(self) -> None:
        """Configures the main window properties."""
        self.title("Rock Paper Scissors")
        self.geometry("950x800")
        ctk.set_appearance_mode("dark")
        self.configure(fg_color=self.BG_COLOR)
        self.grid_columnconfigure(0, weight=1)

    # ── UI builders ────────────────────────────────────────────────────

    def _build_header(self) -> None:
        """Creates the title label at the top of the window."""
        ctk.CTkLabel(
            self, text="ROCK, PAPER, SCISSORS - THE MATCH",
            font=("Impact", 28), text_color="#ffffff"
        ).grid(row=0, column=0, pady=(25, 20))

    def _build_scoreboard(self) -> None:
        """Creates the scoreboard with player cards and round indicator."""
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=1, column=0, sticky="ew", padx=40, pady=10)
        container.grid_columnconfigure((0, 1, 2), weight=1)

        self.score_labels: dict[str, ctk.CTkLabel] = {}

        for column_index, player_key, display_name, border_color, avatar_icon, avatar_bg_color in self._PLAYER_CONFIGS:
            card = ctk.CTkFrame(
                container, fg_color="#1a1d29", border_color=border_color,
                border_width=2, corner_radius=15, height=140
            )
            card.grid(row=0, column=column_index, padx=15, sticky="nsew")
            card.grid_propagate(False)
            card.grid_columnconfigure((0, 1, 2), weight=1)
            card.grid_rowconfigure((0, 1), weight=1)

            ctk.CTkLabel(card, text=display_name, font=("Arial", 13, "bold"), text_color=border_color).grid(row=0, column=0, columnspan=3, pady=(10, 0))
            ctk.CTkLabel(card, text="SCORE", font=("Impact", 14), text_color="#8aa0b4").grid(row=1, column=1, pady=(0, 25))

            self.score_labels[player_key] = ctk.CTkLabel(card, text="0", font=("Impact", 28), text_color="#ffffff")
            self.score_labels[player_key].grid(row=1, column=1, pady=(20, 0))

            ctk.CTkLabel(
                card, text=avatar_icon, font=("Arial", 35),
                fg_color=avatar_bg_color, width=60, height=60, corner_radius=10
            ).grid(row=1, column=column_index, padx=15, pady=(0, 15))

        # Round indicator
        round_card = ctk.CTkFrame(container, fg_color="transparent")
        round_card.grid(row=0, column=1, padx=10, sticky="nsew")

        ctk.CTkLabel(round_card, text="BEST OF 3 ROUNDS", font=("Arial", 11, "bold"), text_color="#627285").pack(pady=(5, 5))

        self._round_circle = ctk.CTkFrame(
            round_card, fg_color="#1a1d29", border_color="#4caf50",
            border_width=3, corner_radius=45, width=90, height=90
        )
        self._round_circle.pack(pady=5)
        self._round_circle.pack_propagate(False)

        self._round_display = ctk.CTkLabel(
            self._round_circle, text=self._ROUND_INITIAL_TEXT,
            font=("Impact", 16), text_color="#ffffff"
        )
        self._round_display.pack(expand=True)

    def _build_status_label(self) -> None:
        """Creates the status label that shows round results and match outcome."""
        self._status_label = ctk.CTkLabel(
            self, text=self._STATUS_INITIAL,
            font=("Impact", 24), text_color=self._STATUS_INITIAL_COLOR
        )
        self._status_label.grid(row=2, column=0, pady=(35, 10))

    def _build_game_buttons(self) -> None:
        """Creates the three move buttons with neon glow effect."""
        game_frame = ctk.CTkFrame(self, fg_color="transparent")
        game_frame.grid(row=3, column=0, sticky="ew", padx=40, pady=10)
        game_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self._buttons: list[ctk.CTkButton] = []

        for index, config in enumerate(self._BUTTON_CONFIGS):
            image = self._generate_glow_button_image(config["image_path"], config["glow_color"], config["bind_key"])

            btn = ctk.CTkButton(
                game_frame, text="",
                image=ctk.CTkImage(light_image=image.resize((180, 180), Image.Resampling.LANCZOS), size=(180, 180)),
                fg_color="transparent", hover_color=self.BG_COLOR, width=180, height=180,
                command=lambda move=config["move_type"]: self._on_move_selected(move)
            )
            btn.grid(row=0, column=index, padx=15)
            self._buttons.append(btn)

    def _build_footer(self) -> None:
        """Creates the hint label below the move buttons."""
        ctk.CTkLabel(
            self, text="Choose your move (0, 1, or 2)",
            font=("Arial", 14), text_color="#627285"
        ).grid(row=4, column=0, pady=(25, 10))

    def _build_restart_button(self) -> None:
        """Creates the Play Again button (hidden by default)."""
        self._restart_btn = ctk.CTkButton(
            self, text="PLAY AGAIN", font=("Impact", 18),
            fg_color="#1a1d29", border_color="#4caf50", border_width=2,
            hover_color="#252836", text_color="#4caf50",
            width=180, height=45, command=self._new_match
        )
        self._restart_btn.grid(row=5, column=0, pady=(10, 25))
        self._restart_btn.grid_remove()

    # ── image generation ───────────────────────────────────────────────

    def _generate_glow_button_image(self, image_path: str, glow_color: str, badge_key: str) -> Image.Image:
        """Generates a button image with neon glow effect.

        Args:
            image_path: Path to the move icon image.
            glow_color: Hex color for the neon glow ring.
            badge_key:  Character to display in the bottom badge.

        Returns:
            A PIL Image with the glow effect applied.
        """
        base_canvas = Image.new("RGBA", (400, 400), self.BG_COLOR)
        glow_mask = Image.new("RGBA", (400, 400), (0, 0, 0, 0))
        ImageDraw.Draw(glow_mask).ellipse([30, 30, 370, 370], outline=glow_color, width=20)
        blurred = glow_mask.filter(ImageFilter.GaussianBlur(radius=12))
        base_canvas.paste(blurred, (0, 0), mask=blurred)

        drawer = ImageDraw.Draw(base_canvas)
        drawer.ellipse([30, 30, 370, 370], outline=glow_color, width=6)

        icon = Image.open(image_path).convert("RGBA")
        icon.putdata([
            (0, 0, 0, 0) if (115 <= p[0] <= 140 and 115 <= p[1] <= 140 and 115 <= p[2] <= 140) else p
            for p in icon.getdata()
        ])
        icon = icon.resize((210, 210), Image.Resampling.LANCZOS)
        base_canvas.paste(icon, (95, 95), mask=icon)

        drawer.ellipse([165, 335, 235, 405], fill=glow_color)
        try:
            font = ImageFont.truetype("arial.ttf", 36)
        except Exception:
            font = ImageFont.load_default()
        drawer.text((184, 345), badge_key, fill="#ffffff", font=font)

        return base_canvas

    # ── match lifecycle ────────────────────────────────────────────────

    def _new_match(self) -> None:
        """Resets the match state and restores the UI for a new game."""
        self.match = GameMatch(best_of=3)
        self.score_labels["player"].configure(text="0")
        self.score_labels["cpu"].configure(text="0")
        self._round_display.configure(text=self._ROUND_INITIAL_TEXT, font=("Impact", 16))
        self._status_label.configure(text=self._STATUS_INITIAL, text_color=self._STATUS_INITIAL_COLOR)
        self._restart_btn.grid_remove()
        for btn in self._buttons:
            btn.configure(state="normal")

    # ── event handlers ─────────────────────────────────────────────────

    def _on_move_selected(self, selected_move: MoveType) -> None:
        """Handles a move selection and updates the UI accordingly.

        Args:
            selected_move: The move chosen by the human player.
        """
        self.match.play_round(selected_move)

        self.score_labels["player"].configure(text=str(self.match.human_score))
        self.score_labels["cpu"].configure(text=str(self.match.cpu_score))

        cpu_move_text = GameMatch.MOVE_NAMES.get(self.match.cpu_move, "unknown")

        if selected_move == self.match.cpu_move:
            round_message, color = self._MSG_TIE.format(move=cpu_move_text), self._COLOR_TIE
        elif GameMatch.WIN_CONDITIONS[selected_move] == self.match.cpu_move:
            round_message, color = self._MSG_WIN.format(move=cpu_move_text), self._COLOR_WIN
        else:
            round_message, color = self._MSG_LOSS.format(move=cpu_move_text), self._COLOR_LOSS

        if not self.match.game_over:
            self._round_display.configure(text=self._ROUND_TEXT.format(round=self.match.current_round))
            self._status_label.configure(text=round_message, text_color=color)
        else:
            self._show_match_end(round_message, color)

    def _show_match_end(self, last_round_message: str, last_round_color: str) -> None:
        """Displays the final match result and disables move buttons.

        Args:
            last_round_message: The result message of the last round.
            last_round_color:   The color associated with the last round result.
        """
        self._round_display.configure(text=self._ROUND_END_TEXT, font=("Impact", 14))

        if self.match.human_score > self.match.cpu_score:
            verdict, final_color = self._VERDICT_WIN, self._COLOR_WIN
        elif self.match.cpu_score > self.match.human_score:
            verdict, final_color = self._VERDICT_LOSS, self._COLOR_LOSS
        else:
            verdict, final_color = self._VERDICT_DRAW, self._COLOR_TIE

        self._status_label.configure(text=f"{last_round_message}\n{verdict}", text_color=final_color)

        for btn in self._buttons:
            btn.configure(state="disabled")
        self._restart_btn.grid()