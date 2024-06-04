<script lang="ts">
  import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome'
  import { faArrowAltCircleRight, faPaperclip } from '@fortawesome/free-solid-svg-icons'
  import ThemeSwitcher from '$lib/ThemeSwitcher.svelte';
  import Log from '$lib/Log.svelte';
  import Header from '$lib/Header.svelte';
  import SidebarNew from '$lib/SidebarNew.svelte';
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
  import axios from 'axios';
  import { Button, buttonVariants } from "$lib/components/ui/button";
  import * as Avatar from "$lib/components/ui/avatar";
  import { Input } from "$lib/components/ui/input";
  import { Textarea } from "$lib/components/ui/textarea";
  import * as DropdownMenu from "$lib/components/ui/dropdown-menu";
    import * as Resizable from "$lib/components/ui/resizable";
  import { PaneGroup } from 'paneforge';
  import * as Card from "$lib/components/ui/card";
  import { root } from 'postcss';
  import * as Collapsible from "$lib/components/ui/collapsible";
  import CaretSort from "svelte-radix/CaretSort.svelte";
  import * as Dialog from "$lib/components/ui/dialog";
  import { Label } from "$lib/components/ui/label";
 
  import Paperclip from "lucide-svelte/icons/paperclip";
  import Mic from "lucide-svelte/icons/mic";
  import CornerDownLeft from "lucide-svelte/icons/corner-down-left";

  import * as Tooltip from "$lib/components/ui/tooltip";
  import CircleUser from "lucide-svelte/icons/circle-user";
    import LineChart from "lucide-svelte/icons/line-chart";
    import Package from "lucide-svelte/icons/package";
    import Home from "lucide-svelte/icons/home";
    import ShoppingCart from "lucide-svelte/icons/shopping-cart";
    import Bell from "lucide-svelte/icons/bell";
    import Package2 from "lucide-svelte/icons/package-2";
    import Users from "lucide-svelte/icons/users";
    import { Badge } from "$lib/components/ui/badge";




 import { showLogs } from '$lib/index';
  import { redirect } from '@sveltejs/kit';

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
    type?: string;
    data?: string;
    image?: string;
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
    socket = new WebSocket('ws://192.168.1.10:3000');
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
      messageStore.createIndex("type", "type", { unique: false })
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
        else if(type == 'image'){
          var transaction = db.transaction(["messages"], "readwrite");
          var messageStore = transaction.objectStore("messages");
          let message = data
          console.log(`Message: ${JSON.stringify(message)}`);
          var addImageRequest = messageStore.add(message);
          addImageRequest.onsuccess = function(event) {
            console.log("New image added successfully");
            messagesStore.update((mess) => {
              mess.push(message);
              markedDirty = !markedDirty;
              return mess;
            });
          };
          addImageRequest.onerror = function(event) {
            console.log("Error adding image:", event.target.error);
          };
          } 
          // messageStore.update(messages => [...messages, { type: 'image', data: message.data , sender: data.nickname, receiver: data.recipient, timestamp: Date.now(), encrypted: false}]);

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
            // decryptedMessages = [...decryptedMessages, { type: 'image', data: message.data , sender: data.nickname, receiver: data.recipient, timestamp: Date.now(), encrypted: false}];
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

async function sendImage() {
  const fileInput = document.getElementById('fileInput');
  var file = fileInput.files[0];
  console.log(file.name);
  const reader = new FileReader();
  let patientInfo = null;
  // Check if the file is a DICOM file
  if (file.name.toLowerCase().endsWith('.dcm')) {
    // Send a request to the FastAPI endpoint to convert the DICOM file to JPEG
    const formData = new FormData();
    formData.append('file', file);
    const response = await axios.post('http://localhost:8001/convert/', formData, {
      responseType: 'blob', // Tell axios to expect an image blob as the response
    });

    // Create a new File object from the response
    const blob = new Blob([response.data], { type: 'image/jpeg' });
    const convertedFile = new File([blob], file.name.replace('.dcm', '.jpg'), { type: 'image/jpeg' });

    // Replace the original file with the converted file
    var file = convertedFile;
  

  // Send a request to the FastAPI endpoint to extract patient info from the DICOM file
  const patientInfoResponse = await axios.post('http://localhost:8001/extract-patient-info/', formData);

  // Store the patient info in a variable
  patientInfo = patientInfoResponse.data.patient_info;

  }

  reader.onload = async (event) => {
    const dataUrl = event.target.result;
    const message = {
      type: 'image',
      data: {
        type: 'image',
        image: dataUrl,
        sender: data.nickname,
        receiver: selectedUser?.nickname,
        timestamp: Date.now(),
        encrypted: false}
    };

        // Assume `socket` is the WebSocket connection to the server
        socket.send(JSON.stringify(message));

        if (patientInfo) {
      // Send a request to the FastAPI endpoint to get the patient summary
      const patientSummaryResponse = await axios.post('http://localhost:8001/get-patient-summary/', { patient_info: patientInfo });

      // Store the patient summary in a variable
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

      socket.send(JSON.stringify(summaryMessage));
    }
      fileInput.value = '';
  };

  reader.readAsDataURL(file);
}

