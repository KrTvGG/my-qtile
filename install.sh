#! /bin/bash

install_dependencies() {
	INSTALLATION_DEPENDENCIES="sudo flatpak pipx"
	QTILE_DEPENDENCIES="xserver-xorg xinit xterm libpangocairo-1.0-0 python3-pip python3-xcffib python3-cairocffi imagemagick dbus-x11 xdg-desktop-portal xdg-desktop-portal-gtk sddm qml-module-qtquick-controls qml-module-qtquick-controls2 qml-module-qtquick-layouts qml-module-qtgraphicaleffects"
	UTILS="kitty polybar rofi feh btop dunst curl thunar"

	echo -e "\n\n##### Updating the system #####"
	sudo apt update
	sudo apt upgrade -y
	
	echo -e "\n\n##### Installing APT packages #####"
	sudo apt install -y ${INSTALLATION_DEPENDENCIES} ${QTILE_DEPENDENCIES} ${UTILS}

	echo -e "\n\n##### Installing PIP packages #####"
	pipx install qtile pywal mypy
	pipx inject qtile libcst psutil

	mypy --install-types
}

install_extra_apps() {
	echo -e "\n\n##### Installing Flatpak packages #####"
	flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
	flatpak install --assumeyes flathub ${@}
}

install_dotfiles() {
	echo -e "\n\n##### Installing dotfiles #####"

	set -x
	
	# Coping dotfiles
	cp ./dotfiles/.bashrc ./dotfiles/.xinitrc ./dotfiles/.Xresources ~/
	mkdir -p ~/.local/bin/
	cp ./dotfiles/.local/bin/* ~/.local/bin/
	
	# Coping qtile config
	rm -rf ~/.config/qtile
	cp -r ./dotfiles/.config/qtile ~/.config/
	
	# Coping backgrounds
	rm -rf ~/.local/share/backgrounds
	mkdir -p ~/.local/share/
	cp -r ./dotfiles/.local/share/backgrounds ~/.local/share/
	
	# Coping fonts
	rm -rf ~/.local/share/fonts
	cp -r ./dotfiles/.local/share/fonts ~/.local/share/
	
	# Coping scripts
	rm -rf ~/.local/share/scripts
	cp -r ./dotfiles/.local/share/scripts ~/.local/share/
	
	set +x

	echo -e "\n\n##### Caching X11 fonts #####"
	fc-cache -fv ~/.local/share/fonts

	sudo mkdir -p /usr/share/xsessions/
	sudo cp ./dotfiles/global/qtile.desktop /usr/share/xsessions/qtile.desktop
}

install_system_configs() {
	echo -e "\n\n##### Installing global system configs #####"
	set -x
	
	sudo mkdir -p /etc/default
	sudo cp ./dotfiles/global/keyboard /etc/default/keyboard

	set +x
}

install_sddm_theme() {
	echo -e "\n\n##### Installing SDDM theme #####"
	
	set -x
	sudo cp ./dotfiles/global/sddm.conf /etc/sddm.conf
	sudo mkdir -p /usr/share/sddm/themes
	sudo rm -rf /usr/share/sddm/themes/sugar-dark
	sudo cp -r ./dotfiles/global/sddm-sugar-dark-1.2 /usr/share/sddm/themes/sugar-dark
	sudo dpkg-reconfigure sddm
	
	set +x
}

install_grub_theme() {
	echo -e "\n\n##### Installing GRUB theme #####"
	
	cd ./dotfiles/global/Elegant-wave-float-grub-themes/left-dark-1080p
	sudo ./install.sh
	cd -
}

install_plymouth_theme() {
	echo -e "\n\n##### Installing plymouth theme ($1) #####"
	sudo mkdir -p /usr/share/plymouth/themes/
	sudo cp -r ./dotfiles/global/plymouth-themes/* /usr/share/plymouth/themes/
	
	sudo plymouth-set-default-theme -R $1
}


FLATPAK_APPS="ru.yandex.Browser com.visualstudio.code com.anydesk.Anydesk org.onlyoffice.desktopeditors org.videolan.VLC org.telegram.desktop com.getpostman.Postman org.qbittorrent.qBittorrent us.zoom.Zoom org.filezillaproject.Filezilla"

install_dependencies
install_extra_apps $FLATPAK_APPS
install_dotfiles
install_system_configs
install_sddm_theme
install_grub_theme
install_plymouth_theme owl
