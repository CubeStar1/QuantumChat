<script lang="ts">
    import CircleUser from "lucide-svelte/icons/circle-user";
    import LineChart from "lucide-svelte/icons/line-chart";
    import Package from "lucide-svelte/icons/package";
    import Home from "lucide-svelte/icons/home";
    import ShoppingCart from "lucide-svelte/icons/shopping-cart";
    import Bell from "lucide-svelte/icons/bell";
    import Package2 from "lucide-svelte/icons/package-2";
    import Users from "lucide-svelte/icons/users";
    import { Badge } from "$lib/components/ui/badge";
    import { Button } from "$lib/components/ui/button";
    import * as Card from "$lib/components/ui/card";
  </script>
  
  <div class="grid min-h-screen w-full md:grid-cols-[220px_1fr] lg:grid-cols-[280px_1fr]">
    <div class="hidden border-r bg-muted/40 md:block">
      <div class="flex h-full max-h-screen flex-col gap-2">
        <div class="flex h-14 items-center border-b px-4 lg:h-[60px] lg:px-6">
          <a href="/" class="flex items-center gap-2 font-semibold">
            <Package2 class="h-6 w-6" />
            <span>Quantum Chat </span>
          </a>
          <Button variant="outline" size="icon" class="ml-auto h-8 w-8">
            <Bell class="h-4 w-4" />
            <span class="sr-only">Toggle notifications</span>
          </Button>
        </div>
        <div class="flex-1">
          <nav class="grid items-start px-2 text-sm font-medium lg:px-4">
            <a href="##" class="flex items-center gap-3 rounded-lg px-3 py-2 text-muted-foreground transition-all hover:text-primary">
              <Home class="h-4 w-4" />
              Users
            </a>
            <a href="##" class="flex items-center gap-3 rounded-lg px-3 py-2 text-muted-foreground transition-all hover:text-primary">
              <ShoppingCart class="h-4 w-4" />
              Orders
              <Badge class="ml-auto flex h-6 w-6 shrink-0 items-center justify-center rounded-full">
                6
              </Badge>
            </a>
            <a href="##" class="flex items-center gap-3 rounded-lg bg-muted px-3 py-2 text-primary transition-all hover:text-primary">
              <Package class="h-4 w-4" />
              Products
            </a>
            <a href="##" class="flex items-center gap-3 rounded-lg px-3 py-2 text-muted-foreground transition-all hover:text-primary">
              <Users class="h-4 w-4" />
              Customers
            </a>
            <a href="##" class="flex items-center gap-3 rounded-lg px-3 py-2 text-muted-foreground transition-all hover:text-primary">
              <LineChart class="h-4 w-4" />
              Analytics
            </a>
          </nav>
        </div>
        <div class="mt-auto p-4">
          <Card.Root>
            <Card.Header class="p-2 pt-0 md:p-4">
              <Card.Title>New Chat</Card.Title>
              <Card.Description>
                Start a new chat with a user.
              </Card.Description>
            </Card.Header>
            <Card.Content class="p-2 pt-0 md:p-4 md:pt-0">
              <Button size="sm" class="w-full">Chat</Button>
            </Card.Content>
          </Card.Root>
        </div>
      </div>
    </div>
  </div>
  
  <style>
    /* .bg-muted { background-color: #f9fafb; }
    .bg-muted { background-color: rgba(249, 250, 251, 0.4); }
    .text-muted-foreground { color: #6b7280; }
    .text-primary { color: #3b82f6; }
    .hover\:text-primary:hover { color: #3b82f6; }
    .hover\:text-foreground:hover { color: #374151; } */
  </style>
  