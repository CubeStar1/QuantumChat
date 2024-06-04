<!-- Header.svelte -->
<script lang="ts">
    import { Button, buttonVariants } from "$lib/components/ui/button";
    import * as Menubar from "$lib/components/ui/menubar";
    import { toggleMode } from "mode-watcher";
    import * as DropdownMenu from "$lib/components/ui/dropdown-menu";
    import ThemeSwitcher from '$lib/ThemeSwitcher.svelte';
    import * as Dialog from "$lib/components/ui/dialog";
    import { Input } from "$lib/components/ui/input";
    import { Label } from "$lib/components/ui/label";
    import { toast } from "svelte-sonner";
    import {showLogs} from '$lib/index';
    export let data;
    export let logout;
    export let callback: (arg0: string) => void;
    let nickname = "";
    import Sun from "svelte-radix/Sun.svelte";
  import Moon from "svelte-radix/Moon.svelte";
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


  function toggleLogs() {
    showLogs.update(value => !value);
  }

  </script>
  
  <div class="flex flex-row justify-start bg-gradient-to-r from-red-500 to-orange-400 p-4 ">
    <div>
      <img src="./src/qclogo.png" alt="Quantum Chat logo" class="w-12" />
    </div>
    <h1 class="text-4xl font-bold text-white">Quantum Chat</h1>
    <div class="flex items-center gap-2 ml-auto">

        <Menubar.Root>
            <Menubar.Menu>
              <Menubar.Trigger>Settings</Menubar.Trigger>
              <Menubar.Content>
                <Menubar.Item>Logged in as {data.nickname}</Menubar.Item>
                <Menubar.Separator />
                <Menubar.Item>QKD Protocol: Bell State</Menubar.Item>
                <Menubar.Item href = '/about' >About</Menubar.Item>
                <Menubar.Item on:click={toggleLogs}>DevTools</Menubar.Item>
                <Menubar.Item on:click={logout}>Logout</Menubar.Item>
              </Menubar.Content>
            </Menubar.Menu>
          
      <Dialog.Root>
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
            
          </Dialog.Footer>
        </Dialog.Content>
      </Dialog.Root>

      <Button on:click={toggleMode} variant="outline" size="icon">
        <Sun
          class="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0"
        />
        <Moon
          class="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100"
        />
        <span class="sr-only">Toggle theme</span>
      </Button>
      </Menubar.Root>

    </div>
  </div>