import Adafruit_DHT
import queue, threading, time

sensor = Adafruit_DHT.AM2302
pin = 4


def read():
    return Adafruit_DHT.read(sensor, pin)

def read_retry():
    return Adafruit_DHT.read(sensor, pin)


class ClimateReader(threading.Thread):

    def __init__(self, result_queue, sensor=Adafruit_DHT.AM2302, pin=4):
        threading.Thread.__init__(self)
        #Thread settings
        self.result_queue = result_queue
        self._stop_event = threading.Event()
        #Sensor settings
        self.sensor = sensor
        self.pin = pin
        #Initial sensor read
        self.humidity, self.temperature = Adafruit_DHT.read(sensor, pin)

    def run(self):
        while not self._stop_event.isSet():
            self._read_climate()
            if self.temperature != None:
                self.result_queue.put(("ClimateReader", self.temperature, self.humidity))
            time.sleep(2)

    def join(self, timeout=None):
        self._stop_event.set()
        super(ClimateReader, self).join(timeout)

    def _read_climate(self):
        h, t = Adafruit_DHT.read(self.sensor, self.pin)
        self.humidity = round(h, 1)
        self.temperature = round(t, 1)


