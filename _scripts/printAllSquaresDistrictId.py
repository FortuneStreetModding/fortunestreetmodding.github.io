import validation.frb as frb
from pathlib import Path
from termcolor import cprint
import colorama


def main() -> None:
    colorama.init()

    boardfile_paths = list(Path().glob("../_maps/*/*.frb"))
    for boardfile_path in boardfile_paths:
        boardfile = frb.read(boardfile_path)
        for i, square in enumerate(boardfile.squares):
            if square.square_type == frb.SquareType.SwitchSquare:
                cprint(
                    f"Switch square {i:02} in {boardfile_path.as_posix():<55} has district_destination_id {square.district_destination_id:>3}",
                    "grey",
                )


if __name__ == "__main__":
    main()
