import { decryptSymmetricKey } from './encryption';
import { get } from 'svelte/store';
import type { Writable } from 'svelte/store';
import type { User, Message } from '../types';

export function initializeWebSocket(nickname: string, publicKey: string): WebSocket {
  const socket = new WebSocket('ws://localhost:3000');
  socket.onopen = () => {
    console.log('Connected to server');
    let body = {
      type: 'nickname',
      data: { nickname, publicKey }
    };
    console.log('Creating new RSA key pair:', { publicKey });
    socket.send(JSON.stringify(body));
  };
  return socket;
}

export async function handleWebSocketMessage(
  event, 
  keyPair, 
  db, 
  usersStore: Writable<User[]>, 
  messagesStore: Writable<Message[]>,
  selectedUserStore: Writable<User | null>
) {
  let message = JSON.parse(event.data);
  let { type, data } = message;
  console.log('Received message:', message);

  switch (type) {
    case 'conversation':
      console.log('Received conversation:', data);
      const decryptedKey = await decryptSymmetricKey(data.key, keyPair.privateKey);
      var transaction = db.transaction(["users"], "readwrite");
      var userStore = transaction.objectStore("users");
      let user = {
        "nickname": data.recipient,
        "key": decryptedKey
      };
      console.log(user);
      userStore.add(user).onsuccess = function(event) {
        console.log("New user added successfully");
        usersStore.update(users => [...users, user]);
      };
      break;

    case 'ai':
    case 'user':
    case 'image':
    case 'message':
      var transaction = db.transaction(["messages"], "readwrite");
      var messageStore = transaction.objectStore("messages");
      let messageToAdd = type === 'message' ? data.message : data;
      messageStore.add(messageToAdd).onsuccess = function(event) {
        console.log(`New ${type} added successfully`);
        messagesStore.update(mess => [...mess, messageToAdd]);
      };
      break;

    case 'typing':
      // Handle typing indicator in the main component
      break;

    case 'error':
      console.log('Error:', data.message);
      // Handle error (e.g., show toast) in the main component
      break;

    default:
      console.log('Unknown message type:', type);
  }
}
