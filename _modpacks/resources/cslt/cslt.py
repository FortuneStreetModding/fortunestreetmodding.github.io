import pycsmm
import os

from pathlib import Path

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


def replCharacterIcons(arcDir, modpackDir):
	arcFileDir = Path(*Path(arcDir).parts[Path(arcDir).parts.index('game'):])
	arcFileDirStr = str(arcFileDir)

	charaDirAll = os.path.join(modpackDir, arcFileDirStr)

	for dirEntry in os.scandir(charaDirAll):
		tplPath = os.path.join(arcDir, 'arc/timg', os.path.splitext(dirEntry.name)[0] + '.tpl')
		#print(tplPath, file=sys.stderr)
		pycsmm.convertPngToTpl(dirEntry.path, tplPath, "RGB5A3")


def replCharacterDartIcons(locale, brresDir, modpackDir):
	gameCharacterIconDarts = os.path.join(modpackDir, 'game/mg_darts.brres/icons')
	for dirEntry in os.scandir(gameCharacterIconDarts):
		texPath = os.path.join(brresDir, 'Textures(NW4R)', os.path.splitext(dirEntry.name)[0])
		pycsmm.convertPngToTex(dirEntry.path, texPath)

MODID = __name__

class Mod(pycsmm.CSMMMod, pycsmm.GeneralInterface, pycsmm.ArcFileInterface, pycsmm.BrresFileInterface, pycsmm.UiMessageInterface):
	def __init__(self):
		pycsmm.CSMMMod.__init__(self)
		pycsmm.GeneralInterface.__init__(self)
		pycsmm.ArcFileInterface.__init__(self)
		pycsmm.BrresFileInterface.__init__(self)
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
		title_files = {
			arcFile:
			lambda root, gameInstance, modList, arcDir, locale=locale, modpackDir=self.modpackDir(): replTitleImages(locale, arcDir, modpackDir)
			for locale, arcFile in localeToTitleArcFile.items()
		}

		characterArcFiles = [
			'files/game/ui_game_f_aln.arc',
			'files/game/ui_game_f_bnk.arc',
			'files/game/ui_game_f_cpa.arc',
			'files/game/ui_game_f_cpj.arc',
			'files/game/ui_game_f_ctr.arc',
			'files/game/ui_game_f_ddk.arc',
			'files/game/ui_game_f_dkk.arc',
			'files/game/ui_game_f_dzy.arc',
			'files/game/ui_game_f_hsn.arc',
			'files/game/ui_game_f_kkr.arc',
			'files/game/ui_game_f_knp.arc',
			'files/game/ui_game_f_krf.arc',
			'files/game/ui_game_f_lig.arc',
			'files/game/ui_game_f_mmj.arc',
			'files/game/ui_game_f_mro.arc',
			'files/game/ui_game_f_pch.arc',
			'files/game/ui_game_f_pdn.arc',
			'files/game/ui_game_f_red.arc',
			'files/game/ui_game_f_ruo.arc',
			'files/game/ui_game_f_slm.arc',
			'files/game/ui_game_f_snd.arc',
			'files/game/ui_game_f_wlg.arc',
			'files/game/ui_game_f_wro.arc',
			'files/game/ui_game_f_ygs.arc',
			'files/game/ui_game_f_yss.arc',
			'files/game/ui_game_f_zsc.arc',
		]
		character_files = {
			arcFile:
			lambda root, gameInstance, modList, arcDir, locale="", modpackDir=self.modpackDir(): replCharacterIcons(arcDir, modpackDir)
			for arcFile in characterArcFiles
		}

		all_files = {**title_files, **character_files}

		return all_files


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
			lambda root, gameInstance, modList, brresDir, locale=locale, modpackDir=self.modpackDir(): replCharacterDartIcons(locale, brresDir, modpackDir)
			for locale, brresFile in localeToTitleBrresFile.items()
		}

mod = Mod()
