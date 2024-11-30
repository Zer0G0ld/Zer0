const { send } = require("process");
const { extractDataFromMessage, baileysIs, download, question } = require(".");
const fs = require("fs");

exports.loadCommonfunctions = (socket, webMessage) => {
    const { remoteJid, prefix, commandName, args, userJid, isReply, replyJid } =
        extractDataFromMessage(webMessage);

    const isImage = baileysIs(webMessage, "image");
    const isVideo = baileysIs(webMessage, "video");
    const isSticker = baileysIs(webMessage, "sticker");

    const downloadImage = async (webMessage, fileName) => {
        return await download(webMessage, fileName, "image", "pgn");
    };
    const downloadSticker = async (webMessage, fileName) => {
        return await download(webMessage, fileName, "sticker", "webp");
    };
    const downloadVideo = async (webMessage, fileName) => {
        return await download(webMessage, fileName, "video", "mp4");
    };

    const sendText = async(text) => {
        return await socket.sendMessage(remoteJid, {
            text: `${BOT_EMOJI} ${text}`,
        });
    };

    const sendReply = async (text) => {
        return await socket.sendMessage(remoteJid,
            { text: `${BOT_EMOJI} ${text}` },
            { quoted: webMessage }
        );
    };

    const sendReact = async (emoji) => {
        return await socket.sendMessage(remoteJid, {
            react: {
                text: emoji,
                key: webMessage.key,
            },
        });
    };

    const sendSuccessReact = async () => {
        return await sendReact("✔");
    };

    const sendWaitReact = async () => {
        return await sendReact("⌛");
    };

    const sendWarningReact = async () => {
        return await sendReact("⚠");
    };

    const sendErrorReact = async () => {
        return await sendReact("❌");
    };

    const sendLoveReact = async () => {
        return await sendReact("❤");
    };

    const sendSuccessReply = async (text) => {
        await sendSuccessReact();
        return await sendReply(`✅ ${text}`);
    };

    const sendWaitReply = async (text) => {
        await sendWaitReact();
        return await sendReply(`⌛ ${text}`);
    };
    const sendWarningReply = async (text) => {
        await sendWarningReact();
        return await sendReply(`⚠ ${text}`);
    };
    const sendErrorReply = async (text) => {
        await sendErrorReact();
        return await sendReply(`❌ ${text}`);
    };
    const sendLoveReply = async (text) => {
        await sendLoveReact();
        return await sendReply(`❤ ${text}`);
    };

    const sendStickerFromFile = async (file) => {
        return await socket.sendMessage(remoteJid, {
            sticker: fs.readFileSync(file),
        });
    };

    const sendImageFromFile = async (file) => {
        return await socket.sendMessage(remoteJid, {
            image: fs.readFileSync(file),
        });
    };

    return {
        socket,
        remoteJid,
        userJid,
        prefix,
        commandName,
        args,
        isReply,
        isImage,
        isSticker,
        isVideo,
        remoteJid,
        webMessage,
        sendText,
        sendReact,
        sendReply,
        sendStickerFromFile,
        sendImageFromFile,
        sendSuccessReact,
        sendSuccessReply,
        sendWaitReact,
        sendWaitReply,
        sendWarningReact,
        sendWarningReply,
        sendErrorReact,
        sendErrorReply,
        sendLoveReact,
        sendLoveReply,
        download,
        downloadImage,
        downloadSticker,
        downloadVideo,
    }
};