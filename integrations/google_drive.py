"""
Google Drive integration — folder management and photo uploads.

Folder structure in Drive:
  AlocasiaTrack/
    Stock/
      PLT-0001/
      PUP-0002/
    Plants/
      Big Mama (Dragon Scale)/

Requires drive.file scope (already in google_sheets.py SCOPES).
"""

from __future__ import annotations

import mimetypes
from pathlib import Path

from integrations.config import get as cfg_get, set_value as cfg_set

ROOT_FOLDER_NAME = "AlocasiaTrack"
FOLDER_MIME      = "application/vnd.google-apps.folder"


# ------------------------------------------------------------------ internals

def _svc(credentials_path: str):
    from googleapiclient.discovery import build
    from integrations.google_sheets import get_credentials
    return build("drive", "v3", credentials=get_credentials(credentials_path),
                 cache_discovery=False)


def _find_folder(svc, name: str, parent_id: str | None = None) -> str | None:
    q = f"name='{name}' and mimeType='{FOLDER_MIME}' and trashed=false"
    if parent_id:
        q += f" and '{parent_id}' in parents"
    results = svc.files().list(q=q, fields="files(id)", pageSize=1).execute()
    files = results.get("files", [])
    return files[0]["id"] if files else None


def _create_folder(svc, name: str, parent_id: str | None = None) -> str:
    body = {"name": name, "mimeType": FOLDER_MIME}
    if parent_id:
        body["parents"] = [parent_id]
    f = svc.files().create(body=body, fields="id").execute()
    return f["id"]


# ------------------------------------------------------------------ public API

def get_or_create_folder(credentials_path: str,
                          name: str,
                          parent_id: str | None = None) -> str:
    """Idempotently get or create a Drive folder, returns its ID."""
    svc = _svc(credentials_path)
    fid = _find_folder(svc, name, parent_id)
    if not fid:
        fid = _create_folder(svc, name, parent_id)
    return fid


def get_or_create_root_folder(credentials_path: str) -> str:
    cached = cfg_get("drive_root_folder_id")
    if cached:
        # Verify it still exists
        try:
            svc = _svc(credentials_path)
            svc.files().get(fileId=cached, fields="id").execute()
            return cached
        except Exception:
            pass
    fid = get_or_create_folder(credentials_path, ROOT_FOLDER_NAME)
    cfg_set("drive_root_folder_id", fid)
    return fid


def get_item_folder(credentials_path: str,
                     category: str,
                     item_label: str) -> str:
    """Get/create: AlocasiaTrack / {category} / {item_label}"""
    root     = get_or_create_root_folder(credentials_path)
    cat_fid  = get_or_create_folder(credentials_path, category, root)
    item_fid = get_or_create_folder(credentials_path, item_label, cat_fid)
    return item_fid


def upload_photo(credentials_path: str,
                  folder_id: str,
                  file_path: str) -> dict:
    """Upload a photo to Drive, make it publicly readable.

    Returns {"drive_id": str, "drive_url": str}
    """
    from googleapiclient.http import MediaFileUpload

    svc  = _svc(credentials_path)
    name = Path(file_path).name
    mime = mimetypes.guess_type(file_path)[0] or "image/jpeg"

    media  = MediaFileUpload(file_path, mimetype=mime, resumable=False)
    result = svc.files().create(
        body={"name": name, "parents": [folder_id]},
        media_body=media,
        fields="id, webViewLink",
    ).execute()

    svc.permissions().create(
        fileId=result["id"],
        body={"type": "anyone", "role": "reader"},
    ).execute()

    return {
        "drive_id":  result["id"],
        "drive_url": result.get("webViewLink", ""),
    }


def delete_file(credentials_path: str, file_id: str):
    _svc(credentials_path).files().delete(fileId=file_id).execute()


def folder_url(folder_id: str) -> str:
    return f"https://drive.google.com/drive/folders/{folder_id}"
