#!/bin/bash -
#===============================================================================
#
#          FILE: run.sh
#
#         USAGE: ./run.sh
#
#   DESCRIPTION: run the gama
#
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jean, 
#  ORGANIZATION: 
#       CREATED: 06/16/26 10:06:03
#      REVISION:  ---
#===============================================================================

PATH_TO_DIR="../../../mnt/c/Работа/MyBrainObsidian/personal-obsidian-vault/English/Dictionaries"

PATH_TO_FORGOTTEN="../../../mnt/c/Работа/MyBrainObsidian/personal-obsidian-vault/English/Forgotten/Forgotten.md"

python3 -m english_learning_app.models.game --mode $1 --format 2 --speed 1 --path "$PATH_TO_DIR" --path_forgotten "$PATH_TO_FORGOTTEN"
