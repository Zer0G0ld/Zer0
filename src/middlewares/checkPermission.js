exports.checkPermission = async ({ type, socket, userjid, remoteJid }) => {
    if (type === "member") {
        return true;
    }

    const { participants, owner } = await socket.groupMetadata(remoteJid);
    const participant = participants.find(
        (participant) => participant.id === userjid
    );

    if (!participant) {
        return false;
    }

    const isOwner = 
        participant.id === owner || participant.admin === "superadmin";
    const isAdmin = participant.admin === "admin";

    if (type === "admin") {
        return isOwner || isAdmin;
    }

    if (type === "owner") {
        return isOwner;
    }

    return false;
}