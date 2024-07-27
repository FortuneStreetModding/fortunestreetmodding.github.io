from tempfile import TemporaryDirectory
import dolphin_memory_engine
import sys
import os
from subprocess import run
from pathlib import Path
import colorama
import argparse
import asyncio
import time
import struct
import addressTranslator

repo_root = Path(__file__).parent.parent

def formatConfig() -> list[str]:
    config = []
    config.append("--config=Dolphin.Display.RenderToMain=False")
    config.append("--config=Dolphin.Display.Fullscreen=False")
    config.append("--config=Dolphin.Analytics.PermissionAsked=True")
    config.append("--config=Dolphin.Interface.ShowActiveTitle=True")
    config.append("--config=GFX.Settings.BorderlessFullscreen=True")
    config.append("--config=Dolphin.Core.WiiSDCardAllowWrites=False")
    config.append("--config=Dolphin.Input.BackgroundInput=False")
    config.append("--config=Dolphin.Core.FastDiscSpeed=True") # Speed up loading game files
    config.append("--config=Dolphin.Core.OverclockEnable=True") # Enable Emulated CPU Clock override
    config.append("--config=Dolphin.Core.Overclock=4.") # Set overclock to 400%
    config.append("--config=Dolphin.Core.GFXBackend=Null") # Do not render anything
    return config

def unsigned_to_signed_32bit(value):
    if value & 0x80000000:  # Check if the MSB is set (value is negative in signed interpretation)
        return value - 0x100000000
    else:
        return value

def hack_start_immediately_yoshi_island(boom_to_standard):
    dolphin_memory_engine.write_word(boom_to_standard(0x80218508), 0x3800000e) # skip all the splash screens
    dolphin_memory_engine.write_word(boom_to_standard(0x80216e6c), 0x48000020) # automatically select to not create a save file, if asked
    dolphin_memory_engine.write_word(boom_to_standard(0x802174a8), 0x48000014) # automatically select to confirm to not create a save file, if asked
    dolphin_memory_engine.write_word(boom_to_standard(0x801e8fb4), 0x48000510) # when in title screen, start immediately
    dolphin_memory_engine.write_word(boom_to_standard(0x801f969c), 0x480000b0) # skip all board settings and start board immediately
    dolphin_memory_engine.write_word(boom_to_standard(0x8020cf9c), 0x38600000) # When starting tour mode all players are CPU
    dolphin_memory_engine.write_word(boom_to_standard(0x80011678), 0x38000001) # Set Player Order as picked instead of deciding randomly
    dolphin_memory_engine.write_word(boom_to_standard(0x80011628), 0x38000000) # Set map id to 0
    dolphin_memory_engine.write_word(boom_to_standard(0x80189de8), 0x380000d8) # Skip "This is the target amount for this board" dialog when starting board

def hack_speedup_game(boom_to_standard):
    dolphin_memory_engine.write_word(boom_to_standard(0x800197c8), 0x38040009) # Maximum Speedup
    dolphin_memory_engine.write_word(boom_to_standard(0x80099e4c), 0x38600001) # AI instantly chooses square
    dolphin_memory_engine.write_word(boom_to_standard(0x80011688), 0x380000ff) # Set Game Speed to Super Fast
    dolphin_memory_engine.write_word(boom_to_standard(0x80011690), 0x38000002) # Switch off dialogs
    dolphin_memory_engine.write_word(boom_to_standard(0x80818fa8), 0x41200069) # Multiply Game Speed by 10x

async def install_hacks(boom_to_standard):
    dolphin_memory_engine.assert_hooked()
    hacked = False
    while not hacked:
        try:
            hack_start_immediately_yoshi_island(boom_to_standard)
            hack_speedup_game(boom_to_standard)
            print("Hacked!")
            hacked = True
        except RuntimeError as e:
            print("Attempting to hack...")
            await asyncio.sleep(1)

