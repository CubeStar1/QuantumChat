<script lang="ts">
    import CircleUser from "lucide-svelte/icons/circle-user";
    import LineChart from "lucide-svelte/icons/line-chart";
    import Package from "lucide-svelte/icons/package";
    import Home from "lucide-svelte/icons/home";
    import ShoppingCart from "lucide-svelte/icons/shopping-cart";
    import Bell from "lucide-svelte/icons/bell";
    import Menu from "lucide-svelte/icons/menu";
    import Package2 from "lucide-svelte/icons/package-2";
    import Search from "lucide-svelte/icons/search";
    import Users from "lucide-svelte/icons/users";
  
    import { Badge } from "$lib/components/ui/badge";
    import { Button } from "$lib/components/ui/button";
    import * as Card from "$lib/components/ui/card/";
    import * as DropdownMenu from "$lib/components/ui/dropdown-menu";
    import { Input } from "$lib/components/ui/input";
    import * as Sheet from "$lib/components/ui/sheet";
  </script>
  
  <div class="grid min-h-screen w-full md:grid-cols-[220px_1fr] lg:grid-cols-[280px_1fr]">
    <div class="hidden border-r bg-muted/40 md:block">
      <div class="flex h-full max-h-screen flex-col gap-2">
        <div class="flex h-14 items-center border-b px-4 lg:h-[60px] lg:px-6">
          <a href="/" class="flex items-center gap-2 font-semibold">
            <Package2 class="h-6 w-6" />
            <span class="">Quantum Chat</span>
          </a>
          <Button variant="outline" size="icon" class="ml-auto h-8 w-8">
            <Bell class="h-4 w-4" />
            <span class="sr-only">Toggle notifications</span>
          </Button>
        </div>
        <div class="flex-1">
          <nav class="grid items-start px-2 text-sm font-medium lg:px-4">
            <a
              href="##"
              class="flex items-center gap-3 rounded-lg px-3 py-2 text-muted-foreground transition-all hover:text-primary"
            >
              <Home class="h-4 w-4" />
              Users
            </a>
            <a
              href="##"
              class="flex items-center gap-3 rounded-lg px-3 py-2 text-muted-foreground transition-all hover:text-primary"
            >
              <ShoppingCart class="h-4 w-4" />
              Avinash
              <Badge
                class="ml-auto flex h-6 w-6 shrink-0 items-center justify-center rounded-full"
              >
                6
              </Badge>
            </a>
            <a
              href="##"
              class="flex items-center gap-3 rounded-lg bg-muted px-3 py-2 text-primary transition-all hover:text-primary"
            >
              <Package class="h-4 w-4" />
              Anish
            </a>
            <a
              href="##"
              class="flex items-center gap-3 rounded-lg px-3 py-2 text-muted-foreground transition-all hover:text-primary"
            >
              <Users class="h-4 w-4" />
              Ankit
            </a>
            <a
              href="##"
              class="flex items-center gap-3 rounded-lg px-3 py-2 text-muted-foreground transition-all hover:text-primary"
            >
              <LineChart class="h-4 w-4" />
              Alice
            </a>
          </nav>
        </div>
        <div class="mt-auto p-4">
          <Card.Root>
            <Card.Header class="p-2 pt-0 md:p-4">
              <Card.Title>New Chat</Card.Title>
              <Card.Description>
                Start a new conversation with another user
              </Card.Description>
            </Card.Header>
            <Card.Content class="p-2 pt-0 md:p-4 md:pt-0">
              <Button size="sm" class="w-full">Chat</Button>
            </Card.Content>
          </Card.Root>
        </div>
      </div>
    </div>
    <div class="flex flex-col">
      <header class="flex h-14 items-center gap-4 border-b bg-muted/40 px-4 lg:h-[60px] lg:px-6">
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
            <nav class="grid gap-2 text-lg font-medium">
              <a href="##" class="flex items-center gap-2 text-lg font-semibold">
                <Package2 class="h-6 w-6" />
                <span class="sr-only">Acme Inc</span>
              </a>
              <a
                href="##"
                class="mx-[-0.65rem] flex items-center gap-4 rounded-xl px-3 py-2 text-muted-foreground hover:text-foreground"
              >
                <Home class="h-5 w-5" />
                Dashboard
              </a>
              <a
                href="##"
                class="mx-[-0.65rem] flex items-center gap-4 rounded-xl bg-muted px-3 py-2 text-foreground hover:text-foreground"
              >
                <ShoppingCart class="h-5 w-5" />
                Orders
                <Badge
                  class="ml-auto flex h-6 w-6 shrink-0 items-center justify-center rounded-full"
                >
                  6
                </Badge>
              </a>
              <a
                href="##"
                class="mx-[-0.65rem] flex items-center gap-4 rounded-xl px-3 py-2 text-muted-foreground hover:text-foreground"
              >
                <Package class="h-5 w-5" />
                Products
              </a>
              <a
                href="##"
                class="mx-[-0.65rem] flex items-center gap-4 rounded-xl px-3 py-2 text-muted-foreground hover:text-foreground"
              >
                <Users class="h-5 w-5" />
                Customers
              </a>
              <a
                href="##"
                class="mx-[-0.65rem] flex items-center gap-4 rounded-xl px-3 py-2 text-muted-foreground hover:text-foreground"
              >
                <LineChart class="h-5 w-5" />
                Analytics
              </a>
            </nav>
            <div class="mt-auto">
              <Card.Root>
                <Card.Header>
                  <Card.Title>Welcome to Quantum Chat</Card.Title>
                  <Card.Description>
                   Click here to start a new chat
                  </Card.Description>
                </Card.Header>
                <Card.Content>
                  <Button size="sm" class="w-full">New Chat</Button>
                </Card.Content>
              </Card.Root>
            </div>
          </Sheet.Content>
        </Sheet.Root>
        <div class="w-full flex-1">
          <form>
            <div class="relative">
              <Search class="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input
                type="search"
                placeholder="Search products..."
                class="w-full appearance-none bg-background pl-8 shadow-none md:w-2/3 lg:w-1/3"
              />
            </div>
          </form>
        </div>
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
            <DropdownMenu.Label>My Account</DropdownMenu.Label>
            <DropdownMenu.Separator />
            <DropdownMenu.Item>Settings</DropdownMenu.Item>
            <DropdownMenu.Item>Support</DropdownMenu.Item>
            <DropdownMenu.Separator />
            <DropdownMenu.Item>Logout</DropdownMenu.Item>
          </DropdownMenu.Content>
        </DropdownMenu.Root>
      </header>
      <main class="flex flex-1 flex-col gap-4 p-4 lg:gap-6 lg:p-6">
        <div class="flex items-center">
          <h1 class="text-lg font-semibold md:text-2xl">Inventory</h1>
        </div>
        <div class="flex flex-1 items-center justify-center rounded-lg border border-dashed shadow-sm">
          <div class="flex flex-col items-center gap-1 text-center">
            <iframe
            title="streamlit"
              src="https://qkdsim.streamlit.app/?embed=true"
              width="1000rem"
              height="1000rem"
              frameBorder="0"
              allowFullScreen></iframe> 
          </div>
        </div>
      </main>
    </div>
  </div>
  