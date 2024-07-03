import pycsmm
import os
import tempfile
import sys

UI_MSGS_ALL = {
	4292: "Official Boards: Official boards which have been ported to Fortune Street",
	4293: "Custom Boards: Boards which were created by the Custom Street Modding Community",
	4294: "Official Boards",
	4295: "Custom Boards",
	4309: "Main Menu (Official Boards)",
	4311: "Main Menu (Custom Boards)",
	4316: "Tutorial: Learn the rules of the game whilst playing on a special practice board.",
	4317: "Tutorial: Learn the rules of the game whilst playing on a special practice board.",
	4319: "Start the tutorial?",
	4320: "Start the tutorial?",
	4381: "You've completed all available tours with the offical boards!",
	4382: "You've completed all available tours with the custom boards!",
	4446: "Tour Mode (Official Boards)",
	4447: "Tour Mode (Custom Boards)",
	4476: "Free Play (Official Boards)",
	4477: "Free Play (Custom Boards)",
	4812: "Official Boards",
	4813: "Custom Boards",
	4945: "Official Boards",
	4946: "Custom Boards",
}

UI_MSGS = {
	"de": {
		2881: "Ladenwert steigt um <price_diff><g>!<n>Ladenpreise steigen um <fee_diff><g>!<n>Max. Kapital ist nun <zoushi_full><g>.",
		2885: "Ladenwert sinkt um <price_diff><g>.<n>Ladenpreise sinken um <fee_diff><g>.<n>Max. Kapital sinkt auf <zoushi_full><g>.",
		3295: "Dein Gesamtvermögen wird mit 5 % besteuert.",
		3305: "Du kaufst ein Geschenk für<n>60<g> x Stufe des Gastgebers = <bar><g>.",
		3370: "Wenn du vor dem Finanzamt<n>eines anderen Spielers Halt<n>machst, musst du eine<n>Vermögenssteuer von 5 %<n>bezahlen.",
		3572: "Der Preis glitscht an <en>! 100<g> x Stufe = <slgold><g> für den korrekten Wetteinsatz!",
	},
	"en": {
		2881: "<price_diff><g> rise in shop value!<n><fee_diff><g> rise in shop prices!<n>Max. capital becomes <zoushi_full><g>.",
		2885: "<price_diff><g> fall in shop value.<n><fee_diff><g> fall in shop prices.<n>Max. capital becomes <zoushi_full><g>.",
		3295: "You pay a 5% tax on your net worth.",
		3305: "You buy a gift to take with you for 60<g> x homeowner's level = <bar><g>.",
		3370: "If you don't own the tax office, when you land on it you have to pay a 5% tax on your net worth.",
		3572: "<en> takes away a prize of 100<g> x level = <slgold><g> for backing the winning boinger!",
	},
	"fr": {
		2881: "La valeur de la boutique grimpe de <price_diff><g> !<n>Les prix de la boutique grimpent de <fee_diff><g> !<n>Le capital max. est désormais de <zoushi_full><g>.",
		2885: "La valeur de la boutique chute de <price_diff><g>.<n>Les prix de la boutique chutent de <fee_diff><g>.<n>Le capital max. est désormais de <zoushi_full><g>.",
		3295: "Tu paies une taxe de 5% sur le total de tes biens.",
		3305: "Tu achètes un cadeau pour 60<g> x le niveau du propriétaire = <bar><g>.",
		3370: "Si l'hôtel des impôts ne t'appartient pas, tu dois payer un impôt de 5% du total de tes biens lorsque tu t'y arrêtes.",
		3572: "<en> remporte 100<g> x niveau = <slgold><g> pour avoir soutenu le gluant gluagnant !",
	},
	"it": {
		2881: "Il valore del negozio aumenta di <price_diff><g>!<n>I prezzi salgono di <fee_diff><g>!<n>Il limite d'investimento diventa <zoushi_full><g>.",
		2885: "Il valore del negozio si riduce di <price_diff><g>!<n>I prezzi nel negozio calano di <fee_diff><g>!<n>Il limite d'investimento diventa <zoushi_full><g>.",
		3295: "Paghi una tassa del 5% sul totale del tuo patrimonio.",
		3305: "Acquisti un regalo. Il prezzo è pari a 60<g> x il livello<n>del proprietario di casa = <bar><g>.",
		3370: "Se l'ufficio delle imposte<n>non è tuo, pagherai una tassa<n>pari al 5% del tuo patrimonio.",
		3572: "<en> ha indovinato chi<n>slimavrebbe vinto e intasca<n>100<g> x livello = <slgold><g>!",
	},
	"jp": {
		2881: "お店価格が <price_diff><g>アップ！<n>買い物料が <fee_diff><g>アップ！<n>増資あまりが <zoushi_full><g>になりました。",
		2885: "お店価格が <price_diff><g>ダウン・・・<n>買い物料が <fee_diff><g>ダウン・・・<n>増資あまりが <zoushi_full><g>になりました。",
		3295: "総資産の5％を払います。",
		3305: "おみやげ代として<n>持ち主のレベル×60<g><n>を払います。",
		3370: "持ち主以外が止まったとき<n>総資産の5％を払います。",
		3572: "<en>さんには<n>優勝賞金として<n>100<g>×レベル＝<slgold><g>さしあげます！",
	},
	"su": {
		2881: "¡El valor del local aumenta en <price_diff><g>!<n>¡Los precios del local aumentan en <fee_diff><g>!<n>El capital máx. es ahora <zoushi_full><g>.",
		2885: "El valor del local cae en <price_diff><g>.<n>Los precios del local caen en <fee_diff><g>.<n>El capital máx. es ahora <zoushi_full><g>.",
		3295: "Pagas un impuesto del 5% de todos tus bienes.",
		3305: "Compras un regalo por 60<g> x nivel del propietario = <bar><g>.",
		3370: "Si la tesorería no es tuya,<n>tendrás que pagar un<n>impuesto del 5% de tus<n>bienes totales.",
		3572: "<en> se lleva un premio<n>de 100<g> x nivel = <slgold><g><n>por haber acertaglop el limo glapnador.",
	},
	"uk": {
		2881: "<price_diff><g> rise in shop value!<n><fee_diff><g> rise in shop prices!<n>Max. capital becomes <zoushi_full><g>.",
		2885: "<price_diff><g> fall in shop value.<n><fee_diff><g> fall in shop prices.<n>Max. capital becomes <zoushi_full><g>.",
		3295: "You pay a 5% tax on your net worth.",
		3305: "You buy a gift to take with you for 60<g> x homeowner's level = <bar><g>.",
		3370: "If you don't own the tax office, when you land on it you have to pay a 5% tax on your net worth.",
		3572: "<en> takes away a prize of 100<g> x level = <slgold><g> for backing the winning boinger!",
	}
}

