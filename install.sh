#! /bin/bash

install_dependencies() {
	QTILE_DEPENDENCIES="xserver-xorg xinit xterm libpangocairo-1.0-0 python3-pip python3-xcffib python3-cairocffi imagemagick pipx dbus-x11 xdg-desktop-portal xdg-desktop-portal-gtk sddm"
	UTILS="kitty polybar rofi feh flatpak btop dunst curl"
	FLATPAK_APPS="ru.yandex.Browser"

	echo -e "\n\n##### Updating the system #####"
	sudo apt update
	sudo apt upgrade
	
	echo -e "\n\n##### Installing APT packages #####"
	sudo apt install -y ${QTILE_DEPENDENCIES} ${UTILS}

	echo -e "\n\n##### Installing PIP packages #####"
	pipx inject qtile pywal libcst

	echo -e "\n\n##### Installing Flatpak packages #####"
	flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
	flatpak install --assumeyes flathub ${FLATPAK_APPS}
}

install_dotfiles() {
	echo -e "\n\n##### Installing dotfiles #####"

	set -x
	
	# Coping dotfiles
	cp ./dotfiles/.bashrc ./dotfiles/.xinitrc ./dotfiles/.Xresources ~/
	cp ./dotfiles/.local/bin/* ~/.local/bin/
	
	# Coping qtile config
	rm -rf ~/.config/qtile
	cp -r ./dotfiles/.config/qtile ~/.config/
	
	# Coping backgrounds
	rm -rf ~/.local/share/backgrounds
	cp -r ./dotfiles/.local/share/backgrounds ~/.local/share/
	
	# Coping fonts
	rm -rf ~/.local/share/fonts
	cp -r ./dotfiles/.local/share/fonts ~/.local/share/
	
	# Coping scripts
	rm -rf ~/.local/share/fonts
	cp -r ./dotfiles/.local/share/fonts ~/.local/share/
	
	set +x

	echo -e "\n\n##### Caching X11 fonts #####"
	fc-cache -fv ~/.local/share/fonts

	mkdir -p /usr/share/xsessions/
	cp ./dotfiles/global/qtile.desktop /usr/share/xsessions/qtile.desktop
}

install_sddm_theme() {
	echo -e "\n\n##### Installing SDDM theme #####"
	
	set -x
	cp ./dotfiles/global/sddm.conf /etc/sddm.conf
	mkdir -p /usr/share/sddm/themes
	rm -rf /usr/share/sddm/themes/sugar-dark
	cp -r ./dotfiles/global/sddm-sugar-dark-1.2 /usr/share/sddm/themes/sugar-dark
	dpkg-reconfigure sddm
	
	set +x
}

install_grub_theme() {
	echo -e "\n\n##### Installing GRUB theme #####"
	
	cd ./dotfiles/global/Elegant-wave-float-grub-themes/left-dark-1080p
	./install.sh
	cd -
}

install_plymouth_theme() {
	echo -e "\n\n##### Installing plymouth theme ($1) #####"	
	cp -r ./dotfiles/global/plymouth-themes/* /usr/share/plymouth/themes/
	
	plymouth-set-default-theme -R $1
}
#install_dependencies
install_dotfiles
#install_sddm_theme
#install_grub_theme
#install_plymouth_theme owl
