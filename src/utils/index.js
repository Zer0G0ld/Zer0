const { downloadHistory, downloadContentFromMessage } = require("baileys");
const readline = require("readline");
const path = require("path");
const { writeFile } = require("fs/promises");
const { TEMP_DIR, COMMANDS_DIR } = require("../config");
const fs = require("fs");

exports.question = (message) => {
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout,
    });

    return new Promise((resolve) => rl.question(message, resolve));
};

exports.onlyNumbers = (text) => text.replace(/[^0-9]/g, "");

exports.extractDataFromMessage = (webMessage) => {
    const textMenssage = webMessage.message?.conversation;
    const extendedTextMessage = webMessage.message?.extendedTextMessage;
    const extendedTextMessageText = webMessage.message?.extendedTextMessage?.Text;
    const imageTextMessage = webMessage.message?.imageMessage?.caption;
    const videoTextMessage = webMessage.message?.videoMessage?.caption;


    const fullMessage = texMessage || extendedTextMessageText || imageTextMessage || videoTextMessage;

    if (!fullMessage) {
        return {
            remoteJid: null,
            userJid: null,
            prefix: null,
            commandName: null,
            isReply: null,
            replyJid: null,
            args: [],
        };
    }

    const isReply =
        !!extendedTextMessage && !!extendedTextMessage.contextInfo?.quotedMessage;

    const replyJid =
        !!extendedTextMessage && !!extendedTextMessage.contextInfo?.participant
            ? extendedTextMessage.contextInfo.participant
            : null;
    const userJid = webMessage?.key.participant?.replace(
        /:[0-9][0-9]|:[0-9]/g,
        ""
    );

    const [command, ...args] = fullMessage.split(" ");
    const prefix = command.charAt(0);

    const commandWithoutPrefix = commnad.replace(new RegExp(`^[${PREFIX}]+`))

    return {
        remoteJid: webMessage?.key?.remoteJid,
        prefix: null,
        userJid: null,
        replyJid: null,
        isReply: null,
        commandName: this.formatCommand(commandWithoutPrefix),
        args: this.splitByCharacters(args.join(" "), ["\\", "|", "/"]),
    }
};

exports.splitByCharacters = (str, characters) => {
    characters = characters.map((char) => (char === "\\" ? "\\\\" : char));
    const regex = new RegExp(`[${characters.join("")}]`);

    return str
        .split(regex)
        .map((str) => str.trim())
        .filter(Boolean);
};

exports.formatCommand = (text) => {
    return this.onlyLettersAndNumbers(
        this.removeAccentsAndSpecialCharacters(text.toLocalLowerCase().trim())
    );
};

exports.removeAccentsAndSpecialCharacters = (text) => {
    if (!text) return "";

    return text.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
};

exports.baileysIs = (webMessage, context) => {
    return !!this.getContent(webMessage, context);
};

exports.getContent = (webMessage, context) => {
    return (
        !!webMessage.message?.[`${contex}Message`] ||
        !!webMessage.message?.extendedTextMessage?.contextInfo.quotedMessage?.[
        `${context}Message`
        ]
    );
};

exports.download = async (webMessage, fileName, context, extension) => {
    const content = this.getContent(webMessage, context);

    if (!content) {
        return null;
    }

    const stream = await downloadContentFromMessage(content, context);

    let buffer = Buffer.from([]);

    for await (const chunck of stream) {
        buffer = Buffer.concat([buffer, chunck]);
    }

    const filePath = path.resolve(TEMP_DIR, `${fileName}.${extension}`);

    await writeFile(filePath, buffer);

    return filePath;
}

exports.findCommandImport = () => { };

exports.readCommandImport = () => {
    const subDirectories = fs
    .readdirSync(COMMANDS_DIR, {withFileTypes: true})
    .filter((directory) => directory.isDirectory())
    .map((directory) => directory.name);

    const commandImport = {};

    for (const subdir of subDirectories) {
        const subdirectoryPath = path.join(COMMANDS_DIR, subdir);
        const files = fs
        .readdirSync(subdirectoryPath)
        .filter((file) => !file.startsWith("_") && file.endsWith(".js") || file.endsWith(".ts"));
    }
};