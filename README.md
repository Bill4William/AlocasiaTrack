# AlocasiaTrack

Plant inventory, sales tracking, and marketplace integrations for Alocasia collectors and small-scale sellers.

## Features

| Feature | Description |
|---|---|
| **Stock** | Add / edit / sell Plants, Pups, and Corms with photos and auto-assigned SKUs |
| **Mother Plants** | Track your personal collection — the source plants you propagate from |
| **Species Library** | 56+ pre-loaded Alocasia cultivars with care levels and price ranges |
| **Sales** | Log sales with buyer info, shipping, and automatic profit calculation |
| **Google Sheets** | Mirror your inventory to a spreadsheet in real time |
| **Google Drive** | Automatically back up all stock photos to the cloud |
| **Gmail** | Email alerts on sales and low-stock events |
| **Facebook Marketplace** | Auto-fill and submit Marketplace listings via browser automation |
| **Shopify** | Publish / update products; auto-unpublish when an item sells |

## Installation

### Windows

Download `AlocasiaTrackSetup.exe` from [Releases](../../releases) and run it.  
No administrator rights required.

### macOS

Download `AlocasiaTrackSetup_v1.0.0.dmg` from [Releases](../../releases).  
Open the DMG, drag **AlocasiaTrack** into your Applications folder, and launch it.

> **macOS note:** On first launch macOS may show "unidentified developer."  
> Right-click the app → **Open** → **Open** to bypass this once.

### Run from Source

Requires **Python 3.11+**.

```bash
git clone https://github.com/Bill4William/AlocasiaTrack.git
cd AlocasiaTrack
pip install -r requirements.txt
python main.py
```

## Building

### Windows installer

```powershell
# From the project root (requires Inno Setup 6 and Python in PATH)
powershell -ExecutionPolicy Bypass -File build.ps1
# Output: dist\installer\AlocasiaTrackSetup.exe
```

### macOS DMG

```bash
# From the project root (requires Python 3.11+ and Xcode Command Line Tools)
bash scripts/build_mac.sh
# Output: installer_output/AlocasiaTrackSetup_v1.0.0.dmg
```

The macOS DMG is also built automatically by GitHub Actions on every push to `main`  
and attached to tagged releases. See `.github/workflows/build-mac.yml`.

## Facebook Marketplace (optional)

Facebook integration requires Playwright and Chromium (~150 MB).  
The app will offer to install them on first launch, or run manually:

```bash
pip install playwright
playwright install chromium
```

## Data Storage

All data is stored locally at `%LOCALAPPDATA%\AlocasiaTrack\` (Windows) or  
`~/Library/Application Support/AlocasiaTrack/` (macOS).  
Nothing is written inside the install directory.

## License

MIT
