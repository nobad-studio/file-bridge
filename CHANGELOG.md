# NOBAD File Bridge changelog

## 0.5.1

* Windows: File Bridge now comes as an installer, `NobadFileBridge-Setup-0.5.1.exe`, in place of the zip. It
  installs for your user without an admin prompt (or for all users), adds a Start menu entry, an optional desktop
  shortcut and an uninstaller, closes a running copy before an upgrade, and tells you if Edge WebView2 is missing.
  Uninstalling asks before deleting your data and vault; the default is to keep them.
* Release: the Windows `.sha256` file has an LF line ending, so `sha256sum -c` accepts it.

## 0.5.0

The first release of NOBAD File Bridge.

* Fixed (Windows): a folder on a server with a file dated just after 1970 couldn't be listed, because the date
  conversion failed. Unknown or out-of-range dates now show as blank.
* Fixed (Windows): cancelling a deployment's local build left the build running. The whole process tree is
  stopped now.
* Fixed: pruning old deployment backups split names on spaces. In a folder like `my site/.rfm-backups` it could
  fail, or remove the wrong file. Names are kept whole now.
* Fixed: a backslash in a playbook value (in a regex, for example) was read as an escape when the script was built.
* Security: importing a vault export no longer accepts Argon2 settings that would take huge memory or time before
  the password is even checked.
* xterm.js 5.5.0 and its fit addon are listed with their versions and MIT licence.
* The classic Qt window is removed. File Bridge's window has every screen it had, and more. Your saved servers,
  sync jobs, deployments, the credential vault and settings are kept, because both windows used the same database.
  `--classic` now says it was removed.
* Smaller Windows app: it no longer bundles Qt, because the window uses Edge WebView2. On Linux, Qt is still used
  for the window when GTK's WebKit isn't installed.
* The new interface is now File Bridge's window: `nobad-file-bridge` (or `python -m app.main`) opens it, and
  `--browser` opens it in your web browser. The previous window is still there with `--classic` for now.
* Packaging: the app now ships the new interface. Before, `pip install` and the packaged app would have left it
  out. The Windows build bundles Edge WebView2's pywebview backend. The Linux build and `.deb` use Qt WebEngine from
  the bundled PySide6.
* Fixed (new interface):
  * Double-clicking a folder in Files opens it.
  * Files can switch to other drives (D:, E:, USB disks, mounted disks on Linux) and common folders. Click the path
    bar or press Ctrl+L to type any path.
  * The terminal's scrollbar can be dragged.
  * Scrollbars are thin and match the theme.
* Linux: the new interface opens with GTK's WebKit2GTK, or with Qt WebEngine from the PySide6 the app already
  installs. If neither is available it says which packages to install.
* New interface: Playbooks.
  * Run ready-made maintenance scripts or your own snippets on the server, with live output and a history.
  * Scripts that use sudo ask once per run, either for the sudo password or to run without one.
  * Playbooks that delete things show the exact script and ask first.
* Security (classic window too): a playbook value could run as a shell command. For example, a domain like
  `example.com; rm -rf ~` would have run the second part. Values are now checked before the script is built.
  Text fields refuse characters that could start a command, and the message says which characters are allowed.
* New interface: Tunnels and Live logs.
  * Tunnels forward a database or internal site on the server to this computer (or the other way round, or as a
    SOCKS proxy). They stay private to this computer unless you choose otherwise, and close when you disconnect.
  * Live logs follow log files and services as they are written, with filters for errors and warnings and a search.
    A log that stops says why, for example a missing file or sudo asking for a password.
* Fixed: after reloading the new interface while it was busy, part of the page sometimes didn't load.
* New interface: Server health and Services.
  * Server health shows CPU, memory, network, disks, the biggest folders and the busiest processes, with a small
    chart for the last minute. It reads the server only while you look at it.
  * Services lists systemd services with failed ones first. You can start, stop, restart and reload them, choose
    whether they start at boot, read their logs, and install a new one.
* Fixed (classic window too): starting, stopping or restarting a service, reloading systemd, installing a unit file
  and stopping a process no longer report success when the command failed. You now see the server's reason. When
  sudo needs a password, it says so at once instead of waiting forever.
* New interface: Deployments.
  * Every deploy starts with a preview, with an optional build on your computer first.
  * Deploying makes a backup, uploads, runs your commands and checks that the site works. If any step fails, the
    site goes back to how it was by itself.
  * A pipeline shows each step as it happens.
  * History keeps every run with its steps and output.
  * Earlier backups and releases can be restored.
  * A lock left behind by a crashed run is only removed if you say so.
* New interface: Sync folders. Every sync starts with a preview of what would be copied, replaced or deleted, and
  nothing changes until you press Sync now. Replacing or deleting files asks first. Two-way jobs remember the
  last sync, so changes and deletions on either side cross over. Files changed on both sides wait for your choice:
  keep yours, keep the server's, keep both or skip, with a side-by-side compare. If files change between the
  preview and the sync, nothing runs and you get a fresh preview.
* New interface: the Credential vault. Secrets stay hidden until you reveal or copy one; revealed values hide again
  after 30 seconds and a copied secret is cleared from the clipboard after 30 seconds. The vault locks itself after
  10 minutes without use (change it in Settings), slows down repeated wrong master passwords, and includes a
  strong password generator. The classic window reads the same vault.
* Security: the code editor no longer loads Monaco from cdnjs or unpkg. It ships with the app, in the classic window
  and in the new interface, so editing works offline and no outside code runs next to the app (#30).
* New interface: an Editor for server and local files. Saving checks that nobody changed the file since you opened
  it; if they did, you can compare both versions side by side, overwrite with yours or take theirs. Unsaved
  changes are marked, kept across screen changes, and survive a disconnect.
* New interface: Terminal tabs for the connected server and for this computer, next to your files. They keep
  running when you switch screens, keep what they showed if the window reloads, and close with the server's
  connection. "Open terminal here" from the Files context menu. Copy and paste with Ctrl+Shift+C / Ctrl+Shift+V.
* New interface (`python -m app.web`): Connections and Files. Save servers, connect with a password, SSH key or
  agent (paste an `ssh` command to fill the form), and check an unknown server's fingerprint before trusting it.
  Files shows this computer and the server side by side, stays quick in folders with thousands of files, and
  works from the keyboard (F5 copy, F2 rename, F7 new folder, Delete). Uploads and downloads show live progress in
  the dock; if something already exists you choose once: keep both, skip or replace.
* Security: a server can no longer make a download write outside the folder you chose. Names such as `../x`,
  `..\x`, `a/b` or `/etc/x` in a listing are hidden (with a warning) and refused by folder downloads (#29).
* Fixed: deleting a folder on an SFTP server no longer follows symlinks inside it, and deleting a symlink to a
  folder removes only the link. Folder downloads no longer follow symlinked folders.
* Security: the data folder (`~/.remote-file-manager`) is now private on Linux and macOS: the folder is 0700 and
  the database, `known_hosts` and diagnostics log are 0600. Existing files are tightened on start, and a data
  folder that is a symlink or belongs to another user is refused (#31).
* If the data folder can't be used, the app no longer falls back to a shared `/tmp` folder. It uses a new private
  temporary folder for that session and says so in the log: saved connections and settings won't be kept.

## 0.4.0

* First version in the NOBAD repository (imported from the standalone Remote File Manager project, renamed to NOBAD File Bridge).
* SSH/SFTP and FTP/FTPS browsing, queued transfers, cross-server relay, baseline-aware two-way sync, remote
  editing, embedded terminals, a master-password encrypted credential vault, and deployments with health checks
  and rollback.
