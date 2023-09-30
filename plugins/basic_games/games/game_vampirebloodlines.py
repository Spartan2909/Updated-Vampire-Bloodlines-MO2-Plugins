# -*- encoding: utf-8 -*-
import os, sys
import mobase

from PyQt5.QtCore import QDir

from typing import List
from pathlib import Path

from ..basic_game import BasicGame, BasicGameSaveGame


class VampireModDataChecker(mobase.ModDataChecker):
    def __init__(self):
        super().__init__()
        self.validDirNames = [
            "cfg",
            "cl_dlls",
            "dlg",
            "dlls",
            "maps",
            "materials",
            "media",
            "models",
            "particles",
            "python",
            "resource",
            "scripts",
            "sound",
            "vdata",
        ]

    def dataLooksValid(
        self, tree: mobase.IFileTree
    ) -> mobase.ModDataChecker.CheckReturn:
        for entry in tree:
            if not entry.isDir():
                continue
            if entry.name().casefold() in self.validDirNames:
                return mobase.ModDataChecker.VALID
        return mobase.ModDataChecker.INVALID


class VampireSaveGame(BasicGameSaveGame):
    _filepath: Path

    def __init__(self, filepath: Path):
        super().__init__(filepath)
        self._filepath = filepath
        self.name = None
        self.elapsedTime = None


class VampireLocalSavegames(mobase.LocalSavegames):
    def __init__(self, myGameSaveDir):
        super().__init__()
        self._savesDir = myGameSaveDir.absolutePath()

    def mappings(self, profile_save_dir):
        m = mobase.Mapping()
        m.createTarget = True
        m.isDirectory = True
        m.source = profile_save_dir.absolutePath()
        m.destination = self._savesDir

        return [m]

    def prepareProfile(self, profile):
        return profile.localSavesEnabled()


class VampireTheMasqueradeBloodlinesGame(BasicGame):
    Name = "Vampire - The Masquerade: Bloodlines Support Plugin"
    Author = "Caleb Robson"
    Version = "2.0.0"
    Description = "Adds support for Vampires: The Masquerade - Bloodlines"

    GameName = "Vampire - The Masquerade: Bloodlines"
    GameShortName = "vampirebloodlines"
    GameNexusName = "vampirebloodlines"
    GameNexusId = 437
    GameSteamId = [2600]
    GameGogId = [1207659240]
    GameBinary = "vampire.exe"
    GameDataPath = "test dir"
    GameDocumentsDirectory = "%GAME_PATH%/vampire/cfg"
    GameSavesDirectory = "%GAME_PATH%/test dir/save"
    GameSaveExtension = "sav"

    def __init__(self):
        super().__init__()

    def init(self, organizer: mobase.IOrganizer) -> bool:
        super().init(organizer)
        self._featureMap[mobase.ModDataChecker] = VampireModDataChecker()
        self._featureMap[mobase.SaveGameInfo] = VampireSaveGame(
            Path(self.savesDirectory().absolutePath())
        )
        self._featureMap[mobase.LocalSavegames] = VampireLocalSavegames(
            self.savesDirectory()
        )

        VampireTheMasqueradeBloodlinesGame.GameDataPath = f'{self.detectGameDataPath()}'
        VampireTheMasqueradeBloodlinesGame.GameDocumentsDirectory = f'%GAME_PATH%/{self.detectGameDataPath()}/cfg'
        VampireTheMasqueradeBloodlinesGame.GameSavesDirectory = f'%GAME_PATH%/{self.detectGameDataPath()}/save'

        return True

    def initializeProfile(self, path: QDir, settings: int):
        # Create .cfg files if they don't exist
        for iniFile in self.iniFiles():
            iniPath = self.documentsDirectory().absoluteFilePath(iniFile)
            if not os.path.exists(iniPath):
                with open(iniPath, "w") as _:
                    pass

        super().initializeProfile(path, settings)

    def version(self):
        # Don't forget to import mobase!
        return mobase.VersionInfo(2, 0, 0, mobase.ReleaseType.final)

    def iniFiles(self):
        return ["autoexec.cfg", "user.cfg"]

    def listSaves(self, folder: QDir) -> List[mobase.ISaveGame]:
        ext = self._mappings.savegameExtension.get()
        return [
            VampireSaveGame(path)
            for path in Path(folder.absolutePath()).glob(f"*.{ext}")
        ]

    def detectGameDataPath(self) -> str:
        print(f'VTMB Plugin: detecting game data path, game absolute path is {self.gameDirectory().absolutePath()}', file=sys.stderr)
        if os.path.isdir(f'{self.gameDirectory().absolutePath()}/CQM'):
            print('VTMB Plugin: detected CQM', file=sys.stderr)
            return 'CQM'
        elif os.path.isdir(f'{self.gameDirectory().absolutePath()}/Unofficial_Patch'):
            print('VTMB Plugin: detected Unofficial Patch', file=sys.stderr)
            return 'Unofficial_Patch'
        else:
            print('VTMB Plugin: didn\'t detect anything', file=sys.stderr)
            return 'Vampire'
