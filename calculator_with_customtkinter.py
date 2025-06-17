import customtkinter as ctk
import math


class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Professional Calculator")
        self.root.geometry("400x600")
        self.root.minsize(300, 450)

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.expression = ctk.StringVar()
        self.current_input = ""
        self.is_result_shown = False

        self.create_widgets()
        self.configure_grid_responsiveness()
        self.bind_keyboard_events()

    def create_widgets(self):
        display_frame = ctk.CTkFrame(self.root, fg_color="#333333")
        display_frame.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)
        display_frame.grid_rowconfigure(0, weight=1)
        display_frame.grid_columnconfigure(0, weight=1)

        # CORRECTED LINE: Import CTkFont directly from ctk
        display_font = ctk.CTkFont(family="Arial", size=36, weight="bold")
        self.display_label = ctk.CTkLabel(
            display_frame,
            textvariable=self.expression,
            font=display_font,
            text_color="white",
            anchor="e",
            padx=10,
            pady=10,
            wraplength=380
        )
        self.display_label.grid(row=0, column=0, sticky="nsew")

        buttons_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        buttons_frame.grid(row=1, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)

        for i in range(4):
            buttons_frame.grid_columnconfigure(i, weight=1)
        for i in range(6):
            buttons_frame.grid_rowconfigure(i, weight=1)

        buttons = [
            ('AC', 1, 0, '#FF5733'), ('DEL', 1, 1, '#FF5733'), ('%', 1, 2, '#FFC300'), ('/', 1, 3, '#FFC300'),
            ('7', 2, 0, '#555555'), ('8', 2, 1, '#555555'), ('9', 2, 2, '#555555'), ('*', 2, 3, '#FFC300'),
            ('4', 3, 0, '#555555'), ('5', 3, 1, '#555555'), ('6', 3, 2, '#555555'), ('-', 3, 3, '#FFC300'),
            ('1', 4, 0, '#555555'), ('2', 4, 1, '#555555'), ('3', 4, 2, '#555555'), ('+', 4, 3, '#FFC300'),
            ('00', 5, 0, '#555555'), ('0', 5, 1, '#555555'), ('.', 5, 2, '#555555'), ('=', 5, 3, '#4CAF50')
        ]

        button_font = ctk.CTkFont(family="Arial", size=20, weight="bold")  # CORRECTED LINE

        for (text, row, col, color) in buttons:
            btn = ctk.CTkButton(
                buttons_frame,
                text=text,
                font=button_font,
                fg_color=color,
                hover_color=self.darken_color(color, 20),
                text_color="white",
                command=lambda t=text: self.on_button_click(t),
                corner_radius=10
            )
            btn.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)

    def configure_grid_responsiveness(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=3)
        self.root.grid_columnconfigure(0, weight=1)

    def bind_keyboard_events(self):
        self.root.bind("<Key>", self.on_key_press)
        self.root.bind("<BackSpace>", lambda event: self.on_button_click('DEL'))
        self.root.bind("<Return>", lambda event: self.on_button_click('='))
        self.root.bind("<KP_Enter>", lambda event: self.on_button_click('='))

    def on_button_click(self, char):
        if self.is_result_shown and char not in ['AC', 'DEL', '=', '%', '+', '-', '*', '/']:
            self.current_input = ""
            self.is_result_shown = False

        self.is_result_shown = False

        if char == 'AC':
            self.current_input = ""
            self.expression.set("")
        elif char == 'DEL':
            self.current_input = self.current_input[:-1]
            self.expression.set(self.current_input)
        elif char == '=':
            try:
                expression_to_eval = self.current_input.replace('%', '/100')
                result = eval(expression_to_eval)
                self.expression.set(str(result))
                self.current_input = str(result)
                self.is_result_shown = True
            except ZeroDivisionError:
                self.expression.set("Error: Div by Zero")
                self.current_input = ""
                self.is_result_shown = True
            except Exception:
                self.expression.set("Error")
                self.current_input = ""
                self.is_result_shown = True
        else:
            if self.current_input and self.is_operator(char) and self.is_operator(self.current_input[-1]):
                self.current_input = self.current_input[:-1] + char
            else:
                self.current_input += char
            self.expression.set(self.current_input)

    def on_key_press(self, event):
        key = event.char
        if key.isdigit() or key in ['.', '+', '-', '*', '/', '%']:
            self.on_button_click(key)
        elif key == '\r':
            self.on_button_click('=')
        elif key == '\x08':
            self.on_button_click('DEL')

    def is_operator(self, char):
        return char in ['+', '-', '*', '/', '%']

    def darken_color(self, hex_color, amount):
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        darkened_rgb = tuple(max(0, c - amount) for c in rgb)
        return '#%02x%02x%02x' % darkened_rgb


if __name__ == "__main__":
    root = ctk.CTk()
    app = CalculatorApp(root)
    root.mainloop()