#!/bin/bash -
#===============================================================================
#
#          FILE: requests.sh
#
#         USAGE: ./requests.sh
#
#   DESCRIPTION: 
#
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: YOUR NAME (), 
#  ORGANIZATION: 
#       CREATED: 06/26/26 18:08:31
#      REVISION:  ---
#===============================================================================

curl -X DELETE "http://localhost:8000/words/del_word" -H "Content-Type: application/json" -d '{"dict_i
d": 1, "word_id": 29}'

curl -X POST "http://localhost:8000/words/add_word" -H "Content-Type: application/json" -d '{"dict_id": 1, "word": ["slim", "худой"]}'
