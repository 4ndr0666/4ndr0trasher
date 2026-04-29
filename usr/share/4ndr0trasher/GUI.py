import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

def GUI(self, Gtk, GdkPixbuf, fn):
    self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    self.add(self.vbox)

    hbox0 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.notification_revealer = Gtk.Revealer()
    self.notification_label = Gtk.Label()
    pb_panel = GdkPixbuf.Pixbuf().new_from_file(fn.base_dir + '/images/panel.png')
    panel = Gtk.Image().new_from_pixbuf(pb_panel)
    overlayFrame = Gtk.Overlay()
    overlayFrame.add(panel)
    overlayFrame.add_overlay(self.notification_label)
    self.notification_revealer.add(overlayFrame)
    hbox0.pack_start(self.notification_revealer, True, False, 0)

    hbox2, hbox3, hbox4 = Gtk.Box(spacing=10), Gtk.Box(spacing=10), Gtk.Box(spacing=10)
    hbox7, hbox8, hbox9 = Gtk.Box(spacing=10), Gtk.Box(spacing=10), Gtk.Box(spacing=10)
    hbox10, hbox11, hbox12 = Gtk.Box(spacing=10), Gtk.Box(spacing=10), Gtk.Box(spacing=10)
    hbox13, hbox14, hbox15, hbox16 = Gtk.Box(spacing=10), Gtk.Box(spacing=10), Gtk.Box(spacing=10), Gtk.Box(spacing=10)

    img_pb = GdkPixbuf.Pixbuf().new_from_file_at_size(
        fn.os.path.join(fn.base_dir, 'images/4ndr0trasher-logo.png'), 235, 235
    )
    hbox4.pack_start(Gtk.Image().new_from_pixbuf(img_pb), True, False, 0)

    self.lbl_backup = Gtk.Label(label="Perform backup before trashing desktop")
    self.backup_switch = Gtk.Switch()
    self.backup_switch.set_active(True)
    hbox15.pack_start(self.lbl_backup, False, False, 0)
    hbox15.pack_end(self.backup_switch, False, False, 0)

    self.lbl_surgical = Gtk.Label(label="Surgical backup — omit heavy directories")
    self.surgical_switch = Gtk.Switch()
    self.surgical_switch.set_active(True)
    hbox16.pack_start(self.lbl_surgical, False, False, 0)
    hbox16.pack_end(self.surgical_switch, False, False, 0)

    self.backup_switch.connect("notify::active", lambda s, p: self.surgical_switch.set_sensitive(s.get_active()))

    self.donottouch = Gtk.Switch()
    self.donottouch.set_active(True)
    hbox14.pack_start(Gtk.Label(label="Protect current ~/.config content"), False, False, 0)
    hbox14.pack_end(self.donottouch, False, False, 0)

    self.installed_sessions = Gtk.ComboBoxText()
    fn.pop_box(self, self.installed_sessions)
    self.installed_sessions.set_active(0)
    hbox9.pack_start(Gtk.Label(label="Option 1 : Purge Installed Desktop"), False, False, 0)
    hbox9.pack_end(self.installed_sessions, False, False, 0)

    btnRemoveInstalled = Gtk.Button(label="Purge Matrix")
    btnRemoveInstalled.connect('clicked', self.on_remove_clicked_installed)
    hbox10.pack_end(btnRemoveInstalled, True, False, 0)

    self.desktopr = Gtk.ComboBoxText()
    fn.pop_box_all(self, self.desktopr)
    self.desktopr.set_active(0)
    hbox7.pack_start(Gtk.Label(label="Option 2 : Remove Any possible Desktop"), False, False, 0)
    hbox7.pack_end(self.desktopr, False, False, 0)

    btnRemove = Gtk.Button(label="Purge Matrix")
    btnRemove.connect('clicked', self.on_remove_clicked)
    hbox8.pack_end(btnRemove, True, False, 0)

    btnClose = Gtk.Button(label="Close Terminal")
    btnClose.connect('clicked', self.on_close_clicked)
    btnReboot = Gtk.Button(label="Reboot System")
    btnReboot.connect('clicked', self.on_reboot_clicked)
    hbox2.pack_end(btnClose, True, False, 0)
    hbox2.pack_end(btnReboot, True, False, 0)

    btnRefresh = Gtk.Button(label="Refresh View")
    btnRefresh.connect('clicked', self.on_refresh_clicked)
    hbox12.pack_end(btnRefresh, True, False, 0)

    lblmessage = Gtk.Label()
    lblmessage.set_markup(f'<span foreground="red" size="xx-large">{fn.message}</span>')
    hbox3.pack_start(lblmessage, True, False, 0)

    for box in [hbox0, hbox4, hbox3, hbox15, hbox16, hbox14, hbox13, hbox12, hbox9, hbox10, hbox7, hbox8, hbox11, hbox2]:
        self.vbox.pack_start(box, False, False, 5)