def replUiMessages(msgDict, toReplaceWith):
	for k,v in toReplaceWith.items():
		msgDict[k] = v

def replTitleImages(locale, arcDir, modpackDir):
	gameSeqTitleAll = os.path.join(modpackDir, 'cswtpycsmm/game_sequence_title_ALL.arc')
	for dirEntry in os.scandir(gameSeqTitleAll):
		tplPath = os.path.join(arcDir, 'arc/timg', os.path.splitext(dirEntry.name)[0] + '.tpl')
		#print(tplPath, file=sys.stderr)
		pycsmm.convertPngToTpl(dirEntry.path, tplPath)
	if locale == 'de':
		gameSeqTitleDe = os.path.join(modpackDir, 'cswtpycsmm/game_sequence_title_DE.arc')
		for dirEntry in os.scandir(gameSeqTitleDe):
			tplPath = os.path.join(arcDir, 'arc/timg', os.path.splitext(dirEntry.name)[0] + '.tpl')
			#print(tplPath, file=sys.stderr)
			pycsmm.convertPngToTpl(dirEntry.path, tplPath)

class Mod(pycsmm.CSMMMod, pycsmm.GeneralInterface, pycsmm.ArcFileInterface, pycsmm.UiMessageInterface):
	def __init__(self):
		pycsmm.CSMMMod.__init__(self)
		pycsmm.GeneralInterface.__init__(self)
		pycsmm.ArcFileInterface.__init__(self)
		pycsmm.UiMessageInterface.__init__(self)
	def modId(self):
		return "cswtpycsmm"
	def saveFiles(self, root, gameInstance, modList):
		mapper = gameInstance.addressMapper()
		with open(os.path.join(root, 'sys/main.dol'), 'rb+') as mainDol:
			# patch home price / level
			homePriceVal = (60).to_bytes(2, 'big')
			mainDol.seek(mapper.boomToFileAddress(0x8008fade))
			mainDol.write(homePriceVal)
			mainDol.seek(mapper.boomToFileAddress(0x8010da32))
			mainDol.write(homePriceVal)
			# change slurpodrome prizes to match standard mode
			mainDol.seek(mapper.boomToFileAddress(0x8081b5a8))
			mainDol.write((100).to_bytes(4, 'big'))
			# and coins
			mainDol.seek(mapper.boomToFileAddress(0x8081b5a0))
			mainDol.write((20).to_bytes(4, 'big'))
			# change dart of gold prizes to match standard mode
			mainDol.seek(mapper.boomToFileAddress(0x8013cda4))
			mainDol.write(b'\x48\x00\x00\x0c')
			# increase AI memory lookahead
			memoryLookaheadPatch = b'\x3c\x80\x00\x02'
			mainDol.seek(mapper.boomToFileAddress(0x8009e6c4))
			mainDol.write(memoryLookaheadPatch)
			mainDol.seek(mapper.boomToFileAddress(0x8009d368))
			mainDol.write(memoryLookaheadPatch)
			# decrease tax office tax to 5%
			mainDol.seek(mapper.boomToFileAddress(0x8008fa34))
			mainDol.write(b'\x7C\x00\x1E\x70')
			# change 3 star shop value to 500
			threeStarVal = 500
			for boomAddr in (0x8008f18e, 0x800ead3a, 0x800fcae2, 0x8015cf36, 0x80160ee2):
				mainDol.seek(mapper.boomToFileAddress(boomAddr))
				mainDol.write(threeStarVal.to_bytes(2, 'big'))
			mainDol.seek(mapper.boomToFileAddress(0x80411bb4))
			mainDol.write(threeStarVal.to_bytes(4, 'big'))
			# and price
			mainDol.seek(mapper.boomToFileAddress(0x8008f192))
			mainDol.write((100).to_bytes(2, 'big'))
			# unlock all characters
			mainDol.seek(mapper.boomToFileAddress(0x80210a4c))
			mainDol.write(b'\x3C\x60\xFF\xFF\x60\x63\xFF\xFF\x3C\x80\xFF\xFF\x60\x84\xFF\xFF\x60\x00\x00\x00')
			# unlock all maps
			mainDol.seek(mapper.boomToFileAddress(0x8020f8d8))
			mainDol.write(b'\x38\x60\x00\x01')
			mainDol.seek(mapper.boomToFileAddress(0x8020f91c))
			mainDol.write(b'\x38\x60\x00\x01')
			
	def saveUiMessages(self):
		return {f'files/localize/ui_message.{k}.csv':
			(lambda root, gameInstance, modList, msgDict, toReplaceWith=v: replUiMessages(msgDict, UI_MSGS_ALL | toReplaceWith))
			for k,v in UI_MSGS.items()}
	
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
