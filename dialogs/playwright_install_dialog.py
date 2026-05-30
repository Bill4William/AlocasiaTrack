"""
Playwright install dialog — shown on first launch when Chromium is missing.
Offers to install playwright (pip) and download Chromium automatically.
"""
from __future__ import annotations

import glob
import os
import subprocess
import sys
import threading

import customtkinter as ctk


# ── Python executable resolution ─────────────────────────────────────────────

def _find_python() -> str:
    """Return a usable python.exe path for pip / playwright commands.

    When the app is bundled by PyInstaller, sys.executable is the app .exe
    itself — running it with '-m pip' would just relaunch AlocasiaTrack.
    In that case we search PATH for a real Python interpreter instead.
    """
    import shutil

    if not hasattr(sys, "_MEIPASS"):
        # Running from source — sys.executable is already python.exe
        return sys.executable

    # Bundled: look for any Python in PATH
    for name in ("python", "python3", "py"):
        found = shutil.which(name)
        if found and "AlocasiaTrack" not in found:
            return found

    raise RuntimeError(
        "Python was not found in PATH.\n\n"
        "To enable Facebook Marketplace, open a Command Prompt and run:\n\n"
        "    pip install playwright\n"
        "    playwright install chromium"
    )


# ── detection ────────────────────────────────────────────────────────────────

def playwright_ready() -> bool:
    """Return True only when both the package and Chromium binary are present."""
    try:
        import playwright  # noqa: F401
    except Exception:
        return False

    # Try playwright's own API first — most reliable, version-independent
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            exe = pw.chromium.executable_path
            if os.path.exists(exe):
                return True
    except Exception:
        pass

    # Fallback: glob known install paths
    # Directory name varies by version: chrome-win (older) or chrome-win64 (newer)
    local_app = os.environ.get("LOCALAPPDATA", "")
    home = os.path.expanduser("~")
    patterns = [
        os.path.join(local_app, "ms-playwright", "chromium-*", "chrome-win64", "chrome.exe"),
        os.path.join(local_app, "ms-playwright", "chromium-*", "chrome-win",   "chrome.exe"),
        # macOS
        os.path.join(home, "Library", "Caches", "ms-playwright", "chromium-*",
                     "chrome-mac", "Chromium.app", "Contents", "MacOS", "Chromium"),
    ]
    for pattern in patterns:
        if glob.glob(pattern):
            return True
    return False


# ── dialog ───────────────────────────────────────────────────────────────────

class PlaywrightInstallDialog(ctk.CTkToplevel):
    """
    Modal dialog that explains what Playwright is, offers to install it,
    and reports progress.  After closing, check .suppress_future to know
    whether to set the 'playwright_dont_ask' config flag.
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.result: str | None = None   # 'installed' | 'skipped' | 'failed'
        self._suppress = False

        self.title("Facebook Marketplace — Optional Setup")
        self.geometry("500x400")
        self.resizable(False, False)
        self.grab_set()
        self._build()
        self.after(100, self.lift)

    # ── UI ───────────────────────────────────────────────────────────────────

    def _build(self):
        ctk.CTkLabel(
            self,
            text="Facebook Marketplace Integration",
            font=ctk.CTkFont(size=17, weight="bold"),
            anchor="w",
        ).pack(fill="x", padx=24, pady=(22, 6))

        body = (
            "AlocasiaTrack can post listings to Facebook Marketplace automatically "
            "using a browser tool called Playwright.\n\n"
            "Playwright is not currently installed.  "
            "Would you like to install it now?\n\n"
            "•  Requires an internet connection  (~200 MB download)\n"
            "•  Only needed for the Facebook Marketplace feature\n"
            "•  All other features work without it"
        )
        ctk.CTkLabel(
            self, text=body,
            anchor="nw", justify="left", wraplength=452,
        ).pack(fill="x", padx=24, pady=(0, 14))

        self._status_lbl = ctk.CTkLabel(
            self, text="", anchor="w",
            text_color=("gray50", "gray60"),
        )
        self._status_lbl.pack(fill="x", padx=24)

        self._bar = ctk.CTkProgressBar(self)
        self._bar.set(0)
        # hidden until install starts
        self._bar_visible = False

        ctk.CTkLabel(
            self,
            text="You can install it later from Settings → Facebook.",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray55"),
            anchor="w",
        ).pack(fill="x", padx=24, pady=(10, 4))

        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack(fill="x", padx=24, pady=(0, 20))

        self._skip_btn = ctk.CTkButton(
            btn_row, text="Skip for now", width=120,
            fg_color="gray40", hover_color="gray30",
            command=self._skip,
        )
        self._skip_btn.pack(side="right", padx=(8, 0))

        self._install_btn = ctk.CTkButton(
            btn_row, text="Install Playwright", width=160,
            command=self._start_install,
        )
        self._install_btn.pack(side="right")

    # ── actions ──────────────────────────────────────────────────────────────

    def _skip(self):
        # Always suppress future prompts when the user skips —
        # they can install from Settings → Facebook whenever ready.
        self._suppress = True
        self.result = "skipped"
        self.destroy()

    def _start_install(self):
        self._install_btn.configure(state="disabled", text="Installing…")
        self._skip_btn.configure(state="disabled")
        # Show progress bar
        self._bar.pack(fill="x", padx=24, pady=(4, 0))
        self._bar_visible = True
        self._bar.configure(mode="indeterminate")
        self._bar.start()
        threading.Thread(target=self._run_install, daemon=True).start()

    def _run_install(self):
        try:
            python = _find_python()
        except RuntimeError as exc:
            self.after(0, lambda e=str(exc): self._on_error(e))
            return

        steps = [
            ("Installing playwright package…",
             [python, "-m", "pip", "install", "--quiet", "playwright"]),
            ("Downloading Chromium browser (this may take a minute)…",
             [python, "-m", "playwright", "install", "chromium"]),
        ]
        try:
            for msg, cmd in steps:
                self.after(0, lambda m=msg: self._status_lbl.configure(text=m))
                proc = subprocess.run(cmd, capture_output=True, text=True)
                if proc.returncode != 0:
                    raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "Unknown error")
            self.after(0, self._on_success)
        except Exception as exc:
            self.after(0, lambda e=str(exc): self._on_error(e))

    def _on_success(self):
        self._bar.stop()
        self._bar.configure(mode="determinate")
        self._bar.set(1)
        self._status_lbl.configure(
            text="Playwright installed successfully!",
            text_color=("green", "#66bb6a"),
        )
        self._install_btn.configure(state="normal", text="Done", command=self.destroy)
        self._skip_btn.configure(state="normal", text="Close", command=self.destroy)
        self.result = "installed"

    def _on_error(self, msg: str):
        self._bar.stop()
        self._bar.pack_forget()
        self._bar_visible = False
        self._status_lbl.configure(
            text=f"Installation failed: {msg[:140]}",
            text_color=("red", "#ef5350"),
        )
        self._install_btn.configure(state="normal", text="Retry", command=self._start_install)
        self._skip_btn.configure(state="normal")
        self.result = "failed"

    # ── public ───────────────────────────────────────────────────────────────

    @property
    def suppress_future(self) -> bool:
        """True if the user ticked 'Don't ask me again'."""
        return self._suppress
