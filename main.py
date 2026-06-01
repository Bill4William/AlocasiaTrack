from database.connection import initialize_db
from app import AlocasiaTrackApp


def _check_playwright(app: AlocasiaTrackApp):
    """Show install dialog once if Playwright / Chromium is not available."""
    from integrations.config import get as cfg_get, set_value
    if cfg_get("playwright_dont_ask"):
        return
    from dialogs.playwright_install_dialog import playwright_ready
    if playwright_ready():
        return
    from dialogs.playwright_install_dialog import PlaywrightInstallDialog
    dlg = PlaywrightInstallDialog(app)
    app.wait_window(dlg)
    # Suppress future prompts on skip (user chose not to install now)
    # or on success (playwright_ready() will return True next launch anyway,
    # but the flag avoids the import overhead entirely).
    if dlg.suppress_future or dlg.result == "installed":
        set_value("playwright_dont_ask", True)


def _maybe_autostart_web():
    """Start the web server in the background if auto-start is enabled."""
    from integrations.config import get as cfg_get
    if cfg_get("web_autostart"):
        try:
            from web_app.server import start
            port = int(cfg_get("web_port") or 5000)
            start(port)
        except Exception:
            pass


def main():
    initialize_db()
    app = AlocasiaTrackApp()
    # Defer playwright check until after the main window is fully painted
    app.after(800, lambda: _check_playwright(app))
    # Start web server in background if configured
    app.after(1000, _maybe_autostart_web)
    app.mainloop()


if __name__ == "__main__":
    main()
