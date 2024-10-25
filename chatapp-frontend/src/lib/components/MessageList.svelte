<script lang="ts">
  import { fly } from 'svelte/transition';
  import SvelteMarkdown from 'svelte-markdown';
  import * as ContextMenu from "$lib/components/ui/context-menu";
  import { toast } from "svelte-sonner";

  export let decryptedMessages;
  export let data;
  export let copyMessage;
  export let deleteMessage;
  export let forwardMessage;

  let messageElement: HTMLElement | null = null;
</script>

<div class="flex flex-col flex-1 overflow-y-auto overflow-x-hidden">
  <div class="flex flex-col flex-1 gap-1 text-lg border-3">
    {#each decryptedMessages as message}
    <ContextMenu.Root>
      <ContextMenu.Trigger>
        <div class="flex justify-between my-2 relative mx-4" class:flex-row-reverse={message.sender === data.nickname}>
          <div bind:this={messageElement} transition:fly={{ duration: 200, y: 50 }}
            class="max-w-md px-3 py-3 rounded-lg shadow transition-all duration-200 relative group text-white"
            class:bg-neutral-300={message.sender !== data.nickname}
            class:dark:bg-neutral-600={message.sender !== data.nickname}
            class:bg-sky-400={message.sender === data.nickname}
            class:dark:bg-sky-500={message.sender === data.nickname}
          >
            {#if message.type === 'image'}
              <img src={message.image} alt="im" class="rounded-lg" />
            {/if}

            {#if message.type === 'message'}
            <div class="overflow-auto break-words">
              <SvelteMarkdown source={message.content} />
            </div>
            {/if}

            <div class={`text-xs mt-0 ${message.sender === data.nickname ? 'text-right text-gray-200' : 'text-gray-400'}`}>
               {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </div>
          </div>
        </div>
      </ContextMenu.Trigger>
      <ContextMenu.Content>
        <ContextMenu.Item on:click={() => copyMessage(message.content)}>
          Copy
        </ContextMenu.Item>
        <ContextMenu.Item on:click={() => forwardMessage(message.content)}>
          Forward
        </ContextMenu.Item>
        <ContextMenu.Item on:click={() => deleteMessage(message.timestamp)}>
          Delete
        </ContextMenu.Item>
      </ContextMenu.Content>
    </ContextMenu.Root>
    {/each}
  </div>
</div>
