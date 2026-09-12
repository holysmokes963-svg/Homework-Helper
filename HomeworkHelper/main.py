import os
import base64
import io
import time
import threading
import tkinter as tk
from tkinter import scrolledtext
from pathlib import Path

import keyboard
import mss
from PIL import Image
from openai import OpenAI
from pynput import mouse
from dotenv import load_dotenv


load_dotenv(Path(__file__).with_name(".env"))


MODEL = "gpt-5.6-luna"
ANSWER_DELAY = 2.0

armed = False
processing = False
booting = True


api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("ERROR: OPENAI_API_KEY is not set.")
    print("Make sure your .env file contains:")
    print("OPENAI_API_KEY=your_api_key_here")
    raise SystemExit


client = OpenAI(api_key=api_key)


class HomeworkWindow:

    def __init__(self):

        self.root = tk.Tk()

        self.root.title("Homework Helper")
        self.root.geometry("620x560")
        self.root.minsize(500, 420)

        self.root.configure(bg="#05070a")
        self.root.attributes("-topmost", True)

        self.cyan = "#00e5ff"
        self.bright_cyan = "#8cF8ff"
        self.dark_cyan = "#06232a"
        self.bg = "#05070a"
        self.panel = "#091116"
        self.panel2 = "#0c171d"
        self.text = "#d9faff"
        self.gray = "#6d8a91"
        self.green = "#00ff9d"
        self.red = "#ff3158"
        self.yellow = "#ffd166"

        self.boot_frame = tk.Frame(
            self.root,
            bg=self.bg
        )

        self.main_frame = tk.Frame(
            self.root,
            bg=self.bg
        )

        self.boot_canvas = tk.Canvas(
            self.boot_frame,
            bg=self.bg,
            highlightthickness=0
        )

        self.boot_canvas.pack(
            fill=tk.BOTH,
            expand=True
        )

        self.build_main_ui()

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.close
        )

        self.boot_frame.pack(
            fill=tk.BOTH,
            expand=True
        )

        self.boot_start()

    # ---------------------------------------------------------
    # BOOT SCREEN
    # ---------------------------------------------------------

    def boot_start(self):

        self.boot_start_time = time.time()
        self.boot_step = 0
        self.boot_progress = 0

        self.boot_lines = [
            "INITIALIZING HOMEWORK HELPER",
            "LOADING NEURAL INTERFACE",
            "CONNECTING TO AI CORE",
            "CALIBRATING SCREEN ANALYSIS",
            "VERIFYING SYSTEMS",
            "INTERFACE READY"
        ]

        self.animate_boot()

    def animate_boot(self):

        if not self.boot_frame.winfo_exists():
            return

        elapsed = time.time() - self.boot_start_time

        width = max(
            self.boot_canvas.winfo_width(),
            620
        )

        height = max(
            self.boot_canvas.winfo_height(),
            560
        )

        self.boot_canvas.delete("all")

        # Background grid
        for x in range(0, width, 40):
            self.boot_canvas.create_line(
                x,
                0,
                x,
                height,
                fill="#071319"
            )

        for y in range(0, height, 40):
            self.boot_canvas.create_line(
                0,
                y,
                width,
                y,
                fill="#071319"
            )

        # Top accent
        self.boot_canvas.create_rectangle(
            0,
            0,
            width,
            3,
            fill=self.cyan,
            outline=""
        )

        # Main title
        self.boot_canvas.create_text(
            width / 2,
            height * 0.28,
            text="HOMEWORK",
            fill=self.cyan,
            font=("Arial", 31, "bold")
        )

        self.boot_canvas.create_text(
            width / 2,
            height * 0.35,
            text="HELPER",
            fill=self.bright_cyan,
            font=("Arial", 31, "bold")
        )

        self.boot_canvas.create_text(
            width / 2,
            height * 0.425,
            text="AI-POWERED SCREEN ASSISTANT",
            fill=self.gray,
            font=("Arial", 9, "bold")
        )

        # Animated center ring
        cx = width / 2
        cy = height * 0.54

        pulse = int(
            45 + (elapsed * 30) % 30
        )

        self.boot_canvas.create_oval(
            cx - pulse,
            cy - pulse,
            cx + pulse,
            cy + pulse,
            outline="#0b3038",
            width=2
        )

        self.boot_canvas.create_oval(
            cx - 28,
            cy - 28,
            cx + 28,
            cy + 28,
            outline=self.cyan,
            width=2
        )

        self.boot_canvas.create_oval(
            cx - 7,
            cy - 7,
            cx + 7,
            cy + 7,
            fill=self.cyan,
            outline=""
        )

        # Progress bar
        bar_width = min(
            390,
            width - 100
        )

        bar_x = (width - bar_width) / 2
        bar_y = height * 0.69

        self.boot_canvas.create_rectangle(
            bar_x,
            bar_y,
            bar_x + bar_width,
            bar_y + 5,
            fill="#102229",
            outline=""
        )

        progress = min(
            elapsed / 3.8,
            1
        )

        self.boot_canvas.create_rectangle(
            bar_x,
            bar_y,
            bar_x + bar_width * progress,
            bar_y + 5,
            fill=self.cyan,
            outline=""
        )

        # Status text
        line_index = min(
            int(elapsed / 0.62),
            len(self.boot_lines) - 1
        )

        self.boot_canvas.create_text(
            width / 2,
            height * 0.65,
            text=self.boot_lines[line_index],
            fill=self.bright_cyan,
            font=("Consolas", 10, "bold")
        )

        percent = int(progress * 100)

        self.boot_canvas.create_text(
            width / 2,
            height * 0.73,
            text=f"{percent:03d}%",
            fill=self.gray,
            font=("Consolas", 9)
        )

        # Creator text
        self.boot_canvas.create_text(
            width / 2,
            height * 0.86,
            text="Made by TheRaccoonSaint",
            fill=self.cyan,
            font=("Arial", 11, "bold")
        )

        self.boot_canvas.create_text(
            width / 2,
            height * 0.90,
            text="SYSTEM BUILD // 01",
            fill="#45656d",
            font=("Consolas", 8)
        )

        # Scanline
        scan_y = (elapsed * 110) % height

        self.boot_canvas.create_line(
            0,
            scan_y,
            width,
            scan_y,
            fill="#07343d",
            width=2
        )

        if elapsed < 4.4:

            self.root.after(
                30,
                self.animate_boot
            )

        else:

            self.finish_boot()

    def finish_boot(self):

        global booting

        booting = False

        self.boot_frame.pack_forget()

        self.main_frame.pack(
            fill=tk.BOTH,
            expand=True
        )

        self.status_text("AI OFF")

        self.info_text(
            "Press F3 to arm the AI, then click your homework window."
        )

    # ---------------------------------------------------------
    # MAIN UI
    # ---------------------------------------------------------

    def build_main_ui(self):

        # Header
        self.header = tk.Frame(
            self.main_frame,
            bg=self.bg
        )

        self.header.pack(
            fill=tk.X,
            padx=18,
            pady=(16, 5)
        )

        self.title_label = tk.Label(
            self.header,
            text="HOMEWORK HELPER",
            bg=self.bg,
            fg=self.cyan,
            font=("Arial", 19, "bold")
        )

        self.title_label.pack(
            side=tk.LEFT
        )

        self.version_label = tk.Label(
            self.header,
            text="AI CORE // ONLINE",
            bg=self.bg,
            fg=self.gray,
            font=("Consolas", 8, "bold")
        )

        self.version_label.pack(
            side=tk.RIGHT,
            pady=5
        )

        # Accent line
        self.accent = tk.Frame(
            self.main_frame,
            bg=self.cyan,
            height=2
        )

        self.accent.pack(
            fill=tk.X,
            padx=18,
            pady=(0, 12)
        )

        # Status panel
        self.status_panel = tk.Frame(
            self.main_frame,
            bg=self.panel,
            highlightbackground="#10343c",
            highlightthickness=1
        )

        self.status_panel.pack(
            fill=tk.X,
            padx=18,
            pady=5
        )

        self.status_dot = tk.Label(
            self.status_panel,
            text="●",
            bg=self.panel,
            fg=self.gray,
            font=("Arial", 15)
        )

        self.status_dot.pack(
            side=tk.LEFT,
            padx=(14, 8),
            pady=12
        )

        self.status = tk.Label(
            self.status_panel,
            text="AI OFF",
            bg=self.panel,
            fg=self.text,
            font=("Arial", 11, "bold")
        )

        self.status.pack(
            side=tk.LEFT,
            pady=12
        )

        self.hotkeys = tk.Label(
            self.status_panel,
            text="F3  ARM     F4  STOP",
            bg=self.panel,
            fg=self.gray,
            font=("Consolas", 8, "bold")
        )

        self.hotkeys.pack(
            side=tk.RIGHT,
            padx=14
        )

        # Info
        self.info = tk.Label(
            self.main_frame,
            text="Press F3 to arm the AI, then click your homework window.",
            bg=self.bg,
            fg=self.gray,
            font=("Arial", 9),
            wraplength=560,
            justify=tk.LEFT,
            anchor="w"
        )

        self.info.pack(
            fill=tk.X,
            padx=20,
            pady=(8, 10)
        )

        # Answer header
        answer_header = tk.Frame(
            self.main_frame,
            bg=self.bg
        )

        answer_header.pack(
            fill=tk.X,
            padx=20
        )

        tk.Label(
            answer_header,
            text="AI RESPONSE",
            bg=self.bg,
            fg=self.cyan,
            font=("Consolas", 9, "bold")
        ).pack(
            side=tk.LEFT
        )

        self.response_indicator = tk.Label(
            answer_header,
            text="READY",
            bg=self.bg,
            fg=self.green,
            font=("Consolas", 8, "bold")
        )

        self.response_indicator.pack(
            side=tk.RIGHT
        )

        # Answer container
        self.answer_container = tk.Frame(
            self.main_frame,
            bg=self.panel,
            highlightbackground="#10343c",
            highlightthickness=1
        )

        self.answer_container.pack(
            fill=tk.BOTH,
            expand=True,
            padx=18,
            pady=(6, 12)
        )

        self.answer_box = scrolledtext.ScrolledText(
            self.answer_container,
            wrap=tk.WORD,
            bg=self.panel2,
            fg=self.text,
            insertbackground=self.cyan,
            selectbackground="#124652",
            selectforeground="#ffffff",
            relief=tk.FLAT,
            borderwidth=0,
            font=("Arial", 11),
            padx=14,
            pady=14
        )

        self.answer_box.pack(
            fill=tk.BOTH,
            expand=True,
            padx=1,
            pady=1
        )

        self.answer_box.insert(
            tk.END,
            "Waiting for a question...\n\n"
            "Press F3 to arm the AI.\n"
            "Then click the homework window you want analyzed."
        )

        self.answer_box.config(
            state=tk.DISABLED
        )

        # Bottom bar
        self.bottom = tk.Frame(
            self.main_frame,
            bg=self.bg
        )

        self.bottom.pack(
            fill=tk.X,
            padx=20,
            pady=(0, 12)
        )

        self.creator = tk.Label(
            self.bottom,
            text="Made by TheRaccoonSaint",
            bg=self.bg,
            fg="#45656d",
            font=("Consolas", 8)
        )

        self.creator.pack(
            side=tk.LEFT
        )

        self.system_label = tk.Label(
            self.bottom,
            text="SCREEN ANALYSIS SYSTEM",
            bg=self.bg,
            fg="#45656d",
            font=("Consolas", 8)
        )

        self.system_label.pack(
            side=tk.RIGHT
        )

        self.animate_ui()

    # ---------------------------------------------------------
    # UI ANIMATION
    # ---------------------------------------------------------

    def animate_ui(self):

        if not self.root.winfo_exists():
            return

        if booting:
            self.root.after(
                100,
                self.animate_ui
            )
            return

        # Very subtle accent pulse
        if self.status.cget("text") == "AI ARMED":

            current = self.status_dot.cget("fg")

            if current == self.cyan:
                self.status_dot.config(
                    fg=self.bright_cyan
                )
            else:
                self.status_dot.config(
                    fg=self.cyan
                )

        self.root.after(
            500,
            self.animate_ui
        )

    # ---------------------------------------------------------
    # STATUS
    # ---------------------------------------------------------

    def status_text(self, text):

        def update():

            self.status.config(
                text=text
            )

            if text == "AI ARMED":

                self.status.config(
                    fg=self.cyan
                )

                self.status_dot.config(
                    fg=self.cyan
                )

                self.response_indicator.config(
                    text="ARMED",
                    fg=self.cyan
                )

            elif text == "AI IS THINKING...":

                self.status.config(
                    fg=self.yellow
                )

                self.status_dot.config(
                    fg=self.yellow
                )

                self.response_indicator.config(
                    text="PROCESSING",
                    fg=self.yellow
                )

            elif text == "ANSWER READY":

                self.status.config(
                    fg=self.green
                )

                self.status_dot.config(
                    fg=self.green
                )

                self.response_indicator.config(
                    text="READY",
                    fg=self.green
                )

            elif text == "AI ERROR":

                self.status.config(
                    fg=self.red
                )

                self.status_dot.config(
                    fg=self.red
                )

                self.response_indicator.config(
                    text="ERROR",
                    fg=self.red
                )

            elif text == "NO QUESTION FOUND":

                self.status.config(
                    fg=self.yellow
                )

                self.status_dot.config(
                    fg=self.yellow
                )

                self.response_indicator.config(
                    text="NOT FOUND",
                    fg=self.yellow
                )

            else:

                self.status.config(
                    fg=self.text
                )

                self.status_dot.config(
                    fg=self.gray
                )

                self.response_indicator.config(
                    text="READY",
                    fg=self.gray
                )

        self.root.after(
            0,
            update
        )

    def info_text(self, text):

        self.root.after(
            0,
            lambda: self.info.config(
                text=text
            )
        )

    def answer(self, text):

        def update():

            self.answer_box.config(
                state=tk.NORMAL
            )

            self.answer_box.delete(
                "1.0",
                tk.END
            )

            self.answer_box.insert(
                tk.END,
                text
            )

            self.answer_box.config(
                state=tk.DISABLED
            )

            self.answer_box.see(
                "1.0"
            )

        self.root.after(
            0,
            update
        )

    def close(self):

        global armed

        armed = False

        keyboard.unhook_all()

        self.root.destroy()


