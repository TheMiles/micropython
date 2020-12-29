import time
import machine

class ElapsedTime:

    def __init__(self, waittime_ms):

        self.waittime = waittime_ms
        self.nextValid = time.ticks_ms() + self.waittime


    def reset(self):

        self.nextValid = time.ticks_ms() + self.waittime


    def hasElapsed(self):

        if time.ticks_ms() > self.nextValid:
            self.reset()
            return True
        return False


class Button:
    def __init__(self, pin, callback, pullmode=machine.Pin.PULL_UP, trigger=machine.Pin.IRQ_RISING):
        self.pin           = machine.Pin(pin, machine.Pin.IN, pullmode)
        self.trigger       = trigger
        self.callback      = callback
        self.debounceTimer = ElapsedTime(100)

    def debounceHandler(self, p):

        if self.debounceTimer.hasElapsed():
            self.callback(p)


    def startListen(self):

        self.pin.irq(trigger=self.trigger, handler=self.debounceHandler)



    def stopListen(self):

        self.pin.irq(trigger=self.trigger, handler=None)
