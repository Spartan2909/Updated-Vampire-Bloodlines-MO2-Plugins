# Updated Plugins for Vampire: The Masquerade - Bloodlines
 A set of plugins to improve MO2's functionality when managing Vampire - The Masquerade: Bloodlines.
 
## Details
 These plugins let MO2 deploy mods to the `Unofficial_Patch` and `CQM` directories, instead of the `vampire` directory. This stops modded files from being overwritten by those in the Unofficial Patch or the Clan Quest Mod. 
 
## Use
 Install as below, and it will work out of the box. If you use the Clan Quest Mod, make sure to choose the game 'Vampire The Masquerade - Clan Quest', or MO2 will crash.

## Installing
 Place the contents of the `plugins` folder in `MO2/plugins` (usually located in `C:/Modding` on windows), overwriting when asked.

## Uninstalling
 Remove `game_vampirebloodlines.py` and `game_vampireclanquest.py` from `MO2/plugins/basic_games/games`, and rename `game_vampirebloodlines.py.backup` (found in the same folder) to `game_vampirebloodlines.py`.
