import os
import re
import socket
import subprocess
import psutil
import json

from typing import List  # noqa: F401

# Proboblematic code
#from custom.bsp import Bsp as CustomBsp

from libqtile import bar, layout, widget, hook
#from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.config import (KeyChord,Key,Screen,Group,Drag,Click,ScratchPad,DropDown,Match,)
from libqtile.utils import guess_terminal
from libqtile.lazy import lazy
from libqtile import qtile


mod = "mod4"
terminal = guess_terminal()
myconfig = "/home/uriel/.config/qtile/config.py"

################################################
## Resize functions for bsp layout #############
################################################

def resize(qtile, direction):
    layout = qtile.current_layout
    child = layout.current
    parent = child.parent

    while parent:
        if child in parent.children:
            layout_all = False

            if (direction == "left" and parent.split_horizontal) or (
                direction == "up" and not parent.split_horizontal
            ):
                parent.split_ratio = max(5, parent.split_ratio - layout.grow_amount)
                layout_all = True
            elif (direction == "right" and parent.split_horizontal) or (
                direction == "down" and not parent.split_horizontal
            ):
                parent.split_ratio = min(95, parent.split_ratio + layout.grow_amount)
                layout_all = True

            if layout_all:
                layout.group.layout_all()
                break

        child = parent
        parent = child.parent


@lazy.function
def resize_left(qtile):
    resize(qtile, "left")


@lazy.function
def resize_right(qtile):
    resize(qtile, "right")


@lazy.function
def resize_up(qtile):
    resize(qtile, "up")


@lazy.function
def resize_down(qtile):
    resize(qtile, "down")
    
keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "shift"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "shift"], "c", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),
    Key(
        [mod],
        "d",
        lazy.spawn("appmenu"),
        desc="rofi instantos pywal ",
    ),
    Key(
        [mod, "shift"],
        "d",
        lazy.spawn("rofi -modi run,drun,window -lines 12 -padding 18 -width 60 -location 0 -show drun -sidebar-mode -columns 3"),
        desc="rofi pywal ",
    ),
    Key(
        [mod, "shift"],
        "m",
        lazy.spawn("walp"),
        desc="theme pywal ",
   ),
   Key(
        [],
        "Print",
        lazy.spawn("scrot '%S.png' -e -d 5'mv $f $$(xdg-user-dir PICTURES)/Ubuntu-%S-$wx$h.png ; feh $$(xdg-user-dir PICTURES)/Ubuntu-%S-$wx$h.png'"),
        desc="Print Screen",     
   ),
   Key(
        [mod],
        "w",
        lazy.spawn("firefox"),
        desc="launch firefox",
  ),      
  Key(
        [mod],
        "f",
        lazy.spawn("thunar"),
        desc="launch thunar",
  ),
  Key(
        [mod],
        "t",
        lazy.window.toggle_floating(),
        desc="Toggle floating on focused window",
  ),
             
]

def show_keys():
    key_help = ""
    for k in keys:
        mods = ""

        for m in k.modifiers:
            if m == "mod4":
                mods += "Super + "
            else:
                mods += m.capitalize() + " + "

        if len(k.key) > 1:
            mods += k.key.capitalize()
        else:
            mods += k.key

        key_help += "{:<30} {}".format(mods, k.desc + "\n")

    return key_help


keys.extend(
    []
)

