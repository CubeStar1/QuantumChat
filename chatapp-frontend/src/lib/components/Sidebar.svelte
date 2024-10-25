<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import * as Avatar from "$lib/components/ui/avatar";
  import * as Card from "$lib/components/ui/card";
  import Log from '$lib/Log.svelte';
  import BackgroundGradient from '$lib/components/ui/BackgroundGradient/BackgroundGradient.svelte';
  import Home from "lucide-svelte/icons/home";

  export let users;
  export let selectedUser;
  export let typingUsers;
  export let showLogs;
  export let logEncryptMessages;
  export let logDecryptMessages;
  export let setSelectedUser;

  let markedDirty = false;
</script>

<div class="hidden max-h-screen border-r-4 border-foreground-muted bg-background md:block">
  <div class="flex h-full max-h-screen flex-col gap-2">
    <div class="flex min-h-24 bg-gradient-to-r from-orange-400 to-red-500 items-center border-b px-4 lg:min-h-24 lg:px-6">
      <a href="/" class="flex items-center gap-2 font-semibold">
        <div>
          <img src="src/public/images/qclogo.png" alt="Quantum Chat logo" class="w-14" />
        </div>
        <span class="text-3xl">Quantum Chat</span>
      </a>
    </div>
    <BackgroundGradient>
      <div class="flex-1 bg-neutral-900 rounded-3xl p-3">
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
                class:odd:dark:bg-muted-900={selectedUser?.nickname !== user.nickname}
                class:even:dark:bg-muted-800={selectedUser?.nickname !== user.nickname}
                class:odd:bg-muted-100={selectedUser?.nickname !== user.nickname}
                class:even:bg-muted-200={selectedUser?.nickname !== user.nickname}
                class:hover:cursor-default={selectedUser?.nickname === user.nickname}
                on:click={() => setSelectedUser(user)}
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
    </BackgroundGradient>
    <div class="mt-auto p-0.5">
      <Card.Root class="rounded-2xl">
        <Card.Header class="p-2 pt-0 md:p-4">
          <Card.Title>Logs</Card.Title>
          <Card.Description>
            View encryption and decryption logs.
          </Card.Description>
        </Card.Header>
        <Card.Content class="p-2 pt-0 md:p-4 md:pt-0">
          {#if $showLogs}
          <Log logTitle="Encryption Log" logMessages={logEncryptMessages} logElement={logEncryptMessages}/>        
          <Log logTitle="Decryption Log" logMessages={logDecryptMessages} logElement={logDecryptMessages}/>
          {/if}
        </Card.Content>
      </Card.Root>
    </div>
  </div>
</div>

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
