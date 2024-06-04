import express from 'express';
import http from 'http';
import WebSocket from 'ws';
import axios from 'axios';
import * as crypto from 'crypto';
import forge from 'node-forge';
import { publicEncrypt, createPublicKey } from 'crypto';

function hexStringToBase64(hexString: string): string {
  const buffer = Buffer.from(hexString, 'hex');

  const base64String = buffer.toString('base64');

  return base64String;
}

function binaryStringToBase64(binaryString: string): string {
    const bytes = new Uint8Array(binaryString.length / 8);
    for (let i = 0; i < binaryString.length; i += 8) {
        bytes[i / 8] = parseInt(binaryString.slice(i, i + 8), 2);
    }
    return Buffer.from(bytes).toString('base64');
}

async function generateKey(): Promise<string> {
    try {
      let key: string = '';
      let finalKey: string = '';
      let keySize = 16;
      let rep = 128 / keySize;
      let ct = 0;
      while (finalKey.length <= keySize) {
        ct++;
        console.log(ct);
        const urls = [
          `http://192.168.1.10:8000/bs_key/${keySize}`
          // `http://192.168.1.10:8000/bb84_key/${keySize}`,
          // `http://192.168.1.10:8000/e91_key/${keySize}`
        ];
      
      const randomUrl = urls[Math.floor(Math.random() * urls.length)];
      const response = await axios.get(randomUrl);
        const { alice_key, bob_key, time_taken }: { alice_key: string, bob_key: string, time_taken: string } = response.data;
        finalKey += alice_key;
      }
  
      finalKey = finalKey.slice(0, keySize);
      key = finalKey.repeat(rep);
      console.log(key);
      const base64Key: string = binaryStringToBase64(key);
        console.log(base64Key);
      return key;
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
            if (type === 'typing') {
                console.log(`${data.user} is typing: ${data.typing}`);
                wss.clients.forEach((client) => {
                  if (client !== ws && client.readyState === WebSocket.OPEN) {
                    client.send(JSON.stringify({ type: 'typing', data: {user: data.user, typing: data.typing }}));
                  }
                });
              }

              else if(type =='image') {
                const senderWs = connections.get(data.sender);
                const recipientWs = connections.get(data.recipient);
                
                [senderWs, recipientWs].forEach((ws) => {
                  if (ws && ws.readyState === WebSocket.OPEN) {
                    ws.send(JSON.stringify({ type: 'image', data: data}));
                  }
                });
              }

            else if (type === 'nickname') {

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
                        let currentNick = nicknames.get(ws);
                    
                        // Convert the recipient's public key from PEM to a public key object
                        const recipientPublicKey = forge.pki.publicKeyFromPem(clients.get(recipientNick)?.publicKey as string);
                    
                        // Encrypt the key with the recipient's public key
                        const encryptedKeyForRecipient = recipientPublicKey.encrypt(key, 'RSA-OAEP');
                    
                        // Convert the encrypted key to base64
                        const encryptedKeyForRecipientBase64 = forge.util.encode64(encryptedKeyForRecipient);
                        console.log(`encrypted key for recipient: ${encryptedKeyForRecipientBase64}`);
                    
                        // Convert the sender's public key from PEM to a public key object
                        const senderPublicKey = forge.pki.publicKeyFromPem(clients.get(currentNick as string)?.publicKey as string);
                    
                        // Encrypt the key with the sender's public key
                        const encryptedKeyForSender = senderPublicKey.encrypt(key, 'RSA-OAEP');
                        
                        // Convert the encrypted key to base64
                        const encryptedKeyForSenderBase64 = forge.util.encode64(encryptedKeyForSender);
                        console.log(`encrypted key for sender: ${encryptedKeyForSenderBase64}`);
                        // Send the encrypted keys
                        let body1 = { type: 'conversation', data: { recipient: recipientNick, key: encryptedKeyForSenderBase64 }};
                        let body2 = { type: 'conversation', data: { recipient: currentNick, key: encryptedKeyForRecipientBase64 }};
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

server.listen(3000, '0.0.0.0',() => {
  console.log('Server started on port 3000');
});
