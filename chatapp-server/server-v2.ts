import express from 'express';
import http from 'http';
import WebSocket from 'ws';
import axios from 'axios';
import * as crypto from 'crypto';

function hexStringToBase64(hexString: string): string {
  const buffer = Buffer.from(hexString, 'hex');

  const base64String = buffer.toString('base64');

  return base64String;
}


function binaryStringToBase64(binaryString: string): string {
    
let base64String = '';
  for (let i = 0; i < binaryString.length; i += 4) {
    // Extract 6 bits from the binary string
    const bits = binaryString.slice(i, i + 4);

    // Convert the 6 bits to decimal
    const decimalValue = parseInt(bits, 2);

    // Get the corresponding Base64 character
    const base64Char = decimalValue.toString(16);

    base64String += base64Char;
  }

  return base64String;
}

async function generateKey(): Promise<string> {
    try {
      let key: string = '';
      let finalKey: string = '';
      let keySize = 16;
      let rep = 128 / keySize;
      let ct = 0;
      while (finalKey.length < keySize) {
        ct++;
        console.log(ct);
        const response = await axios.get('http://192.168.1.5:8000/key');
        const { alice_key, bob_key }: { alice_key: string, bob_key: string } = response.data;
        finalKey += alice_key;
      }
  
      finalKey = finalKey.slice(0, keySize);
      key = finalKey.repeat(rep);
      console.log(key);
      const base64Key: string = binaryStringToBase64(key);
        console.log(base64Key);
      return base64Key;
    } catch (error) {
  console.log(error);
      throw error;
    }
  }

interface Message {
    sender: string;
    receiver: string;
    content: string;
    encrypted: boolean;
    timestamp: number;
}

interface Client {
    socket: WebSocket;
    publicKey?: string;
  }

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

const clients = new Map<string, Client>();

app.get('/keygen', async (req, res) => {
try {
    const nickname = req.query.nickname as string; 
    const client = clients.get(nickname);
    if (!client || !client.publicKey) {
            throw new Error('Client not found or public key not set');
        }
    const url: string = 'http://192.168.1.5:8000/key';
    const response: string = await generateKey();
    const encryptedKey = crypto.publicEncrypt(client.publicKey, Buffer.from(response));

    res.send(JSON.stringify({key: encryptedKey.toString('base64')}));
} catch (error) {
    res.send('{error: true}');
  }
});

const connections = new Map<string, WebSocket>();
const nicknames = new Map<WebSocket, string>();

function getNickname(conn: WebSocket): string {
    return [...connections].find(([key, val]) => val == conn)![0]!
}

wss.on('connection', (ws: WebSocket) => {
    connections.set(ws.url, ws);

    ws.on('message', (message: string) => {
        try {
            const parsedMessage = JSON.parse(message);
            const { type, data } = parsedMessage;

            if (type === 'nickname') {

                const { nickname, publicKey } = data;
                clients.set(nickname, { socket: ws, publicKey });
                connections.set(nickname, ws);
		nicknames.set(ws, nickname);
                console.log(`Received nickname: ${nickname}`);
                console.log(`Public key: ${publicKey}`);
            } else if (type == 'conversation') {
	            const { recipientNick } = data;
                console.log(`Conversation thing ${recipientNick}`);
	            if (connections.has(recipientNick)) {
                    console.log("it is valid lol");
                    generateKey().then((key) => {
                        const recipientSocket = connections.get(recipientNick as string)!;
	                    let body1 = { type: 'conversation', data: { recipient: recipientNick, key: key}};
	                    let currentNick = nicknames.get(ws);
                        console.log(`current nick: ${currentNick}`);
		                let body2 = { type: 'conversation', data: { recipient: currentNick, key: key}};
		                recipientSocket.send(JSON.stringify(body2));
		                ws.send(JSON.stringify(body1)); 
                    });
                }
            } else if (type == 'message') {
                console.log(`Received message: ${JSON.stringify(data)}`);
                
                if (connections.has(data.receiver)) {
                    const recipientSocket = connections.get(data.receiver);
                    if (recipientSocket) {
                        recipientSocket.send(JSON.stringify({ type: 'message', data: { message: data } }));
                        ws.send(JSON.stringify({ type: 'message', data: { message: data } }));
                    }
                }
            }
        }
        catch (error) {
            console.error('Error parsing message:', error);
        }
    });

        ws.on('close', () => {
            // Remove disconnected client from the list of connections
            connections.forEach((socket, key) => {
                if (socket === ws) {
                    connections.delete(key);
                }
    });
	nicknames.forEach((thing, socket) => {
		if (socket === ws) nicknames.delete(socket);
	});
  });
});

server.listen(3000, () => {
  console.log('Server started on port 3000');
});
