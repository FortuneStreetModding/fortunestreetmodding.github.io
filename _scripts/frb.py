from dataclasses import dataclass, field
from bytechomp import Reader, Annotated, serialize, ByteOrder
from enum import Enum
from pathlib import Path

from bytechomp.datatypes import (
    U8,  # 8-bit unsigned integer
    U16,  # 16-bit unsigned integer
    U32,  # 32-bit unsigned integer
    U64,  # 64-bit unsigned integer
    I8,  # 8-bit signed integer
    I16,  # 16-bit signed integer
    I32,  # 32-bit signed integer
    I64,  # 64-bit signed integer
    F16,  # 16-bit float
    F32,  # 32-bit float
    F64,  # 64-bit float
)


class SquareType(Enum):
    Property: U16 = 0x00
    Bank: U16 = 0x01
    VentureSquare: U16 = 0x02

    SuitSquareSpade: U16 = 0x03
    SuitSquareHeart: U16 = 0x04
    SuitSquareDiamond: U16 = 0x05
    SuitSquareClub: U16 = 0x06
    ChangeOfSuitSquareSpade: U16 = 0x07
    ChangeOfSuitSquareHeart: U16 = 0x08
    ChangeOfSuitSquareDiamond: U16 = 0x09
    ChangeOfSuitSquareClub: U16 = 0x0A

    TakeABreakSquare: U16 = 0x0B
    BoonSquare: U16 = 0x0C
    BoomSquare: U16 = 0x0D
    StockBrokerSquare: U16 = 0x0E
    RollOnSquare: U16 = 0x10
    ArcadeSquare: U16 = 0x11
    SwitchSquare: U16 = 0x12
    CannonSquare: U16 = 0x13

    BackStreetSquareA: U16 = 0x14
    BackStreetSquareB: U16 = 0x15
    BackStreetSquareC: U16 = 0x16
    BackStreetSquareD: U16 = 0x17
    BackStreetSquareE: U16 = 0x18

    OneWayAlleyDoorA: U16 = 0x1C
    OneWayAlleyDoorB: U16 = 0x1D
    OneWayAlleyDoorC: U16 = 0x1E
    OneWayAlleyDoorD: U16 = 0x1F

    LiftMagmaliceSquareStart: U16 = 0x20
    MagmaliceSquare: U16 = 0x21
    OneWayAlleySquare: U16 = 0x22
    LiftSquareEnd: U16 = 0x23

    unknown0x24: U16 = 0x24
    unknown0x25: U16 = 0x25
    unknown0x26: U16 = 0x26
    unknown0x27: U16 = 0x27
    unknown0x28: U16 = 0x28
    unknown0x29: U16 = 0x29
    unknown0x2A: U16 = 0x2A
    unknown0x2B: U16 = 0x2B
    unknown0x2C: U16 = 0x2C
    unknown0x2D: U16 = 0x2D

    EventSquare: U16 = 0x2E
    unknown0x2F: U16 = 0x2F

    VacantPlot: U16 = 0x30


class LoopingMode(Enum):
    NONE: U16 = 0
    VERTICAL: U16 = 2
    BOTH: U16 = 1


class MagicNumber(Enum):
    BOARD_FILE = bytes("I4DT", encoding="utf8")
    BOARD_DATA = bytes("I4PL", encoding="utf8")
    BOARD_INFO = bytes("I4DT", encoding="utf8")


@dataclass
class Header:
    magic_number: Annotated[bytes, 4] = field(repr=False, compare=False)
    header_size: I32 = field(repr=False, compare=False)

    @staticmethod
    def size() -> int:
        return 0x10


@dataclass
class WaypointData:
    entryId: U8
    destinations: Annotated[list[U8], 3]


@dataclass
class Square:
    _square_type: U16
    positionX: I16
    positionY: I16
    _unknown1: U16 = field(repr=False, compare=False)
    waypoints: Annotated[list[WaypointData], 4]
    district_destination_id: U8
    one_way_lift: U8
    value: U16
    price: U16
    _unknown2: U8 = field(repr=False, compare=False)
    shop_model: U8

    @property
    def square_type(self) -> SquareType:
        return SquareType(self._square_type)

    @square_type.setter
    def square_type(self, v: SquareType) -> None:
        self._square_type = v.value

    @staticmethod
    def size() -> int:
        return 0x20


