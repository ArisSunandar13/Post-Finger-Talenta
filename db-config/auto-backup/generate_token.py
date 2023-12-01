from google_auth_oauthlib.flow import Flow


def main():
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
    print(f'\nPlease go to this URL:\n\n{auth_url}\n')
    code = input('Enter the authorization code : ')

    if not code:
        print('No the authorization code entered\n')
        exit(0)
    else:
        try:
            flow.fetch_token(code=code)
            creds = flow.credentials

            with open(path_file_token, 'w') as token:
                token.write(creds.to_json())
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == '__main__':
    main()
