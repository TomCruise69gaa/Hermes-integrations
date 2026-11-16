from pathlib import Path
import logging

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from mcp.server.mcpserver import MCPServer


# --------------------------------------------------
# FRIDAY GOOGLE DRIVE INTEGRATION
# --------------------------------------------------

SERVER = MCPServer("friday-google-drive")

BASE_DIR = Path(__file__).resolve().parent.parent
CREDENTIALS_DIR = BASE_DIR / "credentials"

TOKEN_FILE = CREDENTIALS_DIR / "token.json"
CLIENT_FILE = CREDENTIALS_DIR / "client_secret.json"

SCOPES = ["https://www.googleapis.com/auth/drive.file"]

TEST_FOLDER_NAME = "FRIDAY_TEST"

logging.basicConfig(level=logging.INFO)


def get_google_services():
    """Load the existing Google OAuth token and connect to Drive and Docs."""

    if not TOKEN_FILE.exists():
        raise RuntimeError("Google OAuth token was not found.")

    if not CLIENT_FILE.exists():
        raise RuntimeError("Google OAuth client file was not found.")

    credentials = Credentials.from_authorized_user_file(
        str(TOKEN_FILE),
        SCOPES
    )

    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
        TOKEN_FILE.write_text(credentials.to_json(), encoding="utf-8")

    if not credentials.valid:
        raise RuntimeError(
            "Google authorization is invalid. Re-run the existing OAuth setup."
        )

    drive = build(
        "drive",
        "v3",
        credentials=credentials,
        cache_discovery=False
    )

    docs = build(
        "docs",
        "v1",
        credentials=credentials,
        cache_discovery=False
    )

    return drive, docs


def get_or_create_test_folder(drive):
    """Find or create FRIDAY's dedicated Google Drive test folder."""

    query = (
        f"name = '{TEST_FOLDER_NAME}' "
        "and mimeType = 'application/vnd.google-apps.folder' "
        "and trashed = false"
    )

    results = drive.files().list(
        q=query,
        spaces="drive",
        fields="files(id, name)",
        pageSize=10
    ).execute()

    folders = results.get("files", [])

    if folders:
        return folders[0]["id"]

    folder = drive.files().create(
        body={
            "name": TEST_FOLDER_NAME,
            "mimeType": "application/vnd.google-apps.folder"
        },
        fields="id, name"
    ).execute()

    return folder["id"]


@SERVER.tool()
def create_google_doc(title: str, content: str) -> str:
    """
    Create a Google Docs document in FRIDAY's dedicated test folder.

    Args:
        title: Document title, maximum 150 characters.
        content: Text to insert, maximum 20000 characters.
    """

    title = title.strip()

    if not title:
        return "Error: Document title cannot be empty."

    if len(title) > 150:
        return "Error: Document title cannot exceed 150 characters."

    if not content.strip():
        return "Error: Document content cannot be empty."

    if len(content) > 20000:
        return "Error: Document content cannot exceed 20000 characters."

    try:
        drive, docs = get_google_services()

        folder_id = get_or_create_test_folder(drive)

        document = drive.files().create(
            body={
                "name": title,
                "mimeType": "application/vnd.google-apps.document",
                "parents": [folder_id]
            },
            fields="id, name, webViewLink"
        ).execute()

        document_id = document["id"]

        docs.documents().batchUpdate(
            documentId=document_id,
            body={
                "requests": [
                    {
                        "insertText": {
                            "location": {"index": 1},
                            "text": content
                        }
                    }
                ]
            }
        ).execute()

        link = document.get(
            "webViewLink",
            f"https://docs.google.com/document/d/{document_id}/edit"
        )

        return (
            "FRIDAY Google Drive document created successfully.\n"
            f"Title: {document['name']}\n"
            f"Document ID: {document_id}\n"
            f"Link: {link}"
        )

    except Exception:
        logging.exception("FRIDAY Google Drive document creation failed.")
        return (
            "Google Drive document creation failed. "
            "Check the integration logs for details."
        )


if __name__ == "__main__":
    SERVER.run()
