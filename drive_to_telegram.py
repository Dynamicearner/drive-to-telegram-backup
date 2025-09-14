import os
import io
from dotenv import load_dotenv
from pyrogram import Client
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account


load_dotenv()

API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
CHANNEL_ID = os.getenv('CHANNEL_ID')
SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE', 'service_account.json')
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']


MAX_SIZE = int(os.getenv('MAX_SIZE', 1900 * 1024 * 1024))  


def google_drive_auth():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    drive_service = build("drive", "v3", credentials=creds)
    return drive_service


def list_all_files(service, folder_id, level=0):
    query = f"'{folder_id}' in parents and trashed=false"
    results = service.files().list(
        q=query,
        fields="files(id, name, mimeType)"
    ).execute()
    items = results.get("files", [])
    files = []

    for item in items:
        prefix = "  " * level
        if item["mimeType"] == "application/vnd.google-apps.folder":
            print(f"{prefix}📂 {item['name']} ({item['id']})")
            files.extend(list_all_files(service, item["id"], level + 1))
        else:
            print(f"{prefix}📄 {item['name']} ({item['id']})")
            files.append(item)
    return files

def list_shared_files(service):
    results = service.files().list(
        q="sharedWithMe and trashed=false",
        fields="files(id, name, mimeType, owners)"
    ).execute()
    items = results.get("files", [])
    for item in items:
        owner = item.get("owners", [{}])[0].get("emailAddress", "Unknown")
        if item["mimeType"] == "application/vnd.google-apps.folder":
            print(f"📂 [Shared] {item['name']} ({item['id']}) - Owner: {owner}")
        else:
            print(f"📄 [Shared] {item['name']} ({item['id']}) - Owner: {owner}")
    return items


def download_file(service, file_id, file_name):
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(file_name, "wb")
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        if status:
            print(f"⬇️ Downloading {file_name} {int(status.progress() * 100)}%")
    fh.close()
    return file_name

def split_file(path):
    parts = []
    part_num = 1
    with open(path, "rb") as f:
        while True:
            chunk = f.read(MAX_SIZE)
            if not chunk:
                break
            part_name = f"{path}.part{part_num}"
            with open(part_name, "wb") as p:
                p.write(chunk)
            parts.append(part_name)
            part_num += 1
    return parts


def main():
    drive_service = google_drive_auth()

    app = Client("my_account", api_id=API_ID, api_hash=API_HASH)
    with app:
        print("🔍 Scanning Google Drive (My Drive + Shared With Me)...\n")

        
        print("=== 🗂 My Drive ===")
        my_drive_files = list_all_files(drive_service, "root")

        
        print("\n=== 🤝 Shared With Me ===")
        shared_files = list_shared_files(drive_service)

        
        all_files = []
        all_files.extend(my_drive_files)
        for f in shared_files:
            if f["mimeType"] == "application/vnd.google-apps.folder":
                all_files.extend(list_all_files(drive_service, f["id"]))
            else:
                all_files.append(f)

        print(f"\n📦 Total files to process: {len(all_files)}\n")

                        
        for f in all_files:
            try:
                print("➡️ Processing:", f["name"])
                local_path = download_file(drive_service, f["id"], f["name"])

                size = os.path.getsize(local_path)
                if size > MAX_SIZE:
                    print(f"⚠️ File too big ({size/1024/1024:.2f} MB), splitting...")
                    parts = split_file(local_path)
                    for i, part in enumerate(parts, start=1):
                        app.send_document(
                            CHANNEL_ID, 
                            part, 
                            caption=f"{f['name']} (part {i})"
                        )
                        os.remove(part)
                else:
                    app.send_document(CHANNEL_ID, local_path, caption=f["name"])
                
                os.remove(local_path)

            except Exception as e:
                print("❌ Error with", f["name"], e)

if __name__ == "__main__":
    main()
