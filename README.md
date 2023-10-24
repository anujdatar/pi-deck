# PiDeck - a StreamDeck Like Device Using RPi Zero and a Touch Screen

Just a random test project because I had a Raspberry Pi Zero W and a Waveshare
7-inch touch screen display lying around.

As of now, the RPi Zero is connected to the touchscreen via HDMI and USB. The Pi
is connected to the Arduino over I2C. This just uses the USB HID protocol to
emulate a keyboard and send keystrokes over USB. So you do not need
any drivers on your host PC. You should be able to use an ESP-32 instead of
the Arduino, so you can use Bluetooth instead of USB.

For more details about why I chose this hardware set, check
[here](#some-thoughts-and-notes-on-micro-controller-selection).

The GUI is built in Tkinter, it's pretty lightweight, and I already know how to
build UIs in python-tkinter.

## Setting up the Raspberry Pi OS for this.
1. Write the legacy Raspberry Pi OS minimal to an SD card. Setup WiFi and SSH

2. Add power button functionality. Edit `/boot/config.txt`
```bash
# By default pin #5 is power switch, but you can change it
# Pin to ground acts as power On/Off
dtoverlay=gpio-shutdown,gpio_pin=X
```

3. Update and upgrade the Pi. Install the dependencies for the GUI, some are a
bit excessive, and may not be needed. I'll refine the list later.
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

4. Clone this repo to your desired location. You can add the folder to your
profile or shell's dot file.

5. Install python dependencies for the PiDeck application
```bash
sudo apt install -y python3 python-is-python3 python3-pip python3-venv \
python3-tk python3-ujson python3-serial python3-smbus \
python3-pil python3-pil.imagetk
```
On Fedora
- serial module will be `python3-pyserial`,
- the smbus module will be `python3-i2c-tools`
- and the pillow modules will be `python3-pillow` and `python3-pillow-tk`

Or use pip to install the dependencies in a virtual env
```bash
cd $Pi_DECK_FOLDER
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# or
pip install pillow pyserial smbus2 ujson
# on pi-zero I also had to install the following for Pillow to work
sudo apt install libopenjp2-7
```

6. With `lightdm` installed, you can now go into `raspi-config` >
`System Options` > `Boot / Auto Login` > `Desktop Autologin`. This should boot
the system up, login to default user and start `Openbox`

7. Set up openbox for kiosk mode `/etc/xdg/openbox/autostart`
```bash
xset -dpms  # disable DPMS (energy star/power saver) features
xset s off  # disable screen saver
xset s noblank  # disable screen blanking

# Hide mouse cursor, when no activity
unclutter-xfixes &

# Start the pcmanfm desktop manager, lets you have desktop icons etc
pcmanfm --desktop &
# you can probably disable this once the initial setup is complete
# to minimize active processes, replace with your pi-deck application

# Launch desktop prefs dialog on first launch, lets you set preferences
# disable trash icon, etc. Can be disabled after.
# pcmanfm --desktop-pref

# Desktop wallpaper
# pcmanfm --set-wallpaper=<path-to-file>
# pcmanfm --walpaper-mode=MODE  # MODE=(color|stretch|fit|crop|center|tile|screen)
```

8. Adding scripts that can shutdown and restart the Pi from desktop shortcuts.
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

9.  Add your desktop shortcuts or symlinks
```bash
mkdir ~/Desktop
ln -s /usr/bin/pcmanfm ~/Desktop/pcmanfm
ln -s /usr/bin/sakura ~/Desktop/sakura
ln -s ~/.local/bin/poweroff ~/Desktop/poweroff
ln -s ~/.local/bin/reboot ~/Desktop/reboot
```
I also added a pi-deck executable file to the desktop. The exact syntax will
depend on your choice of environment setup.
```bash
!#/usr/bin/bash
cd $PI_DECK_FOLDER
# for local virtual environment
.venv/bin/python main.py
# or if you global system packages
python3 main.py
```

10. Connect up the micro-controller to the Pi over I2C. Open the
`micro_controller/leo-i2c` folder in the Arduino IDE and upload the code.
> Note: Make sure you use a logic level converter if your micro-controller
> has a 5V logic level.

11. Update the sample `keymap.json` file to suit your needs and you should be
good to go. The sample has key binds for buying equipment in CS2.

## Some Thoughts and Notes on Micro-controller Selection
### Pico
I was initially planning to use a Raspberry Pi Pico. Send data or
button command from the Pi to the Pico over `Serial`, and use the Pico is USB
HID. Since the Pico can't run in slave mode for `I2C` and `SPI`, that was not an
option, and getting that to work is too complicated for me.

But that did not work out too well. For one `MicroPython` does not have a
proper USB HID keyboard library yet. And `CircuitPython` and `Arduino C/C++`
were real slow when responding to serial messages for some reason. Could have
something to do with the clone boards I was sent by the Amazon seller.

### Arduino Pro Micro (Leonardo)
Using this as the fallback because I know it works, and I already have a
keyboard library to handle media commands. And they can communicate with the Pi
over Serial, I2C and SPI. So I decided to use this for now. One thing to
remember, most Arduino's run at 5V logic, the Pi, runs at 3V3, so you'll need
a logic level converter for device safety and longevity.

### ESP-32
Since they have BlueTooth, I could probably use it as a wireless deck too.
Shouldn't be too hard. I'll try this later. They also work at 3V3 logic voltage.

### Communication between Pi to Arduino
`Serial` sends one char at a time. Can be an issue when parsing complex
commands. So you have to start using loops to go over each *char* and then
execute you commands accordingly. Doesn't seem very efficient. It is also the
slowest of the three. I just ended up picking `I2C` because I have used it
before`.
