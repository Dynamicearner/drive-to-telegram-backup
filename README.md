# Google Drive to Telegram channel

A Python script that automatically downloads files from Google Drive (including shared files) and uploads them to a Telegram channel. The scripts handles large files by splitting them into smaller parts to comply with Telegram's upload limits.

## Features

- 📁 Downloads files from Google Drive (My Drive + Shared with Me)
- 📤 Uploads files to Telegram channel
- 🔄 Automatically splits large files (>1.9GB) into smaller parts
- 🔐 Uses Google Service Account for authentication
- 📊 Progress tracking for downloads and uploads

## Prerequisites

- Python 3.7 or higher
- Google Cloud Platform account
- Telegram account with API access
- A Telegram channel where you want to upload files

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Dynamicearner/drive-to-telegram-backup/
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Google Drive Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Drive API:
   - Go to "APIs & Services" > "Library"
   - Search for "Google Drive API"
   - Click "Enable"

4. Create a Service Account:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "Service Account"
   - Fill in the service account details
   - Click "Create and Continue"
   - Skip the optional steps and click "Done"

5. Generate Service Account Key:
   - Click on the created service account
   - Go to "Keys" tab
   - Click "Add Key" > "Create new key"
   - Choose "JSON" format
   - Download the JSON file
   - Rename it to `service_account.json` and place it in the project root

6. Share Google Drive folders with the service account:
   - Open the downloaded JSON file
   - Copy the `client_email` value
   - Share your Google Drive folders with this email address
   - Give "Viewer" permissions

### 4. Telegram Setup

1. Get your Telegram API credentials:
   - Go to [my.telegram.org](https://my.telegram.org/)
   - Log in with your phone number
   - Go to "API development tools"
   - Create a new application
   - Note down your `api_id` and `api_hash`

2. Get your Channel ID:
   - Add your user account to the channel as an admin
   - Forward a message from the channel to [@userinfobot](https://t.me/userinfobot)
   - The channel ID will be shown (it starts with -100)

**Note:** This script uses Telegram MTProto library for user account login, not a bot. You'll need to authenticate with your personal Telegram account.

### 5. Environment Configuration

1. Create your `.env` file (`.env.local` is just an example):

```bash
cp .env.local .env
```

2. Edit `.env` with your actual values:

```env
# Telegram Pyrogram User account Configuration
API_ID=your_api_id_here
API_HASH=your_api_hash_here
CHANNEL_ID=your_channel_id_here

# Google Drive Configuration
SERVICE_ACCOUNT_FILE=service_account.json

# File Upload Settings
MAX_SIZE=1992294400
```

**Important:** The actual environment file should be named `.env`, not `.env.local`. The `.env.local` file is just an example template.


## Usage

1. Make sure your `service_account.json` file is in the project root
2. Update your `.env` file with correct values
3. Run the Script:

```bash
python3 drive_to_telegram.py
```

The script will:
- Scan your Google Drive (My Drive + Shared with Me)
- Download each file
- Upload to your Telegram channel using your user account
- Split large files automatically
- Clean up temporary files

**Note:** On first run, you'll be prompted to authenticate with your Telegram account using your phone number and verification code.

## File Structure

```
googledrivebotbackup/
├── drive_to_telegram.py      # Main script
├── service_account.json      # Google service account credentials (not in git)
├── .env                     # Your actual environment variables (not in git)
├── .env.local               # Example environment file template
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Important Notes

- 📁 The script processes all files in your Google Drive and shared folders
- 🔄 Large files (>1.9GB) are automatically split into parts
- 📱 Make sure your Telegram channel has enough storage space
- 🔐 Keep your API credentials secure
- 👤 This uses your personal Telegram account (not a bot) via MTProto library

## Troubleshooting

### Common Issues

1. **"Service account not found" error:**
   - Make sure `service_account.json` is in the project root
   - Verify the service account has access to your Google Drive

2. **"Channel not found" error:**
   - Check your `CHANNEL_ID` in the `.env` file
   - Make sure your user account is added to the channel as an admin

3. **"API credentials invalid" error:**
   - Verify your `API_ID` and `API_HASH` in the `.env` file
   - Make sure you're using the correct credentials from my.telegram.org

4. **"File too large" error:**
   - The script automatically handles large files by splitting them
   - If you still get this error, check your `MAX_SIZE` setting

5. **"Authentication failed" error:**
   - Make sure you're using your personal Telegram account credentials
   - Check that your phone number and verification code are entered correctly
   - Ensure your account has access to the target channel

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Disclaimer

This script is for personal use only. Make sure you have the right to download and share the files you're processing. The authors are not responsible for any misuse of this software.
