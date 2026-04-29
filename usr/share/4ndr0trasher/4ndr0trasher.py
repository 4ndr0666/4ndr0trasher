#!/usr/bin/env python3
# /* ---- 💫 4NDR0666OS: HUD ORCHESTRATOR 💫 ---- */
# Architecture: Statistically pure 3lectric-Glass implementation
# Priority: TOTALITARIAN OVERRIDE (USER: 800)

import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib

import GUI
import Functions as fn

# --- 3LECTRIC 6LASS CSS HUD (GTK3 SPEC COMPLIANT) ---
#
# GTK3 CSS parser constraints addressed:
#   1. The universal `*` selector CANNOT carry `color: <hex> !important` —
#      GTK3's parser resolves this at parse time and rejects hex values in
#      that position, emitting "is not a valid color name". Fix: remove color
#      from `*`, set it per-widget class below.
#   2. `text-shadow` is not a GTK3 CSS property. It is silently ignored in
#      most positions but can cause parse failures in strict contexts. Removed.
#   3. `font-family` with a comma-list in `*` is legal in GTK3 but only the
#      first matching family is used. Kept as-is (harmless).
#   4. `transition` on `*` is legal in GTK3 3.22+. Kept.
#
HUD_STYLE = b"""
/* --- RESET: safe properties only on universal selector --- */
* {
    background: none;
    font-family: "JetBrains Mono", monospace;
    transition: all 150ms ease-in-out;
}

/* --- MAIN WINDOW --- */
window.main-window {
    background-color: rgba(10, 19, 26, 0.72);
    border: 1px solid rgba(0, 229, 255, 0.2);
    box-shadow: 0 0 40px rgba(0, 229, 255, 0.15);
    color: #00E5FF;
}

/* --- HEADERBAR --- */
headerbar {
    background: rgba(10, 19, 26, 0.95);
    border-bottom: 2px solid #00E5FF;
    padding: 10px;
    color: #00E5FF;
}

headerbar .title {
    font-family: "Orbitron", sans-serif;
    font-size: 14pt;
    font-weight: 700;
    color: #67E8F9;
}

headerbar .subtitle {
    font-family: "JetBrains Mono", monospace;
    font-size: 9pt;
    color: rgba(0, 229, 255, 0.7);
}

/* --- GENERIC LABEL COLOUR (replaces the * color rule) --- */
label {
    color: #00E5FF;
}

/* --- GLASS PANEL --- */
.glass-panel {
    background: rgba(10, 19, 26, 0.55);
    border: 1px solid rgba(0, 229, 255, 0.3);
    border-radius: 4px;
    margin: 5px;
    color: #00E5FF;
}

/* --- BUTTONS: base --- */
button {
    background: rgba(10, 19, 26, 0.65);
    border: 1px solid rgba(0, 229, 255, 0.4);
    color: #00E5FF;
    border-radius: 0px;
    padding: 10px 20px;
    font-weight: bold;
}

button:hover {
    background: rgba(0, 229, 255, 0.2);
    border-color: #00E5FF;
    box-shadow: 0 0 20px rgba(0, 229, 255, 0.5);
    color: #67E8F9;
}

button:active {
    background: rgba(0, 229, 255, 0.3);
    color: #ffffff;
}

/* --- DESTRUCTIVE BUTTONS --- */
button.destructive-action,
button.destructive {
    border-color: #ff0055;
    color: #ff0055;
}

button.destructive-action:hover,
button.destructive:hover {
    background: rgba(255, 0, 85, 0.3);
    box-shadow: 0 0 25px #ff0055;
    color: #ffffff;
}

/* --- SWITCHES --- */
switch {
    background: #050A0F;
    border: 1px solid #00E5FF;
    color: #00E5FF;
}

switch slider {
    background: #00E5FF;
    box-shadow: 0 0 12px rgba(0, 229, 255, 0.8);
}

switch:checked {
    background: rgba(0, 229, 255, 0.2);
}

/* --- COMBOBOX / DROPDOWNS / POPOVERS --- */
combobox,
combobox button {
    background: rgba(10, 19, 26, 0.55);
    border: 1px solid rgba(0, 229, 255, 0.4);
    color: #00E5FF;
}

/* Target the spawned dropdown popups for glassmorphism */
combobox window.popup,
combobox window.popup menu,
menu,
popover {
    background: rgba(10, 19, 26, 0.65);
    border: 1px solid rgba(0, 229, 255, 0.3);
    box-shadow: 0 0 20px rgba(0, 229, 255, 0.15);
    color: #00E5FF;
}

menuitem {
    color: #00E5FF;
    padding: 5px;
}

menuitem:hover {
    background: rgba(0, 229, 255, 0.2);
    color: #ffffff;
}

/* --- SCROLLBARS --- */
scrollbar trough {
    background-color: rgba(0, 0, 0, 0.4);
}

scrollbar slider {
    background-color: #00E5FF;
    border-radius: 0;
    min-width: 6px;
    min-height: 6px;
}

scrollbar slider:hover {
    background-color: #67E8F9;
}

/* --- REVEALER / NOTIFICATION OVERLAY --- */
.notification-label {
    color: #ffffff;
    font-weight: bold;
}
"""