@dataclass
class BoardData:
    _header: Header = field(repr=False, compare=False)
    _unknown1: U32 = field(repr=False, compare=False)
    _square_count: U16 = field(repr=False, compare=False)
    _unknown2: U16 = field(repr=False, compare=False)
    # we have to put 0 as length for the list of squares, since bytechomp does not support it properly yet
    squares: Annotated[list[Square], 0]

    @staticmethod
    def size() -> int:
        return 0x10


@dataclass
class BoardInfo:
    _header: Header = field(repr=False, compare=False)
    _unknown: U64 = field(repr=False, compare=False)
    initial_cash: U16
    target_amount: U16
    base_salary: U16
    salary_increment: U16
    max_dice_roll: U16
    _galaxy_status: U16
    version_flag: U32 = field(repr=False, compare=False)

    @property
    def galaxy_status(self) -> LoopingMode:
        return LoopingMode(self._galaxy_status)

    @galaxy_status.setter
    def galaxy_status(self, v: LoopingMode) -> None:
        self._galaxy_status = v.value

    @staticmethod
    def size() -> int:
        return 0x20


@dataclass
class BoardFile:
    _header: Header = field(repr=False, compare=False)
    _unknown: U64 = field(repr=False, compare=False)
    board_info: BoardInfo
    _board_data: BoardData
    custom_data: Annotated[bytes, 0] = field(repr=False, compare=True)

    @property
    def squares(self) -> list[Square]:
        return self._board_data.squares

    @staticmethod
    def size() -> int:
        return Header.size() + BoardInfo.size() + BoardData.size()

    def normalize(self):
        # determine the square count
        self._board_data._square_count = len(self._board_data.squares)
        # fix the headers
        # self
        self._header.magic_number = MagicNumber.BOARD_FILE.value
        self._header.header_size = BoardFile.size() + Square.size() * len(
            self._board_data.squares
        )
        # board_info
        self.board_info._header.magic_number = MagicNumber.BOARD_INFO.value
        self.board_info._header.header_size = BoardInfo.size()
        # board_data
        self._board_data._header.magic_number = MagicNumber.BOARD_DATA.value
        self._board_data._header.header_size = BoardData.size() + Square.size() * len(
            self._board_data.squares
        )


def read(file_path: Path) -> BoardFile:
    # HACK: fix the length of the list annotation for the squares field
    BoardData.__annotations__["squares"].__metadata__ = (0,)
    # HACK: fix the length of the annotation for the custom_data field
    BoardFile.__annotations__["custom_data"].__metadata__ = (0,)
    reader = Reader[BoardFile](ByteOrder.BIG).allocate()
    board_file: BoardFile = None
    with open(file_path, "rb") as fp:
        while data := fp.read(1):
            reader.feed(data)
            if reader.is_complete():
                if board_file is None:
                    board_file = reader.build()

                    # now that we know the size of the squares, read the rest of it
                    @dataclass
                    class Squares:
                        squares: Annotated[
                            list[Square], board_file._board_data._square_count
                        ]

                    reader = Reader[Squares](ByteOrder.BIG).allocate()
                else:
                    # we read the squares and put it into our original board_file struct
                    board_file._board_data.squares = reader.build().squares
                    # and now read the rest of the custom meta data (i.e. advanced auto-path data, auto-path range, etc.)
                    bytes_left = fp.read()
                    board_file.custom_data = bytes_left
                    return board_file
    return None


def write(board_file: BoardFile, file_path: Path):
    board_file.normalize()
    # HACK: fix the length of the list annotation for the squares field
    BoardData.__annotations__["squares"].__metadata__ = (
        board_file._board_data._square_count,
    )
    # HACK: fix the length of the annotation for the custom_data field
    BoardFile.__annotations__["custom_data"].__metadata__ = (
        len(board_file.custom_data),
    )
    data = serialize(board_file, ByteOrder.BIG)
    with open(file_path, "wb") as fp:
        fp.write(data)
