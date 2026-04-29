# 4ndr0trasher
### Absolute Desktop Deconstruction & Environmental Purge Matrix
**Author:** Ψ-4ndr0666os (Refactored from ArcoLinux Desktop Trasher)

---

## I. ARCHITECTURAL MANIFESTO
**4ndr0trasher** is a high-stakes, system-level orchestrator designed for the ruthless reclamation of architectural purity. It enables the surgical removal of entire desktop environments from an active Linux installation. Moving beyond simple package uninstallation, **4ndr0trasher** manages the volatile intersection of root-level system mutation and user-space configuration persistence.

## II. THE GUI BRIDGE & ELEVATION STRATEGY
Built for the Wayland era, **4ndr0trasher** employs a hardened elevation bridge to solve the "Display Socket Isolation" problem inherent in root-level GUI applications.

### 1. Environment Preservation
The wrapper (`/usr/local/bin/4ndr0trasher`) executes a `sudo` elevation that explicitly preserves the Wayland and X11 communication channels. By passing `DISPLAY`, `WAYLAND_DISPLAY`, and `XDG_RUNTIME_DIR`, the root payload can communicate with the user's display server natively.

### 2. Polkit Session Resolution
To support `greetd` and Wayland seat topologies where Polkit often misclassifies sessions as "inactive," the included policy utilizes `auth_self`. This ensures the invoking user proves their identity with their own credentials, bypassing seat-string bottlenecks that lead to "Not authorized" failures.

## III. FILE SYSTEM HIERARCHY
The project follows a strict FHS-compliant deployment matrix:

```text
.
├── etc
│   └── sudoers.d
│       └── 4ndr0trasher                     # NOPASSWD elevation rule
├── install.sh                               # Atomic deployment orchestrator
└── usr
    ├── local
    │   └── bin
    │       └── 4ndr0trasher                 # Bash GUI Bridge (Entry point)
    └── share
        ├── applications
        │   └── 4ndr0trasher.desktop         # XDG Menu Entry
        ├── 4ndr0trasher
        │   ├── 4ndr0trasher.py             # Main Orchestrator (Python)
        │   ├── Functions.py                 # Core Logic & Operations
        │   ├── GUI.py                       # GTK3 Interface Definition
        │   └── images                       # Asset Matrix
        │       ├── 4ndr0trasher-logo.png
        │       ├── 4ndr0666os-icon.png
        │       └── panel.png
        ├── icons
        │   └── hicolor
        │       └── scalable
        │           └── apps
        │               └── 4ndr0trasher.svg # Scalable Branding
        └── polkit-1
            └── actions
                └── org.4ndr0666os.pkexec.4ndr0trasher.policy
```

## IV. FUNCTIONAL RECOVERY & SAFETY
The "Trasher" logic is built on the principle of **Atomic Reversion**.

### 1. 5-Tier User Detection
The application accurately identifies the human operator even under root elevation by scanning:
1. `PKEXEC_UID` (Polkit)
2. `SUDO_USER` (Sudo)
3. `os.getlogin()` (TTY)
4. `logname` (POSIX)
5. `HOME` path derivation

### 2. Surgical Backup Matrix
Before any purge, **4ndr0trasher** captures the environment state in `~/.config-4ndr0trasher/`.
* **Full Mode**: Absolute backup of `.config` and `.local`.
* **Surgical Mode**: Leverages an `OMIT_LIST` to exclude massive transient caches (Brave, Chrome, Discord, Mozilla), preventing disk exhaustion and backup hangs.

### 3. Two-Pass Purge Logic
Uninstallations are performed via a two-stage strategy:
* **Stage 1 (`pacman -Rs`)**: Respects the standard dependency graph for clean removal.
* **Stage 2 (`pacman -Rdd`)**: Force-removes critical leaf nodes (like GNOME/Budgie core components) that otherwise block removal via circular dependency loops.

## V. INSTALLATION
Deploy the matrix via the enhanced `install.sh`. The installer performs atomic synchronization, verifies Python GTK3 dependencies, and validates the `sudoers` rule via `visudo` before persistence.

```bash
sudo ./install.sh
```

## VI. USER INTERFACE (GUI.PY)
The interface is a hardened GTK3 container:
* **Option 1 (Matrix Discovery)**: Parses `/usr/share/xsessions` and `/usr/share/wayland-sessions` to show currently installed environments.
* **Option 2 (Global Purge)**: A master list for removing residual packages from environments no longer detected by the display manager.
* **Protection Switch**: Prevents the deletion of `~/.config` content if the user only intends to purge binary packages.

## VII. LOGGING & AUDIT
Every operation is preceded and followed by a system package snapshot. Logs are stored with microsecond precision in:
`/var/log/4ndr0trasher/logs/`

## VIII. DISCLAIMER
**4ndr0trasher IS DESTRUCTIVE.** It is designed to wipe system configurations and uninstall critical desktop components.
* **Always** keep the Backup Switch enabled.
* Backups are stored in `~/.config-4ndr0trasher`.
* The author assumes no liability for corrupted user sessions.

⊰💀•-⦑4NDR0666OS⦒-•💀⊱
