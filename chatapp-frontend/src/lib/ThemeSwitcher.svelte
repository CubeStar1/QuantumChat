<script lang="ts">
  import { browser } from '$app/environment';


  let theme: 'system' | 'light' | 'dark' = 'system';
  let themes: ['system', 'light', 'dark'] = ['system', 'light', 'dark'];
  if (browser) {
    theme = localStorage.theme ?? 'system';
  }

  function setTheme(theme: 'system' | 'light' | 'dark') {
    if (theme === 'system') {
      localStorage.removeItem('theme');
    } else {
      localStorage.theme = theme;
    }
    refreshTheme()
  }

  function refreshTheme() {
    if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }
</script>

<select bind:value={theme} on:change={() => {setTheme(theme)}}
        class="rounded-lg dark:bg-neutral-700 bg-neutral-100 w-24 flex-none text-lg px-1 ml-0 text-center transition">
  <option value="system">System</option>
  <option value="light">Light</option>
  <option value="dark">Dark</option>
</select>