function logout() {
// Clear chat history
messages = []; // Replace this with the actual code to clear your chat history

// Clear all cookies
var cookies = document.cookie.split(";");

for (var i = 0; i < cookies.length; i++) {
  var cookie = cookies[i];
  var eqPos = cookie.indexOf("=");
  var name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
  document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT";
}

// Clear IndexedDB
clearIndexedDB();

// Redirect to login page
window.location.href = '/login'; // Replace this with the actual path to your login page
}
function clearIndexedDB() {
  const request = indexedDB.open('messages', 2);

  request.onsuccess = function(event) {
    const db = event.target.result;
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

    clearMessageRequest.onerror = function(event) {
      console.error('Error clearing message store:', event.target.error);
    };

    clearUserRequest.onerror = function(event) {
      console.error('Error clearing user store:', event.target.error);
    };
  };

  request.onerror = function(event) {
    console.error('Error opening database:', event.target.error);
  };
}
</script>

<svelte:head>
  <title>Chat</title>
</svelte:head>

<div class="flex flex-col h-screen">
  <header>
  <Header data={data} logout={logout} callback={newConversation}/>
  </header>
  <Resizable.PaneGroup direction= "horizontal" class="min-h-[200px] ">
  <div class="flex flex-row flex-1 gap-2 overflow-auto ">
    <Resizable.Pane defaultSize={25} class="flex flex-col  p-2 min-w-[200px] ">
    <!-- <div class="flex flex-col border-r-4 dark:border-neutral-950 pr-2"> -->
      
      <div class="flex flex-col flex-1 mt-2">
        {#key markedDirty}
          {#each users as user}
            <button
              class="flex flex-row gap-5  items-center p-2 rounded-lg mx-2"
              class:bg-sky-500={selectedUser?.nickname === user.nickname}
              class:dark:bg-sky-600={selectedUser?.nickname === user.nickname}
              class:odd:dark:bg-neutral-900={selectedUser?.nickname !== user.nickname}
              class:even:dark:bg-neutral-800={selectedUser?.nickname !== user.nickname}
              class:odd:bg-neutral-100={selectedUser?.nickname !== user.nickname}
              class:even:bg-neutral-200={selectedUser?.nickname !== user.nickname}
              class:hover:cursor-default={selectedUser?.nickname === user.nickname}
              on:click={() => selectedUser = user}
              >
              <Avatar.Root>
                <Avatar.Image src={`https://ui-avatars.com/api/?name=${user.nickname}&background=random`} alt="User avatar" />
                <Avatar.Fallback>"User avatar"</Avatar.Fallback>
              </Avatar.Root>

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
      {#if $showLogs}
      <Log logTitle="Encryption Log" logElement= {encryptLogElement} logMessages = {logEncryptMessages} />        
      <Log logTitle="Decryption Log" logElement= {decryptLogElement} logMessages = {logDecryptMessages} />
      {/if}
      <Button class="p-4 mt-5 mb-3" on:click={() => showNewModal = true}>New Chat</Button>

      <!-- <div class="grid min-h-screen w-full ">
        <div class="hidden border-r  md:block">
          <div class="flex h-full max-h-screen flex-col gap-2">
            <div class="flex h-14 items-center border-b px-4 lg:h-[60px] lg:px-6">
              <a href="/" class="flex items-center gap-2 font-semibold">
                <Package2 class="h-6 w-6" />
                <span>Quantum Chat </span>
              </a>
              <Button variant="outline" size="icon" class="ml-auto h-8 w-8">
                <Bell class="h-4 w-4" />
                <span class="sr-only">Toggle notifications</span>
              </Button>
            </div>
            <div class="flex-1">
              <nav class="grid items-start px-2 text-sm font-medium lg:px-4">
                <a href="##" class="flex items-center gap-3 rounded-lg px-3 py-2 text-muted-foreground transition-all hover:text-primary">
                  <Home class="h-4 w-4" />
                  Users
                </a>
                {#key markedDirty}
                  {#each users as user}
                    <button
                      class="flex items-center gap-3 rounded-lg px-3 py-2 text-muted-foreground transition-all hover:text-primary"
                      class:bg-muted={selectedUser?.nickname === user.nickname}
                      class:dark:bg-muted={selectedUser?.nickname === user.nickname}
                      class:odd:dark:bg-neutral-900={selectedUser?.nickname !== user.nickname}
                      class:even:dark:bg-neutral-800={selectedUser?.nickname !== user.nickname}
                      class:odd:bg-neutral-100={selectedUser?.nickname !== user.nickname}
                      class:even:bg-neutral-200={selectedUser?.nickname !== user.nickname}
                      class:hover:cursor-default={selectedUser?.nickname === user.nickname}
                      on:click={() => selectedUser = user}
                      >
                      <Avatar.Root>
                        <Avatar.Image src={`https://ui-avatars.com/api/?name=${user.nickname}&background=random`} alt="User avatar" />
                        <Avatar.Fallback>"User avatar"</Avatar.Fallback>
                      </Avatar.Root>

                      {user.nickname}
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
              </nav>
            </div>
            <div class="mt-auto p-4">
              <Card.Root>
                <Card.Header class="p-2 pt-0 md:p-4">
                  <Card.Title>Logs</Card.Title>
                  <Card.Description>
                    View encryption and decryption logs.
                  </Card.Description>
                </Card.Header>
                <Card.Content class="p-2 pt-0 md:p-4 md:pt-0">
                  {#if $showLogs}
                  <Log logTitle="Encryption Log" logElement= {encryptLogElement} logMessages = {logEncryptMessages} />        
                  <Log logTitle="Decryption Log" logElement= {decryptLogElement} logMessages = {logDecryptMessages} />
                  {/if}
                </Card.Content>
              </Card.Root>
            </div>
          </div>
        </div>
      </div> -->

      
   </Resizable.Pane>
    <Resizable.Handle withHandle />
    <Resizable.Pane defaultSize={75} class="flex flex-col flex-1">
    <div class="flex flex-col flex-1 overflow-scroll">
      <div class="flex flex-col flex-1 overflow-scroll gap-1 text-lg  border-3">
        {#each decryptedMessages as message}
        <div class="flex justify-between mb-4 relative mx-4" class:flex-row-reverse={message.sender === data.nickname}>
          <div bind:this={messageElement} transition:fly={{ duration: 200, y: 50 }}
            class="max-w-md px-3 py-3 rounded-lg shadow transition-all duration-200 relative group"
            class:bg-neutral-300={message.sender !== data.nickname}
            class:dark:bg-neutral-600={message.sender !== data.nickname}
            class:bg-sky-400={message.sender === data.nickname}
            class:dark:bg-sky-500={message.sender === data.nickname}
          >

            {#if message.type === 'image'}

              <img src= {message.image} alt="Image" class="rounded-lg" />
            {/if}

            {#if message.type === 'message'}
            <div class = "overflow-auto break-words">
              <SvelteMarkdown source={message.content} />
            </div>
            {/if}

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

      
      <form class="relative overflow-hidden rounded-lg border bg-background focus-within:ring-1 focus-within:ring-ring" on:submit|preventDefault={handleSubmit}>
        <Label for="message" class="sr-only">Message</Label>
        <Textarea
          id="message"
          placeholder="Type your message here..."
          class="min-h-12 resize-none border-0 p-3 shadow-none focus-visible:ring-0"
          on:keydown={handleKeyDown}
          on:input={handleInput}
          bind:value={messageText}
        />
        <div class="flex items-center p-3 pt-0">
          <Tooltip.Root>
            <Tooltip.Trigger asChild let:builder>
              <input type="file" id="fileInput" class="hidden" on:change={sendImage} />
              <Button builders={[builder]} variant="ghost" size="icon" on:click={() => document.getElementById('fileInput').click()}>
                <Paperclip class="size-4" />
                <span class="sr-only">Attach file</span>
              </Button>
            </Tooltip.Trigger>
            <Tooltip.Content side="top">Attach File</Tooltip.Content>
          </Tooltip.Root>
          <Tooltip.Root>
            <Tooltip.Trigger asChild>
              <Button variant="ghost" size="icon">
                <Mic class="size-4" />
                <span class="sr-only">Use Microphone</span>
              </Button>
            </Tooltip.Trigger>
            <Tooltip.Content side="top">Use Microphone</Tooltip.Content>
          </Tooltip.Root>
          <Button type="submit" size="sm" class="ml-auto gap-1.5">
            Send Message
            <CornerDownLeft class="size-3.5" />
          </Button>
        </div>
      </form>
      
  
    </div>
  </Resizable.Pane>
  <!-- </div> -->
</Resizable.PaneGroup>
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