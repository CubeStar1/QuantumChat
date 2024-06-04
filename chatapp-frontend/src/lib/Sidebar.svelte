<!-- Sidebar.svelte -->
<script>
    import { Button } from "$lib/components/ui/button";
    import * as Avatar from "$lib/components/ui/avatar";
    import * as Resizable from "$lib/components/ui/resizable";
    import Log from '$lib/Log.svelte';
    export let users;
    export let selectedUser;
    export let typingUsers;
    export let encryptLogElement;
    export let logEncryptMessages;
    export let decryptLogElement;
    export let logDecryptMessages;
    export let showNewModal;
    export let markedDirty;
  </script>
  
  <Resizable.Pane defaultSize={25} class="flex flex-col rounded-lg border p-2 min-w-[200px]">
    <div class="flex flex-col flex-1 mt-5">
      {#key markedDirty}
        {#each users as user}
          <button
            class="flex flex-row gap-5  items-center p-2 rounded-md"
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
      
    <Log logTitle="Encryption Log" logElement={encryptLogElement} logMessages={logEncryptMessages} />        
    <Log logTitle="Decryption Log" logElement={decryptLogElement} logMessages={logDecryptMessages} />
  
    <Button class="p-4 mt-5 mb-3" on:click={() => showNewModal = true}>New Chat</Button>
  </Resizable.Pane>

