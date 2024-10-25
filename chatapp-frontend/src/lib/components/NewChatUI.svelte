<script lang="ts">
import { Button, buttonVariants } from "$lib/components/ui/button";
import * as Menubar from "$lib/components/ui/menubar";
import { toggleMode } from "mode-watcher";
import * as DropdownMenu from "$lib/components/ui/dropdown-menu";
import ThemeSwitcher from '$lib/components/ThemeSwitcher.svelte';
import * as Dialog from "$lib/components/ui/dialog";
import { Input } from "$lib/components/ui/input";
import { Label } from "$lib/components/ui/label";
import { toast } from "svelte-sonner";
import {showLogs} from '$lib/index';
	import MultiStepLoader from '$lib/components/ui/MultiStepLoader/MultiStepLoader.svelte';

	let loading = false;
  const loadingStates = [
		{
			text: 'Generating Bell Pairs'
		},
		{
			text: 'Creating Quantum Channel'
		},
		{
			text: 'Sending Qubits'
		},
		{
			text: 'Receiving Qubits'
		},
		{
			text: 'Decoding Qubits'
		},
		{
			text: 'Sending Classical Bits'
		},
		{
			text: 'Receiving Classical Bits'
		},
		{
			text: 'Generating Shared Key'
		}
	];

export let callback: (arg0: string) => void;
let nickname = "";

function handleSubmit() {
callback(nickname);
toast.success("Looking for user...", {
    description: `Searching for user with nickname ${nickname}`,
    action: {
    label: "Undo",
    onClick: () => console.info("Undo")
    }
});
}



</script>

<Dialog.Root>
  <MultiStepLoader {loadingStates} {loading} duration={2000} loop={false} />
    <Dialog.Trigger class={buttonVariants({ variant: "outline" })}
      >New Chat </Dialog.Trigger
    >
    <Dialog.Content class="sm:max-w-[425px]">
      <Dialog.Header>
        <Dialog.Title>New  Chat</Dialog.Title>
        <Dialog.Description>
            Enter the nickname of the user you want to chat with.
        </Dialog.Description>
      </Dialog.Header>
      <div class="grid gap-4 py-4">
        <div class="grid grid-cols-4 items-center gap-4">
          <Label for="name" class="text-right">Name</Label>
          <Input id="name" placeholder="Name" class="col-span-3" />
        </div>
        <div class="grid grid-cols-4 items-center gap-4">
          <Label for="nickname" class="text-right">Username</Label>
          <Input id="nickname" placeholder="Nickname" bind:value={nickname}  class="col-span-3" />
        </div>
      </div>
      <Dialog.Footer>
        <Button type="submit" on:click={handleSubmit}>Submit</Button>
        <Button type="button" on:click={() => (loading = true)}>Start QKD</Button>
        
      </Dialog.Footer>
    </Dialog.Content>
    {#if loading}
		<button
			class="fixed right-4 top-4 z-[120] text-black dark:text-white"
			on:click={() => (loading = false)}
		>
    <Button type="submit" on:click={handleSubmit}>Continue</Button>
		</button>
	{/if}
  </Dialog.Root>