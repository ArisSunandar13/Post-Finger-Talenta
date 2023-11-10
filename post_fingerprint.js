import CryptoJS from "crypto-js"; // Perlu install
import { File } from "node-fetch"; // Perlu install
import fetch from "node-fetch";
import { exec } from "child_process";
import fs from "fs";
import strftime from "strftime"

const datetime_now = strftime('%d%m%Y %H:%M:%S', new Date());
const date_string = new Date().toUTCString();

// ENV Production
const hmac_username = process.env.HMAC_USERNAME_PROD;
const hmac_secret = process.env.HMAC_SECRET_PROD;
const url = process.env.URL_PROD;
const token = process.env.TOKEN_PROD;

// ENV Development
// const hmac_username = process.env.HMAC_USERNAME_DEV;
// const hmac_secret = process.env.HMAC_SECRET_DEV;
// const url = process.env.URL_DEV;
// const token = process.env.TOKEN_DEV;

function writeLog(status, message) {
    fs.appendFile(
        `${process.argv[1].slice(0, -2)}log`,
        `[${datetime_now}] ${status}: ${message} \n`,
        () => { }
    );
}

async function dbToCsv() {
    const child = new Promise((res) => {
        exec(`python3 ${process.cwd()}/db_to_csv.py`, (error, stdout) => {
            if (error) writeLog("Error dbToCsv", error.message);
            else res(stdout);
        });
    });

    return await child;
}

async function generateHmacSignature() {
    const hmac = new Promise((res) => {
        const requestLine = "POST " + new URL(url).pathname + " HTTP/1.1";
        const digest = CryptoJS.HmacSHA256(
            ["date: " + date_string, requestLine].join("\n"),
            hmac_secret
        );
        const signature = CryptoJS.enc.Base64.stringify(digest);

        res(
            'hmac username="' +
            hmac_username +
            '", algorithm="hmac-sha256", headers="date request-line", signature="' +
            signature +
            '"'
        );
    });

    return await hmac;
}

async function updateStatus() {
    const child = new Promise((res) => {
        exec(`python3 ${process.cwd()}/update_status.py`, (error, stdout) => {
            if (error) writeLog("Error updateStatus", error.message);
            res(stdout);
        });
    });

    return await child;
}

async function importFingerprint() {
    try {
        await dbToCsv();

        const file_csv_name = "absensi_formatted.csv";
        const formData = new FormData();

        formData.append("token", token);
        formData.append(
            "file",
            new File(
                [
                    new Uint8Array(
                        fs.readFileSync(`${process.cwd()}/data_csv/${file_csv_name}`)
                    ),
                ],
                file_csv_name,
                { type: "text/csv" }
            ),
            file_csv_name
        );

        await fetch(url, {
            method: "POST",
            headers: {
                Authorization: await generateHmacSignature(),
                Date: date_string,
            },
            body: formData,
        }).then(async (res) => {
            const result = await res.json();

            await updateStatus();

            writeLog('Success post', JSON.stringify(result));
        }).catch((err) => {
            writeLog("Error post", err.message);
        })
    } catch (error) {
        writeLog('Error importFinger', error.message)
    }
}

importFingerprint();