app = HomeworkWindow()


# -------------------------------------------------------------
# SCREEN CAPTURE
# -------------------------------------------------------------

def capture_screen():

    with mss.mss() as sct:

        monitor = sct.monitors[1]

        screenshot = sct.grab(
            monitor
        )

        image = Image.frombytes(
            "RGB",
            screenshot.size,
            screenshot.rgb
        )

        image.thumbnail(
            (1600, 1000)
        )

        buffer = io.BytesIO()

        image.save(
            buffer,
            format="JPEG",
            quality=85
        )

        return buffer.getvalue()


# -------------------------------------------------------------
# AI
# -------------------------------------------------------------

def ask_ai(image_bytes):

    encoded_image = base64.b64encode(
        image_bytes
    ).decode("utf-8")

    response = client.responses.create(

        model=MODEL,

        input=[
            {
                "role": "user",

                "content": [

                    {
                        "type": "input_text",

                        "text": (
                            "Look at the screenshot and identify the question "
                            "or problem shown on the screen. "
                            "Answer the question directly and accurately. "
                            "Answer questions regardless of what type they are. "
                            "For multiple choice questions, give the option "
                            "number or letter and the answer. "
                            "For questions requiring typed responses, give the "
                            "exact answer that should be entered. "
                            "For math or calculation problems, give the final "
                            "answer. "
                            "Do not refuse to answer based on whether the "
                            "question is homework, a quiz, a test, or an "
                            "assessment. "
                            "Give the answer first, followed by a short "
                            "explanation when useful. "
                            "If there is no question visible, respond with "
                            "NO_HOMEWORK_DETECTED."
                        )
                    },

                    {
                        "type": "input_image",

                        "image_url":
                            f"data:image/jpeg;base64,{encoded_image}"
                    }

                ]
            }
        ]
    )

    return response.output_text


