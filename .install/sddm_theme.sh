#! /bin/bash

echo -e "${CYAN}"
echo -e "\n\n##### Installing SDDM theme #####"
echo -e "${NONE}"
	
set -x
cp ./dotfiles/global/sddm.conf /etc/sddm.conf
mkdir -p /usr/share/sddm/themes
rm -rf /usr/share/sddm/themes/sugar-dark
cp -r ./dotfiles/global/sddm-sugar-dark-1.2 /usr/share/sddm/themes/sugar-dark
dpkg-reconfigure sddm

set +x