#!/usr/bin/python

import click
import evdev
import logging
import selectors

from evdev import ecodes

LOG = logging.getLogger(__name__)


def find_by_name(pattern, exact=False):
    '''Find an input device with name matching `pattern`.

    On success, returns a single evdev.InputDevice. Raises
    KeyError if there are no matching devices, or ValueError
    if there is more than one matching device.'''
    matches = []
    for name in evdev.list_devices():
        dev = evdev.InputDevice(name)
        if (
            exact and
                pattern.lower() == dev.name.lower()
        ) or (
            not exact and
            pattern.lower() in dev.name.lower()
        ):
            matches.append(dev)

    if not matches:
        raise KeyError(f'no input device matching {pattern}')

    if len(matches) > 1:
        raise ValueError(f'more than one device matched {pattern}')

    return matches[0]


@click.group()
@click.option('--verbose', '-v', count=True)
def main(verbose):
    try:
        level = ['WARNING', 'INFO', 'DEBUG'][verbose]
    except IndexError:
        level = 'DEBUG'

    logging.basicConfig(level=level)


@main.command(name='list')
def list_devices():
    '''List avaiable input devices'''
    for i, name in enumerate(evdev.list_devices()):
        dev = evdev.InputDevice(name)
        print(f'[{i}] {dev.name} ({dev.path})')


@main.command()
@click.option('--pass', '-p', 'pass_when_locked', multiple=True)
@click.argument('patterns', nargs=-1)
def run(patterns, pass_when_locked):
    '''Lock input devices when key sequence is received.

    Grabs the input devices listed on the command line. Proxies
    events to the input subsystem until ALT-F12 is received. Resumes
    proxying events after receiving another ALT-F12.

    Use --pass <keycode> to have specific keycodes passed even when
    in lock mode.'''

    devices = []
    for pattern in patterns:
        if pattern.startswith('/'):
            dev = evdev.InputDevice(pattern)
        else:
            dev = find_by_name(pattern)

        LOG.info('found device %s (%s)', dev.name, dev.path)
        devices.append(dev)

    selector = selectors.DefaultSelector()
    ui = {}
    for i, dev in enumerate(devices):
        ui[dev.name] = evdev.UInput.from_device(dev, name=f'py-evdev-uinput-{i}')
        selector.register(dev, selectors.EVENT_READ)
        LOG.warning('grabbing device %s (%s)', dev.name, dev.path)
        dev.grab()

    locked = False
    want_lock = False
    trigger_dev = None

    while True:
        for key, mask in selector.select(0.1):
            dev = key.fileobj

            for event in dev.read():
                cat = evdev.categorize(event)
                LOG.debug('event: %s', cat)
                if event.type == ecodes.EV_KEY:
                    if cat.keycode == 'KEY_F12':
                        if cat.keystate == 1 and ecodes.KEY_LEFTALT in dev.active_keys():
                            want_lock = True
                            trigger_dev = dev
                            continue

                if (
                    not locked
                ) or (
                    event.type == ecodes.EV_KEY
                    and cat.keycode in pass_when_locked
                ) or (
                    event.type == ecodes.EV_SYN
                ):
                    ui[dev.name].write_event(event)

        # wait until all keys are released before locking
        if want_lock and not trigger_dev.active_keys():
            locked = not locked
            want_lock = False

            LOG.warning('locked' if locked else 'unlocked')


if __name__ == '__main__':
    main()
