from functools import partial
from tkinter import (
    Button,
    Frame,
    IntVar,
    PhotoImage,
    Radiobutton,
    Tk,
    Toplevel,
    ttk,
)
from typing import List, Optional  # , Callable

from src import Key, keymap_json_loader, send_i2c_msg, reboot, shutdown


# class DeckButton(Button):
#     def __init__(
#         self,
#         parent: Optional[Frame] = None,
#         text: Optional[str] = None,
#         imgPath: Optional[str] = None,
#         command: Optional[Callable[[], None]] = None,
#     ):
#         super().__init__(parent)
#         if imgPath is not None:
#             self.btn_image = PhotoImage(file=imgPath)
#             self.configure(image=self.btn_image)
#         else:
#             label = text if text is not None else "button"
#             self.configure(text=label)
#         if command is not None:
#             self.configure(command=command)


class DeckButton(Button):
    def __init__(self, key: Key, parent: Optional[Frame] = None):
        super().__init__(parent)
        if key.type == "image" and key.imgPath is not None:
            self.btn_image = PhotoImage(file=key.imgPath)
            self.configure(image=self.btn_image)
        else:
            self.configure(text=key.label)

        self.configure(command=partial(send_i2c_msg, key.command))


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


class PowerDialog(DeckModal):
    def __init__(self, parent: Tk):
        super().__init__(parent, "PiDeck: Power Menu")

        cancel_btn = Button(self, text="Cancel", command=self.close)
        cancel_btn.pack(side="left", anchor="center", padx=5, pady=10)

        quit_btn = Button(self, text="Quit", command=parent.quit)
        quit_btn.pack(side="left", anchor="center", padx=5, pady=10)

        reboot_btn = Button(self, text="Reboot", command=reboot)
        reboot_btn.pack(side="left", anchor="center", padx=5, pady=10)

        shutdown_btn = Button(self, text="Shutdown", command=shutdown)
        shutdown_btn.pack(side="left", anchor="center", padx=5, pady=10)


class KeypadFrame(Frame):
    def __init__(self, parent: Frame, packing: str, buttons: List[Key]):
        super().__init__(parent)
        self.pack(fill="both", expand=True)

        self.packing = packing
        self.buttons = buttons

        if self.packing == "auto":
            self.auto_pack()
        else:
            self.manual_pack()

    def auto_pack(self) -> None:
        num_buttons = len(self.buttons)
        max_columns = int(num_buttons**0.5) + 1
        num_rows = (num_buttons + max_columns - 1) // max_columns
        num_columns = (num_buttons + num_rows - 1) // num_rows

        for i, button in enumerate(self.buttons):
            row = i // num_columns
            column = i % num_columns
            # DeckButton(
            #     self,
            #     text=button.label,
            #     command=partial(send_i2c_msg, button.command),
            DeckButton(parent=self, key=button).grid(
                row=row, column=column, padx=5, pady=5, sticky="nsew"
            )

        self.expand_to_fit(num_rows, num_columns)

    def manual_pack(self) -> None:
        for button in self.buttons:
            if (
                button.row is None
                or button.column is None
                or button.height is None
                or button.width is None
            ):
                raise ValueError("Row and column must be specified for manual packing.")
            # DeckButton(
            #     self,
            #     text=button.label,
            #     command=partial(send_i2c_msg, button.command),
            DeckButton(parent=self, key=button).grid(
                row=button.row,
                column=button.column,
                padx=5,
                pady=5,
                sticky="nsew",
                rowspan=button.height,
                columnspan=button.width,
            )
        # print(type(self.buttons[-1].row), type(self.buttons[-1].column))
        num_rows: int = (
            self.buttons[-1].row + 1 if self.buttons[-1].row is not None else 1
        )
        num_columns: int = (
            self.buttons[-1].column + 1 if self.buttons[-1].column is not None else 1
        )
        self.expand_to_fit(num_rows, num_columns)

    def expand_to_fit(self, rows: int, cols: int) -> None:
        for i in range(rows):
            self.grid_rowconfigure(i, weight=1)
        for j in range(cols):
            self.grid_columnconfigure(j, weight=1)


class PiDeckUi(Tk):
    def __init__(self):
        super().__init__()
        self.keymaps = keymap_json_loader()

        # set app root's attributes
        self.title("PiDeck")
        self.attributes("-fullscreen", True)  # set fullscreen  # type:ignore
        # self.attributes("-zoomed", True)  # set maximized  # type:ignore
        # self.overrideredirect(True)  # remove titlebar

        # *************************************************************
        # define basic app structure
        self.app_container = Frame(self)
        self.app_container.pack(fill="both", expand=True)

        self.top_row = Frame(self.app_container)
        self.top_row.pack(fill="x")

        self.keypad_frame: Frame | None = None

        # *************************************************************
        # var to store active tab, init at tab 0
        self.active_tab = IntVar()
        self.active_tab.set(0)

        # *************************************************************
        self.tab_selection_frame = ttk.LabelFrame(self.top_row, text="Select Tab")
        self.tab_selection_frame.pack(
            side="left", fill="x", expand=True, padx=5, pady=5
        )

        self.power_btn = Button(
            self.top_row,
            text="Power",
            command=partial(PowerDialog, self),
        )
        self.power_btn.pack(
            side="bottom", anchor="center", padx=5, pady=10, ipadx=10, ipady=15
        )

        self.create_tab_selectors()

        # *************************************************************
        # add the initial buttons
        self.keypad_frame = KeypadFrame(
            self.app_container, self.keymaps[0].packing, self.keymaps[0].keymap
        )

    def create_tab_selectors(self):
        for index, tab in enumerate(self.keymaps):
            Radiobutton(
                self.tab_selection_frame,
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
                ipady=10,
            )

    def set_active_tab(self):
        new_tab = self.active_tab.get()
        if self.keypad_frame is not None:
            self.keypad_frame.destroy()
        self.keypad_frame = KeypadFrame(
            self.app_container,
            self.keymaps[new_tab].packing,
            self.keymaps[new_tab].keymap,
        )
