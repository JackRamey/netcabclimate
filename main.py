#!/usr/bin/env python3

import automationhat
import climate
import datetime
import netutils
import queue
import signal

from lcd import lcd
from time import sleep

TEMPERATURE_THRESHOLD = 23 # degrees celcius

climate_queue = queue.Queue()
pool = [climate.ClimateReader(result_queue=climate_queue)]
t, h = (0.0, 0.0)
now = datetime.datetime.now()

def on_exit():
    lcd.backlight_enabled = False
    lcd.close(clear=True)
    for thread in pool:
        thread.join()

def signal_term_handler(signal, frame):
    on_exit()
    exit(0)

if __name__ == "__main__":
    # Handle SIGTERM
    signal.signal(signal.SIGTERM, signal_term_handler)

    try:
        for thread in pool:
            thread.start()
        automationhat.relay.one.off()
        lcd.clear()
        lcd.write_string(netutils.get_ip_address('eth0'))
        while(True):
            prev_now = now
            prev_t, prev_h = (t, h)
            now = datetime.datetime.now()
            if not climate_queue.empty():
                _, t, h = climate_queue.get()
            if prev_now.minute != now.minute or prev_t != t or prev_h != h:
                lcd.clear()
                lcd.write_string(netutils.get_ip_address('eth0'))
                lcd.cursor_pos = (1,0)
                lcd.write_string('{0:0.1f}C {1:0.1f}%'.format(t, h))
            if t > TEMPERATURE_THRESHOLD:
                automationhat.relay.one.on()
            else:
                automationhat.relay.one.off()
            sleep(1)
    except KeyboardInterrupt:
        on_exit()