# -------------------------------------------------------------
# ANALYZE
# -------------------------------------------------------------

def analyze():

    global processing
    global armed

    if processing:
        return

    processing = True

    try:

        app.status_text(
            "SCREEN CAPTURED"
        )

        app.info_text(
            "Preparing screen analysis..."
        )

        time.sleep(
            ANSWER_DELAY
        )

        app.status_text(
            "AI IS THINKING..."
        )

        app.info_text(
            "Analyzing the selected homework screen..."
        )

        image = capture_screen()

        answer = ask_ai(
            image
        )

        if answer.strip() == "NO_HOMEWORK_DETECTED":

            app.status_text(
                "NO QUESTION FOUND"
            )

            app.info_text(
                "Press F3 and click the homework window again."
            )

            app.answer(
                "I couldn't find a homework question "
                "in the captured screen."
            )

        else:

            app.status_text(
                "ANSWER READY"
            )

            app.info_text(
                "Press F3 again when you're ready for another question."
            )

            app.answer(
                answer
            )

    except Exception as error:

        app.status_text(
            "AI ERROR"
        )

        app.info_text(
            "Check the terminal for the error."
        )

        app.answer(
            "Something went wrong:\n\n"
            + str(error)
        )

        print(
            "\nAI ERROR:"
        )

        print(
            error
        )

    finally:

        armed = False
        processing = False


