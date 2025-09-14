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
   - Add your bot to the channel as an admin
   - Forward a message from the channel to [@userinfobot](https://t.me/userinfobot)
   - The channel ID will be shown (it starts with -100)

### 5. Environment Configuration

1. Copy the `.env` file and update the values:

```bash
cp .env .env.local
```

2. Edit `.env.local` with your actual values:

```env
# Telegram Bot Configuration
API_ID=your_api_id_here
API_HASH=your_api_hash_here
CHANNEL_ID=your_channel_id_here

# Google Drive Configuration
SERVICE_ACCOUNT_FILE=service_account.json

# File Upload Settings
MAX_SIZE=1992294400
```


## Usage

1. Make sure your `service_account.json` file is in the project root
2. Update your `.env.local` file with correct values
3. Run the bot:

```bash
python drive_to_telegram.py
```

The bot will:
- Scan your Google Drive (My Drive + Shared with Me)
- Download each file
- Upload to your Telegram channel
- Split large files automatically
- Clean up temporary files

## File Structure

```
googledrivebotbackup/
├── drive_to_telegram.py      # Main bot script
├── service_account.json      # Google service account credentials (not in git)
├── .env                      # Environment variables template
├── .env.local               # Your actual environment variables (not in git)
├── .gitignore               # Git ignore file
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Important Notes

- ⚠️ **Never commit your `service_account.json` or `.env.local` files to git**
- 📁 The bot processes all files in your Google Drive and shared folders
- 🔄 Large files (>1.9GB) are automatically split into parts
- 📱 Make sure your Telegram channel has enough storage space
- 🔐 Keep your API credentials secure

## Troubleshooting

### Common Issues

1. **"Service account not found" error:**
   - Make sure `service_account.json` is in the project root
   - Verify the service account has access to your Google Drive

2. **"Channel not found" error:**
   - Check your `CHANNEL_ID` in the `.env.local` file
   - Make sure the bot is added to the channel as an admin

3. **"API credentials invalid" error:**
   - Verify your `API_ID` and `API_HASH` in the `.env.local` file
   - Make sure you're using the correct credentials from my.telegram.org

4. **"File too large" error:**
   - The bot automatically handles large files by splitting them
   - If you still get this error, check your `MAX_SIZE` setting

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Disclaimer

This bot is for personal use only. Make sure you have the right to download and share the files you're processing. The authors are not responsible for any misuse of this software.



