# POST-FINGER-TALENTA

## Set Cron

### - Post Absensi to Talenta

- `00 19,05 * * * bash <<path to this folder>>/run.sh`

### - Auto Backup DB Absensi

- `00 20 * * * bash <<path to auto-backup folder>>/run.sh`

### - Auto Startup DB Absensi when Server is Reboot

- `@reboot bash <<path to restore folder>>/system-reboot.sh`

## Decrypt file.gpg

### - In directory post-finger-talenta

- run "`echo <<secret>> | base64`" to get password
- copy the password
- run "`gpg .env.gpg`" to decrypt file .env

### - In directory auto-backup

- run "`echo <<secret>> | base64`" to get password
- copy the password
- run "`gpg .env.gpg && gpg client_secret_desktop_app.json.gpg`" to decrypt file ".env" and "client_secret_desktop_app.json"

### - In directory restore

- run "`echo <<secret>> | base64`" to get password
- copy the password
- run "`gpg .env.gpg`" to decrypt file .env

## Restore Database

- Download file "`DbAbsensi-<<date>>.sql`" from Google Drive
- Save the file into `restore` directory
- Run "`bash run.sh`"

## Update Token for Auto Backup Database via Telegram

Every week, token authorization needs to be updated, when the token requests to be updated, the program will send the URL to the registered telegram account.

- Open the URL
- Login with account IT TMS (mastersteel2020@gmail.com)
- Check all access
- Copy authorization code
- Send the authorization code to the telegram bot (@sendTokenBackupDBAbsensi_bot)
- Done