####################################################
######   🌿🍀🐌🐣🐙🐢🐋🐸🐧🐬🐲🐀🐘🐝🐥  ###########
######         ♈♉♊♋♌♍♎♏♐♑      ###########
######          ᚠ ᚢ ᚦ ᚨ ᚱ ᚳ ᚷ ᚹ ᛏ ᛒ      ###########
######                          ###########
######                         ###########
####################################################
####################################################
workspaces = [
    {"name": "", "key": "1", "matches": [Match(wm_class="firefox")]},
    {
        "name": "",
        "key": "2",
        "matches": [
            Match(wm_class="Thunderbird"),
            Match(wm_class="transmission"),
            Match(wm_class="gnome-calendar"),
        ],
    },
    {
        "name": "",
        "key": "3",
        "matches": [
            Match(wm_class="joplin"),
            Match(wm_class="libreoffice"),
            Match(wm_class="org.pwmt.zathura"),
        ],
    },
    {"name": "", "key": "4", "matches": [Match(wm_class="geany")]},
    {"name": "", "key": "5", "matches": [Match(wm_class="thunar")]},                      

    {
        "name": "",
        "key": "6",
        "matches": [
            Match(wm_class="slack"),
            Match(wm_class="lightcord"),
            Match(wm_class="polari"),
        ],
    },
    {"name": "", "key": "7", "matches": [Match(wm_class="spotify")]},
    {"name": "", "key": "8", "matches": [Match(wm_class="gimp")]},
    {"name": "", "key": "9", "matches": []},
    {
        "name": "",
        "key": "0",
        "matches": [
            Match(wm_class="lxappearance"),
            Match(wm_class="pavucontrol"),
            Match(wm_class="connman-gtk"),
        ],
    },
]

groups = [
    ScratchPad(
        "scratchpad",
        [
            # define a drop down terminal.
            # it is placed in the upper third of screen by default.
            DropDown(
                "term",
                "alacritty --class dropdown -e tmux_startup.sh",
                height=0.6,
                on_focus_lost_hide=False,
                opacity=1,
                warp_pointer=False,
            ),
        ],
    ),
]

for workspace in workspaces:
    matches = workspace["matches"] if "matches" in workspace else None
    groups.append(Group(workspace["name"], matches=matches, layout="bsp"))
    keys.append(
        Key(
            [mod],
            workspace["key"],
            lazy.group[workspace["name"]].toscreen(),
            desc="Focus this desktop",
        )
    )
    keys.append(
        Key(
            [mod, "shift"],
            workspace["key"],
            lazy.window.togroup(workspace["name"]),
            desc="Move focused window to another group",
        )
    )
    
########################
# Define colors ########
########################
#Pywal Colors
colors = os.path.expanduser('~/.cache/wal/colors.json')
colordict = json.load(open(colors))
ColorZ=(colordict['colors']['color0'])
ColorA=(colordict['colors']['color1'])
ColorB=(colordict['colors']['color2'])
ColorC=(colordict['colors']['color3'])
ColorD=(colordict['colors']['color4'])
ColorE=(colordict['colors']['color5'])
ColorF=(colordict['colors']['color6'])
ColorG=(colordict['colors']['color7'])
ColorH=(colordict['colors']['color8'])
ColorI=(colordict['colors']['color9'])

colors = [
    ["#1c2023", "#1c2023"],  # background 0
    ["#d8dee9", "#d8dee9"],  # foreground 1
    ["#3b4252", "#3b4252"],  # background lighter 2
    ["#bf616a", "#bf616a"],  # red 3
    ["#a3be8c", "#a3be8c"],  # green 4
    ["#ebcb8b", "#ebcb8b"],  # yellow 5
    ["#81a1c1", "#81a1c1"],  # blue 6
    ["#b48ead", "#b48ead"],  # magenta 7
    ["#88c0d0", "#88c0d0"],  # cyan 8
    ["#e5e9f0", "#e5e9f0"],  # white 9
    ["#4c566a", "#4c566a"],  # grey 10
    ["#d08770", "#d08770"],  # orange 11
    ["#8fbcbb", "#8fbcbb"],  # super cyan 12
    ["#5e81ac", "#5e81ac"],  # super blue 13
    ["#242831", "#242831"],  # super dark background 14
]

layout_theme = {
    "border_width": 3,
    "margin": 9,
    "border_focus": ColorC,
    "border_normal": ColorZ,
    "font": "FiraCode Nerd Font",
    "grow_amount": 2,
}


