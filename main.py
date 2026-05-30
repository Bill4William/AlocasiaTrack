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
    if dlg.suppress_future:
        set_value("playwright_dont_ask", True)


def main():
    initialize_db()
    app = AlocasiaTrackApp()
    # Defer playwright check until after the main window is fully painted
    app.after(800, lambda: _check_playwright(app))
    app.mainloop()


if __name__ == "__main__":
    main()
