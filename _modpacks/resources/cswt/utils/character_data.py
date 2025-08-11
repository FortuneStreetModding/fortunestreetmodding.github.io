from enum import Enum

color_data_base_address = '0x80427'


class CharacterCode(Enum):
    MARIO = 'd2'
    LUIGI = 'd3'
    PEACH = 'd4'
    YOSHI = 'd5'
    BOWSER = 'd6'
    TOAD = 'd7'
    DONKEYKONG = 'd8'
    WARIO = 'd9'
    WALUIGI = 'da'
    DAISY = 'db'
    BIRDO = 'dc'
    DIDDYKONG = 'dd'
    BOWSERJR = 'de'
    SLIME = 'df'
    PRINCESSA = 'e0'
    KIRYL = 'e1'
    YANGUS = 'e2'
    ANGELO = 'e3'
    PLATYPUNK = 'e4'
    BIANCA = 'e5'
    ALENA = 'e6'
    CARVER = 'e7'
    JESSICA = 'e8'
    DRAGONLORD = 'e9'
    STELLA = 'ea'
    PATTY = 'eb'


class ColorAddressSuffix(Enum):
    PRIMARY = '1'
    SECONDARY = '5'
    TERTIARY = '9'
    QUATERNARY = 'd'


class ColorData:
    primary_color_address: int
    secondary_color_address: int
    tertiary_color_address: int
    quaternary_color_address: int


class ColorTable(Enum):
    RED = b'\x00'
    BLUE = b'\x01'
    YELLOW = b'\x02'
    GREEN = b'\x03'
    WHITE = b'\x04'
    LAVENDER = b'\x05'
    LIME = b'\x06'
    PINK = b'\x07'
    TEAL = b'\x08'
    ORANGE = b'\x09'
    DARKGREEN = b'\x0A'
    APRICOT = b'\x0B'
    FUCHSIA = b'\x0C'
    PURPLE = b'\x0D'
    LIGHTBLUE = b'\x0E'
    WINE = b'\x0F'


def generate_color_data(character_code: CharacterCode):
    data = ColorData()

    character_primary_color_address_string = f"{color_data_base_address}{character_code.value}{ColorAddressSuffix.PRIMARY.value}"
    data.primary_color_address = int(character_primary_color_address_string, 16)

    character_secondary_color_address_string = f"{color_data_base_address}{character_code.value}{ColorAddressSuffix.SECONDARY.value}"
    data.secondary_color_address = int(character_secondary_color_address_string, 16)

    character_tertiary_color_address_string = f"{color_data_base_address}{character_code.value}{ColorAddressSuffix.TERTIARY.value}"
    data.tertiary_color_address = int(character_tertiary_color_address_string, 16)

    character_quaternary_color_address_string = f"{color_data_base_address}{character_code.value}{ColorAddressSuffix.QUATERNARY.value}"
    data.quaternary_color_address = int(character_quaternary_color_address_string, 16)

    return data
