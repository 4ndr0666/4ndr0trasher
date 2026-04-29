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

# --- 3LECTRIC 6LASS CSS HUD (SPEC COMPLIANT) ---
# FIXED: Replaced 'background-image: none' with 'background: none' to mitigate GTK3 parser error.
HUD_STYLE = b"""
/* Force system-wide reset for application scope */
* {
    background: none !important;
    font-family: "JetBrains Mono", monospace !important;
    color: #00E5FF !important; /* --accent-cyan */
    transition: all 150ms ease-in-out !important;
}

window.main-window {
    background-color: rgba(10, 19, 26, 0.25) !important; /* --bg-glass-panel */
    border: 1px solid rgba(0, 229, 255, 0.2) !important; /* --accent-cyan-border-idle */
    box-shadow: 0 0 40px rgba(0, 229, 255, 0.15) !important;
}

headerbar {
    background: rgba(10, 19, 26, 0.95) !important;
    border-bottom: 2px solid #00E5FF !important;
    padding: 10px !important;
}

headerbar .title {
    font-family: "Orbitron", sans-serif !important;
    font-size: 14pt !important;
    font-weight: 700 !important;
    color: #67E8F9 !important; /* --text-cyan-active */
    text-shadow: 0 0 15px rgba(0, 229, 255, 0.8) !important;
}

.glass-panel {
    background: rgba(10, 19, 26, 0.15) !important;
    border: 1px solid rgba(0, 229, 255, 0.3) !important;
    border-radius: 4px !important;
    margin: 5px !important;
}

button {
    background: rgba(10, 19, 26, 0.6) !important;
    border: 1px solid rgba(0, 229, 255, 0.4) !important;
    color: #00E5FF !important;
    border-radius: 0px !important;
    padding: 10px 20px !important;
    font-weight: bold !important;
    text-shadow: 0 0 5px #00E5FF !important;
}

button:hover {
    background: rgba(0, 229, 255, 0.2) !important; /* --accent-cyan-bg-hover */
    border-color: #00E5FF !important;
    box-shadow: 0 0 20px rgba(0, 229, 255, 0.5) !important;
    color: #67E8F9 !important;
}

button.destructive {
    border-color: #ff0055 !important;
    color: #ff0055 !important;
    text-shadow: 0 0 10px #ff0055 !important;
}

button.destructive:hover {
    background: rgba(255, 0, 85, 0.3) !important;
    box-shadow: 0 0 25px #ff0055 !important;
    color: #ffffff !important;
}

switch {
    background: #050A0F !important;
    border: 1px solid #00E5FF !important;
}

switch slider {
    background: #00E5FF !important;
    box-shadow: 0 0 12px #00E5FF !important;
}

combobox {
    background: rgba(10, 19, 26, 0.9) !important;
    border: 1px solid #00E5FF !important;
}

/* Scrollbar Rebranding */
scrollbar trough { background-color: rgba(0, 0, 0, 0.4) !important; }
scrollbar slider { background-color: #00E5FF !important; border-radius: 0 !important; }
"""

class Main(Gtk.Window):
    def __init__(self):
        super(Main, self).__init__()
        
        # --- PHASE 1: HARDWARE ALPHA ENABLEMENT ---
        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual:
            self.set_visual(visual)
        else:
            print("[WARN] RGBA Visual unavailable. Compositor check required.")

        # --- PHASE 2: HUD STYLE INJECTION ---
        provider = Gtk.CssProvider()
        provider.load_from_data(HUD_STYLE)
        # Using USER priority (800) to crush system-wide Adwaita/Breeze themes
        Gtk.StyleContext.add_provider_for_screen(
            screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_USER
        )

        self.set_default_size(800, 550)
        self.get_style_context().add_class("main-window")

        # --- PHASE 3: TITLEBAR HUD DECAPITATION ---
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

        # Create Log Infrastructure offensively
        for d in [fn.log_dir, fn.adt_log_dir]:
            os.makedirs(d, exist_ok=True)

    def on_close_clicked(self, widget):
        Gtk.main_quit()

    def on_refresh_clicked(self, widget):
        fn.restart_program()

    def execute_purge(self, target):
        if not target: return
        fn.create_log(self)
        # Surgical Backup Integration
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