class Main(Gtk.Window):
    def __init__(self):
        super(Main, self).__init__()

        # Instance state required by fn.show_in_app_notification
        self.timeout_id = None

        # --- PHASE 1: HARDWARE ALPHA ENABLEMENT ---
        # set_app_paintable(True) MUST precede set_visual() — without it GTK
        # ignores the RGBA visual and renders a fully opaque solid background,
        # killing all glassmorphism transparency regardless of CSS alpha values.
        self.set_app_paintable(True)
        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual:
            self.set_visual(visual)
        else:
            print("[WARN] RGBA Visual unavailable. Compositor check required.")

        # --- PHASE 2: HUD STYLE INJECTION ---
        provider = Gtk.CssProvider()
        try:
            provider.load_from_data(HUD_STYLE)
        except Exception as e:
            # Surface parse errors without crashing; GTK will skip bad rules.
            print(f"[WARN] CSS parse warning: {e}")

        # Using USER priority (800) to override system-wide Adwaita/Breeze themes
        Gtk.StyleContext.add_provider_for_screen(
            screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_USER
        )

        self.set_default_size(800, 550)
        self.get_style_context().add_class("main-window")

        # --- PHASE 3: TITLEBAR HUD ---
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.set_title("4NDR0TRASHER // ENVIRONMENTAL PURGE")
        hb.set_subtitle("MATRIX STATE: ARMED")
        self.set_titlebar(hb)

        # Asset Mapping
        icon_path = os.path.join(fn.base_dir, 'images/4ndr0666os-icon.png')
        if os.path.exists(icon_path):
            self.set_icon_from_file(icon_path)

        # Build UI Matrix
        GUI.GUI(self, Gtk, GdkPixbuf, fn)

        # Create Log Infrastructure
        for d in [fn.log_dir, fn.adt_log_dir]:
            os.makedirs(d, exist_ok=True)

    def on_close_clicked(self, widget):
        Gtk.main_quit()

    def on_refresh_clicked(self, widget):
        fn.restart_program()

    def execute_purge(self, target):
        if not target:
            return
        fn.create_log(self)
        fn.make_backups(
            enabled=self.backup_switch.get_active(),
            surgical=self.surgical_switch.get_active()
        )
        fn.remove_desktop(self, target)
        if not self.donottouch.get_active():
            fn.remove_content_folders()
            fn.copy_skel()
        fn.create_log(self)
        GLib.idle_add(fn.show_in_app_notification, self, f"Matrix {target} purged.")

    def on_remove_clicked_installed(self, widget):
        self.execute_purge(self.installed_sessions.get_active_text())

    def on_remove_clicked(self, widget):
        self.execute_purge(self.desktopr.get_active_text())

    def on_reboot_clicked(self, widget):
        fn.shutdown()


if __name__ == "__main__":
    w = Main()
    w.connect("delete-event", Gtk.main_quit)
    w.show_all()
    Gtk.main()
