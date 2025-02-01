#! /bin/bash

QTILE_DEPENDENCIES="xserver-xorg xinit xterm libpangocairo-1.0-0 python3-pip python3-xcffib python3-cairocffi imagemagick pipx dbus-x11 xdg-desktop-portal xdg-desktop-portal-gtk sddm"
UTILS="kitty polybar rofi feh flatpak btop dunst curl"
FLATPAK_APPS=("ru.yandex.Browser" "com.visualstudio.code" "com.anydesk.Anydesk" "org.onlyoffice.desktopeditors" "org.videolan.VLC" "org.telegram.desktop" "com.getpostman.Postman" "org.qbittorrent.qBittorrent" "us.zoom.Zoom" "org.filezillaproject.Filezilla")

echo -e "${CYAN}"
echo -e "\n\n##### Installing APT packages #####"
echo -e "${NONE}"
sudo apt install -y ${QTILE_DEPENDENCIES} ${UTILS}

echo -e "${CYAN}"
echo -e "\n\n##### Installing PIP packages #####"
echo -e "${NONE}"
pipx inject qtile pywal libcst

echo -e "${CYAN}"
echo -e "\n\n##### Installing Flatpak packages #####"
echo -e "${NONE}"
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo

echo -e "${CYAN}"
cat <<"EOF"

 _____ _       _                    _                            
|  ___| | __ _| |_ _ __   __ _  ___| | __   __ _ _ __  _ __  ___ 
| |_  | |/ _` | __| '_ \ / _` |/ __| |/ /  / _` | '_ \| '_ \/ __|
|  _| | | (_| | |_| |_) | (_| | (__|   <  | (_| | |_) | |_) \__ \
|_|   |_|\__,_|\__| .__/ \__,_|\___|_|\_\  \__,_| .__/| .__/|___/
                  |_|                           |_|   |_|        

EOF
echo -e "${NONE}"

# Запрос на установку Flatpak приложений
echo -e "${YELLOW}Do you want to install Flatpak applications? (Y/N):${NONE}"
read -p "Enter your choice: " install_choice

if [[ $install_choice == "Y" || $install_choice == "y" ]]; then
    echo -e "${GREEN}Select Flatpak applications to install (separate with spaces):${NONE}"
    for i in "${!FLATPAK_APPS[@]}"; do
        echo -e "${GREEN}[ $((i + 1)) ] ${FLATPAK_APPS[$i]}${NONE}"  # Счетчик начинается с 1
    done

    read -p "Enter the indices of the applications you want to install: " -a selected_indices

    # Установка выбранных приложений
    for index in "${selected_indices[@]}"; do
        # Преобразуем индекс в 0-основной
        zero_based_index=$((index - 1))
        if [[ $zero_based_index =~ ^[0-9]+$ ]] && [ "$zero_based_index" -lt "${#FLATPAK_APPS[@]}" ]; then
            app="${FLATPAK_APPS[$zero_based_index]}"
            echo -e "${CYAN}Installing $app...${NONE}"
            flatpak install --assumeyes flathub "$app"

            # Создание десктоп-файла
            app_name=$(echo "$app" | awk -F. '{print $NF}')  # Получаем имя приложения
            desktop_file="$HOME/.local/share/applications/$app_name.desktop"

            echo -e "[Desktop Entry]" > "$desktop_file"
            echo -e "Name=$app_name" >> "$desktop_file"
            echo -e "Exec=flatpak run $app" >> "$desktop_file"
            echo -e "Icon=$app_name" >> "$desktop_file"
            echo -e "Type=Application" >> "$desktop_file"
            echo -e "Categories=Utility;" >> "$desktop_file"  # Вы можете изменить категории по необходимости
            echo -e "StartupNotify=true" >> "$desktop_file"

            echo -e "${GREEN}Desktop file created: $desktop_file${NONE}"
        else
            echo "Invalid index: $index"
        fi
    done
else
    echo -e "${RED}Flatpak application installation skipped.${NONE}"
fi

# flatpak install --assumeyes flathub ${FLATPAK_APPS}