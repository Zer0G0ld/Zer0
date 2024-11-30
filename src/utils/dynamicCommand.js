const { verifyPrefix, hasTypeOrCommand } = require("../middlewares");
const { checkPermission } = require("../middlewares/checkPermission");
const { DangerError, WarningError, InvalidParameterError } = require("../errors");
const { findCommandImport } = require(".");

exports.dynamicCommand = async (paramsHandler) => {
    const { commandName, prefix, sendWaringReply, sendErrorReply } =
    paramsHandler;

    const {type, command} = findCommandImport(commandName);

    if (!verifyPrefix(prefix) || !hasTypeOrCommand({ type, command})) {
        return;
    }

    if (! await checkPermission({ type, ...paramsHandler })) {
        return sendErrorReply("Você não tem permissão para executar esse comando!");
    }
    
    try {
        await command.handle({ ...paramsHandler, type });
    } catch (error) {
        console.log(error);

        if (error instanceof InvalidParameterError) {
            await sendWaringReply(`Parâmetros inválidos! ${error.message}`);
        } else if (error instanceof WarningError) {
            await sendWaringReply(error.message);
        } else if (error instanceof DangerError) {
            await sendErrorReply(error.message);
        } else {
            await sendErrorReply(
                `Ocorreu um erro ao executar o comando ${commnad.name}! O desenvolvedor foi notificado!
                
                📋 *Detalhes:* ${error.message}
                `
            );
        }
    }
}

