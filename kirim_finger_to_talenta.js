import CryptoJS from 'crypto-js';
import fs from 'fs'
import { fetch, File } from 'node-fetch'

const date_string = new Date().toUTCString()
const hmac_username = 'XRhT8s2crtd8fSoK';
const hmac_secret = 'xquzB0GDtx5T6TZE0LZhQ7RmE9pgYKFS';

const url = 'https://sandbox-api.mekari.com/v2/talenta/v2/attendance/import-fingerprint'
const token = '33b2446c16faf8fc69aba0e33ea7a30b';
const user_id = 'T001';

const file_csv_name = 'kirim.csv'
const file_csv_path = `${process.cwd()}/${file_csv_name}`

async function fileCsv() {
    try {
        const fileStream = fs.readFileSync(file_csv_path);
        const uint8array = new Uint8Array(fileStream)
        return new File([uint8array], file_csv_name, { type: 'text/csv' });
    } catch (error) {
        console.error('Terjadi kesalahan:', error);
        return null;
    }
}

async function generateHmacSignature() {
    const requestLine = 'POST ' + new URL(url).pathname + ' HTTP/1.1';
    const digest = CryptoJS.HmacSHA256(['date: ' + date_string, requestLine].join('\n'), hmac_secret);
    const signature = CryptoJS.enc.Base64.stringify(digest);

    return 'hmac username=\"' + hmac_username + '\", algorithm=\"hmac-sha256\", headers=\"date request-line\", signature=\"' + signature + '\"'
}

async function importFingerprint() {
    const formData = new FormData();
    formData.append('token', token);
    formData.append('user_id', user_id);
    formData.append('file', await fileCsv(), file_csv_name)

    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Authorization': await generateHmacSignature(),
            'Date': date_string
        },
        body: formData
    });

    console.log(await response.json())
}

importFingerprint()