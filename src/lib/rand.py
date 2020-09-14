from utime import ticks_us
import urandom

def randint(max):
    urandom.seed(ticks_us())
    return round(urandom.getrandbits(8) / 255 * max)
