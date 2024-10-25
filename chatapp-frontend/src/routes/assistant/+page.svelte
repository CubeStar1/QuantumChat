<script>
    import axios from 'axios';
    import { writable } from 'svelte/store';
    import { onMount } from 'svelte';
    import { fly } from 'svelte/transition';
  
    // Define writable store for chat history
    let chatHistory = writable([
      { role: 'system', content: 'You are an intelligent assistant specialized in medical applications. Always provide well-reasoned and helpful answers, and clarify any medical information.' }
    ]);
  
    // Define writable store for message text
    let messageText = writable('');
  
    // Function to send message
    async function sendMessage() {
      // Get current message text
      const text = $messageText;
  
      // Clear message text input
      messageText.set('');
  
      // Add user message to chat history
      chatHistory.update(history => [...history, { role: 'user', content: text }]);
  
      try {
        // Send message to server
        const response = await axios.post('http://localhost:8003/chatgemini/', {
          messages: $chatHistory
        });
  
        // Add server response to chat history
        chatHistory.update(history => [...history, response.data.message]);
      } catch (error) {
        console.error('Error sending message:', error);
      }
    }
  
    // Function to handle form submission
    function handleSubmit(event) {
      event.preventDefault();
      if ($messageText.trim()) {
        sendMessage();
      }
    }
  
    // Function to handle key down events
    function handleKeyDown(event) {
      if (event.key === 'Enter') {
        handleSubmit(event);
      }
    }
  </script>
  
  <div class="grid min-h-screen w-full md:grid-cols-[220px_1fr] lg:grid-cols-[280px_1fr]">
    <div class="hidden max-h-screen border-r bg-muted/40 md:block">
      <div class="flex h-full max-h-screen flex-col gap-2">
        <div class="flex h-14 bg-gradient-to-r from-red-500 to-orange-400 items-center border-b px-4 lg:h-[60px] lg:px-6">
          <a href="/" class="flex items-center gap-2 font-semibold">
            <div>
              <img src="./src/qclogo.png" alt="Quantum Chat logo" class="w-12" />
            </div>
            <span class="text-xl">Quantum Chat</span>
          </a>
        </div>
        <div class="flex-1">
          <nav class="grid items-start px-2 text-sm font-medium lg:px-4">
            <a href="##" class="flex items-center gap-3 rounded-lg px-3 py-2 text-muted-foreground transition-all hover:text-primary">
              <span class="h-4 w-4">🏠</span>
              Home
            </a>
          </nav>
        </div>
      </div>
    </div>
    <div class="flex flex-col max-h-screen">
      <header class="flex h-14 items-center gap-4 border-b bg-gradient-to-r from-red-500 to-orange-400 p-4 lg:h-[60px] lg:px-6">
        <div class="w-full flex-1">
          <form>
            <div class="relative">
              <input
                type="search"
                placeholder="Search messages..."
                class="w-full appearance-none bg-background pl-8 shadow-none md:w-2/3 lg:w-1/3"
              />
            </div>
          </form>
        </div>
        <button on:click={() => document.body.classList.toggle('dark')} class="ml-4">
          🌞 / 🌜
        </button>
      </header>
      <main class="flex flex-1 flex-col overflow-y-auto p-4 gap-2">
        {#each $chatHistory as message (message.content)}
          <div class="my-2" in:fly={{ duration: 200, y: 50 }}>
            <div class={`max-w-md px-3 py-3 rounded-lg shadow transition-all duration-200 relative group ${message.role === 'user' ? 'bg-neutral-300 text-right' : 'bg-sky-400 text-left'}`}>
              <div class="overflow-auto break-words">
                {message.content}
              </div>
            </div>
          </div>
        {/each}
      </main>
      <form class="flex items-center p-4" on:submit|preventDefault={handleSubmit}>
        <textarea
          class="flex-1 rounded p-2"
          bind:value={$messageText}
          on:keydown={handleKeyDown}
          placeholder="Type your message here..."
        ></textarea>
        <button type="submit" class="ml-2 px-4 py-2 bg-blue-500 text-white rounded">Send</button>
      </form>
    </div>
  </div>
  
  <style>
        .bg-muted {
      background-color: #f1f5f9;
    }
    .text-muted-foreground {
      color: #64748b;
    }
    .bg-background {
      background-color: white;
    }
  </style>
  