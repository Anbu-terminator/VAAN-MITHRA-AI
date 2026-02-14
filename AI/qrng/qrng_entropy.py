import os

def qrng_entropy():
    return int.from_bytes(os.urandom(2), "big") / 65535
