const fs = require('fs');
const qrcode = require('qrcode-terminal');
const fetch = require('node-fetch');
const FormData = require('form-data');
const http = require('http');

const {
    Client,
    MessageTypes,
    MessageMedia
} = require('whatsapp-web.js');
const {
    Readable
} = require('stream');

const server = 'http://localhost:5000/';



const SESSION_FILE_PATH = './session.json';

let sessionData;
if (fs.existsSync(SESSION_FILE_PATH)) {
    sessionData = require(SESSION_FILE_PATH);
}


const client = new Client({
    puppeteer: {
        headless: false,
        session: sessionData,
        executablePath: 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
    }
});


client.on('authenticated', (session) => {
    sessionData = session;
    fs.writeFile(SESSION_FILE_PATH, JSON.stringify(session), function (err) {
        if (err) {
            console.error(err);
        }
    });
});



client.on('ready', () => {
    console.log("מוכן ומזומן לתפעל 😎");
})

client.on('qr', qr => {
    qrcode.generate(qr, {
        small: true
    })
})

async function nextLetter(name, msg) {
    let letterData = await fetch(server + "members/" + name);
    let vowels = (await (await fetch(server + "vowels")).json()).response;

    let letter = await letterData.text();
    if (letter == '#') msg.reply("ברכותיי, סיימת את התהליך")
    else
        msg.reply("#" + letter + "#" + name + "#\n" + "אנא הגב להודעה זאת עם הקלטה לצלילים: \n" + vowels.join(", ") + "\nבאות שמופיעה בין ה# עם מרווח של לפחות שנייה בין ההברות")

}

client.on('message_create', async msg => {
    let signupFormat = /^הרשמה: \w+$/g

    if (signupFormat.test(msg.body)) {
        return await signUp(msg);
    }
    await record(msg);

    let genFormat = /^v: \w+: \w+$/g

    if(genFormat.test(msg.body)) {
        let name = msg.body.split(':')[1].substr(1);
        let toRecord = msg.body.split(':')[2].substr(1);

        let file = fs.createWriteStream('./pipi.mp3');
        http.get(`${server}generate_sentence/${name}/${toRecord}`, response => {
            response.pipe(file);
            file.on('finish', () => {
                msg.reply(MessageMedia.fromFilePath('./pipi.mp3'),null,{ sendAudioAsVoice: true })
            })  
        })
    }

})

async function record(msg) {
    let recordFormat = /^#\w#\w+#/g
    if (!msg.hasQuotedMsg) return;
    let qMsg = await msg.getQuotedMessage();
    if (!qMsg.fromMe) return;
    if (msg.type != MessageTypes.VOICE) return;
    if (!recordFormat.test(qMsg.body)) return;

    let media = await msg.downloadMedia();

    const filename = "kaki.ogg";

    fs.writeFile(filename, media.data, {
        encoding: 'base64'
    }, function (err) {
        console.log('File created');
    });


    let letter = qMsg.body.split('#')[1];
    let name = qMsg.body.split('#')[2];


    const form = new FormData();

    form.append('tone', letter);
    form.append('name', name);
    form.append('mp3', fs.createReadStream(filename), {
        contentType: media.mimetype
    });

    let response = await fetch(server + "upload_sound", {
        method: 'POST',
        body: form
    });
    const contentType = response.headers.get("content-type");
    if (contentType != "zip") {
        let text = await response.text();
        await msg.reply("בולבול" + text)

    }

    await nextLetter(name, msg);

}

client.initialize();

async function signUp(msg) {
    let name = msg.body.replace(/הרשמה: /g, "");
    let respone = await fetch(server + "sign_member/" + name);
    let text = await respone.text();
    console.log(text);
    if (text == '') {

        await msg.reply("נרשם בהצלחה");
        await nextLetter(name, msg);
    } else
        msg.reply(text);



    return;
}


