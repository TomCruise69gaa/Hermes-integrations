from pathlib import Path
from datetime import datetime, timezone

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

BASE_DIR = Path(__file__).resolve().parent.parent
CREDENTIALS_DIR = BASE_DIR / "credentials"

CLIENT_FILE = CREDENTIALS_DIR / "client_secret.json"
TOKEN_FILE = CREDENTIALS_DIR / "token.json"

SCOPES = ["https://www.googleapis.com/auth/drive.file"]


def authenticate():
    credentials = None

    if TOKEN_FILE.exists():
        credentials = Credentials.from_authorized_user_file(
            str(TOKEN_FILE), SCOPES
        )

    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())

    if not credentials or not credentials.valid:
        if not CLIENT_FILE.exists():
            raise FileNotFoundError(
                f"Google OAuth credential not found: {CLIENT_FILE}"
            )

        flow = InstalledAppFlow.from_client_secrets_file(
            str(CLIENT_FILE), SCOPES
        )

        credentials = flow.run_local_server(
            port=0,
            access_type="offline",
            prompt="consent"
        )

        TOKEN_FILE.write_text(credentials.to_json(), encoding="utf-8")

    return credentials


def get_or_create_folder(drive):
    folder_name = "JARVIS_TEST"

    results = drive.files().list(
        q=(
            "name = 'JARVIS_TEST' "
            "and mimeType = 'application/vnd.google-apps.folder' "
            "and trashed = false"
        ),
        spaces="drive",
        fields="files(id, name)",
        pageSize=10
    ).execute()

    folders = results.get("files", [])

    if folders:
        print("Using existing JARVIS_TEST folder.")
        return folders[0]["id"]

    folder = drive.files().create(
        body={
            "name": folder_name,
            "mimeType": "application/vnd.google-apps.folder"
        },
        fields="id, name"
    ).execute()

    print("Created JARVIS_TEST folder.")
    return folder["id"]


def create_test_document(drive, docs, folder_id):
    document = drive.files().create(
        body={
            "name": "JARVIS_Integration_Test_001",
            "mimeType": "application/vnd.google-apps.document",
            "parents": [folder_id]
        },
        fields="id, name, webViewLink"
    ).execute()

    document_id = document["id"]

    text = (
        "JARVIS GOOGLE DRIVE INTEGRATION TEST 001\n\n"
        "Status: Successful\n"
        "Created by: Hermes Local Integration Service\n"
        f"Created at (UTC): {datetime.now(timezone.utc).isoformat()}\n\n"
        "This document confirms that the local integration service "
        "successfully authenticated with Google and created a document."
    )

    docs.documents().batchUpdate(
        documentId=document_id,
        body={
            "requests": [
                {
                    "insertText": {
                        "location": {"index": 1},
                        "text": text
                    }
                }
            ]
        }
    ).execute()

    return document


def main():
    print("Starting Hermes Google Drive integration...")

    credentials = authenticate()

    drive = build("drive", "v3", credentials=credentials,
                  cache_discovery=False)

    docs = build("docs", "v1", credentials=credentials,
                 cache_discovery=False)

    folder_id = get_or_create_folder(drive)

    document = create_test_document(drive, docs, folder_id)

    print("\nGOOGLE DRIVE TEST SUCCESSFUL")
    print(f"Document: {document['name']}")
    print(f"Document ID: {document['id']}")
    print(f"Link: {document.get('webViewLink', 'Link unavailable')}")


if __name__ == "__main__":
    main()
