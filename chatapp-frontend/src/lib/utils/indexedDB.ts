import { writable } from 'svelte/store';
import type { User, Message } from '../types';

export function initializeIndexedDB(usersStore, selectedUserStore, messagesStore) {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open("messages", 2);
    
    request.onupgradeneeded = function() {
      const db = request.result;
      db.createObjectStore("messages", { keyPath: "timestamp" });
      const messageStore = db.createObjectStore("messages", { keyPath: "timestamp" });
      messageStore.createIndex("type", "type", { unique: false });
      messageStore.createIndex("sender", "sender", { unique: false });
      messageStore.createIndex("receiver", "receiver", { unique: false });
      messageStore.createIndex("encrypted", "encrypted", { unique: false });
      messageStore.createIndex("content", "content", { unique: false });
      const userStore = db.createObjectStore("users", { keyPath: "nickname" });
      userStore.createIndex("key", "key", { unique: false });
    };

    request.onsuccess = function() {
      const db = request.result;
      
      const userTransaction = db.transaction(["users"], "readonly");
      const userStore = userTransaction.objectStore("users");
      const getAllUsersRequest = userStore.getAll();
      getAllUsersRequest.onsuccess = function(event) {
        const users = event.target.result || [];
        usersStore.set(users);
        if (users.length > 0) {
          selectedUserStore.set(users[0]);
        }
        console.log("Users retrieved successfully:", users);
      };

      const messageTransaction = db.transaction(["messages"], "readonly");
      const messageStore = messageTransaction.objectStore("messages");
      const getAllMessagesRequest = messageStore.getAll();
      getAllMessagesRequest.onsuccess = function(event) {
        messagesStore.set(event.target.result || []);
        console.log("Messages retrieved successfully:", messagesStore);
      };

      resolve(db);
    };

    request.onerror = function(event) {
      console.error("Database error: " + event.target.error);
      reject(event.target.error);
    };
  });
}

export function clearIndexedDB() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open('messages', 2);

    request.onsuccess = function(event) {
      const db = event.target.result;
      const transaction = db.transaction(['messages', 'users'], 'readwrite');
      const messageStore = transaction.objectStore('messages');
      const userStore = transaction.objectStore('users');
      
      messageStore.clear().onsuccess = function() {
        console.log('Message store cleared');
      };

      userStore.clear().onsuccess = function() {
        console.log('User store cleared');
      };

      transaction.oncomplete = function() {
        db.close();
        resolve();
      };

      transaction.onerror = function(event) {
        console.error('Error clearing stores:', event.target.error);
        reject(event.target.error);
      };
    };

    request.onerror = function(event) {
      console.error('Error opening database:', event.target.error);
      reject(event.target.error);
    };
  });
}
