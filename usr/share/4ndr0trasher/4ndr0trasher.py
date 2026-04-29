#!/usr/bin/env python3
# 4ndr0trasher: Hardened Desktop Deconstruction Matrix
import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf, Pango, GLib
import GUI
import Functions as fn

class Main(Gtk.Window):
    def __init__(self):
        super(Main, self).__init__(title="4ndr0trasher")
        self.timeout_id = None
        self.set_border_width(10)
        self.set_default_size(700, 300)
        
        icon_path = os.path.join(fn.base_dir, 'images/4ndr0666os-icon.png')
        if os.path.exists(icon_path):
            self.set_icon_from_file(icon_path)

        GUI.GUI(self, Gtk, GdkPixbuf, fn)

        for d in [fn.log_dir, fn.adt_log_dir]:
            os.makedirs(d, exist_ok=True)
        
        backup_root = os.path.join(fn.home, ".config-4ndr0trasher")
        if os.path.exists(backup_root):
            fn.permissions(backup_root)

    def on_close_clicked(self, widget):
        Gtk.main_quit()

    def on_refresh_clicked(self, widget):
        fn.restart_program()

    def execute_purge(self, target):
        if not target: return
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
