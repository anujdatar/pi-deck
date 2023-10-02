from functools import partial
from tkinter import Button, Frame, IntVar, PhotoImage, Radiobutton, Tk, ttk
from typing import List, Optional, Callable

from src import Key, KeymapTab, keymap_json_loader, send_serial_msg


def dummy_function() -> None:
    print("Hi! I am button...")


def print_command(a: str) -> None:
    print(f"commend: {a}")


class DeckButton(Button):
    def __init__(
        self,
        parent: Optional[Frame] = None,
        text: str = "",
        command: Callable[[], None] = dummy_function,
    ):
        super().__init__(parent)
        self.configure(text=text)
        self.configure(command=command)


class DeckImgButton(Button):
    def __init__(
        self,
        parent: Optional[Frame] = None,
        image_path: str = "",
        command: Callable[[], None] = dummy_function,
    ):
        super().__init__(parent)
        self.btn_image = PhotoImage(file=image_path)
        self.configure(image=self.btn_image)
        self.configure(command=command)


class DeckFrame(Frame):
    def __init__(self, parent: Tk):
        super().__init__(parent)
        self.pack(fill="both", expand=True)


class DeckModal(Toplevel):
    def __init__(self, parent: Tk, title: str = ""):
        super().__init__(parent)
        self.title(title)
        self.grab_set()
        self.transient(parent)

    def close(self) -> None:
        self.grab_release()
        self.destroy()


def open_power_dialog(parent: Tk, title: str = "") -> DeckModal:
    power_dialog = DeckModal(parent, title)
    power_dialog.title("Power Menu")

    quit_btn = Button(power_dialog, text="Quit", command=parent.quit)
    quit_btn.pack(side="left", anchor="center", padx=5, pady=10)

    reboot_btn = Button(power_dialog, text="Reboot", command=reboot)
    reboot_btn.pack(side="left", anchor="center", padx=5, pady=10)

    shutdown_btn = Button(power_dialog, text="Shutdown", command=shutdown)
    shutdown_btn.pack(side="left", anchor="center", padx=5, pady=10)

    cancel_btn = Button(power_dialog, text="Cancel", command=power_dialog.close)
    cancel_btn.pack(side="left", anchor="center", padx=5, pady=10)

    return power_dialog


class PiDeckUi(Tk):
    def __init__(self, keymaps: List[KeymapTab]):
        super().__init__()
        self.keymaps = keymaps

        # set app root's attributes
        self.title("PiDeck")
        self.attributes("-fullscreen", False)  # set fullscreen  # type:ignore
        self.attributes("-zoomed", True)  # set maximized  # type:ignore
        # self.overrideredirect(True)  # remove titlebar

        # var to store active tab, init at tab 0
        self.active_tab = IntVar()
        self.active_tab.set(0)

        # create app container
        self.app_container = Frame(self)
        self.app_container.pack(fill="both", expand=True)

        # top row of app container, tab selection and power btn
        self.top_row = Frame(self.app_container)
        self.top_row.pack(fill="x")

        self.tab_selection_container = ttk.LabelFrame(
            self.top_row, text="Select Tab"
        )
        self.tab_selection_container.pack(
            side="left", fill="x", expand=True, padx=5, pady=5
        )

        self.power_btn = Button(self.top_row, text="Power", command=self.quit)
        self.power_btn.pack(
            side="bottom", anchor="center", padx=5, pady=10, ipady=10
        )

        self.keypad_frame = None

        # add the tab switcher radio buttons
        for index, tab in enumerate(self.keymaps):
            Radiobutton(
                self.tab_selection_container,
                text=tab.title,
                indicatoron=False,
                variable=self.active_tab,
                value=index,
                command=self.set_active_tab,
            ).pack(
                side="left",
                fill="x",
                expand=True,
                padx=2,
                pady=5,
                ipadx=5,
                ipady=5,
            )

        # add the initial buttons
        self.generate_keypad_grid(self.keymaps[self.active_tab.get()].keymap)

    def set_active_tab(self):
        new_tab = self.active_tab.get()
        self.generate_keypad_grid(self.keymaps[new_tab].keymap)

    def generate_keypad_grid(self, buttons: List[Key]):
        if self.keypad_frame is not None:
            self.keypad_frame.destroy()

        self.keypad_frame = Frame(self.app_container)
        self.keypad_frame.pack(fill="both", expand=True)

        num_buttons = len(buttons)
        max_columns = int(num_buttons**0.5) + 1
        num_rows = (num_buttons + max_columns - 1) // max_columns
        num_columns = (num_buttons + num_rows - 1) // num_rows
        print(num_buttons, max_columns, num_rows, num_columns)

        for i, button in enumerate(buttons):
            row = i // num_columns
            column = i % num_columns
            Button(
                self.keypad_frame,
                text=button.label,
                command=partial(send_serial_msg, button.command),
                padx=10,
                pady=5,
            ).grid(row=row, column=column, padx=5, pady=5, sticky="nsew")

        for i in range(num_rows):
            self.keypad_frame.grid_rowconfigure(i, weight=1)
        for j in range(num_columns):
            self.keypad_frame.grid_columnconfigure(j, weight=1)


if __name__ == "__main__":
    # fetch the keymap form file
    imported_keymap = keymap_json_loader()

    app = PiDeckUi(imported_keymap)
    app.mainloop()