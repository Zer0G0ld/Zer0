const {
    default: makeWASocket,
    useMultiFileAuthState,
    fetchLatesBaileysVersion,
    DisconnectReason,
} = require("@whiskeysockets/baileys");
const { Socket } = require("dgram");
const path = require("path");
const pino = require("pino");
const { question, onlyNumbers } = require("./utils");

exports.connect = async () => {
    const { state, saveCards } = await useMultiFileAuthState(
        path.resolve(__dirname, "..", "assets", "auth", "baileys")
    );

    const { version } = await fetchLatesBaileysVersion();

    const Socket = makeWASocket({
        printQRInTerminal: false,
        version,
        logger: pino({ level: "error" }),
        auth: state,
        browser: ["Chrome (Linux)", "", ""],
        makeOnlineOnConnect: true,
    });

    if (!Socket.authState.creds.registered) {
        const phoneNumber = await question("Informe seu número de telefone: ");

        if (!phoneNumber) {
            throw new Error("Número de telefone inválido");
        }

        const code = await Socket.requestPairingCode(onlyNumbers(phoneNumber));

        console.log(`Código de pareamento: ${code}`);
    }

    Socket.ev.on("connection.update", (update) => {
        const { connection, lastDisconnect } = update;

        if (connection === "close") {
            const shouldReconnect = lastDisconnect.Error?.output?.statusCode !== DisconnectReason.loggedOut;

            if (shouldReconnect) {
                this.connect();
            }
        }

    });

    Socket.ev.on("creds.update", saveCreds);
};