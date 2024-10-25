<script lang="ts">
  import { Button } from "$lib/components/ui/button/index.js";
  import { Input } from "$lib/components/ui/input/index.js";
  import { Label } from "$lib/components/ui/label/index.js";
</script>

<svelte:head>
  <title>Log in</title>
</svelte:head>

<div class="w-full lg:grid lg:min-h-[600px] lg:grid-cols-2 xl:min-h-[800px]">
  <form class="flex items-center justify-center py-12 " action="/login/receive" method="POST">
    <!-- <div class="flex items-center justify-center py-12"> -->
      <div class="mx-auto grid w-[350px] gap-6">
        <div class="grid gap-2 text-center">
          <h1 class="text-3xl font-bold">Login</h1>
          <p class="text-balance text-muted-foreground">
            Enter your username below to login to your account
          </p>
        </div>
        <div class="grid gap-4">
          <div class="grid gap-2">
            <Label for="email">Username</Label>
            <input type="text" placeholder="Username" name="nickname" id="nickname" class="bg-neutral-100 dark:bg-black w-full px-3 py-2 rounded dark:bg-neutral-900 dark:border-neutral-700 border border-neutral-300 rounded-md"/>
          </div>
          <div class="grid gap-2">
            <div class="flex items-center">
              <Label for="password">Password</Label>
              <a href="##" class="ml-auto inline-block text-sm underline">
                Forgot your password?
              </a>
            </div>
            <Input id="password" type="password" required />
          </div>
          <button class="btn-success py-1 px-2" type="submit" >Login</button>
          <Button variant="outline" class="w-full">Login with Google</Button>
        </div>
        <div class="mt-4 text-center text-sm">
          Don&apos;t have an account?
          <a href="##" class="underline"> Sign up </a>
        </div>
      </div>
    <!-- </div> -->
  </form>
  <div class="hidden bg-black lg:block">
    <img
      src="./src/qclogo.png"
      alt="placeholder"
      width="1920"
      height="1080"
      class="h-full w-full object-cover dark:brightness-[0.2]"
    />
  </div>
</div>

<!-- <div class="flex flex-col justify-center items-center h-screen">
  <form class="bg-neutral-100 dark:bg-neutral-800 rounded-md p-4" action="/login/receive" method="POST">
    <div class="flex flex-col gap-4">
      <h1 class="text-3xl">Choose a nickname</h1>
      <input type="text" placeholder="Nickname" name="nickname" id="nickname" class="bg-neutral-100 dark:bg-black w-full px-3 py-2 rounded dark:bg-neutral-900 dark:border-neutral-700 border border-neutral-300 rounded-md"/>
      <div class="flex justify-end gap-5 invertColors">
        <button class="btn-success py-1 px-2" type="submit" >Submit</button>
      </div>
    </div>
  </form>
</div> -->
