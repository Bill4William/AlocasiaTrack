# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec for AlocasiaTrack  --  works on both Windows and macOS.

Windows (from project root):
    python  -m PyInstaller AlocasiaTrack.spec --clean --noconfirm
    Output: dist/AlocasiaTrack/AlocasiaTrack.exe  (then Inno Setup for installer)

macOS (from project root):
    python3 -m PyInstaller AlocasiaTrack.spec --clean --noconfirm
    Output: dist/AlocasiaTrack.app  (then build_mac.sh wraps it in a .dmg)
"""

import os
import sys
from PyInstaller.utils.hooks import collect_all

# customtkinter ships theme JSON + image files that must travel with the bundle
ctk_datas, ctk_binaries, ctk_hiddenimports = collect_all("customtkinter")

project_root = SPECPATH  # spec lives in the project root

# Platform-specific icon format
if sys.platform == "darwin":
    icon_path = os.path.join(project_root, "icon.icns")
else:
    icon_path = os.path.join(project_root, "icon.ico")

icon = icon_path if os.path.exists(icon_path) else None

a = Analysis(
    [os.path.join(project_root, "main.py")],
    pathex=[project_root],
    binaries=ctk_binaries,
    datas=ctk_datas + [
        (os.path.join(project_root, "docs"), "docs"),
        # Bundle icon so app.py can call iconbitmap() at runtime
        (os.path.join(project_root, "icon.ico"), "."),
        # Playwright worker — called via system Python when running as bundled exe
        (os.path.join(project_root, "scripts", "facebook_worker.py"), "scripts"),
        # Species seed packs — drop a .py file here to add a new genus
        (os.path.join(project_root, "species_seeds"), "species_seeds"),
    ],
    hiddenimports=ctk_hiddenimports + [
        # Google auth / API
        "google.auth.transport.requests",
        "google.auth.transport.urllib3",
        "google.oauth2.credentials",
        "google.oauth2.service_account",
        "googleapiclient.discovery",
        "googleapiclient.http",
        "googleapiclient.errors",
        "google_auth_oauthlib.flow",
        "cachetools",
        "pyasn1",
        "pyasn1_modules",
        "rsa",
        "uritemplate",
        # gspread
        "gspread",
        "gspread.auth",
        # tkinter (sometimes missed on macOS / Windows)
        "tkinter",
        "tkinter.ttk",
        "tkinter.messagebox",
        "tkinter.filedialog",
    ],
    hookspath=[],
    runtime_hooks=[],
    # Playwright is an *optional* integration — it's large (~150 MB of browser
    # binaries) and cannot be bundled.  Users who want Facebook integration
    # must run  `playwright install chromium`  after installing the app.
    #
    # pycparser 3.x removed the legacy lextab/yacctab generated-table files;
    # the PyInstaller contrib hook still tries to find them and emits WARNINGs.
    # Listing them here tells PyInstaller to stop looking.
    excludes=[
        "playwright", "pytest", "setuptools", "pip", "IPython",
        "pycparser.lextab", "pycparser.yacctab",
    ],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="AlocasiaTrack",
    debug=False,
    strip=False,
    upx=True,
    console=False,          # no terminal window
    icon=icon,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="AlocasiaTrack",
)

# macOS only: wrap the collected folder into a proper .app bundle
if sys.platform == "darwin":
    app = BUNDLE(
        coll,
        name="AlocasiaTrack.app",
        icon=icon,
        bundle_identifier="com.alocasiatrack.app",
        info_plist={
            "CFBundleName":               "AlocasiaTrack",
            "CFBundleDisplayName":        "AlocasiaTrack",
            "CFBundleShortVersionString": "1.0.0",
            "CFBundleVersion":            "1.0.0",
            "NSHighResolutionCapable":    True,
            "NSHumanReadableCopyright":   "AlocasiaTrack",
        },
    )
