#! /bin/bash

source .install/colors.sh
clear

source .install/banner.sh
source .install/update.sh
source .install/dependencies.sh
# source .install/dotfiles.sh
# source .install/sddm_theme.sh
# source .install/grub_theme.sh


install_plymouth_theme() {
	echo -e "\n\n##### Installing plymouth theme ($1) #####"	
	cp -r ./dotfiles/global/plymouth-themes/* /usr/share/plymouth/themes/
	
	plymouth-set-default-theme -R $1
}

#install_plymouth_theme owl
