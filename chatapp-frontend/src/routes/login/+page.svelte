<svelte:head>
  <title>Log in</title>
</svelte:head>

<div class="flex flex-col justify-center items-center h-screen">
  <form class="bg-neutral-100 dark:bg-neutral-800 rounded-md p-4" action="/login/receive" method="POST">
    <div class="flex flex-col gap-4">
      <h1 class="text-3xl">Choose a nickname</h1>
      <input type="text" placeholder="Nickname" name="nickname" id="nickname" class="bg-neutral-100 dark:bg-black w-full px-3 py-2 rounded dark:bg-neutral-900 dark:border-neutral-700 border border-neutral-300 rounded-md"/>
      <div class="flex justify-end gap-5 invertColors">
        <button class="btn-success py-1 px-2" type="submit" >Submit</button>
      </div>
    </div>
  </form>
</div>
