exports.dynamicCommand = async (paramsHandler) => {
    const { commandName, prefix, sendWaringReply, sendErrorReply } =
    paramsHandler;

    const {type, command} = findeCommandImport(commandName);
}