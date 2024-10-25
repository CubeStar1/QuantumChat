<script lang="ts">
  // External Libraries
  import * as aesjs from 'aes-js';
  import forge from 'node-forge';
  import axios from 'axios';
  import { writable } from "svelte/store";
  import { onMount, afterUpdate } from "svelte";
  import { browser } from "$app/environment"; 
  import { toast } from "svelte-sonner";
  import { toggleMode } from "mode-watcher";
  import { selectedProtocol, showLogs } from '$lib/index';

  // UI Components

  import BackgroundGradient from '$lib/components/ui/BackgroundGradient/BackgroundGradient.svelte';



  // State Management
  import { DotBackground } from '$lib/components/ui/GridAndDotBackground';

  // Import new components
  import ChatHeader from '$lib/components/ChatHeader.svelte';
  import Sidebar from '$lib/components/Sidebar.svelte';
  import MessageList from '$lib/components/MessageList.svelte';
  import MessageInput from '$lib/components/MessageInput.svelte';

  import type { Writable } from 'svelte/store';

  let protocol;
  selectedProtocol.subscribe(value => {
    protocol = value;
  });

  let messageElement: HTMLElement | null = null;

  let typing = false;
  let userExists = true;
  let typingUsers: string[] = [];
  let typingTimeout: ReturnType<typeof setTimeout>;
  let messageText = '';
  let showNewModal = false;

  afterUpdate(() => {
    if (messageElement) {
      messageElement.scrollIntoView({ behavior: 'smooth' });
    }
  });

  interface User {
    nickname: string;
    key: string;
  }

  interface Message {
    timestamp: number;
    sender: string;
    receiver: string;
    encrypted: boolean;
    content: string;
    type?: string;
    data?: string;
    image?: string;
  }

  let messagesStore: Writable<Message[]> = writable<Message[]>([]);
  let users: User[] = [];
  let messages: Message[] = [];
  let selectedUser: User | null = null;
  $: relevantMessages = selectedUser ? $messagesStore.filter((message: Message) => message.sender === selectedUser!.nickname || message.receiver === selectedUser!.nickname) : [];
  $: sortedMessages = relevantMessages.sort((a: Message, b: Message) => a.timestamp - b.timestamp);
  $: decryptedMessages = sortedMessages.map((message: Message) => decryptMessage(message, selectedUser));

  let logEncryptMessages = '';
  let logDecryptMessages = '';

  function decryptMessage(message: Message, user: User | null): Message {
    if (!user) {
      return message;
    }
    if (message.encrypted) {
      let binaryKey = atob(user.key).split('').map(function(c) {
        return c.charCodeAt(0);
      }).join('');

      let key = new Uint8Array(16);
      for (let i = 0; i < 16; i++) {
        key[i] = parseInt(binaryKey.substr(i * 8, 8), 2);
      }

      var aesCtr = new aesjs.ModeOfOperation.ctr(key, new aesjs.Counter(1));
      var encryptedBytes = aesjs.utils.hex.toBytes(message.content);
      var decryptedBytes = aesCtr.decrypt(encryptedBytes);
      var decryptedText = aesjs.utils.utf8.fromBytes(decryptedBytes);
      logDecryptMessages += `Timestamp: ${new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}\n`;
      logDecryptMessages += `Symmetric Key: ${user.key}\n`;
      logDecryptMessages += `Message decrypted: ${decryptedText}\n`;
      return {
        type: 'message',
        encrypted: false,
        content: decryptedText,
        timestamp: message.timestamp,
        sender: message.sender,
        receiver: message.receiver
      }
    }
    return message;
  }

  async function generateKeyPair(): Promise<{ publicKey: string; privateKey: string }> {
    let keyPair = forge.pki.rsa.generateKeyPair(2048);
    let publicKey = forge.pki.publicKeyToPem(keyPair.publicKey);
    let privateKey = forge.pki.privateKeyToPem(keyPair.privateKey);
    return {
      publicKey: publicKey,
      privateKey: privateKey
    };
  }

  async function decryptSymmetricKey(encryptedKey: string, privateKeyPem: string): Promise<string | undefined> {
    try {
      console.log(`Encrypted key: ${encryptedKey}`);
      if (!(/^[A-Za-z0-9+/=]*$/.test(encryptedKey))) {
        console.error("Encrypted key is not a valid base64 string");
      }

      let encryptedKeyBytes = forge.util.decode64(encryptedKey);
      let privateKey = forge.pki.privateKeyFromPem(privateKeyPem);
      let decryptedKeyBytes = privateKey.decrypt(encryptedKeyBytes, 'RSA-OAEP');
      let decryptedKey = btoa(decryptedKeyBytes);

      return decryptedKey;
    } 
    catch (error) {
      console.error(error);
      return undefined;
    }
  }

  async function InitializeAIConversation(): Promise<void> {
    keyPair = await generateKeyPair();
    let body = {
      type: 'ai',
      data: {
        nickname: data.nickname,
        publicKey: keyPair.publicKey
      }
    };
    console.log('Creating new RSA key pair:', keyPair);
    socket.send(JSON.stringify(body));
    const aiPrivateKey = keyPair.privateKey;
  }

  let db: IDBDatabase;
  let socket: WebSocket;
  let keyPair: { publicKey: string, privateKey: string };

  function handleSubmit(): void {
    if (!messageText || !(messageText = messageText.trim()) || !selectedUser) {
      return
    }
    console.log()
    let binaryKey = atob(selectedUser.key).split('').map(function(c) {
    return c.charCodeAt(0);
    }).join('');

    let key = new Uint8Array(16);
    for (let i = 0; i < 16; i++) {
      key[i] = parseInt(binaryKey.substr(i * 8, 8), 2);
    }

    var aesCtr = new aesjs.ModeOfOperation.ctr(key, new aesjs.Counter(1));
    var textBytes = aesjs.utils.utf8.toBytes(messageText);
    var encryptedBytes = aesCtr.encrypt(textBytes);
    var encryptedHex = aesjs.utils.hex.fromBytes(encryptedBytes);
    let message = {
      encrypted: true,
      content: encryptedHex,
      timestamp: Date.now(),
      receiver: selectedUser.nickname,
      sender: data.nickname
    }
    logEncryptMessages += `Timestamp: ${new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}\n`;
    logEncryptMessages += `Symmetric Key: ${selectedUser.key}\n`;
    logEncryptMessages += `Message encrypted: ${message.content}\n`;

    console.log(selectedUser);
    let payload = {
      type: 'message',
      data: message
    }
    socket.send(JSON.stringify(payload));
    messageText = '';
  }
  
  export let data: { nickname: string };

  let markedDirty = false;

  if (browser) {
    onMount(async () => {
      keyPair = await generateKeyPair();
      socket = new WebSocket('ws://localhost:3000');
      socket.onopen = () => {
        console.log('Connected to server');
        let body = {
          type: 'nickname',
          data: {
            nickname: data.nickname,
            publicKey: keyPair.publicKey
          }
        };
        console.log('Creating new RSA key pair:', keyPair);
        socket.send(JSON.stringify(body));
      };

      const request = indexedDB.open("messages", 2);
      
      request.onupgradeneeded = function(event: IDBVersionChangeEvent) {
        const db = (event.target as IDBOpenDBRequest).result;
        var messageStore = db.createObjectStore("messages", { keyPath: "timestamp" });
        messageStore.createIndex("type", "type", { unique: false })
        messageStore.createIndex("sender", "sender", { unique: false });
        messageStore.createIndex("receiver", "receiver", { unique: false });
        messageStore.createIndex("encrypted", "encrypted", { unique: false });
        messageStore.createIndex("content", "content", { unique: false });
        var userStore = db.createObjectStore("users", { keyPath: "nickname" });
        userStore.createIndex("key", "key", { unique: false });
      };

      request.onsuccess = function(event: Event) {
        db = (event.target as IDBOpenDBRequest).result;
        
        const transaction = db.transaction(["users"], "readonly");
        const userStore = transaction.objectStore("users");
        const getAllUsersRequest = userStore.getAll();
        getAllUsersRequest.onsuccess = function(event: Event) {
          const usersRes = (event.target as IDBRequest).result;
          users = usersRes ?? [];
          if (users.length > 0) {
            selectedUser = users[0];
          }
          console.log("Users retrieved successfully:", users);
        };

        const transaction2 = db.transaction(["messages"], "readonly");
        const messageStore = transaction2.objectStore("messages");
        const getAllMessagesRequest = messageStore.getAll();
        getAllMessagesRequest.onsuccess = function(event: Event) {
          const messagesRes = (event.target as IDBRequest).result;
          messagesStore.set(messagesRes ?? []);
          console.log("Messages retrieved successfully:", messagesStore);
        };
      };

      socket.onmessage = async (event: MessageEvent) => {
        let message = JSON.parse(event.data);
        let { type, data } = message;
        console.log('Received message:', message);
        if (type === 'conversation') {
          console.log('Received conversation:', data);
          const decryptedKey = await decryptSymmetricKey(data.key, keyPair.privateKey);
          var transaction = db.transaction(["users"], "readwrite");
          var userStore = transaction.objectStore("users");
          let user = {
            "nickname": data.recipient,
            "key": decryptedKey
          }
          console.log(user);
          var addRequest = userStore.add(user);
          addRequest.onsuccess = function(event: Event) {
            console.log("New user added successfully");
            users = [...users, user];
            markedDirty = !markedDirty;
          };
          addRequest.onerror = function(event: Event) {
            console.error("Error adding user:", (event.target as IDBRequest).error);
          };

          console.log('Users:', users)
        } 
        else if (type == 'ai' || type == 'user') {
          var transaction = db.transaction(["messages"], "readwrite");
          var messageStore = transaction.objectStore("messages");
          let message = data;
          console.log(`Message: ${JSON.stringify(message)}`);

          // Determine if the message is from the AI or the user
          if (data.user === 'AI') {
            message.type = 'ai';
          } else {
            message.type = 'user';
          }

          var addMessageRequest = messageStore.add(message);
          addMessageRequest.onsuccess = function(event: Event) {
            console.log("Message added successfully");
            messagesStore.update((mess: Message[]) => {
              mess.push(message);
              markedDirty = !markedDirty;
              return mess;
            });
          };
          addMessageRequest.onerror = function(event: Event) {
            console.log("Error adding message:", (event.target as IDBRequest).error);
          };
        }
        else if(type == 'image'){
          var transaction = db.transaction(["messages"], "readwrite");
          var messageStore = transaction.objectStore("messages");
          let message = data
          console.log(`Message: ${JSON.stringify(message)}`);
          var addImageRequest = messageStore.add(message);
          addImageRequest.onsuccess = function(event: Event) {
            console.log("New image added successfully");
            messagesStore.update((mess: Message[]) => {
              mess.push(message);
              markedDirty = !markedDirty;
              return mess;
            });
          };
          addImageRequest.onerror = function(event) {
            console.log("Error adding image:", event?.target?.error);
          };
        } 
        else if (type === 'typing') {
          if (data.typing && !typingUsers.includes(data.user)) {
            typingUsers = [...typingUsers, data.user];
          } else if (!data.typing) {
            typingUsers = typingUsers.filter(u => u !== data.user);
          }
        }
        else if(type === 'error'){
          userExists = false;
          console.log('User does not exist');
          toast.error("User does not exist", {
            description: `${data.message}`,
            action: {
              label: "Undo",
              onClick: () => console.info("Undo")
            }
          });
        }
        else if (type === 'message') {
          var transaction = db.transaction(["messages"], "readwrite");
          var messageStore = transaction.objectStore("messages");
          let message = data.message;
          console.log(`Message: ${JSON.stringify(message)}`);
          var addRequest = messageStore.add(message);
          addRequest.onsuccess = function(event: Event) {
            console.log("New message added successfully");
            messagesStore.update((mess: Message[]) => {
              mess.push(message);
              markedDirty = !markedDirty;
              return mess;
            });
          };
          addRequest.onerror = function(event: Event) {
            console.error("Error adding message:", (event.target as IDBRequest).error);
          };
        }
      };
    });
  }

  function newConversation(arg0: string): void {
    console.log('New conversation:', arg0);
    socket.send(JSON.stringify({
      type: 'conversation',
      data: {
        recipientNick: arg0
      }
    }));
  }

  function newAIConversation(): void {
    InitializeAIConversation();
    console.log('Starting new conversation with AI');
    socket.send(JSON.stringify({
      type: 'ai-conversation',
      data: {
        recipientNick: 'ai'
      }
    }));
  }

  function handleInput(): void {
    clearTimeout(typingTimeout);
    if (!typing) {
      typing = true;
      socket.send(JSON.stringify({ type: 'typing', data: {user: data.nickname, typing: true }})); 
    }
    typingTimeout = setTimeout(stopTyping, 1000);
  }

  function stopTyping(): void {
    typing = false;
    socket.send(JSON.stringify({ type: 'typing', data: {user: data.nickname, typing: false }}));
  }

  async function sendImage(): Promise<void> {
    const fileInput = document.getElementById('fileInput') as HTMLInputElement;
    var file = fileInput.files?.[0];
    if (!file) return;

    console.log(file.name);
    const reader = new FileReader();
    let patientInfo = null;

    if (file.name.toLowerCase().endsWith('.dcm')) {
      const formData = new FormData();
      formData.append('file', file);
      const response = await axios.post('http://localhost:8001/convert/', formData, {
        responseType: 'blob',
      });

      const blob = new Blob([response.data], { type: 'image/jpeg' });
      file = new File([blob], file.name.replace('.dcm', '.jpg'), { type: 'image/jpeg' });

      const patientInfoResponse = await axios.post('http://localhost:8001/extract-patient-info/', formData);
      patientInfo = patientInfoResponse.data.patient_info;
    }

    reader.onload = async (event) => {
      const dataUrl = event.target?.result as string;
      const message = {
        type: 'image',
        data: {
          type: 'image',
          image: dataUrl,
          sender: data.nickname,
          receiver: selectedUser?.nickname,
          timestamp: Date.now(),
          encrypted: false
        }
      };

      socket.send(JSON.stringify(message));

      if (patientInfo) {
        const patientSummaryResponse = await axios.post('http://localhost:8001/get-patient-summary/', { patient_info: patientInfo });
        const patientVitals = await axios.get('http://localhost:8003/api/health_data/1');
        console.log(patientVitals);
        const patientVitalsProcessed = patientVitals.data.average_heart_rate + ' bpm, ' + patientVitals.data.average_temperature + ' mmHg';

        const patientSummary = patientSummaryResponse.data.patient_summary;

        const summaryMessage = {
          type: 'message',
          data: {
            type: 'message',
            encrypted: false,
            content: patientSummary,
            timestamp: Date.now(),
            sender: data.nickname,
            receiver: selectedUser?.nickname
          }
        };

        const contentString = "**Patient vitals:** "  + "\n\n" + "Heart rate: " + patientVitals.data.average_heart_rate + " bpm\n\n" + "Temperature: " + patientVitals.data.average_temperature + "º F";

        const vitalsMessage = {
          type: 'message',
          data: {
            type: 'message',
            encrypted: false,
            content: contentString,
            timestamp: Date.now() + 1,
            sender: data.nickname,
            receiver: selectedUser?.nickname
          }
        };
        socket.send(JSON.stringify(summaryMessage));
        socket.send(JSON.stringify(vitalsMessage));
      }
      
      fileInput.value = '';
    };

    reader.readAsDataURL(file);
  }

  function logout(): void {
    messages = [];
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i];
      var eqPos = cookie.indexOf("=");
      var name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
      document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT";
    }
    clearIndexedDB();
    window.location.href = '/login';
  }

  function clearIndexedDB(): void {
    const request = indexedDB.open('messages', 2);

    request.onsuccess = function(event: Event) {
      const db = (event.target as IDBOpenDBRequest).result;
      const transaction = db.transaction(['messages', 'users'], 'readwrite');
      const messageStore = transaction.objectStore('messages');
      const userStore = transaction.objectStore('users');
      const clearMessageRequest = messageStore.clear();
      const clearUserRequest = userStore.clear();

      clearMessageRequest.onsuccess = function() {
        console.log('Message store cleared');
      };

      clearUserRequest.onsuccess = function() {
        console.log('User store cleared');
      };

      clearMessageRequest.onerror = function(event: Event) {
        console.error('Error clearing message store:', (event.target as IDBRequest).error);
      };

      clearUserRequest.onerror = function(event: Event) {
        console.error('Error clearing user store:', (event.target as IDBRequest).error);
      };
    };

    request.onerror = function(event: Event) {
      console.error('Error opening database:', (event.target as IDBOpenDBRequest).error);
    };
  }

  function copyMessage(content: string): void {
    navigator.clipboard.writeText(content).then(() => {
      console.log('Message copied to clipboard');
      toast.success("Message copied to clipboard");
    }).catch(err => {
      console.error('Could not copy text: ', err);
      toast.error("Failed to copy message");
    });
  }

  function deleteMessage(timestamp: number): void {
    decryptedMessages = decryptedMessages.filter((message: Message) => message.timestamp !== timestamp);
    db.transaction(["messages"], "readwrite").objectStore("messages").delete(timestamp);
    toast.success("Message deleted", {
      description: `Message has been deleted from your chat history.`,
      action: {
        label: "Undo",
        onClick: () => console.info("Undo")
      }
    });
  }

  function forwardMessage(content: string): void {
    console.log('Forwarding message:', content);
    toast.info("Forwarding not implemented yet");
  }

  function setSelectedUser(user: User): void {
    selectedUser = user;
  }

  function toggleLogs(): void {
    showLogs.update(value => !value);
  }
</script>

<svelte:head>
  <title>Chat</title>
</svelte:head>

<div class="grid min-h-screen w-full md:grid-cols-[220px_1fr] lg:grid-cols-[280px_1fr]">
  <Sidebar 
    {users} 
    {selectedUser} 
    {typingUsers} 
    {showLogs} 
    {logEncryptMessages} 
    {logDecryptMessages}
    {setSelectedUser}
  />

  <div class="flex flex-col max-h-screen bg-background">
    <ChatHeader 
      {data} 
      {toggleMode} 
      {toggleLogs} 
      {logout}
      newConversation={newConversation}
    />

    <DotBackground>
      <main class="flex flex-1 h-[calc(100vh-16rem)] gap-4 ">
        <MessageList 
          {decryptedMessages} 
          {data}
          {copyMessage}
          {deleteMessage}
          {forwardMessage}
        />
      </main>
    </DotBackground>

    <BackgroundGradient>
      <MessageInput 
        {handleSubmit} 
        {handleInput} 
        bind:messageText
        {sendImage}
      />
    </BackgroundGradient>
  </div>
</div>
