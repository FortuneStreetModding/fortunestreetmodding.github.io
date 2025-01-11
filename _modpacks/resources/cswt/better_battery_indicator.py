import pycsmm
import os
import json
import shutil

MODID = __name__

class Mod(pycsmm.CSMMMod, pycsmm.GeneralInterface):
	def __init__(self):
		pycsmm.CSMMMod.__init__(self)
		pycsmm.GeneralInterface.__init__(self)
	def modId(self):
		return MODID
	def saveFiles(self, root, gameInstance, modList):
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

mod = Mod()