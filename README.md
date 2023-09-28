# PiDeck - a StreamDeck like device using RPi Zero and RPico

Just a random test project because I had a Raspberry Pi Zero W and a Waveshare
7-inch touch screen display lying around.

As of now, the RPi Zero is connected to the touchscreen via HDMI and USB. It is
connected to the RPico via the serial pins.

The GUI is built in Tkinter, it's pretty lightweight, and I already know how to
build UIs in python-tkinter.

Setting up the Raspberry Pi Zero OS for this.
1. Write the legacy Raspberry Pi OS minimal to an SD card. Setup WiFi and SSH

2. Add power button functionality. Edit `/boot/config.txt`
    ```bash
    # By default pin #5 is power switch, but you can change it
    # Pin to ground acts as power On/Off
    dtoverlay=gpio-shutdown,gpio_pin=X
    ```

3. Update and upgrade the Pi Zero

4. Install the dependencies for the GUI, some are a bit excessive, and may not
be needed. I'll refine the list later.
    ```bash
    sudo apt install --no-install-recommends -y \
    xserver-xorg \
    x11-server-utils \
    xinit \
    lightdm \
    openbox \
    pcmanfm \
    sakura \
    unclutter-xfixes \
    xdotool \
    xautomation \
    git vim htop sed
    ```

5. With `lightdm` installed, you can now go into `raspi-config` >
`System Options` > `Boot / Auto Login` > `Desktop Autologin`. This should boot
the system up, login to default user and start `Openbox`

6. Set up openbox for kiosk mode
    ```bash
    xset -dpms  # disable DPMS (energy star/power saver) features
    xset s off  # disable screen saver
    xset s noblank  # disable screen blanking

    # Hide mouse cursor, when no activity
    unclutter-xfixes &

    # Start the pcmanfm desktop manager, lets you have desktop icons etc
    pcmanfm --desktop &

    # Launch desktop prefs dialog on first launch, lets you set preferences
    # disable trash icon, etc. Can be disabled after.
    # pcmanfm --desktop-pref

    # Desktop wallpaper
    # pcmanfm --set-wallpaper=<path-to-file>
    # pcmanfm --walpaper-mode=MODE  # MODE=(color|stretch|fit|crop|center|tile|screen)
    ```

7. Adding scripts that can shutdown and restart the Pi from desktop shortcuts.
    ```bash
    #!/usr/bin/bash
    systemctl poweroff

    # ~/.local/bin/poweroff
    ```

    ```bash
    #!/usr/bin/bash
    systemctl reboot

    # ~/.local/bin/reboot
    ```
    
    Make them executable
    ```bash
    chmod +x ~/.local/bin/poweroff ~/.local/bin/reboot
    ```

8. Add your desktop shortcuts or symlinks
    ```bash
    mkdir ~/Desktop
    ln -s /usr/bin/pcmanfm ~/Desktop/pcmanfm
    ln -s /usr/bin/sakura ~/Desktop/sakura
    ln -s ~/.local/bin/poweroff ~/Desktop/poweroff
    ln -s ~/.local/bin/reboot ~/Desktop/reboot
    ```

9. Install python dependencies for the PiDeck application
    ```bash
    sudo apt install -y python3 python-is-python3 python3-pip python3-venv \
    python3-tk python3-ujson python3-pyserial
    ```

