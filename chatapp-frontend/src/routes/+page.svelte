<script lang="ts">
  import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome'
  import { faArrowAltCircleRight } from '@fortawesome/free-solid-svg-icons'
  import ThemeSwitcher from '$lib/ThemeSwitcher.svelte';
  import SvelteMarkdown from 'svelte-markdown'
  import autosize from 'svelte-autosize';
  import NewChat from "$lib/NewChat.svelte";
  import { browser } from "$app/environment";
  import { onMount, afterUpdate } from "svelte";
  import * as aesjs from 'aes-js';
  import { writable } from "svelte/store";
  import forge from 'node-forge';
  import { fade, slide, fly } from 'svelte/transition';
  import { cubicOut } from 'svelte/easing';

  let messageElement : HTMLElement | null = null;

  let typing = false;
  let typingUsers :string[] = [];
  let typingTimeout;
  let messageText: string;
  let showNewModal: boolean = false;

  afterUpdate(() => {
    if (messageElement) {
      messageElement.scrollIntoView({ behavior: 'smooth' });
    }
  });


  function handleKeyDown(event: KeyboardEvent): void {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSubmit();
    }
  }

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
  }

  let messagesStore = writable<Message[]>([]);
  let users: User[] = [];
  let messages: Message[] = [];
  let selectedUser: User | null = null;
  $: relevantMessages = selectedUser ? $messagesStore.filter(message => message.sender === selectedUser!.nickname || message.receiver === selectedUser!.nickname) : [];
  $: sortedMessages = relevantMessages.sort((a, b) => a.timestamp - b.timestamp);
  $: decryptedMessages = sortedMessages.map(message => decryptMessage(message, selectedUser));

  let logEncryptMessages = '';
  let logDecryptMessages = '';

  let isEncryptLogExpanded = false;
  let isDecryptLogExpanded = false;

  let encryptLogElement : HTMLElement ;
  let decryptLogElement : HTMLElement ;

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
      encrypted: false,
      content: decryptedText,
      timestamp: message.timestamp,
      sender: message.sender,
      receiver: message.receiver
    }
  }
  return message;
}


  async function generateKeyPair() {
    let keyPair = forge.pki.rsa.generateKeyPair(2048);
    let publicKey = forge.pki.publicKeyToPem(keyPair.publicKey);
    let privateKey = forge.pki.privateKeyToPem(keyPair.privateKey);
    return {
      publicKey: publicKey,
      privateKey: privateKey
    };
  }


  async function decryptSymmetricKey(encryptedKey: string, privateKeyPem: string) {
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
    }
  }


  let db;
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
    return;
  }
  
  export let data: { nickname: string };

  let markedDirty = false;
  
  if (browser) {
    onMount(async () => {
      keyPair = await generateKeyPair();

      // let storedKeyPair = sessionStorage.getItem('keyPair');

      // if (storedKeyPair !== null) {
      //   keyPair = JSON.parse(storedKeyPair);
      // } else {
      //   keyPair = await generateKeyPair();
      //   sessionStorage.setItem('keyPair', JSON.stringify(keyPair));
      // }
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
      
      request.onupgradeneeded = function() {
        const db = request.result;
        var messageStore = db.createObjectStore("messages", { keyPath: "timestamp" });
        messageStore.createIndex("sender", "sender", { unique: false });
        messageStore.createIndex("receiver", "receiver", { unique: false });
        messageStore.createIndex("encrypted", "encrypted", { unique: false });
        messageStore.createIndex("content", "content", { unique: false });
        var userStore = db.createObjectStore("users", { keyPath: "nickname" });
        userStore.createIndex("key", "key", { unique: false });
      };

      request.onsuccess = function() {
        db = request.result;
        
        var transaction = db.transaction(["users"], "readonly");
        var userStore = transaction.objectStore("users");
        var getAllUsersRequest = userStore.getAll();
        getAllUsersRequest.onsuccess = function(event) {
          var usersRes = event.target?.result;
          users = usersRes ?? [];
          if (users.length > 0) {
            selectedUser = users[0];
          }
          console.log("Users retrieved successfully:", users);
        };

        var transaction2 = db.transaction(["messages"], "readonly");
        var messageStore = transaction2.objectStore("messages");
        var getAllMessagesRequest = messageStore.getAll();
        getAllMessagesRequest.onsuccess = function(event) {
          var messagesRes = event.target?.result;
          messagesStore.set(messagesRes ?? []);
          console.log("Messages retrieved successfully:", messagesStore);
        };
      };

      socket.onmessage = async (event) => {
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
          addRequest.onsuccess = function(event) {
            console.log("New user added successfully");
            users.push(user);
            window.location.reload();
          };
          addRequest.onerror = function(event) {
            console.error("Error adding user:", event.target.error);
          };

            console.log('Users:', users)
          } 
          else if (type === 'typing') {
              if (data.typing && !typingUsers.includes(data.user)) {
                typingUsers = [...typingUsers, data.user];
              } else if (!data.typing) {
                typingUsers = typingUsers.filter(u => u !== data.user);
              }
            }
          
          else if (type === 'message') {
            var transaction = db.transaction(["messages"], "readwrite");
            var messageStore = transaction.objectStore("messages");
            let message = data.message;
            console.log(`Message: ${JSON.stringify(message)}`);
            var addRequest = messageStore.add(message);
            addRequest.onsuccess = function(event) {
              console.log("New message added successfully");
              messagesStore.update((mess) => {
                mess.push(message);
                markedDirty = !markedDirty;
                return mess;
              });
            };
            addRequest.onerror = function(event) {
              console.error("Error adding message:", event.target.error);
            };
          }
      };
      });
    }

    function newConversation(arg0: string) {
      console.log('New conversation:', arg0);
      socket.send(JSON.stringify({
        type: 'conversation',
        data: {
          recipientNick: arg0
        }
    }));
  }


  function handleInput() {
    clearTimeout(typingTimeout);
    if (!typing) {
      typing = true;
      socket.send(JSON.stringify({ type: 'typing', data: {user: data.nickname, typing: true }})); 
    }
    typingTimeout = setTimeout(stopTyping, 1000);
  }

  function stopTyping() {
    typing = false;
    socket.send(JSON.stringify({ type: 'typing', data: {user: data.nickname, typing: false }}));
  }