# Problematic code
'''
layouts = [
    CustomBsp(**layout_theme, fair=False),
    layout.Max(**layout_theme),
    layout.Stack(num_stacks=2, **layout_theme),
    layout.Floating(**layout_theme, fullscreen_border_width=3, max_border_width=3),
    #layout.Columns(border_focus_stack='#d75f5f'),
]
'''

widget_defaults = dict(
    font='novamono for powerline bold',
    fontsize=11,
    padding=3,
    background=ColorZ
)
extension_defaults = widget_defaults.copy()

group_box_settings = {
    "padding" : 5,
                    "borderwidth" : 6,
                    "active" : colors[9],
                    "inactive" : colors[10],
                    "disable_drag" : True,
                    "rounded" : True,
                    "margin_y" : 3,
                    "margin_x" : 2,
                    "padding_y" :-1,
                    "padding_x" :4,
                    #hide_unused" :True,
                    "highlight_color" : colors[1],
                    "highlight_method" : "block",
                    "this_current_screen_border" : ColorZ,
                    "this_screen_border" : colors [1],
                    "other_current_screen_border" : colors[1],
                    "other_screen_border" : colors[1],
                    "foreground" : ColorG,
                    "background" : ColorC,
}

### Mouse_callback functions
def open_pavu():
    qtile.cmd_spawn("pavucontrol")

def open_instantsettings():
    qtile.cmd_spawn("instantstartmenu")    

screens = [
    Screen(
        bottom=bar.Gap(5),
        left=bar.Gap(5),
        right=bar.Gap(5),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
cursor_warp = False
main = None  # WARNING: this is deprecated and will be removed soon
bring_front_click = "floating_only"
floating_layout = layout.Floating(
    **layout_theme,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        Match(wm_type="utility"),
        Match(wm_type="notification"),
        Match(wm_type="toolbar"),
        Match(wm_type="splash"),
        Match(wm_type="dialog"),
        Match(wm_class="confirm"),
        Match(wm_class="dialog"),
        Match(wm_class="download"),
        Match(wm_class="error"),
        Match(wm_class="file_progress"),
        Match(wm_class="notification"),
        Match(wm_class="splash"),
        Match(wm_class="toolbar"),
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(wm_class="pomotroid"),
        Match(wm_class="cmatrixterm"),
        Match(title="Farge"),
        Match(wm_class="org.gnome.Nautilus"),
        Match(wm_class="feh"),
        Match(wm_class="gnome-calculator"),
        Match(wm_class="blueberry"),
    ],
)
auto_fullscreen = True
focus_on_window_activation = "focus"
reconfigure_screens = True
auto_minimize = True

# Startup scripts
@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser("~")
    subprocess.call([home + "/.config/qtile/autostart.sh"])
# Window swallowing ;)
@hook.subscribe.client_new
def _swallow(window):
    pid = window.window.get_net_wm_pid()
    ppid = psutil.Process(pid).ppid()
    cpids = {
        c.window.get_net_wm_pid(): wid for wid, c in window.qtile.windows_map.items()
    }
    for i in range(5):
        if not ppid:
            return
        if ppid in cpids:
            parent = window.qtile.windows_map.get(cpids[ppid])
            parent.minimized = True
            window.parent = parent
            return
        ppid = psutil.Process(ppid).ppid()

@hook.subscribe.client_killed
def _unswallow(window):
    if hasattr(window, "parent"):
        window.parent.minimized = False


# Go to group when app opens on matched group
@hook.subscribe.client_new
def modify_window(client):
    # if (client.window.get_wm_transient_for() or client.window.get_wm_type() in floating_types):
    #    client.floating = True

    for group in groups:  # follow on auto-move
        match = next((m for m in group.matches if m.compare(client)), None)
        if match:
            targetgroup = client.qtile.groups_map[
                group.name
            ]  # there can be multiple instances of a group
            targetgroup.cmd_toscreen(toggle=False)
            break


wmname = "LG3D"
