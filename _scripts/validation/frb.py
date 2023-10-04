import struct


class frb_obj(object):
    pass


def load_frb(frbFile):
    frb = frb_obj()
    with open(frbFile, "rb") as stream:
        stream.seek(0x20)
        frb.initialCash = struct.unpack(">H", stream.read(2))[0]
        frb.targetAmount = struct.unpack(">H", stream.read(2))[0]
        frb.baseSalary = struct.unpack(">H", stream.read(2))[0]
        frb.salaryIncrement = struct.unpack(">H", stream.read(2))[0]
        frb.maxDiceRoll = struct.unpack(">H", stream.read(2))[0]
        frb.galaxyStatus = struct.unpack(">H", stream.read(2))[0]
        stream.seek(0x3C)
        frb.squareCount = struct.unpack(">H", stream.read(2))[0]
    return frb
