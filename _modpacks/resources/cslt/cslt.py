import pycsmm
import os

def replTitleImages(locale, arcDir, modpackDir):
	gameSeqTitleAll = os.path.join(modpackDir, 'cslt/game_sequence_title_ALL.arc')
	for dirEntry in os.scandir(gameSeqTitleAll):
		tplPath = os.path.join(arcDir, 'arc/timg', os.path.splitext(dirEntry.name)[0] + '.tpl')
		#print(tplPath, file=sys.stderr)
		pycsmm.convertPngToTpl(dirEntry.path, tplPath)
	if locale == 'de':
		gameSeqTitleDe = os.path.join(modpackDir, 'cslt/game_sequence_title_DE.arc')
		for dirEntry in os.scandir(gameSeqTitleDe):
			tplPath = os.path.join(arcDir, 'arc/timg', os.path.splitext(dirEntry.name)[0] + '.tpl')
			#print(tplPath, file=sys.stderr)
			pycsmm.convertPngToTpl(dirEntry.path, tplPath)

MODID = __name__

class Mod(pycsmm.CSMMMod, pycsmm.GeneralInterface, pycsmm.ArcFileInterface, pycsmm.UiMessageInterface):
	def __init__(self):
		pycsmm.CSMMMod.__init__(self)
		pycsmm.GeneralInterface.__init__(self)
		pycsmm.ArcFileInterface.__init__(self)
		pycsmm.UiMessageInterface.__init__(self)

	def modId(self):
		return MODID

	def saveFiles(self, root, gameInstance, modList):
		mapper = gameInstance.addressMapper()
		with open(os.path.join(root, 'sys/main.dol'), 'rb+') as mainDol:
			# unlock all characters
			mainDol.seek(mapper.boomToFileAddress(0x80210a4c))
			mainDol.write(b'\x3C\x60\xFF\xFF\x60\x63\xFF\xFF\x3C\x80\xFF\xFF\x60\x84\xFF\xFF\x60\x00\x00\x00')
			# unlock all boards
			mainDol.seek(mapper.boomToFileAddress(0x8020f8d8))
			mainDol.write(b'\x38\x60\x00\x01')
			mainDol.seek(mapper.boomToFileAddress(0x8020f91c))
			mainDol.write(b'\x38\x60\x00\x01')

	def modifyArcFile(self):
		localeToTitleArcFile = {
			'ja': 'files/game/game_sequence_title.arc',
			'en': 'files/game/langEN/game_sequence_title_EN.arc',
			'de': 'files/game/langDE/game_sequence_title_DE.arc',
			'su': 'files/game/langES/game_sequence_title_ES.arc',
			'fr': 'files/game/langFR/game_sequence_title_FR.arc',
			'it': 'files/game/langIT/game_sequence_title_IT.arc',
			'uk': 'files/game/langUK/game_sequence_title_UK.arc',
		}

		return {
			arcFile:
			lambda root, gameInstance, modList, arcDir, locale=locale, modpackDir=self.modpackDir(): replTitleImages(locale, arcDir, modpackDir)
			for locale, arcFile in localeToTitleArcFile.items()
		}

mod = Mod()
