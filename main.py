from src import keymap_json_loader, PiDeckUi

if __name__ == "__main__":
    # fetch the keymap form file
    imported_keymaps = keymap_json_loader()
    app = PiDeckUi(imported_keymaps)
    app.mainloop()
