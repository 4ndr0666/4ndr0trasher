import os
import sys
import traceback
import subprocess
import shutil
import datetime
import pwd
from subprocess import PIPE, STDOUT
from pathlib import Path

# [COHESION MANDATE]: Enforce GI version BEFORE repository import
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, Pango, GLib

base_dir = os.path.dirname(os.path.realpath(__file__))

# =====================================================
#             Hardened Original User Detection
# =====================================================


def get_real_user():
    """Identifies the non-root user even when running under sudo."""
    pkexec_uid = os.environ.get("PKEXEC_UID")
    if pkexec_uid:
        try:
            return pwd.getpwuid(int(pkexec_uid)).pw_name
        except (KeyError, ValueError):
            pass

    sudo_user = os.environ.get("SUDO_USER")
    if sudo_user:
        return sudo_user

    try:
        return os.getlogin()
    except OSError:
        pass

    try:
        return (
            subprocess.check_output(["logname"], stderr=subprocess.DEVNULL)
            .decode()
            .strip()
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    home_env = os.environ.get("HOME", "")
    if home_env.startswith("/home/"):
        parts = home_env.split("/")
        if len(parts) >= 3:
            return parts[2]

    raise RuntimeError("get_real_user: Failed to determine identity.")


sudo_username = get_real_user()
home = "/home/" + str(sudo_username)
message = (
    "4ndr0trasher: ENVIRONMENT SANITIZER. "
    "Proceed with extreme prejudice. Ensure backups are enabled."
)

# =====================================================
#             Surgical Omission Matrix
# =====================================================

OMIT_LIST = [
    "BraveSoftware",
    "thorium-browser",
    "thorium",
    "google-chrome",
    "microsoft-edge",
    "mozilla",
    "discord",
    "Signal",
    "nvm",
    "nvim",
    "rustup",
    "virtualenv",
    "ice",
    "cargo",
    "pyenv",
    "mpv",
    "node",
    "vidcut",
    "cache",
    "Cache",
    "chromium",
    "SingletonCookie",
    "SingletonLock",
    ".cache",
    ".local/share/Trash",
]

# =====================================================
#                Logging & Path Checks
# =====================================================

log_dir = "/var/log/4ndr0trasher/"
adt_log_dir = "/var/log/4ndr0trasher/logs/"


def create_log(self):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d-%H-%M-%S")
    destination = adt_log_dir + "trasher-log-" + timestamp
    try:
        result = subprocess.run(
            ["sudo", "pacman", "-Q"],
            capture_output=True,
            text=True,
            check=False,
        )
        with open(destination, "w", encoding="utf-8") as fh:
            fh.write(result.stdout)
    except Exception:
        print(traceback.format_exc())
    GLib.idle_add(show_in_app_notification, self, "System state logged.")


def path_check(path):
    return os.path.isdir(path)


def MessageBox(self, title, message):
    md2 = Gtk.MessageDialog(
        parent=self,
        flags=0,
        message_type=Gtk.MessageType.INFO,
        buttons=Gtk.ButtonsType.OK,
        text=title,
    )
    md2.format_secondary_markup(message)
    md2.run()
    md2.destroy()


def show_in_app_notification(self, message):
    if self.timeout_id is not None:
        GLib.source_remove(self.timeout_id)
        self.timeout_id = None

    self.notification_label.set_markup(
        '<span foreground="white">' + message + "</span>"
    )
    self.notification_revealer.set_reveal_child(True)
    self.timeout_id = GLib.timeout_add(3000, timeOut, self)


def timeOut(self):
    close_in_app_notification(self)
    return False


def close_in_app_notification(self):
    self.notification_revealer.set_reveal_child(False)
    if self.timeout_id is not None:
        GLib.source_remove(self.timeout_id)
        self.timeout_id = None


def pop_box(self, combo):
    coms = []
    combo.get_model().clear()
    for session_dir in ("/usr/share/xsessions/", "/usr/share/wayland-sessions/"):
        if os.path.exists(session_dir):
            for item in os.listdir(session_dir):
                coms.append(item.split(".")[0].lower())
    coms.sort()
    excludes = {
        "gnome-classic",
        "gnome-xorg",
        "i3-with-shmlog",
        "openbox-kde",
        "cinnamon2d",
        "dwl",
        "hyprland",
        "",
    }
    for entry in coms:
        if entry not in excludes:
            combo.append_text(entry)


def pop_box_all(self, combo):
    combo.get_model().clear()
    for entry in desktop:
        combo.append_text(entry)


def permissions(dst):
    try:
        user_info = pwd.getpwnam(sudo_username)
        uid, gid = user_info.pw_uid, user_info.pw_gid
        os.chown(dst, uid, gid)
        for root, dirs, files in os.walk(dst):
            for node in dirs + files:
                full = os.path.join(root, node)
                try:
                    os.chown(full, uid, gid)
                except OSError:
                    pass
    except Exception as e:
        print(f"Permission error: {e}")


def make_backups(enabled=True, surgical=True):
    if not enabled:
        print("[INFO] Surgical backup bypassed by operator.")
        return
    backup_root = home + "/.config-4ndr0trasher"
    if not os.path.exists(backup_root):
        os.makedirs(backup_root, exist_ok=True)
    permissions(backup_root)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
    targets = [
        (".config", home + "/.config/", backup_root + "/config-" + timestamp),
        (".local", home + "/.local/", backup_root + "/local-" + timestamp),
    ]

    def surgical_filter(path, names):
        return [name for name in names if any(omit in name for omit in OMIT_LIST)]

    for label, src, dst in targets:
        if os.path.exists(src):
            print(f"Backing up {label}...")
            try:
                shutil.copytree(
                    src,
                    dst,
                    symlinks=True,
                    ignore=surgical_filter if surgical else None,
                    dirs_exist_ok=True,
                )
                permissions(dst)
            except Exception:
                print(f"[!] Warning: Partial success for {label}. Transient files skipped.")
                print(traceback.format_exc())


def remove_content_folders():
    subprocess.run(["rm", "-rf", home + "/.config/"], check=False)


def copy_skel():
    shutil.copytree("/etc/skel/", home + "/", dirs_exist_ok=True)
    permissions(home + "/")


def shutdown():
    subprocess.call(["sudo", "systemctl", "reboot"])


def restart_program():
    os.execl(sys.executable, sys.executable, *sys.argv)


# =====================================================
#                CONTENT OF DESKTOPS & SANITIZATION
# =====================================================

desktop = [
    "awesome",
    "berry",
    "bspwm",
    "budgie-desktop",
    "cinnamon",
    "chadwm",
    "cutefish-xsession",
    "cwm",
    "deepin",
    "dk",
    "dusk",
    "dwm",
    "enlightenment",
    "fvwm3",
    "gnome",
    "herbstluftwm",
    "hypr",
    "hyprland",
    "i3",
    "icewm",
    "jwm",
    "leftwm",
    "lxqt",
    "mate",
    "nimdow",
    "niri",
    "openbox",
    "pantheon",
    "plasma",
    "qtile",
    "spectrwm",
    "wayfire",
    "wmderland",
    "worm",
    "ukui",
    "xfce",
    "xmonad",
]

awesome = ["arcolinux-awesome-git", "arcolinux-rofi-git", "awesome", "rofi", "picom"]
berry = ["berry", "berry-git", "berry-dev-git"]
bspwm = ["bspwd", "bspwm-git", "bspwm", "sutils-git", "xtitle-git"]
budgie = ["budgie", "budgie-git", "budgie-desktop", "budgie-extras"]
chadwm = ["chadwm", "chadwm-git"]
cinnamon = ["cinnamon", "cinnamon-git", "cinnamon", "nemo-fileroller"]
cutefish = ["cutefish", "cutefish-git", "cutefish"]
cwm = ["cwm", "cwm-git", "cwm", "picom"]
deepin = ["deepin", "deepin-git", "deepin", "deepin-extra"]
dk = ["dk-git", "dk"]
dusk = ["dusk", "dusk-git", "picom"]
dwm = ["dwm", "dwm-titus", "dwm-git", "picom", "rofi"]
enlightenment = ["enlightenment"]
fvwm3 = ["fvwm3", "fvwm3-git", "fvwm3-git", "picom"]
gnome = ["gnome", "gnome-git", "gnome-extra"]
hlwm = ["herbstluftwm", "herbstluftwm-git", "herbstluftwm", "rofi"]
hypr = ["hypr", "hypr-git", "hypr-dev-git"]
hyprland = ["hyprland", "hyprland-git", "hyprland-git", "uwsm"]
i3 = ["i3wm-git", "i3-wm", "rofi"]
icewm = ["icewm-git", "icewm", "picom"]
jwm = ["jwm-git", "jwm", "picom"]
leftwm = ["leftwm-git", "leftwm", "leftwm-git"]
lxqt = ["lxqt-git", "lxqt"]
mate = ["mate-git", "mate-extra", "mate"]
nimdow = ["nimdow-git", "nimdow-bin"]
niri = ["niri-git", "niri"]
openbox = ["openbox-git", "openbox", "obmenu-generator"]
pantheon = ["pantheon"]
plasma = ["plasma-git", "plasma", "kde-applications-meta"]
qtile = ["qtile-git", "qtile"]
spectrwm = ["spectrwm-git", "spectrwm"]
ukui = ["ukui-git", "ukui"]
wayfire = ["wayfire", "wayfire-git", "wcm-git"]
wmderland = ["wmderland-git", "wmderland-git"]
worm = ["worm-git", "worm-dev-git"]
xfce = ["xfce4", "xfce4-goodies"]
xmonad = ["xmonad", "xmonad-contrib"]

# [WAYLAND VANGUARD]: Legacy X11 Purge Vector
x11_legacy_purge = [
    "xorg-server", "xorg-xinit", "xorg-xinput", "xorg-x11perf",
    "xorg-xbacklight", "xorg-xcmsdb", "xorg-xcursorgen",
    "xorg-xdpyinfo", "xorg-xdriinfo", "xorg-xev", "xorg-xgamma",
    "xorg-xhost", "xorg-xmodmap", "xorg-xpr", "xorg-xrandr",
    "xorg-xrdb", "xorg-xrefresh", "xorg-xset", "xorg-xsetroot",
    "xorg-xvinfo", "xorg-xwd", "xorg-xwininfo", "xorg-xwud",
    "xcompmgr", "picom", "arandr", "lxrandr"
]

# [WAYLAND VANGUARD]: Wayland Sanctity Locks
# Absolutely protected packages immune from targeted destruction
WAYLAND_SANCTITY = [
    "wayland", "wlroots", "wayland-protocols", "xorg-xwayland", 
    "dwl", "hyprland", "xwayland-run"
]

_CRITICAL_EXTRAS = {
    "budgie-desktop": ["gnome", "gnome-desktop", "gnome-online-accounts"],
    "gnome": ["gnome", "gnome-desktop", "gnome-online-accounts"],
    "deepin": ["deepin", "deepin-clutter"],
}

_DESKTOP_PACKAGES = {
    "awesome": awesome,
    "berry": berry,
    "bspwm": bspwm,
    "budgie-desktop": budgie,
    "chadwm": chadwm,
    "cinnamon": cinnamon,
    "cwm": cwm,
    "cutefish-xsession": cutefish,
    "deepin": deepin,
    "dk": dk,
    "dusk": dusk,
    "dwm": dwm,
    "enlightenment": enlightenment,
    "fvwm3": fvwm3,
    "gnome": gnome,
    "herbstluftwm": hlwm,
    "hypr": hypr,
    "hyprland": hyprland,
    "i3": i3,
    "icewm": icewm,
    "jwm": jwm,
    "leftwm": leftwm,
    "lxqt": lxqt,
    "mate": mate,
    "nimdow": nimdow,
    "niri": niri,
    "openbox": openbox,
    "pantheon": pantheon,
    "plasma": plasma,
    "qtile": qtile,
    "spectrwm": spectrwm,
    "ukui": ukui,
    "wayfire": wayfire,
    "wmderland": wmderland,
    "worm": worm,
    "xfce": xfce,
    "xmonad": xmonad,
    "x11-legacy-purge": x11_legacy_purge,
}

def remove_desktop(self, desktop_target: str) -> None:
    packages = _DESKTOP_PACKAGES.get(desktop_target)
    if not packages:
        return
        
    # Enforce Sanctity Locks
    safe_packages = [pkg for pkg in packages if pkg not in WAYLAND_SANCTITY]
    
    print(f"------------------------------------------------------------")
    print(f"TRASHING DESKTOP: {desktop_target}")
    print(f"------------------------------------------------------------")
    
    for pkg in safe_packages:
        print(f"Removing package: {pkg}")
        subprocess.call(["sudo", "pacman", "-Rs", pkg, "--noconfirm", "--ask=4"], shell=False)
        
    safe_criticals = [pkg for pkg in _CRITICAL_EXTRAS.get(desktop_target, []) if pkg not in WAYLAND_SANCTITY]
    for pkg in safe_criticals:
        print(f"Removing critical package: {pkg}")
        subprocess.call(["sudo", "pacman", "-Rdd", pkg, "--noconfirm", "--ask=4"], shell=False)

}