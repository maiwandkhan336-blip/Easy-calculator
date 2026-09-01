from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.core.clipboard import Clipboard
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.animation import Animation

import math
import os
import json


class EasyCalculator(App):

    def build(self):

        self.dark_mode = False
        self.scientific_mode = False
        self.degree_mode = True

        self.memory = 0.0
        self.last_answer = 0.0

        self.history_file = os.path.join(
            self.user_data_dir,
            "calculator_history.json"
        )

        self.history_data = []
        self.load_history()

        self.main = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=7
        )

        # =========================
        # HISTORY
        # =========================

        self.history_scroll = ScrollView(
            size_hint_y=None,
            height=0,
            do_scroll_x=False,
            do_scroll_y=True
        )

        self.history_layout = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=5,
            padding=5
        )

        self.history_layout.bind(
            minimum_height=self.history_layout.setter("height")
        )

        self.history_scroll.add_widget(
            self.history_layout
        )

        self.main.add_widget(
            self.history_scroll
        )

        # =========================
        # TOP BUTTONS
        # =========================

        top_buttons = BoxLayout(
            size_hint_y=None,
            height=45,
            spacing=5
        )

        self.history_button = Button(
            text="HISTORY",
            font_size=14,
            bold=True,
            background_normal=""
        )

        self.mode_button = Button(
            text="SCIENTIFIC",
            font_size=14,
            bold=True,
            background_normal=""
        )

        self.theme_button = Button(
            text="DARK",
            font_size=14,
            bold=True,
            background_normal=""
        )

        self.history_button.bind(
            on_press=self.toggle_history
        )

        self.mode_button.bind(
            on_press=self.toggle_scientific
        )

        self.theme_button.bind(
            on_press=self.toggle_theme
        )

        top_buttons.add_widget(
            self.history_button
        )

        top_buttons.add_widget(
            self.mode_button
        )

        top_buttons.add_widget(
            self.theme_button
        )

        self.main.add_widget(
            top_buttons
        )

        # =========================
        # MEMORY
        # =========================

        self.memory_label = Button(
            text="M: 0",
            font_size=14,
            bold=True,
            background_normal="",
            size_hint_y=None,
            height=35
        )

        self.memory_label.disabled = True

        self.main.add_widget(
            self.memory_label
        )

        # =========================
        # DEG / RAD
        # =========================

        self.angle_button = Button(
            text="DEG",
            font_size=14,
            bold=True,
            background_normal="",
            size_hint_y=None,
            height=35
        )

        self.angle_button.bind(
            on_press=self.toggle_angle
        )

        self.main.add_widget(
            self.angle_button
        )

        # =========================
        # DISPLAY
        # =========================

        self.display = TextInput(
            text="0",
            multiline=False,
            halign="right",
            font_size=52,
            size_hint_y=0.20
        )

        self.main.add_widget(
            self.display
        )

        # =========================
        # GRID
        # =========================

        self.grid = GridLayout(
            cols=4,
            spacing=6
        )

        self.buttons = []

        self.create_basic_buttons()

        self.main.add_widget(
            self.grid
        )

        # =========================
        # COPY
        # =========================

        self.copy_button = Button(
            text="COPY",
            font_size=16,
            bold=True,
            background_normal="",
            size_hint_y=None,
            height=42
        )

        self.copy_button.bind(
            on_press=self.copy_result
        )

        self.main.add_widget(
            self.copy_button
        )

        # =========================
        # CLEAR HISTORY
        # =========================

        self.clear_button = Button(
            text="CLEAR HISTORY",
            font_size=16,
            bold=True,
            background_normal="",
            size_hint_y=None,
            height=42
        )

        self.clear_button.bind(
            on_press=self.ask_clear_history
        )

        self.main.add_widget(
            self.clear_button
        )

        self.apply_theme()
        self.refresh_history()

        return self.main

    # =========================================================
    # BUTTON ANIMATION
    # =========================================================

    def button_animation(self, button):

        original_size = button.font_size

        Animation.cancel_all(
            button,
            "font_size"
        )

        animation = Animation(
            font_size=original_size * 0.90,
            duration=0.05
        )

        animation += Animation(
            font_size=original_size,
            duration=0.08
        )

        animation.start(button)

    # =========================================================
    # COLORS
    # =========================================================

    def update_colors(self):

        if self.dark_mode:

            self.background_color = (
                0.06, 0.07, 0.09, 1
            )

            self.display_color = (
                0.10, 0.11, 0.14, 1
            )

            self.text_color = (
                0.95, 0.95, 0.95, 1
            )

            self.history_color = (
                0.11, 0.12, 0.15, 1
            )

            self.number_color = (
                0.12, 0.14, 0.17, 1
            )

            self.function_color = (
                0.22, 0.24, 0.28, 1
            )

            self.operator_color = (
                0.20, 0.48, 0.95, 1
            )

        else:

            self.background_color = (
                0.96, 0.96, 0.97, 1
            )

            self.display_color = (
                1, 1, 1, 1
            )

            self.text_color = (
                0.09, 0.13, 0.17, 1
            )

            self.history_color = (
                0.93, 0.94, 0.96, 1
            )

            self.number_color = (
                0.09, 0.13, 0.17, 1
            )

            self.function_color = (
                0.90, 0.91, 0.93, 1
            )

            self.operator_color = (
                0.23, 0.51, 0.96, 1
            )

    # =========================================================
    # THEME
    # =========================================================

    def apply_theme(self):

        self.update_colors()

        Window.clearcolor = self.background_color

        if hasattr(self, "display"):

            self.display.background_color = (
                self.display_color
            )

            self.display.foreground_color = (
                self.text_color
            )

        if hasattr(self, "history_button"):

            items = [
                self.history_button,
                self.mode_button,
                self.theme_button,
                self.angle_button,
                self.memory_label
            ]

            if hasattr(self, "clear_button"):
                items.append(self.clear_button)

            for button in items:

                button.background_color = (
                    self.function_color
                )

                button.color = (
                    self.text_color
                )

            if hasattr(self, "copy_button"):

                self.copy_button.background_color = (
                    self.operator_color
                )

                self.copy_button.color = (
                    1, 1, 1, 1
                )

        for button in self.buttons:

            name = button.text

            if name == "":
                continue

            if (
                name.isdigit()
                or name == "."
            ):

                button.background_color = (
                    self.number_color
                )

                button.color = (
                    1, 1, 1, 1
                )

            elif name in [
                "+",
                "−",
                "×",
                "÷",
                "="
            ]:

                button.background_color = (
                    self.operator_color
                )

                button.color = (
                    1, 1, 1, 1
                )

            else:

                button.background_color = (
                    self.function_color
                )

                button.color = (
                    self.text_color
                )

        if hasattr(self, "history_layout"):
            self.refresh_history()

    # =========================================================
    # BUTTON FONT SIZE
    # =========================================================

    def get_button_font_size(self, name):

        if (
            name.isdigit()
            or name == "."
            or name in [
                "+",
                "−",
                "×",
                "÷",
                "=",
                "C",
                "CE"
            ]
        ):

            return 32

        return 20

    # =========================================================
    # BASIC BUTTONS
    # =========================================================

    def create_basic_buttons(self):

        self.grid.clear_widgets()

        names = [
            "MC", "MR", "M+", "M−",
            "MS", "CE", "C", "⌫",
            "√", "x²", "xʸ", "%",
            "7", "8", "9", "÷",
            "4", "5", "6", "×",
            "1", "2", "3", "−",
            "0", ".", "±", "+",
            "=", "1/x", "Ans", ""
        ]

        self.buttons = []

        for name in names:

            button = Button(
                text=name,
                font_size=self.get_button_font_size(name),
                bold=True,
                background_normal=""
            )

            if name != "":
                button.bind(
                    on_press=self.press
                )
            else:
                button.disabled = True

            self.buttons.append(button)

            self.grid.add_widget(
                button
            )

    # =========================================================
    # SCIENTIFIC BUTTONS
    # =========================================================

    def create_scientific_buttons(self):

        self.grid.clear_widgets()

        names = [
            "MC", "MR", "M+", "M−",
            "MS", "sin", "cos", "tan",
            "asin", "acos", "atan", "π",
            "log", "ln", "10ˣ", "e",
            "√", "x²", "xʸ", "!",
            "CE", "C", "%", "⌫",
            "7", "8", "9", "÷",
            "4", "5", "6", "×",
            "1", "2", "3", "−",
            "0", ".", "±", "+",
            "=", "1/x", "Ans", "()"
        ]

        self.buttons = []

        for name in names:

            button = Button(
                text=name,
                font_size=self.get_button_font_size(name),
                bold=True,
                background_normal=""
            )

            button.bind(
                on_press=self.press
            )

            self.buttons.append(button)

            self.grid.add_widget(
                button
            )

        self.apply_theme()

    # =========================================================
    # SCIENTIFIC MODE
    # =========================================================

    def toggle_scientific(self, button):

        self.button_animation(button)

        self.scientific_mode = (
            not self.scientific_mode
        )

        if self.scientific_mode:

            self.mode_button.text = "BASIC"

            self.create_scientific_buttons()

        else:

            self.mode_button.text = "SCIENTIFIC"

            self.create_basic_buttons()

            self.apply_theme()

    # =========================================================
    # DEG / RAD
    # =========================================================

    def toggle_angle(self, button):

        self.button_animation(button)

        self.degree_mode = (
            not self.degree_mode
        )

        if self.degree_mode:

            self.angle_button.text = "DEG"

        else:

            self.angle_button.text = "RAD"

    # =========================================================
    # DARK MODE
    # =========================================================

    def toggle_theme(self, button):

        self.button_animation(button)

        self.dark_mode = (
            not self.dark_mode
        )

        if self.dark_mode:

            self.theme_button.text = "LIGHT"

        else:

            self.theme_button.text = "DARK"

        self.apply_theme()

    # =========================================================
    # MEMORY
    # =========================================================

    def update_memory_display(self):

        try:

            value = self.format_result(
                self.memory
            )

        except Exception:

            value = "0"

        self.memory_label.text = (
            "M: " + value
        )

    def memory_clear(self):

        self.memory = 0.0

        self.update_memory_display()

    def memory_recall(self):

        value = self.format_result(
            self.memory
        )

        if self.display.text in [
            "0",
            "Error",
            "Invalid"
        ]:

            self.display.text = value

        else:

            self.display.text += value

    def memory_add(self):

        value = self.get_display_number()

        self.memory += value

        self.update_memory_display()

    def memory_subtract(self):

        value = self.get_display_number()

        self.memory -= value

        self.update_memory_display()

    def memory_store(self):

        value = self.get_display_number()

        self.memory = value

        self.update_memory_display()

    def get_display_number(self):

        text = self.display.text.strip()

        if text in [
            "",
            "Error",
            "Invalid"
        ]:

            raise ValueError()

        expression = (
            text
            .replace("×", "*")
            .replace("÷", "/")
            .replace("−", "-")
        )

        return float(
            self.safe_eval(expression)
        )

    # =========================================================
    # HISTORY
    # =========================================================

    def load_history(self):

        try:

            if os.path.exists(
                self.history_file
            ):

                with open(
                    self.history_file,
                    "r",
                    encoding="utf-8"
                ) as file:

                    data = json.load(file)

                    if isinstance(data, list):

                        self.history_data = data

        except Exception:

            self.history_data = []

    def save_history(self):

        try:

            with open(
                self.history_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    self.history_data,
                    file,
                    ensure_ascii=False,
                    indent=2
                )

        except Exception:

            pass

    def toggle_history(self, button):

        self.button_animation(button)

        if self.history_scroll.height == 0:

            self.history_scroll.height = 500

            button.text = "HIDE HISTORY"

        else:

            self.history_scroll.height = 0

            button.text = "HISTORY"

    def refresh_history(self):

        if not hasattr(
            self,
            "history_layout"
        ):
            return

        self.history_layout.clear_widgets()

        for index, item in enumerate(
            self.history_data
        ):

            self.create_history_row(
                index,
                item
            )

        Clock.schedule_once(
            self.scroll_history_bottom,
            0.1
        )

    def create_history_row(
        self,
        index,
        item
    ):

        row = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=55,
            spacing=4
        )

        expression = item.get(
            "expression",
            ""
        )

        result = item.get(
            "result",
            ""
        )

        text = TextInput(
            text=(
                expression
                + " = "
                + result
            ),
            readonly=True,
            multiline=False,
            font_size=17,
            size_hint_x=0.62,
            background_color=(
                self.history_color
            ),
            foreground_color=(
                self.text_color
            )
        )

        copy_button = Button(
            text="COPY",
            font_size=13,
            bold=True,
            size_hint_x=0.19,
            background_normal="",
            background_color=(
                self.operator_color
            ),
            color=(1, 1, 1, 1)
        )

        delete_button = Button(
            text="DELETE",
            font_size=12,
            bold=True,
            size_hint_x=0.19,
            background_normal="",
            background_color=(
                self.function_color
            ),
            color=(
                self.text_color
            )
        )

        copy_button.bind(
            on_press=lambda btn:
            self.copy_history_item(
                btn,
                result
            )
        )

        delete_button.bind(
            on_press=lambda btn:
            self.ask_delete_history_item(
                index
            )
        )

        row.add_widget(text)
        row.add_widget(copy_button)
        row.add_widget(delete_button)

        self.history_layout.add_widget(
            row
        )

    def add_history(
        self,
        expression,
        result
    ):

        self.history_data.append({
            "expression": expression,
            "result": result
        })

        try:

            self.last_answer = float(
                result
            )

        except Exception:

            pass

        self.save_history()

        self.refresh_history()

    # =========================================================
    # DELETE HISTORY ITEM
    # =========================================================

    def ask_delete_history_item(
        self,
        index
    ):

        if not (
            0 <= index
            < len(self.history_data)
        ):

            return

        item = self.history_data[index]

        expression = item.get(
            "expression",
            ""
        )

        result = item.get(
            "result",
            ""
        )

        content = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=10
        )

        message = TextInput(
            text=(
                "Delete this calculation?\n\n"
                + expression
                + " = "
                + result
            ),
            readonly=True,
            multiline=True,
            font_size=17,
            background_color=(
                self.display_color
            ),
            foreground_color=(
                self.text_color
            )
        )

        buttons = BoxLayout(
            size_hint_y=None,
            height=50,
            spacing=10
        )

        yes_button = Button(
            text="YES",
            bold=True,
            background_normal="",
            background_color=(
                self.operator_color
            ),
            color=(1, 1, 1, 1)
        )

        cancel_button = Button(
            text="CANCEL",
            bold=True,
            background_normal="",
            background_color=(
                self.function_color
            ),
            color=(
                self.text_color
            )
        )

        buttons.add_widget(
            yes_button
        )

        buttons.add_widget(
            cancel_button
        )

        content.add_widget(
            message
        )

        content.add_widget(
            buttons
        )

        popup = Popup(
            title="Delete History",
            content=content,
            size_hint=(0.90, None),
            height=230,
            auto_dismiss=False
        )

        yes_button.bind(
            on_press=lambda btn:
            self.confirm_delete_history_item(
                popup,
                index
            )
        )

        cancel_button.bind(
            on_press=popup.dismiss
        )

        popup.open()

    def confirm_delete_history_item(
        self,
        popup,
        index
    ):

        if (
            0 <= index
            < len(self.history_data)
        ):

            del self.history_data[index]

            self.save_history()

            self.refresh_history()

        popup.dismiss()

    # =========================================================
    # CLEAR HISTORY
    # =========================================================

    def ask_clear_history(
        self,
        button
    ):

        self.button_animation(button)

        if not self.history_data:

            return

        content = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=10
        )

        message = TextInput(
            text=(
                "Are you sure you want to "
                "clear ALL history?\n\n"
                "This action cannot be undone."
            ),
            readonly=True,
            multiline=True,
            font_size=17,
            background_color=(
                self.display_color
            ),
            foreground_color=(
                self.text_color
            )
        )

        buttons = BoxLayout(
            size_hint_y=None,
            height=50,
            spacing=10
        )

        yes_button = Button(
            text="YES, CLEAR",
            bold=True,
            background_normal="",
            background_color=(
                self.operator_color
            ),
            color=(1, 1, 1, 1)
        )

        cancel_button = Button(
            text="CANCEL",
            bold=True,
            background_normal="",
            background_color=(
                self.function_color
            ),
            color=(
                self.text_color
            )
        )

        buttons.add_widget(
            yes_button
        )

        buttons.add_widget(
            cancel_button
        )

        content.add_widget(
            message
        )

        content.add_widget(
            buttons
        )

        popup = Popup(
            title="Clear All History",
            content=content,
            size_hint=(0.90, None),
            height=230,
            auto_dismiss=False
        )

        yes_button.bind(
            on_press=lambda btn:
            self.confirm_clear_history(
                popup
            )
        )

        cancel_button.bind(
            on_press=popup.dismiss
        )

        popup.open()

    def confirm_clear_history(
        self,
        popup
    ):

        self.history_data = []

        self.last_answer = 0.0

        self.save_history()

        self.refresh_history()

        popup.dismiss()

    # =========================================================
    # FORMAT RESULT
    # =========================================================

    def format_result(
        self,
        value
    ):

        if not math.isfinite(value):

            raise ValueError()

        if abs(
            value - round(value)
        ) < 1e-12:

            return str(
                int(round(value))
            )

        return (
            f"{value:.10f}"
            .rstrip("0")
            .rstrip(".")
        )

    # =========================================================
    # NUMBER INPUT
    # =========================================================

    def insert_number(
        self,
        value
    ):

        if self.display.text in [
            "0",
            "Error",
            "Invalid"
        ]:

            self.display.text = value

        else:

            self.display.text += value

    # =========================================================
    # DECIMAL
    # =========================================================

    def insert_decimal(self):

        text = self.display.text

        if text in [
            "Error",
            "Invalid"
        ]:

            self.display.text = "0."

            return

        current = ""

        for char in reversed(text):

            if (
                char.isdigit()
                or char == "."
            ):

                current = char + current

            else:

                break

        if "." not in current:

            if text == "0":

                self.display.text = "0."

            else:

                self.display.text += "."

    # =========================================================
    # OPERATOR
    # =========================================================

    def insert_operator(
        self,
        operator
    ):

        text = self.display.text

        if text in [
            "Error",
            "Invalid"
        ]:

            self.display.text = "0"

            return

        if text == "0":

            if operator == "-":

                self.display.text = "-"

            else:

                self.display.text = operator

            return

        if text == "-":

            return

        if text[-1] in "+-*/":

            self.display.text = (
                text[:-1]
                + operator
            )

        else:

            self.display.text += operator

    # =========================================================
    # SIGN
    # =========================================================

    def toggle_sign(self):

        text = self.display.text

        if text in [
            "0",
            "Error",
            "Invalid"
        ]:

            return

        number = float(text)

        self.display.text = (
            self.format_result(
                -number
            )
        )

    # =========================================================
    # POWER
    # =========================================================

    def insert_power(self):

        text = self.display.text

        if text in [
            "Error",
            "Invalid"
        ]:

            self.display.text = "0"

            return

        if not text.endswith("**"):

            self.display.text += "**"

    # =========================================================
    # PERCENT
    # =========================================================

    def calculate_percentage(self):

        text = self.display.text

        number = float(text)

        result = number / 100

        output = self.format_result(
            result
        )

        self.add_history(
            text + "%",
            output
        )

        self.display.text = output

    # =========================================================
    # SQUARE ROOT
    # =========================================================

    def square_root(self):

        text = self.display.text

        number = float(text)

        result = math.sqrt(number)

        output = self.format_result(
            result
        )

        self.add_history(
            "√" + text,
            output
        )

        self.display.text = output

    # =========================================================
    # SQUARE
    # =========================================================

    def square(self):

        text = self.display.text

        number = float(text)

        result = number ** 2

        output = self.format_result(
            result
        )

        self.add_history(
            text + "²",
            output
        )

        self.display.text = output

    # =========================================================
    # FACTORIAL
    # =========================================================

    def factorial(self):

        text = self.display.text

        number = float(text)

        if number < 0:
            raise ValueError()

        if not number.is_integer():
            raise ValueError()

        if number > 170:
            raise ValueError()

        result = math.factorial(
            int(number)
        )

        output = self.format_result(
            float(result)
        )

        self.add_history(
            text + "!",
            output
        )

        self.display.text = output

    # =========================================================
    # RECIPROCAL
    # =========================================================

    def reciprocal(self):

        text = self.display.text

        number = float(text)

        if number == 0:

            raise ZeroDivisionError()

        result = 1 / number

        output = self.format_result(
            result
        )

        self.add_history(
            "1/" + text,
            output
        )

        self.display.text = output

    # =========================================================
    # 10 POWER
    # =========================================================

    def power_ten(self):

        text = self.display.text

        number = float(text)

        result = 10 ** number

        output = self.format_result(
            result
        )

        self.add_history(
            "10^" + text,
            output
        )

        self.display.text = output

    # =========================================================
    # TRIGONOMETRY
    # =========================================================

    def trigonometric(
        self,
        function
    ):

        text = self.display.text

        number = float(text)

        if function == "sin":

            if self.degree_mode:

                result = math.sin(
                    math.radians(number)
                )

            else:

                result = math.sin(number)

        elif function == "cos":

            if self.degree_mode:

                result = math.cos(
                    math.radians(number)
                )

            else:

                result = math.cos(number)

        elif function == "tan":

            if self.degree_mode:

                result = math.tan(
                    math.radians(number)
                )

            else:

                result = math.tan(number)

        elif function == "asin":

            result = math.asin(number)

            if self.degree_mode:

                result = math.degrees(
                    result
                )

        elif function == "acos":

            result = math.acos(number)

            if self.degree_mode:

                result = math.degrees(
                    result
                )

        elif function == "atan":

            result = math.atan(number)

            if self.degree_mode:

                result = math.degrees(
                    result
                )

        else:

            raise ValueError()

        output = self.format_result(
            result
        )

        self.add_history(
            function
            + "("
            + text
            + ")",
            output
        )

        self.display.text = output

    # =========================================================
    # LOG
    # =========================================================

    def logarithm(self):

        text = self.display.text

        number = float(text)

        result = math.log10(number)

        output = self.format_result(
            result
        )

        self.add_history(
            "log(" + text + ")",
            output
        )

        self.display.text = output

    # =========================================================
    # NATURAL LOG
    # =========================================================

    def natural_log(self):

        text = self.display.text

        number = float(text)

        result = math.log(number)

        output = self.format_result(
            result
        )

        self.add_history(
            "ln(" + text + ")",
            output
        )

        self.display.text = output

    # =========================================================
    # LAST ANSWER
    # =========================================================

    def use_last_answer(self):

        if not self.history_data:

            return

        result = self.history_data[-1].get(
            "result",
            "0"
        )

        if self.display.text == "0":

            self.display.text = result

        else:

            self.display.text += result

    # =========================================================
    # BRACKETS
    # =========================================================

    def insert_bracket_pair(self):

        if self.display.text == "0":

            self.display.text = "()"

        else:

            self.display.text += "()"

    # =========================================================
    # CLEAR ALL
    # =========================================================

    def clear_all(self):

        self.display.text = "0"

    # =========================================================
    # CLEAR ENTRY
    # =========================================================

    def clear_entry(self):

        text = self.display.text

        if text in [
            "",
            "Error",
            "Invalid"
        ]:

            self.display.text = "0"

            return

        if not any(
            op in text
            for op in "+-*/"
        ):

            self.display.text = "0"

            return

        text = text.strip()

        if text[-1] in "+-*/":

            self.display.text = (
                text[:-1]
            )

            if self.display.text == "":

                self.display.text = "0"

            return

        last_operator = -1

        for i in range(
            len(text) - 1,
            0,
            -1
        ):

            if text[i] in "+-*/":

                last_operator = i

                break

        if last_operator == -1:

            self.display.text = "0"

        else:

            left_side = (
                text[:last_operator + 1]
            )

            self.display.text = (
                left_side + "0"
            )

    # =========================================================
    # BACKSPACE
    # =========================================================

    def backspace(self):

        text = self.display.text

        if text in [
            "",
            "0",
            "Error",
            "Invalid"
        ]:

            self.display.text = "0"

            return

        self.display.text = text[:-1]

        if self.display.text in [
            "",
            "-"
        ]:

            self.display.text = "0"

    # =========================================================
    # BUTTON PRESS
    # =========================================================

    def press(
        self,
        button
    ):

        # BUTTON ANIMATION
        self.button_animation(button)

        value = button.text

        try:

            if value == "MC":

                self.memory_clear()

            elif value == "MR":

                self.memory_recall()

            elif value == "M+":

                self.memory_add()

            elif value == "M−":

                self.memory_subtract()

            elif value == "MS":

                self.memory_store()

            elif value.isdigit():

                self.insert_number(
                    value
                )

            elif value == ".":

                self.insert_decimal()

            elif value in [
                "+",
                "−",
                "×",
                "÷"
            ]:

                operators = {
                    "+": "+",
                    "−": "-",
                    "×": "*",
                    "÷": "/"
                }

                self.insert_operator(
                    operators[value]
                )

            elif value == "xʸ":

                self.insert_power()

            elif value == "π":

                self.insert_constant(
                    math.pi
                )

            elif value == "e":

                self.insert_constant(
                    math.e
                )

            elif value == "Ans":

                self.use_last_answer()

            elif value == "C":

                self.clear_all()

            elif value == "CE":

                self.clear_entry()

            elif value == "⌫":

                self.backspace()

            elif value == "±":

                self.toggle_sign()

            elif value == "%":

                self.calculate_percentage()

            elif value == "√":

                self.square_root()

            elif value == "x²":

                self.square()

            elif value == "!":

                self.factorial()

            elif value == "1/x":

                self.reciprocal()

            elif value == "10ˣ":

                self.power_ten()

            elif value in [
                "sin",
                "cos",
                "tan",
                "asin",
                "acos",
                "atan"
            ]:

                self.trigonometric(
                    value
                )

            elif value == "log":

                self.logarithm()

            elif value == "ln":

                self.natural_log()

            elif value == "()":

                self.insert_bracket_pair()

            elif value == "=":

                self.calculate()

        except Exception:

            self.display.text = "Error"

    # =========================================================
    # CONSTANT
    # =========================================================

    def insert_constant(
        self,
        value
    ):

        text = self.display.text

        if text in [
            "0",
            "Error",
            "Invalid"
        ]:

            self.display.text = str(
                value
            )

        else:

            if text[-1].isdigit():

                self.display.text += "*"

            self.display.text += str(
                value
            )

    # =========================================================
    # CALCULATE
    # =========================================================

    def calculate(self):

        original = self.display.text

        expression = (
            original
            .replace("×", "*")
            .replace("÷", "/")
            .replace("−", "-")
        )

        try:

            if expression in [
                "",
                "-"
            ]:

                raise ValueError()

            while (
                expression
                and expression[-1]
                in "+-*/"
            ):

                expression = expression[:-1]

            if not expression:

                raise ValueError()

            result = self.safe_eval(
                expression
            )

            output = self.format_result(
                float(result)
            )

            self.add_history(
                original,
                output
            )

            self.last_answer = float(
                result
            )

            self.display.text = output

        except Exception:

            self.display.text = "Error"

    # =========================================================
    # SAFE EVAL
    # =========================================================

    def safe_eval(
        self,
        expression
    ):

        allowed = set(
            "0123456789."
            "+-*/() "
        )

        if not expression:

            raise ValueError()

        if any(
            character not in allowed
            for character in expression
        ):

            raise ValueError()

        return eval(
            expression,
            {
                "__builtins__": {}
            },
            {}
        )

    # =========================================================
    # COPY RESULT
    # =========================================================

    def copy_result(
        self,
        button
    ):

        self.button_animation(button)

        Clipboard.copy(
            self.display.text
        )

        button.text = "COPIED!"

        Clock.schedule_once(
            lambda dt:
            self.reset_copy(button),
            1
        )

    def reset_copy(
        self,
        button
    ):

        button.text = "COPY"

    # =========================================================
    # COPY HISTORY
    # =========================================================

    def copy_history_item(
        self,
        button,
        result
    ):

        self.button_animation(button)

        Clipboard.copy(
            result
        )

        button.text = "COPIED"

        Clock.schedule_once(
            lambda dt:
            self.reset_history_copy(button),
            1
        )

    def reset_history_copy(
        self,
        button
    ):

        button.text = "COPY"

    # =========================================================
    # SCROLL HISTORY
    # =========================================================

    def scroll_history_bottom(
        self,
        dt
    ):

        self.history_scroll.scroll_y = 0


EasyCalculator().run()