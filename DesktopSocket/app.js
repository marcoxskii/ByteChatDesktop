const net = require('net');

const server = net.createServer((socket) => {
    console.log('Cliente conectado');

    socket.on('data', (data) => {
        console.log('Mensaje recibido del cliente: ' + data.toString());
        socket.write('Mensaje recibido' + data.toString());
    });
 
    socket.on('end', () => {
        console.log('Cliente desconectado');
    });

    socket.on('error', (error) => {
        console.error('Error: ', error);
    });
});

server.listen(3000, () => {
    console.log('Servidor escuchando en el puerto 3000 :)');
});
