import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf

def load_image_safe(path, w, h):
    """EAFP Image loading to prevent system-level crashes on missing assets."""
    try:
        pb = GdkPixbuf.Pixbuf.new_from_file_at_size(path, w, h)
        return Gtk.Image.new_from_pixbuf(pb)
    except:
        return Gtk.Image()

def GUI(self, Gtk, GdkPixbuf, fn):
    # Main Container
    self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    self.vbox.get_style_context().add_class("main-container")
    self.add(self.vbox)

    # 1. ──────────────── STATUS NOTIFICATION HUD ────────────────
    self.notification_revealer = Gtk.Revealer()
    self.notification_label = Gtk.Label()
    panel = load_image_safe(fn.os.path.join(fn.base_dir, 'images/panel.png'), 700, 40)
    overlay = Gtk.Overlay()
    overlay.add(panel)
    overlay.add_overlay(self.notification_label)
    self.notification_revealer.add(overlay)
    self.vbox.pack_start(self.notification_revealer, False, False, 0)

    # 2. ──────────────── LOGO & WARNING MATRIX ────────────────
    logo_hbox = Gtk.Box(spacing=20)
    logo_path = fn.os.path.join(fn.base_dir, 'images/4ndr0trasher-logo.png')
    logo_hbox.pack_start(load_image_safe(logo_path, 180, 180), False, False, 10)

    lblmessage = Gtk.Label()
    lblmessage.set_markup(f'<span foreground="#ff0055" font_desc="JetBrains Mono Bold 14">{fn.message}</span>')
    lblmessage.set_line_wrap(True)
    lblmessage.set_max_width_chars(40)
    logo_hbox.pack_start(lblmessage, True, True, 0)
    self.vbox.pack_start(logo_hbox, False, False, 5)

    # 3. ──────────────── CONFIGURATION GLASS PANEL ────────────────
    config_panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
    config_panel.get_style_context().add_class("glass-panel")
    config_panel.set_margin_start(10)
    config_panel.set_margin_end(10)

    def create_toggle_row(label_text, active_state=True):
        row = Gtk.Box(spacing=10)
        row.set_margin_start(10)
        row.set_margin_end(10)
        lbl = Gtk.Label(label=label_text)
        lbl.set_xalign(0)
        row.pack_start(lbl, True, True, 0)
        sw = Gtk.Switch()
        sw.set_active(active_state)
        row.pack_end(sw, False, False, 0)
        return row, sw

    # Backup Toggle
    row_bk, self.backup_switch = create_toggle_row("SYSTEM SNAPSHOT / BACKUP")
    config_panel.pack_start(row_bk, False, False, 5)

    # Surgical Toggle (Connected to Backup)
    row_sg, self.surgical_switch = create_toggle_row("SURGICAL MODE (OMIT HEAVY CACHE)")
    self.backup_switch.connect("notify::active", lambda s, p: self.surgical_switch.set_sensitive(s.get_active()))
    config_panel.pack_start(row_sg, False, False, 5)

    # Config Protection
    row_pt, self.donottouch = create_toggle_row("PROTECT CURRENT ~/.CONFIG")
    config_panel.pack_start(row_pt, False, False, 5)

    self.vbox.pack_start(config_panel, False, False, 10)

    # 4. ──────────────── PURGE INTERFACE ────────────────
    action_matrix = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    action_matrix.set_margin_start(10)
    action_matrix.set_margin_end(10)

    # Option 1: Detected Sessions
    row_inst = Gtk.Box(spacing=10)
    row_inst.pack_start(Gtk.Label(label="PURGE DETECTED MATRIX:"), False, False, 0)
    self.installed_sessions = Gtk.ComboBoxText()
    fn.pop_box(self, self.installed_sessions)
    self.installed_sessions.set_active(0)
    row_inst.pack_start(self.installed_sessions, True, True, 0)
    
    btn_inst = Gtk.Button(label="EXECUTE")
    btn_inst.get_style_context().add_class("destructive")
    btn_inst.connect('clicked', self.on_remove_clicked_installed)
    row_inst.pack_end(btn_inst, False, False, 0)
    action_matrix.pack_start(row_inst, False, False, 0)

    # Option 2: Global Registry
    row_glob = Gtk.Box(spacing=10)
    row_glob.pack_start(Gtk.Label(label="PURGE GLOBAL REGISTRY:"), False, False, 0)
    self.desktopr = Gtk.ComboBoxText()
    fn.pop_box_all(self, self.desktopr)
    self.desktopr.set_active(0)
    row_glob.pack_start(self.desktopr, True, True, 0)
    
    btn_glob = Gtk.Button(label="EXECUTE")
    btn_glob.get_style_context().add_class("destructive")
    btn_glob.connect('clicked', self.on_remove_clicked)
    row_glob.pack_end(btn_glob, False, False, 0)
    action_matrix.pack_start(row_glob, False, False, 0)

    self.vbox.pack_start(action_matrix, False, False, 10)

    # 5. ──────────────── FOOTER CONTROLS ────────────────
    footer = Gtk.Box(spacing=10)
    footer.set_margin_top(10)
    
    btn_refresh = Gtk.Button(label="REFRESH MATRIX")
    btn_refresh.connect('clicked', self.on_refresh_clicked)
    
    btn_reboot = Gtk.Button(label="SYSTEM REBOOT")
    btn_reboot.connect('clicked', self.on_reboot_clicked)
    
    btn_close = Gtk.Button(label="EXIT HUD")
    btn_close.connect('clicked', self.on_close_clicked)
    
    footer.pack_start(btn_refresh, True, True, 0)
    footer.pack_start(btn_reboot, True, True, 0)
    footer.pack_start(btn_close, True, True, 0)
    
    self.vbox.pack_end(footer, False, False, 10)
