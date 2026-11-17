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

MACHINE_ID=$(cat /etc/machine-id)
APP_SALT="your_app_secret_salt"
HASHED_ID=$(echo -n "${APP_SALT}${MACHINE_ID}" | sha256sum | cut -d' ' -f1)
HASH=$(cat key.txt)

PATH_TO_APP=""
if [[ "$HASHED_ID" == "$HASH" ]];
then
PATH_TO_APP="../../../mnt/c/Работа/MyBrainObsidian/personal-obsidian-vault/English/MyEnglishApp/"
else
  echo "Change App Path"
  exit 1
fi

PATH_TO_DICTS="${PATH_TO_APP}Dictionaries/"
PATH_TO_FORGOTTEN="${PATH_TO_APP}Forgotten.md"
PATH_TO_STATS="${PATH_TO_APP}Knowledge statistics.md"

python3 -m english_learning_app.cli.main --mode $1 --format 2 --speed 0 --path "$PATH_TO_DICTS" --path_forgotten "$PATH_TO_FORGOTTEN" --path_stats "$PATH_TO_STATS"

exit 0