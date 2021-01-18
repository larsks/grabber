I have a convertible laptop (a Yoga 11e). It doesn't seem as if Linux
has any mechanism to detect when this device is tablet mode, which
means the keyboard stays active. This renders tablet mode pretty much
useless.

The script `grabber.py` intercepts devices of your choice, passing
input events on to the kernel until it sees a specific key sequence
(`Alt-F12`). At this point, it will stop passing events to the kernel
until it receives another `Alt-F12`.

You can configure certain keycodes to pass through even when
locked...e.g., I do this so that the volume up/down keys on the side
of the laptop work when the keyboard is locked.


## Usage

```
Usage: grabber.py [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --verbose
  --help         Show this message and exit.

Commands:
  list
  run
```

### List

```
Usage: grabber.py list [OPTIONS]

Options:
  --help  Show this message and exit.
```

### Run

```
Usage: grabber.py run [OPTIONS] [PATTERNS]...

Options:
  -p, --pass TEXT
  --help           Show this message and exit.
```

`PATTERNS` is one or more device names or paths. A path starting with
`/` will be used verbatim (e.g., `/dev/input/event2`). Anything else
will be converted to lower case and matched against input device
names, also converted to lower case.

## Example

My system has the following available devices:

```
[0] UVC Camera (046d:081d) (/dev/input/event25)
[1] HDA Intel PCH Front Headphone (/dev/input/event24)
[2] HDA Intel PCH Line Out (/dev/input/event23)
[3] HDA Intel PCH Rear Mic (/dev/input/event22)
[4] HDA Intel PCH Front Mic (/dev/input/event21)
[5] HDA Intel HDMI HDMI/DP,pcm=9 (/dev/input/event20)
[6] HDA Intel HDMI HDMI/DP,pcm=8 (/dev/input/event19)
[7] HDA Intel HDMI HDMI/DP,pcm=7 (/dev/input/event18)
[8] HDA Intel HDMI HDMI/DP,pcm=3 (/dev/input/event11)
[9] Dell WMI hotkeys (/dev/input/event10)
[10] PC Speaker (/dev/input/event9)
[11] Logitech Anywhere MX (/dev/input/event8)
[12] GN Netcom A/S Jabra EVOLVE LINK MS (/dev/input/event17)
[13] C-Media Electronics Inc. USB Audio Device (/dev/input/event16)
[14] USB-HID Keyboard (/dev/input/event15)
[15] USB-HID Keyboard Consumer Control (/dev/input/event14)
[16] USB-HID Keyboard System Control (/dev/input/event13)
[17] USB-HID Keyboard (/dev/input/event12)
[18] Video Bus (/dev/input/event7)
[19] Hoksi Technology DURGOD Taurus K320 Mouse (/dev/input/event6)
[20] Hoksi Technology DURGOD Taurus K320 Keyboard (/dev/input/event5)
[21] Hoksi Technology DURGOD Taurus K320 Consumer Control (/dev/input/event4)
[22] Hoksi Technology DURGOD Taurus K320 System Control (/dev/input/event3)
[23] Hoksi Technology DURGOD Taurus K320 (/dev/input/event2)
[24] Power Button (/dev/input/event1)
[25] Power Button (/dev/input/event0)
```

I run `grabber` like this:

```
grabber run -p KEY_VOLUMEUP -p KEY_VOLUMEDOWN /dev/input/event2 anyuwhere
```

I specify the path to the keyboard explicitly, because there's not a
good pattern to uniquely match it otherwise. I specify `anywhere` to
match the Logitech Anywhere device.
