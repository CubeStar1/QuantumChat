<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import { Textarea } from "$lib/components/ui/textarea";
  import { Label } from "$lib/components/ui/label";
  import * as Tooltip from "$lib/components/ui/tooltip";
  import Paperclip from "lucide-svelte/icons/paperclip";
  import Mic from "lucide-svelte/icons/mic";
  import CornerDownLeft from "lucide-svelte/icons/corner-down-left";

  export let handleSubmit: () => void;
  export let handleInput: (event: InputEvent) => void;
  export let messageText: string;
  export let sendImage: (event: Event) => void;

  function handleKeyDown(event: KeyboardEvent): void {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSubmit();
    }
  }
</script>

<form class="relative rounded-3xl border bg-neutral-900 focus-within:ring-1 focus-within:ring-ring" on:submit|preventDefault={handleSubmit}>
  <Label for="message" class="sr-only">Message</Label>
  <Textarea
    id="message"
    placeholder="Type your message here..."
    class="min-h-12 resize-none rounded-3xl border-0 bg-neutral-900 p-4 shadow-none focus-visible:ring-0"
    on:keydown={handleKeyDown}
    on:input={handleInput}
    bind:value={messageText}
  />
  <div class="flex items-center p-3 pt-0">
    <Tooltip.Root>
      <Tooltip.Trigger asChild let:builder>
        <input type="file" id="fileInput" class="hidden" on:change={sendImage} />
        <Button builders={[builder]} variant="ghost" size="icon" on:click={() => document.getElementById('fileInput')?.click()}>
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
