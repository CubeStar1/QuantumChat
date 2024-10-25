<!-- Log.svelte -->
<script>
    import * as Card from "$lib/components/ui/card";
    import { Button } from '$lib/components/ui/button';
    import * as Collapsible from "$lib/components/ui/collapsible";
    import CaretSort from "svelte-radix/CaretSort.svelte";
    import BackgroundGradient from '$lib/components/ui/BackgroundGradient/BackgroundGradient.svelte';
    export let logTitle;
    export let logElement;
    export let logMessages;
  </script>
  
  <Collapsible.Root>
    <div class="flex items-center">
      <Card.Root class="w-full mb-2">
        <div class="flex justify-between items-center p-4">
          <Card.Title class="text-center">{logTitle}</Card.Title>
          <Collapsible.Trigger asChild let:builder>
            <Button builders={[builder]} variant="ghost" size="sm" class="w-9 p-0">
              <CaretSort class="h-4 w-4" />
              <!-- <span class="sr-only">Toggle</span> -->
            </Button>
          </Collapsible.Trigger>
        </div>
      </Card.Root>
    </div>
    <Collapsible.Content>
      <Card.Root class="p-4 mx-auto max-h-60 overflow-scroll w-full mb-2">
        <p bind:this={logElement} class="whitespace-normal overflow-scroll">{logMessages}</p>
      </Card.Root>
    </Collapsible.Content>
  </Collapsible.Root>
