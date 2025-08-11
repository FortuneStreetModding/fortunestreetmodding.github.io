import pycsmm
import os
import shutil
import json

from utils.character_data import CharacterCode, ColorTable, generate_color_data

MODID = __name__


def replMapIcons(locale, arcDir, modpackDir):
	gameMapIconAll = os.path.join(modpackDir, 'game/game_board.arc')
	for dirEntry in os.scandir(gameMapIconAll):
		tplPath = os.path.join(arcDir, 'arc/timg', os.path.splitext(dirEntry.name)[0] + '.tpl')
		pycsmm.convertPngToTpl(dirEntry.path, tplPath)


def replColorDartTextures(locale, brresDir, modpackDir):
	gameColorDartTextures = os.path.join(modpackDir, 'game/mg_darts.brres/textures')
	for dirEntry in os.scandir(gameColorDartTextures):
		texPath = os.path.join(brresDir, 'Textures(NW4R)', os.path.splitext(dirEntry.name)[0])
		pycsmm.convertPngToTex(dirEntry.path, texPath)


class Mod(pycsmm.CSMMMod, pycsmm.GeneralInterface, pycsmm.ArcFileInterface, pycsmm.BrresFileInterface):
	def __init__(self):
		pycsmm.CSMMMod.__init__(self)
		pycsmm.GeneralInterface.__init__(self)
		pycsmm.ArcFileInterface.__init__(self)
		pycsmm.BrresFileInterface.__init__(self)


	def modId(self):
		return MODID


	def priority(self):
		return -250


	def saveFiles(self, root, gameInstance, modList):
		mapper = gameInstance.addressMapper()

		# get the character color data, which returns an object containing color addresses 1-4
		# replace MARIO with your desired character slot, in ALL CAPS
		mario_color_data = generate_color_data(CharacterCode.MARIO)
		luigi_color_data = generate_color_data(CharacterCode.LUIGI)
		peach_color_data = generate_color_data(CharacterCode.PEACH)
		yoshi_color_data = generate_color_data(CharacterCode.YOSHI)
		bowser_color_data = generate_color_data(CharacterCode.BOWSER)
		toad_color_data = generate_color_data(CharacterCode.TOAD)
		dk_color_data = generate_color_data(CharacterCode.DONKEYKONG)
		wario_color_data = generate_color_data(CharacterCode.WARIO)
		waluigi_color_data = generate_color_data(CharacterCode.WALUIGI)
		daisy_color_data = generate_color_data(CharacterCode.DAISY)
		birdo_color_data = generate_color_data(CharacterCode.BIRDO)
		diddy_color_data = generate_color_data(CharacterCode.DIDDYKONG)
		bowserjr_color_data = generate_color_data(CharacterCode.BOWSERJR)
		slime_color_data = generate_color_data(CharacterCode.SLIME)
		princessa_color_data = generate_color_data(CharacterCode.PRINCESSA)
		kiryl_color_data = generate_color_data(CharacterCode.KIRYL)
		yangus_color_data = generate_color_data(CharacterCode.YANGUS)
		angelo_color_data = generate_color_data(CharacterCode.ANGELO)
		platypunk_color_data = generate_color_data(CharacterCode.PLATYPUNK)
		bianca_color_data = generate_color_data(CharacterCode.BIANCA)
		alena_color_data = generate_color_data(CharacterCode.ALENA)
		carver_color_data = generate_color_data(CharacterCode.CARVER)
		jessica_color_data = generate_color_data(CharacterCode.JESSICA)
		dragonlord_color_data = generate_color_data(CharacterCode.DRAGONLORD)
		stella_color_data = generate_color_data(CharacterCode.STELLA)
		patty_color_data = generate_color_data(CharacterCode.PATTY)

		with open(os.path.join(root, 'sys/main.dol'), 'rb+') as mainDol:
			# modify character primary color
			mainDol.seek(mapper.boomToFileAddress(mario_color_data.primary_color_address))
			mainDol.write(ColorTable.RED.value)

			# modify character secondary color
			mainDol.seek(mapper.boomToFileAddress(mario_color_data.secondary_color_address))
			mainDol.write(ColorTable.BLUE.value)

			# modify character tertiary color
			mainDol.seek(mapper.boomToFileAddress(mario_color_data.tertiary_color_address))
			mainDol.write(ColorTable.YELLOW.value)

			# modify character quaternary color
			mainDol.seek(mapper.boomToFileAddress(mario_color_data.quaternary_color_address))
			mainDol.write(ColorTable.WHITE.value)

			# modify character primary color
			mainDol.seek(mapper.boomToFileAddress(luigi_color_data.primary_color_address))
			mainDol.write(ColorTable.GREEN.value)

			# modify character secondary color
			mainDol.seek(mapper.boomToFileAddress(luigi_color_data.secondary_color_address))
			mainDol.write(ColorTable.BLUE.value)

			# modify character tertiary color
			mainDol.seek(mapper.boomToFileAddress(luigi_color_data.tertiary_color_address))
			mainDol.write(ColorTable.DARKGREEN.value)

			# modify character quaternary color
			mainDol.seek(mapper.boomToFileAddress(luigi_color_data.quaternary_color_address))
			mainDol.write(ColorTable.LIME.value)

			# modify character primary color
			mainDol.seek(mapper.boomToFileAddress(peach_color_data.primary_color_address))
			mainDol.write(ColorTable.PINK.value)

			# modify character secondary color
			mainDol.seek(mapper.boomToFileAddress(peach_color_data.secondary_color_address))
			mainDol.write(ColorTable.FUCHSIA.value)

			# modify character tertiary color
			mainDol.seek(mapper.boomToFileAddress(peach_color_data.tertiary_color_address))
			mainDol.write(ColorTable.YELLOW.value)

			# modify character quaternary color
			mainDol.seek(mapper.boomToFileAddress(peach_color_data.quaternary_color_address))
			mainDol.write(ColorTable.TEAL.value)

			# modify character primary color
			mainDol.seek(mapper.boomToFileAddress(yoshi_color_data.primary_color_address))
			mainDol.write(ColorTable.GREEN.value)

			# modify character secondary color
			mainDol.seek(mapper.boomToFileAddress(yoshi_color_data.secondary_color_address))
			mainDol.write(ColorTable.LIME.value)

			# modify character tertiary color
			mainDol.seek(mapper.boomToFileAddress(yoshi_color_data.tertiary_color_address))
			mainDol.write(ColorTable.ORANGE.value)

			# modify character quaternary color
			mainDol.seek(mapper.boomToFileAddress(yoshi_color_data.quaternary_color_address))
			mainDol.write(ColorTable.RED.value)

			# modify character primary color
			mainDol.seek(mapper.boomToFileAddress(bowser_color_data.primary_color_address))
			mainDol.write(ColorTable.YELLOW.value)

			# modify character secondary color
			mainDol.seek(mapper.boomToFileAddress(bowser_color_data.secondary_color_address))
			mainDol.write(ColorTable.DARKGREEN.value)

			# modify character tertiary color
			mainDol.seek(mapper.boomToFileAddress(bowser_color_data.tertiary_color_address))
			mainDol.write(ColorTable.RED.value)

			# modify character quaternary color
			mainDol.seek(mapper.boomToFileAddress(bowser_color_data.quaternary_color_address))
			mainDol.write(ColorTable.GREEN.value)

			# modify character primary color
			mainDol.seek(mapper.boomToFileAddress(toad_color_data.primary_color_address))
			mainDol.write(ColorTable.RED.value)

			# modify character secondary color
			mainDol.seek(mapper.boomToFileAddress(toad_color_data.secondary_color_address))
			mainDol.write(ColorTable.BLUE.value)

			# modify character tertiary color
			mainDol.seek(mapper.boomToFileAddress(toad_color_data.tertiary_color_address))
			mainDol.write(ColorTable.WHITE.value)

			# modify character quaternary color
			mainDol.seek(mapper.boomToFileAddress(toad_color_data.quaternary_color_address))
			mainDol.write(ColorTable.YELLOW.value)

			# modify character primary color
			mainDol.seek(mapper.boomToFileAddress(dk_color_data.primary_color_address))
			mainDol.write(ColorTable.WINE.value)

			# modify character secondary color
			mainDol.seek(mapper.boomToFileAddress(dk_color_data.secondary_color_address))
			mainDol.write(ColorTable.RED.value)

			# modify character tertiary color
			mainDol.seek(mapper.boomToFileAddress(dk_color_data.tertiary_color_address))
			mainDol.write(ColorTable.YELLOW.value)

			# modify character quaternary color
			mainDol.seek(mapper.boomToFileAddress(dk_color_data.quaternary_color_address))
			mainDol.write(ColorTable.APRICOT.value)

			# modify character primary color
			mainDol.seek(mapper.boomToFileAddress(wario_color_data.primary_color_address))
			mainDol.write(ColorTable.YELLOW.value)

			# modify character secondary color
			mainDol.seek(mapper.boomToFileAddress(wario_color_data.secondary_color_address))
			mainDol.write(ColorTable.PURPLE.value)

			# modify character tertiary color
			mainDol.seek(mapper.boomToFileAddress(wario_color_data.tertiary_color_address))
			mainDol.write(ColorTable.DARKGREEN.value)

			# modify character quaternary color
			mainDol.seek(mapper.boomToFileAddress(wario_color_data.quaternary_color_address))
			mainDol.write(ColorTable.WHITE.value)

			# modify character primary color
			mainDol.seek(mapper.boomToFileAddress(waluigi_color_data.primary_color_address))
			mainDol.write(ColorTable.PURPLE.value)

			# modify character secondary color
			mainDol.seek(mapper.boomToFileAddress(waluigi_color_data.secondary_color_address))
			mainDol.write(ColorTable.LAVENDER.value)

			# modify character tertiary color
			mainDol.seek(mapper.boomToFileAddress(waluigi_color_data.tertiary_color_address))
			mainDol.write(ColorTable.ORANGE.value)

			# modify character quaternary color
			mainDol.seek(mapper.boomToFileAddress(waluigi_color_data.quaternary_color_address))
			mainDol.write(ColorTable.BLUE.value)

			# modify character primary color
			mainDol.seek(mapper.boomToFileAddress(daisy_color_data.primary_color_address))
			mainDol.write(ColorTable.YELLOW.value)

			# modify character secondary color
			mainDol.seek(mapper.boomToFileAddress(daisy_color_data.secondary_color_address))
			mainDol.write(ColorTable.ORANGE.value)

			# modify character tertiary color
			mainDol.seek(mapper.boomToFileAddress(daisy_color_data.tertiary_color_address))
			mainDol.write(ColorTable.TEAL.value)

			# modify character quaternary color
			mainDol.seek(mapper.boomToFileAddress(daisy_color_data.quaternary_color_address))
			mainDol.write(ColorTable.APRICOT.value)

			# modify character primary color
			mainDol.seek(mapper.boomToFileAddress(birdo_color_data.primary_color_address))
			mainDol.write(ColorTable.FUCHSIA.value)

			# modify character secondary color
			mainDol.seek(mapper.boomToFileAddress(birdo_color_data.secondary_color_address))
			mainDol.write(ColorTable.LAVENDER.value)

			# modify character tertiary color
			mainDol.seek(mapper.boomToFileAddress(birdo_color_data.tertiary_color_address))
			mainDol.write(ColorTable.PINK.value)

			# modify character quaternary color
			mainDol.seek(mapper.boomToFileAddress(birdo_color_data.quaternary_color_address))
			mainDol.write(ColorTable.RED.value)

			# modify character primary color
			mainDol.seek(mapper.boomToFileAddress(diddy_color_data.primary_color_address))
			mainDol.write(ColorTable.RED.value)

			# modify character secondary color
			mainDol.seek(mapper.boomToFileAddress(diddy_color_data.secondary_color_address))
			mainDol.write(ColorTable.YELLOW.value)

			# modify character tertiary color
			mainDol.seek(mapper.boomToFileAddress(diddy_color_data.tertiary_color_address))
			mainDol.write(ColorTable.APRICOT.value)

			# modify character quaternary color
			mainDol.seek(mapper.boomToFileAddress(diddy_color_data.quaternary_color_address))
			mainDol.write(ColorTable.WHITE.value)

			# modify character primary color
			mainDol.seek(mapper.boomToFileAddress(bowserjr_color_data.primary_color_address))
			mainDol.write(ColorTable.LIME.value)

			# modify character secondary color
			mainDol.seek(mapper.boomToFileAddress(bowserjr_color_data.secondary_color_address))
			mainDol.write(ColorTable.YELLOW.value)

			# modify character tertiary color
			mainDol.seek(mapper.boomToFileAddress(bowserjr_color_data.tertiary_color_address))
			mainDol.write(ColorTable.WINE.value)

			# modify character quaternary color
			mainDol.seek(mapper.boomToFileAddress(bowserjr_color_data.quaternary_color_address))
			mainDol.write(ColorTable.RED.value)

			# modify character primary color
			mainDol.seek(mapper.boomToFileAddress(slime_color_data.primary_color_address))
			mainDol.write(ColorTable.BLUE.value)

			# modify character secondary color
			mainDol.seek(mapper.boomToFileAddress(slime_color_data.secondary_color_address))
			mainDol.write(ColorTable.LIGHTBLUE.value)

			# modify character tertiary color
			mainDol.seek(mapper.boomToFileAddress(slime_color_data.tertiary_color_address))
			mainDol.write(ColorTable.RED.value)

			# modify character quaternary color
			mainDol.seek(mapper.boomToFileAddress(slime_color_data.quaternary_color_address))
			mainDol.write(ColorTable.ORANGE.value)

			# modify character primary color
			mainDol.seek(mapper.boomToFileAddress(princessa_color_data.primary_color_address))
			mainDol.write(ColorTable.WINE.value)

			# modify character secondary color
			mainDol.seek(mapper.boomToFileAddress(princessa_color_data.secondary_color_address))
			mainDol.write(ColorTable.FUCHSIA.value)

			# modify character tertiary color
			mainDol.seek(mapper.boomToFileAddress(princessa_color_data.tertiary_color_address))
			mainDol.write(ColorTable.WHITE.value)

			# modify character quaternary color
			mainDol.seek(mapper.boomToFileAddress(princessa_color_data.quaternary_color_address))
			mainDol.write(ColorTable.RED.value)

			# modify character primary color
			mainDol.seek(mapper.boomToFileAddress(kiryl_color_data.primary_color_address))
			mainDol.write(ColorTable.GREEN.value)

			# modify character secondary color
			mainDol.seek(mapper.boomToFileAddress(kiryl_color_data.secondary_color_address))
			mainDol.write(ColorTable.BLUE.value)

			# modify character tertiary color
			mainDol.seek(mapper.boomToFileAddress(kiryl_color_data.tertiary_color_address))
			mainDol.write(ColorTable.LIME.value)

			# modify character quaternary color
			mainDol.seek(mapper.boomToFileAddress(kiryl_color_data.quaternary_color_address))
			mainDol.write(ColorTable.YELLOW.value)

			# modify character primary color
			mainDol.seek(mapper.boomToFileAddress(yangus_color_data.primary_color_address))
			mainDol.write(ColorTable.LIME.value)

			# modify character secondary color
			mainDol.seek(mapper.boomToFileAddress(yangus_color_data.secondary_color_address))
			mainDol.write(ColorTable.TEAL.value)

			# modify character tertiary color
			mainDol.seek(mapper.boomToFileAddress(yangus_color_data.tertiary_color_address))
			mainDol.write(ColorTable.BLUE.value)

			# modify character quaternary color
			mainDol.seek(mapper.boomToFileAddress(yangus_color_data.quaternary_color_address))
			mainDol.write(ColorTable.RED.value)

			# modify character primary color
			mainDol.seek(mapper.boomToFileAddress(angelo_color_data.primary_color_address))
			mainDol.write(ColorTable.WINE.value)

			# modify character secondary color
			mainDol.seek(mapper.boomToFileAddress(angelo_color_data.secondary_color_address))
			mainDol.write(ColorTable.WHITE.value)

			# modify character tertiary color
			mainDol.seek(mapper.boomToFileAddress(angelo_color_data.tertiary_color_address))
			mainDol.write(ColorTable.PURPLE.value)

			# modify character quaternary color
			mainDol.seek(mapper.boomToFileAddress(angelo_color_data.quaternary_color_address))
			mainDol.write(ColorTable.RED.value)

			# modify character primary color
			mainDol.seek(mapper.boomToFileAddress(platypunk_color_data.primary_color_address))
			mainDol.write(ColorTable.WHITE.value)

			# modify character secondary color
			mainDol.seek(mapper.boomToFileAddress(platypunk_color_data.secondary_color_address))
			mainDol.write(ColorTable.BLUE.value)

			# modify character tertiary color
			mainDol.seek(mapper.boomToFileAddress(platypunk_color_data.tertiary_color_address))
			mainDol.write(ColorTable.ORANGE.value)

			# modify character quaternary color
			mainDol.seek(mapper.boomToFileAddress(platypunk_color_data.quaternary_color_address))
			mainDol.write(ColorTable.YELLOW.value)

			# modify character primary color
			mainDol.seek(mapper.boomToFileAddress(bianca_color_data.primary_color_address))
			mainDol.write(ColorTable.TEAL.value)

			# modify character secondary color
			mainDol.seek(mapper.boomToFileAddress(bianca_color_data.secondary_color_address))
			mainDol.write(ColorTable.ORANGE.value)

			# modify character tertiary color
			mainDol.seek(mapper.boomToFileAddress(bianca_color_data.tertiary_color_address))
			mainDol.write(ColorTable.YELLOW.value)

			# modify character quaternary color
			mainDol.seek(mapper.boomToFileAddress(bianca_color_data.quaternary_color_address))
			mainDol.write(ColorTable.DARKGREEN.value)

			# modify character primary color
			mainDol.seek(mapper.boomToFileAddress(alena_color_data.primary_color_address))
			mainDol.write(ColorTable.YELLOW.value)

			# modify character secondary color
			mainDol.seek(mapper.boomToFileAddress(alena_color_data.secondary_color_address))
			mainDol.write(ColorTable.ORANGE.value)

			# modify character tertiary color
			mainDol.seek(mapper.boomToFileAddress(alena_color_data.tertiary_color_address))
			mainDol.write(ColorTable.BLUE.value)

			# modify character quaternary color
			mainDol.seek(mapper.boomToFileAddress(alena_color_data.quaternary_color_address))
			mainDol.write(ColorTable.RED.value)

			# modify character primary color
			mainDol.seek(mapper.boomToFileAddress(carver_color_data.primary_color_address))
			mainDol.write(ColorTable.LIME.value)

			# modify character secondary color
			mainDol.seek(mapper.boomToFileAddress(carver_color_data.secondary_color_address))
			mainDol.write(ColorTable.ORANGE.value)

			# modify character tertiary color
			mainDol.seek(mapper.boomToFileAddress(carver_color_data.tertiary_color_address))
			mainDol.write(ColorTable.PINK.value)

			# modify character quaternary color
			mainDol.seek(mapper.boomToFileAddress(carver_color_data.quaternary_color_address))
			mainDol.write(ColorTable.APRICOT.value)

			# modify character primary color
			mainDol.seek(mapper.boomToFileAddress(jessica_color_data.primary_color_address))
			mainDol.write(ColorTable.WINE.value)

			# modify character secondary color
			mainDol.seek(mapper.boomToFileAddress(jessica_color_data.secondary_color_address))
			mainDol.write(ColorTable.LAVENDER.value)

			# modify character tertiary color
			mainDol.seek(mapper.boomToFileAddress(jessica_color_data.tertiary_color_address))
			mainDol.write(ColorTable.RED.value)

			# modify character quaternary color
			mainDol.seek(mapper.boomToFileAddress(jessica_color_data.quaternary_color_address))
			mainDol.write(ColorTable.ORANGE.value)

			# modify character primary color
			mainDol.seek(mapper.boomToFileAddress(dragonlord_color_data.primary_color_address))
			mainDol.write(ColorTable.LAVENDER.value)

			# modify character secondary color
			mainDol.seek(mapper.boomToFileAddress(dragonlord_color_data.secondary_color_address))
			mainDol.write(ColorTable.PURPLE.value)

			# modify character tertiary color
			mainDol.seek(mapper.boomToFileAddress(dragonlord_color_data.tertiary_color_address))
			mainDol.write(ColorTable.BLUE.value)

			# modify character quaternary color
			mainDol.seek(mapper.boomToFileAddress(dragonlord_color_data.quaternary_color_address))
			mainDol.write(ColorTable.WINE.value)

			# modify character primary color
			mainDol.seek(mapper.boomToFileAddress(stella_color_data.primary_color_address))
			mainDol.write(ColorTable.ORANGE.value)

			# modify character secondary color
			mainDol.seek(mapper.boomToFileAddress(stella_color_data.secondary_color_address))
			mainDol.write(ColorTable.YELLOW.value)

			# modify character tertiary color
			mainDol.seek(mapper.boomToFileAddress(stella_color_data.tertiary_color_address))
			mainDol.write(ColorTable.FUCHSIA.value)

			# modify character quaternary color
			mainDol.seek(mapper.boomToFileAddress(stella_color_data.quaternary_color_address))
			mainDol.write(ColorTable.PINK.value)

			# modify character primary color
			mainDol.seek(mapper.boomToFileAddress(patty_color_data.primary_color_address))
			mainDol.write(ColorTable.ORANGE.value)

			# modify character secondary color
			mainDol.seek(mapper.boomToFileAddress(patty_color_data.secondary_color_address))
			mainDol.write(ColorTable.BLUE.value)

			# modify character tertiary color
			mainDol.seek(mapper.boomToFileAddress(patty_color_data.tertiary_color_address))
			mainDol.write(ColorTable.WINE.value)

			# modify character quaternary color
			mainDol.seek(mapper.boomToFileAddress(patty_color_data.quaternary_color_address))
			mainDol.write(ColorTable.WHITE.value)

			# modify colors of the UI
			mainDol.seek(mapper.boomToFileAddress(0x80417904))
			mainDol.write(b'\xBA\x8A\xEA')                       # Navy UI to Lavender
			mainDol.seek(mapper.boomToFileAddress(0x80417948))
			mainDol.write(b'\xBA\x8A\xEA')

			mainDol.seek(mapper.boomToFileAddress(0x80417910))
			mainDol.write(b'\x3E\xB7\xB3')                       # Tangerine UI to Teal
			mainDol.seek(mapper.boomToFileAddress(0x80417954))
			mainDol.write(b'\x3E\xB7\xB3')

			mainDol.seek(mapper.boomToFileAddress(0x8041791c))
			mainDol.write(b'\xEE\xB8\xA7')                       # Brown UI to Apricot
			mainDol.seek(mapper.boomToFileAddress(0x80417960))
			mainDol.write(b'\xEE\xB8\xA7')

			mainDol.seek(mapper.boomToFileAddress(0x80417920))
			mainDol.write(b'\xEF\x2D\x84')                       # Magenta UI to Fuchsia
			mainDol.seek(mapper.boomToFileAddress(0x80417964))
			mainDol.write(b'\xEF\x2D\x84')

			mainDol.seek(mapper.boomToFileAddress(0x8041792c))
			mainDol.write(b'\x8A\x00\x25')                       # Burgundy UI to Wine
			mainDol.seek(mapper.boomToFileAddress(0x80417970))
			mainDol.write(b'\x8A\x00\x25')

			mainDol.seek(mapper.boomToFileAddress(0x80417968))
			mainDol.write(b'\x78\x28\x8C')                       # Purple UI mismatch fix

		# copy files specified in .json
		modpack_dir = self.modpackDir()
		with open(os.path.join(modpack_dir, f'{MODID}.json'), 'rb') as config_file:
			config = json.load(config_file)
			for command in config:
				copy_from = os.path.join(modpack_dir, command["from"])
				copy_to = os.path.join(root, command["to"])
				if os.path.isdir(copy_from):
					shutil.copytree(copy_from, copy_to, dirs_exist_ok=True)
				else:
					shutil.copy(copy_from, copy_to)


	def modifyArcFile(self):
		localeToTitleArcFile = {
			'ja': 'files/game/game_board.arc',
			'en': 'files/game/langEN/game_board_EN.arc',
			'de': 'files/game/langDE/game_board_DE.arc',
			'su': 'files/game/langES/game_board_ES.arc',
			'fr': 'files/game/langFR/game_board_FR.arc',
			'it': 'files/game/langIT/game_board_IT.arc',
			'uk': 'files/game/langUK/game_board_UK.arc',
		}
		return {
			arcFile:
			lambda root, gameInstance, modList, arcDir, locale=locale, modpackDir=self.modpackDir(): replMapIcons(locale, arcDir, modpackDir)
			for locale, arcFile in localeToTitleArcFile.items()
		}


	def modifyBrresFile(self):
		localeToTitleBrresFile = {
			'ja': 'files/game/mg_darts.brres',
			'en': 'files/game/langEN/mg_darts_EN.brres',
			'de': 'files/game/langDE/mg_darts_DE.brres',
			'su': 'files/game/langES/mg_darts_ES.brres',
			'fr': 'files/game/langFR/mg_darts_FR.brres',
			'it': 'files/game/langIT/mg_darts_IT.brres',
			'uk': 'files/game/langUK/mg_darts_UK.brres',
		}
		return {
			brresFile:
			lambda root, gameInstance, modList, brresDir, locale=locale, modpackDir=self.modpackDir(): replColorDartTextures(locale, brresDir, modpackDir)
			for locale, brresFile in localeToTitleBrresFile.items()
		}


mod = Mod()