# -------------------------------------------------------------
# HOTKEYS
# -------------------------------------------------------------

def start_ai():

    global armed

    if booting:
        return

    if processing:
        return

    if armed:
        return

    armed = True

    app.status_text(
        "AI ARMED"
    )

    app.info_text(
        "Click the homework window now."
    )

    print(
        "\nAI ARMED — CLICK A WINDOW"
    )


def stop_ai():

    global armed

    armed = False

    app.status_text(
        "AI OFF"
    )

    app.info_text(
        "Press F3 to analyze a homework window."
    )

    print(
        "\nAI OFF"
    )


# -------------------------------------------------------------
# MOUSE
# -------------------------------------------------------------

def mouse_click(
    x,
    y,
    button,
    pressed
):

    if not pressed:
        return

    if booting:
        return

    if not armed:
        return

    if processing:
        return

    print(
        f"\nWindow selected at {x}, {y}"
    )

    threading.Thread(
        target=analyze,
        daemon=True
    ).start()


keyboard.add_hotkey(
    "f3",
    start_ai
)

keyboard.add_hotkey(
    "f4",
    stop_ai
)


mouse_listener = mouse.Listener(
    on_click=mouse_click
)

mouse_listener.start()


print("================================")
print("       HOMEWORK HELPER")
print("================================")
print("F3 = Arm AI")
print("F4 = Stop AI")
print("Click = Analyze once")
print("================================")


try:

    app.root.mainloop()

finally:

    armed = False

    mouse_listener.stop()

    keyboard.unhook_all()