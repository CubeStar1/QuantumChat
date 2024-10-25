<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import * as Sheet from "$lib/components/ui/sheet";
  import * as DropdownMenu from "$lib/components/ui/dropdown-menu";
  import Menu from "lucide-svelte/icons/menu";
  import Sun from "svelte-radix/Sun.svelte";
  import Moon from "svelte-radix/Moon.svelte";
  import CircleUser from "lucide-svelte/icons/circle-user";
  import NewChatUi from '$lib/components/NewChatUI.svelte';
  import DropDown from '$lib/components/DropDown.svelte';
  import { selectedProtocol } from '$lib/index';

  export let data;
  export let toggleMode;
  export let toggleLogs;
  export let logout;
  export let newConversation;

  let protocol;
  selectedProtocol.subscribe(value => {
    protocol = value;
  });
</script>

<header class="flex min-h-24 items-center gap-4 border-b bg-gradient-to-r from-red-500 to-orange-400 p-4 lg:min-h-24 lg:px-6">
  <Sheet.Root>
    <Sheet.Trigger asChild let:builder>
      <Button
        variant="outline"
        size="icon"
        class="shrink-0 md:hidden"
        builders={[builder]}
      >
        <Menu class="h-5 w-5" />
        <span class="sr-only">Toggle navigation menu</span>
      </Button>
    </Sheet.Trigger>
    <Sheet.Content side="left" class="flex flex-col">
      <!-- Mobile sidebar content -->
    </Sheet.Content>
  </Sheet.Root>
  <div class="w-full flex-1">
    <form>
      <Button class="m-4 bg-gradient-to-r from-blue-500 to-purple-600 text-white hover:from-purple-600 hover:to-blue-500">Chat with Assistant</Button>      
    </form>
  </div>
  <NewChatUi callback={newConversation} />
  <Button on:click={toggleMode} variant="outline" size="icon">
    <Sun
      class="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0"
    />
    <Moon
      class="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100"
    />
    <span class="sr-only">Toggle theme</span>
  </Button>
  <DropdownMenu.Root>
    <DropdownMenu.Trigger asChild let:builder>
      <Button
        builders={[builder]}
        variant="secondary"
        size="icon"
        class="rounded-full"
      >
        <CircleUser class="h-5 w-5" />
        <span class="sr-only">Toggle user menu</span>
      </Button>
    </DropdownMenu.Trigger>
    <DropdownMenu.Content align="end">
      <DropdownMenu.Label>Logged in as {data.nickname}</DropdownMenu.Label>
      <DropdownMenu.Separator />
      <DropDown/>
      <DropdownMenu.Item on:click={toggleLogs}>DevTools</DropdownMenu.Item>
      <DropdownMenu.Item>About</DropdownMenu.Item>
      <DropdownMenu.Separator />
      <DropdownMenu.Item on:click={logout}>Logout</DropdownMenu.Item>
    </DropdownMenu.Content>
  </DropdownMenu.Root>
</header>
