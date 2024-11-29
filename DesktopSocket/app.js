const net = require('net');
const crypto = require('crypto');

// Clave de encriptación (debe ser la misma que la utilizada en los clientes)
const key = crypto.createHash('sha256').update('yLJHJo5hOzKMYROOTuRoQwLJfZx4W3hBRUYg4opoJZM=').digest();

const clients = [];

const server = net.createServer((socket) => {
    console.log('Cliente conectado');
    clients.push(socket);

    socket.on('data', (data) => {
        const encryptedMessage = data.toString();
        console.log('Mensaje encriptado recibido del cliente: ' + encryptedMessage);
        const decryptedMessage = decryptMessage(encryptedMessage);
        console.log('Mensaje desencriptado: ' + decryptedMessage);
        broadcastMessage(decryptedMessage, socket);
    });

    socket.on('end', () => {
        console.log('Cliente desconectado');
        clients.splice(clients.indexOf(socket), 1);
    });

    socket.on('error', (error) => {
        console.error('Error: ', error);
    });
});

server.listen(3000, () => {
    console.log('Servidor escuchando en el puerto 3000 :)');
});

function decryptMessage(encryptedMessage) {
    const encryptedBuffer = Buffer.from(encryptedMessage, 'base64');
    const nonce = encryptedBuffer.slice(0, 16);
    const tag = encryptedBuffer.slice(16, 32);
    const ciphertext = encryptedBuffer.slice(32);
    const decipher = crypto.createDecipheriv('aes-256-gcm', key, nonce);
    decipher.setAuthTag(tag);
    let decrypted = decipher.update(ciphertext, 'binary', 'utf8');
    decrypted += decipher.final('utf8');
    return decrypted;
}

function broadcastMessage(message, sender) {
    clients.forEach((client) => {
        if (client !== sender) {
            client.write(message);
        }
    });
}