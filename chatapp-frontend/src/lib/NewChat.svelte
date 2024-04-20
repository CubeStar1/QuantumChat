<script lang="ts">
  import { FontAwesomeIcon } from "@fortawesome/svelte-fontawesome";
  import { faMultiply } from "@fortawesome/free-solid-svg-icons";
  
  export let show: boolean;
  export let callback: (arg0: string) => void;

  let disabled = false;
  let nickname = "";

  function closeModal() {
    show = false;
  }

  function handleSubmit() {
    callback(nickname);
    closeModal();
  }
</script>

{#if show}
  <div class="fixed inset-0 z-50 flex items-center justify-center transition">
    <div class="absolute inset-0 bg-black opacity-50"></div>
    <div class="relative bg-white dark:bg-neutral-800 rounded-lg p-8 max-w-md">
      <button class="absolute top-0 right-0 p-2 hover:text-neutral-600 transition" on:click={closeModal}>
        <FontAwesomeIcon icon={faMultiply} />
      </button>
      <h2 class="text-xl mb-4 font-semibold">New chat</h2>
      <div class="flex flex-col gap-4">
        <div>
          <input type="text" placeholder="Nickname" id="nickname" bind:value={nickname} class="bg-neutral-100 dark:bg-black w-full px-3 py-2 rounded dark:bg-neutral-900 dark:border-neutral-700 border border-neutral-300 rounded-md" disabled={disabled}/>
        </div>
        <div class="flex justify-end gap-5 invertColors">
          <button class="btn-secondary py-1 px-2" on:click={closeModal} disabled={disabled}>Cancel</button>
          <button class="btn-success py-1 px-2" on:click={handleSubmit} disabled={disabled}>Submit</button>
        </div>
      </div>
    </div>
  </div>
{/if}