async def run_single_board(csmm_executable: str, dolphin_executable: str, game_dir: str, board: str):
    # patch the board in
    board_yaml_file = list(Path(repo_root, "_maps", board).glob("*.y*ml"))[0].as_posix()
    #run([csmm_executable, "discard", game_dir], check=True)
    #run([csmm_executable, "import", game_dir, board_yaml_file, "--id", "0"], check=True)
    #run([csmm_executable, "save", game_dir], check=True)

    mainDol = Path(game_dir, "sys", "main.dol")

    boom_to_standard = None
    # check if boom street or fortune street
    with open(mainDol, "rb") as stream:
        stream.seek(0x756b4)
        b = stream.read(4)
        v = struct.unpack(">I", b)[0]
        if v == 0x800dab84:
            # boom street
            boom_to_standard = lambda address: address
        else:
            # fortune street
            boom_to_standard = addressTranslator.bsvirt_to_fsvirt

    # create temporary directory
    with TemporaryDirectory() as td:
        # start dolphin
        #my_env = os.environ.copy()
        #my_env["DME_DOLPHIN_PROCESS_NAME"] = Path(dolphin_executable).with_suffix("").name
        args = ["--exec", mainDol, "--video_backend=null", "--user", td, *formatConfig()]
        proc = await asyncio.create_subprocess_exec(dolphin_executable, *args, cwd=game_dir)
        try:
            # hook the memory engine
            for i in range(1, 20):
                await asyncio.sleep(0.5)
                print(f"Attempt {i}/20 to hook dolphin memory engine...")
                dolphin_memory_engine.hook()
                if dolphin_memory_engine.is_hooked():
                    print("Dolphin memory engine hooked")
                    break
            if not dolphin_memory_engine.is_hooked():
                print("Failed to hook dolphin. Make sure dolpin is running and a game has been started.")
                sys.exit(1)
            # install hacks
            await install_hacks(boom_to_standard)
            # print current turn
            previous_turn = 0
            current_turn = 0
            target_amount = 0
            while target_amount == 0:
                target_amount = dolphin_memory_engine.read_word(boom_to_standard(0x80552424))
                await asyncio.sleep(1)
            print(f"Target amount: {target_amount}")
            while True:
                player_1_ready_cash = unsigned_to_signed_32bit(dolphin_memory_engine.read_word(boom_to_standard(0x805503c0)))
                player_2_ready_cash = unsigned_to_signed_32bit(dolphin_memory_engine.read_word(boom_to_standard(0x8055089c)))
                player_3_ready_cash = unsigned_to_signed_32bit(dolphin_memory_engine.read_word(boom_to_standard(0x80550d78)))
                player_4_ready_cash = unsigned_to_signed_32bit(dolphin_memory_engine.read_word(boom_to_standard(0x80551254)))
                player_1_net_worth = unsigned_to_signed_32bit(dolphin_memory_engine.read_word(boom_to_standard(0x80550468)))
                player_2_net_worth = unsigned_to_signed_32bit(dolphin_memory_engine.read_word(boom_to_standard(0x80550944)))
                player_3_net_worth = unsigned_to_signed_32bit(dolphin_memory_engine.read_word(boom_to_standard(0x80550e20)))
                player_4_net_worth = unsigned_to_signed_32bit(dolphin_memory_engine.read_word(boom_to_standard(0x805512fc)))
                player_1_str = "*P1:" if (current_turn%4)+1 == 1 else " P1:"
                player_2_str = "*P2:" if (current_turn%4)+1 == 2 else " P2:"
                player_3_str = "*P3:" if (current_turn%4)+1 == 3 else " P3:"
                player_4_str = "*P4:" if (current_turn%4)+1 == 4 else " P4:"
                print(f"Turn: {int(current_turn/4)+1:>2} {player_1_str}{player_1_ready_cash:>5} {player_1_net_worth:>5} {player_2_str}{player_2_ready_cash:>5} {player_2_net_worth:>5} {player_3_str}{player_3_ready_cash:>5} {player_3_net_worth:>5} {player_4_str}{player_4_ready_cash:>5} {player_4_net_worth:>5}")
                while current_turn == previous_turn:
                    current_turn = dolphin_memory_engine.read_word(boom_to_standard(0x80552414))
                    await asyncio.sleep(1)
                previous_turn = current_turn

            await asyncio.sleep(99999)
        finally:
            # kill dolphin
            proc.kill()
            await proc.wait()
            print(f"Subprocess {proc.pid} killed")

async def run_all_boards(csmm_executable: str, dolphin_executable: str, game_dir: str):
    print("testing all boards not yet implemented")
    pass

async def run_modpack(csmm_executable: str, dolphin_executable: str, game_dir: str, modpack: str):
    print("testing modpack not yet implemented")
    pass

if __name__ == "__main__":
    colorama.init()

    asyncio.run(run_single_board("csmm", "/mnt/workspace/fortunestreet/dolphin-emu/dolphin-emu", "/mnt/workspace/fortunestreet/boom_street_dev", "AlchemistsHouse"))
    sys.exit(0)

    parser = argparse.ArgumentParser()
    parser.add_argument('--csmm-executable', default='csmm', action='store', help='The path to the csmm executable')
    parser.add_argument('--dolphin-executable', default='dolphin-emu', action='store', help='The path to the dolphin emulator executable')
    parser.add_argument('--game-dir', action='store', help='The path to an extracted clean vanilla Fortune Street or Boom Street.')
    parser.add_argument('--modpack', action='store', help='The yaml file which contains the boards that should be tested')
    parser.add_argument('--board', action='store', help='The yaml file of the board to be tested')
    parser.add_argument('--all', type=bool, help='If given, all boards in the repository are tested')
    args = parser.parse_args()
    try:
        version = run([args.csmm_executable, "--version"], check=True, text=True, capture_output=True)
        if not version:
            print("Failed to get csmm version")
            sys.exit(1)
    except FileNotFoundError:
        print("Csmm executable not found. Please provide it with --csmm-executable")
        sys.exit(1)
    try:
        version = run([args.dolphin_executable, "--version"], check=True, text=True, capture_output=True)
        if not version:
            print("Failed to get dolphin version")
            sys.exit(1)
    except FileNotFoundError:
        print("Dolphin executable not found. Please provide it with --dolphin-executable")
        sys.exit(1)
    game_dir_path = Path(args.game_dir)
    if not game_dir_path.exists() or not game_dir_path.is_dir():
        print("Game directory not found. Please provide it with --game-dir")
        sys.exit(1)
    main_dol_path = Path(args.game_dir, "sys", "main.dol")
    if not main_dol_path.exists() or not main_dol_path.is_file():
        print(f"{main_dol_path.as_posix()} not found. Make sure you provide a proper game directory with --game-dir")
        sys.exit(1)
    if not args.modpack and not args.board and not args.all:
        print("Must specify at least one of --modpack, --board, or --all")
        sys.exit(1)
    if args.all:
        run_all_boards(args.csmm_executable, args.dolphin_executable, args.image)
    if args.modpack:
        run_modpack(args.csmm_executable, args.dolphin_executable, args.image, args.modpack)
    if args.board:
        run_single_board(args.csmm_executable, args.dolphin_executable, args.image, args.board)
