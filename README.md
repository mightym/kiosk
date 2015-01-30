 /$$   /$$ /$$                     /$$      
| $$  /$$/|__/                    | $$      
| $$ /$$/  /$$  /$$$$$$   /$$$$$$$| $$   /$$
| $$$$$/  | $$ /$$__  $$ /$$_____/| $$  /$$/
| $$  $$  | $$| $$  \ $$|  $$$$$$ | $$$$$$/ 
| $$\  $$ | $$| $$  | $$ \____  $$| $$_  $$ 
| $$ \  $$| $$|  $$$$$$/ /$$$$$$$/| $$ \  $$
|__/  \__/|__/ \______/ |_______/ |__/  \__/
                                            


Installation
============

Inside the virtualenv:

    pip install -r requirements.txt


Fabric Commands
===============

`$ fab push`

  Push 'origin/master' and pull it on the server side. Then restart the
  server. It does *not* migrate or restart the server. Ideal for small
  frontend chanes.

`$ fab quick`

  Does a 'fab push' and restarts the server.

`$ fab update`

  Complete project update including requirements updates, db migrations,
  cache flush and server restart.


Display Ubuntu Setup
====================

Step 1) Setup & install dependencies:

`$ sudo apt-get update && sudo apt-get dist-upgrade`
`$ sudo apt-get install xorg nodm chromium-browser`

Step 2) Create your kiosk user, add it to any relevant groups (www-data?).

Step 3) Log in as your kiosk user.

Step 4) Create ~/.xsession, add the following;

```
#!/usr/bin/env bash
chromium-browser
```

Step 5) Type `startx`… Chromium will start, and most likely occupy only half of the screen.

Step 6) Open the wrench menu, select “Settings”. Click on “Personal Stuff”.

Step 6a) Under “Appearance”, switch to “Hide system title bar and use compact borders”.

Step 7) Drag chromium to occupy the full screen (because F11 didn’t work, did it? Yeah.)

Step 7a) Switch back to “Use system title bar and borders” (which is none since we have no window manager! (thank you for following along))

Step 7b) You may find it advantageous to take this opportunity to disable saved passwords and autofill as well.

Step 8) Ctrl+Alt+F1 and then Ctrl+C to return to console and kill our X session.

Step 9) Edit ~/.xsession once again, change the last line so the file reads as follows:

```
#!/usr/bin/env bash
export DISPLAY=:0.0 #make the display available
xrandr -o left #use xrandr to adjust screen orientation. in this case flip it left counter clockwise
while true; do
#start chromium browser. ajust window-size and position to your needs. add the url which you want to open at the end
chromium-browser --start-maximized --window-size=1080,1920 --window-position=0,0 --kiosk http://<your_app_url>/;
sleep 5s;
done
```

Step 9a) Save.

You may want to try running `startx` again to make sure you didn’t typo or screw anything up


Step 10) Change user to the one who should be automatically logged. Edit /etc/default/nodm, make it look like this. (don’t forget to sudo):

`
NODM_ENABLED=true
NODM_USER=<kiosk_user>
NODM_FIRST_VT=7
NODM_XSESSION=/etc/X11/Xsession
NODM_X_OPTIONS='-nolisten tcp'
NODM_MIN_SESSION_TIME=60
`

Step 10a) Save.

Thats it.


If you like to rotate your complete terminal screen to for example portrait and you want this to happen automatically when you start your system, you need to modify your boot loader configuration to give it the correct options. In /etc/default/grub add fbcon=rotate:1 to the GRUB_CMDLINE_LINUX line:

`
GRUB_CMDLINE_LINUX="fbcon=rotate:1"
`

(Don't forget to run sudo update-grub after changing this file.)