</script>

<svelte:head>
  <title>Chat</title>
</svelte:head>

<div class="flex flex-col mx-auto p-2 h-screen">
  <div class="flex flex-row justify-between bg-gradient-to-r from-pink-500 to-purple-600 p-4 rounded-lg">
    <h1 class="text-4xl font-bold text-white">Quantum Chat</h1>
    <div class="flex items-center gap-2">
      <div class="bg-white text-purple-600 p-2 rounded-md text-sm">
        Logged in as {data.nickname}
      </div>
    <ThemeSwitcher />
  </div>
</div>

  <div class="flex flex-row flex-1 gap-2 overflow-auto h-screen">

    <div class="flex flex-col border-r-4 dark:border-neutral-950 pr-2">
      <div class="flex flex-col overflow-auto flex-1 mt-5">
        {#key markedDirty}
          {#each users as user}
            <button
              class="flex flex-row gap-5 sm:min-w-72 items-center p-2 rounded-md"
              class:bg-sky-500={selectedUser?.nickname === user.nickname}
              class:dark:bg-sky-600={selectedUser?.nickname === user.nickname}
              class:odd:dark:bg-neutral-900={selectedUser?.nickname !== user.nickname}
              class:even:dark:bg-neutral-800={selectedUser?.nickname !== user.nickname}
              class:odd:bg-neutral-100={selectedUser?.nickname !== user.nickname}
              class:even:bg-neutral-200={selectedUser?.nickname !== user.nickname}
              class:hover:cursor-default={selectedUser?.nickname === user.nickname}
              on:click={() => selectedUser = user}
              >
              <img src={`https://ui-avatars.com/api/?name=${user.nickname}&background=random`} alt="User avatar" class="w-10 h-10 rounded-full" />
              <div class="text-xl">{user.nickname}</div>
              {#if typingUsers.includes(user.nickname)}
              <div class="flex space-x-1">
                <div class="typing-indicator"></div>
                <div class="typing-indicator"></div>
                <div class="typing-indicator"></div>
                <div class="text-sm text-gray-300">typing...</div>
              </div>
            {/if}
            </button>
          {/each}
        {/key}
      </div>
        
        <div class="mt-5 p-3 border rounded-2xl bg-neutral-100 dark:bg-neutral-800 hover:bg-neutral-200 dark:hover:bg-neutral-700 max-w-72 min-w-72 mx-auto max-h-60 overflow-auto">
          <div class="flex justify-center">
            <button on:click={() => isEncryptLogExpanded = !isEncryptLogExpanded} class="text-sm mb-2 ">Encryption Log</button>
          </div>
          {#if isEncryptLogExpanded}
            <div class="flex ">
              <pre transition:slide="{{delay: 200, duration: 250, easing: cubicOut}}" bind:this={encryptLogElement} class="whitespace-pre-wrap">{logEncryptMessages}</pre>
            </div>
          {/if}
        </div>

        
        <div class="mt-5 p-3 border rounded-2xl bg-neutral-100 dark:bg-neutral-800 hover:bg-neutral-200 dark:hover:bg-neutral-700 max-w-72 min-w-72 mx-auto max-h-60 overflow-auto">
          <div class="flex justify-center">
            <button on:click={() => isDecryptLogExpanded = !isDecryptLogExpanded} class="text-sm mb-2 ">Decryption Log</button>
          </div>
          {#if isDecryptLogExpanded}
            <div class="flex">
              <pre transition:slide="{{delay: 200, duration: 250, easing: cubicOut}}" bind:this={decryptLogElement} class="whitespace-pre-wrap">{logDecryptMessages}</pre>
            </div>
          {/if}
        </div>
      <button class="p-4 mt-5 mb-3 bg-sky-500 dark:bg-sky-600 hover:bg-sky-600 dark:hover:bg-sky-700 transition rounded-2xl" on:click={() => showNewModal = true}
        >New Chat</button>
    </div>
    
    <div class="flex flex-col flex-1 overflow-scroll">
      <div class="flex flex-col flex-1 overflow-scroll gap-1 text-lg mt-5">
        {#each decryptedMessages as message}
        <div class="flex justify-between mb-4 relative" class:flex-row-reverse={message.sender === data.nickname}>
          <div bind:this={messageElement} transition:fly={{ duration: 200, y: 50 }}
            class="max-w-md px-3 py-1 rounded-lg shadow transition-all duration-200 relative group"
            class:bg-neutral-300={message.sender !== data.nickname}
            class:dark:bg-neutral-600={message.sender !== data.nickname}
            class:bg-sky-400={message.sender === data.nickname}
            class:dark:bg-sky-500={message.sender === data.nickname}
          >
            <SvelteMarkdown source={message.content} />
            <div 
              class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 text-xs rounded bg-gray-700 text-white opacity-0 group-hover:opacity-100 transition-opacity duration-200"
            >
              This message is encrypted using QKD
            </div>
            <div class={`text-xs mt-0 ${message.sender === data.nickname ? 'text-right text-gray-200' : 'text-gray-400'}`}> <!-- Add this div for the timestamp -->
              {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </div>
          </div>
        </div>
      {/each}
      </div>

      <form class="flex flex-row items-end " on:submit|preventDefault={handleSubmit}>
        <textarea class="max-h-32 flex-1 dark:bg-neutral-900 dark:border-neutral-700 border border-neutral-300 rounded-md w-full my-4 text-xl p-2"
          on:keydown={handleKeyDown}
          on:input={handleInput}
          rows="1"
          placeholder="Send a message..."
          use:autosize
          bind:value={messageText}/>
        <button
          type="submit"
          class="rounded-3xl ml-2 my-4 transition text-5xl text-sky-500 hover:text-sky-600"
        >
          <FontAwesomeIcon icon={faArrowAltCircleRight} /> 
        </button>
      </form>
    </div>
  </div>
</div>

<NewChat bind:show={showNewModal} callback={newConversation} />

<style>
  .typing-indicator {
    display: inline-block;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background-color: #cec7c7;

    animation: typing 1.2s infinite;
    animation-delay: 0.0s;
  }

  .typing-indicator:nth-child(2) {
    animation-delay: 0.2s;
  }

  .typing-indicator:nth-child(3) {
    animation-delay: 0.4s;
  }

  @keyframes typing {
    0% { transform: translateY(0); }
    50% { transform: translateY(-5px); }
    100% { transform: translateY(0); }
  }
</style>