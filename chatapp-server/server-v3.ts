import express from 'express';
import http from 'http';
import WebSocket from 'ws';
import axios from 'axios';
import * as crypto from 'crypto';
import forge from 'node-forge';
import { publicEncrypt, createPublicKey } from 'crypto';

// Constants
const QKD_SERVER_URL = 'http://localhost:8000';
const BS_KEY_ENDPOINT = `${QKD_SERVER_URL}/bs_key`;

// Utility functions
function binaryStringToBase64(binaryString: string): string {
    const bytes = new Uint8Array(binaryString.length / 8);
    for (let i = 0; i < binaryString.length; i += 8) {
        bytes[i / 8] = parseInt(binaryString.slice(i, i + 8), 2);
    }
    return Buffer.from(bytes).toString('base64');
}

async function generateKey(): Promise<string> {
    try {
        let finalKey: string = '';
        let keySize = 4;
        let rep = 128 / keySize;
        let ct = 0;
        while (finalKey.length <= keySize) {
            ct++;
            console.log(ct);
            const url = `${BS_KEY_ENDPOINT}/${keySize}`;
            const response = await axios.get(url);
            const { alice_key }: { alice_key: string, bob_key: string, time_taken: string } = response.data;
            finalKey += alice_key;
        }

        finalKey = finalKey.slice(0, keySize);
        const key = finalKey.repeat(rep);
        console.log(key);
        const base64Key: string = binaryStringToBase64(key);
        console.log(base64Key);
        return key;
    } catch (error) {
        console.log(error);
        throw error;
    }
}

// Interfaces
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

// Server setup
const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

const clients = new Map<string, Client>();
const connections = new Map<string, WebSocket>();
const nicknames = new Map<WebSocket, string>();

// WebSocket connection handler
wss.on('connection', (ws: WebSocket) => {
    connections.set(ws.url, ws);

    ws.on('message', (message: string) => {
        try {
            const parsedMessage = JSON.parse(message);
            const { type, data } = parsedMessage;

            switch (type) {
                case 'typing':
                    handleTyping(ws, data);
                    break;
                case 'image':
                    handleImage(data);
                    break;
                case 'ai':
                case 'nickname':
                    handleNickname(ws, data);
                    break;
                case 'ai-conversation':
                    handleAIConversation(ws, data);
                    break;
                case 'conversation':
                    handleConversation(ws, data);
                    break;
                case 'message':
                    handleMessage(ws, data);
                    break;
                default:
                    console.log(`Unknown message type: ${type}`);
            }
        } catch (error) {
            console.error('Error parsing message:', error);
        }
    });

    ws.on('close', () => {
        handleDisconnect(ws);
    });
});

// Message type handlers
function handleTyping(ws: WebSocket, data: any) {
    console.log(`${data.user} is typing: ${data.typing}`);
    broadcastToOthers(ws, { type: 'typing', data: { user: data.user, typing: data.typing } });
}

function handleImage(data: any) {
    const senderWs = connections.get(data.sender);
    const recipientWs = connections.get(data.recipient);
    
    [senderWs, recipientWs].forEach((ws) => {
        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({ type: 'image', data: data }));
        }
    });
}

function handleNickname(ws: WebSocket, data: any) {
    const { nickname, publicKey } = data;
    clients.set(nickname, { socket: ws, publicKey });
    connections.set(nickname, ws);
    nicknames.set(ws, nickname);
    console.log(`Received nickname: ${nickname}`);
    console.log(`Public key: ${publicKey}`);
}

function handleAIConversation(ws: WebSocket, data: any) {
    const { recipientNick } = data;
    console.log(`Starting AI conversation with initial message: ${recipientNick}`);
    generateKey().then((key) => {
        sendEncryptedKeys(ws, "ai", recipientNick, key);
    });
}

function handleConversation(ws: WebSocket, data: any) {
    const { recipientNick } = data;
    console.log(`Searching for user ${recipientNick}...`);
    if (connections.has(recipientNick)) {
        console.log("User found!");
        generateKey().then((key) => {
            sendEncryptedKeys(ws, recipientNick, nicknames.get(ws) as string, key);
        });
    } else {
        console.log("User not found!");
        ws.send(JSON.stringify({ type: 'error', data: { message: `User with nickname ${recipientNick} does not exist.` } }));
    }
}

function handleMessage(ws: WebSocket, data: any) {
    console.log(`Received message: ${JSON.stringify(data)}`);
    
    if (connections.has(data.receiver)) {
        const recipientSocket = connections.get(data.receiver);
        if (recipientSocket) {
            recipientSocket.send(JSON.stringify({ type: 'message', data: { message: data } }));
            ws.send(JSON.stringify({ type: 'message', data: { message: data } }));
        }
    }
}

function handleDisconnect(ws: WebSocket) {
    connections.forEach((socket, key) => {
        if (socket === ws) {
            connections.delete(key);
        }
    });
    nicknames.delete(ws);
}

// Helper functions
function broadcastToOthers(sender: WebSocket, message: any) {
    wss.clients.forEach((client) => {
        if (client !== sender && client.readyState === WebSocket.OPEN) {
            client.send(JSON.stringify(message));
        }
    });
}

function sendEncryptedKeys(senderWs: WebSocket, recipientNick: string, senderNick: string, key: string) {
    const recipientPublicKey = forge.pki.publicKeyFromPem(clients.get(recipientNick)?.publicKey as string);
    const senderPublicKey = forge.pki.publicKeyFromPem(clients.get(senderNick)?.publicKey as string);

    const encryptedKeyForRecipient = recipientPublicKey.encrypt(key, 'RSA-OAEP');
    const encryptedKeyForSender = senderPublicKey.encrypt(key, 'RSA-OAEP');

    const encryptedKeyForRecipientBase64 = forge.util.encode64(encryptedKeyForRecipient);
    const encryptedKeyForSenderBase64 = forge.util.encode64(encryptedKeyForSender);

    const recipientSocket = connections.get(recipientNick);
    if (recipientSocket) {
        recipientSocket.send(JSON.stringify({ type: 'conversation', data: { recipient: senderNick, key: encryptedKeyForRecipientBase64 } }));
    }
    senderWs.send(JSON.stringify({ type: 'conversation', data: { recipient: recipientNick, key: encryptedKeyForSenderBase64 } }));
}

// Start the server
server.listen(3000, '0.0.0.0', () => {
    console.log('Server started on port 3000');
});
