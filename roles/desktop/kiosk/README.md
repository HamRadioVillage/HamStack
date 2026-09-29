# `desktop/kiosk`

Generic Chromium kiosk role for HamStack display stations.

It installs Chromium and small X11 helpers, disables display blanking for the
session, optionally rotates a named display, hides the mouse cursor, and creates
an XDG autostart launcher for a configurable URL.

The role does **not** configure desktop-manager autologin. Login policy varies
between distributions/desktops and can be layered on later if a deployment
actually needs unattended login.

The kiosk is intentionally application-neutral: Gatus, CONHAM, DCDash, FT8Web,
exam software, or future presentation applications can all use the same role.
