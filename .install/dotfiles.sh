#! /bin/bash

echo -e "${CYAN}"
echo -e "\n\n##### Installing dotfiles #####"
echo -e "${NONE}"

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

echo -e "${CYAN}"
echo -e "\n\n##### Caching X11 fonts #####"
echo -e "${NONE}"
fc-cache -fv ~/.local/share/fonts

mkdir -p /usr/share/xsessions/
cp ./dotfiles/global/qtile.desktop /usr/share/xsessions/qtile.desktop