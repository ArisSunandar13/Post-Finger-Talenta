from google_auth_oauthlib.flow import Flow

import telethon
import asyncio
import os

api_id = os.environ.get("API_ID")
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("BOT_TOKEN")
id_telegram = [
    "@arssnndr",
    "@MuhammadRoni12"
]


def generate():
    path_file_client_secret = 'client_secret_desktop_app.json'
    path_file_token = 'token.json'

    SCOPES = [
        'https://www.googleapis.com/auth/drive.metadata.readonly',
        'https://www.googleapis.com/auth/drive.file'
    ]

    flow = Flow.from_client_secrets_file(
        path_file_client_secret,
        scopes=SCOPES,
        redirect_uri='urn:ietf:wg:oauth:2.0:oob'
    )
    auth_url, _ = flow.authorization_url(prompt='consent')

    client = telethon.TelegramClient(
        "anon",
        api_id,
        api_hash
    ).start(bot_token=bot_token)

    async def start():
        for tele_id in id_telegram:
            await client.send_message(tele_id, f'Token Authorization is Expired.\nPlease go to this URL:\n{auth_url}\n\nThen send me the Authorization Code')

    async def on_message(event):
        if event.sender_id != (await client.get_me()).id:
            code = event.message.text

            if code == "/exit":
                await event.reply("Exited")
                with open("message.txt", "w") as message:
                    message.write("exit")
                await client.disconnect()

            try:
                flow.fetch_token(code=code)
                creds = flow.credentials

                with open(path_file_token, 'w') as token:
                    token.write(creds.to_json())

                await event.reply("Accepted")
                await event.reply("Token has been generated")
                await client.disconnect()
            except Exception as e:
                if "invalid_grant" in str(e):
                    await event.reply(f"Invalid Authorization Code")

    client.add_event_handler(on_message, telethon.events.NewMessage)

    with client:
        client.loop.run_until_complete(start())
        client.run_until_disconnected()
