"""Google Drive API Integration"""

import os
import logging
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.oauth2 import service_account

logger = logging.getLogger(__name__)


class GoogleDriveManager:
    """Manage file operations with Google Drive"""

    SCOPES = ['https://www.googleapis.com/auth/drive']
    VIDEO_MIMETYPES = [
        'video/mp4',
        'video/quicktime',
        'video/x-msvideo',
        'video/x-matroska'
    ]

    def __init__(self):
        creds_path = os.getenv('GOOGLE_DRIVE_CREDENTIALS', 'config/google-credentials.json')

        if not Path(creds_path).exists():
            raise FileNotFoundError(
                f"Google Drive credentials not found at {creds_path}\n"
                "Please download your service account JSON from Google Cloud Console"
            )

        credentials = service_account.Credentials.from_service_account_file(
            creds_path, scopes=self.SCOPES
        )
        self.service = build('drive', 'v3', credentials=credentials)
        logger.info("✅ Google Drive connected")

    def list_videos(self, folder_id: str) -> list:
        """List all video files in a folder"""
        query = f"'{folder_id}' in parents and trashed=false"

        results = self.service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name, mimeType)',
            pageSize=100
        ).execute()

        videos = [
            f for f in results.get('files', [])
            if f['mimeType'] in self.VIDEO_MIMETYPES
        ]

        logger.info(f"Found {len(videos)} videos in folder {folder_id}")
        return videos

    def download_file(self, file_id: str, filename: str, local_path: str = 'data/raw') -> str:
        """Download a file from Google Drive"""
        Path(local_path).mkdir(parents=True, exist_ok=True)
        file_path = Path(local_path) / filename

        logger.info(f"Downloading {filename}...")

        request = self.service.files().get_media(fileId=file_id)

        with open(file_path, 'wb') as f:
            downloader = MediaIoBaseDownload(f, request)
            done = False

            while not done:
                status, done = downloader.next_chunk()
                if status:
                    logger.debug(f"Download {int(status.progress() * 100)}%")

        logger.info(f"✅ Downloaded to {file_path}")
        return str(file_path)

    def upload_file(self, file_path: str, folder_id: str, filename: str = None) -> str:
        """Upload a file to Google Drive"""
        if filename is None:
            filename = Path(file_path).name

        logger.info(f"Uploading {filename}...")

        file_metadata = {
            'name': filename,
            'parents': [folder_id]
        }

        media = MediaFileUpload(file_path, mimetype='video/mp4')
        file = self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, webViewLink'
        ).execute()

        logger.info(f"✅ Uploaded to Google Drive: {file['webViewLink']}")
        return file['id']

    def get_file_info(self, file_id: str) -> dict:
        """Get metadata about a file"""
        file = self.service.files().get(
            fileId=file_id,
            fields='id, name, mimeType, size, createdTime'
        ).execute()
        return file
