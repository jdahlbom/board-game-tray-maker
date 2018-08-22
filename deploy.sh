#!/bin/bash

set -xe

TARGET=~/.config/inkscape/extensions

cp traymaker.py ${TARGET}
cp traymaker.inx ${TARGET}
cp traymaker_logic.py ${TARGET}
cp gloomhaven.py ${TARGET}
mkdir ${TARGET}/gloomhaven ||echo "gloomhaven directory exists."
cp gloomhaven/trays.json ${TARGET}/gloomhaven

