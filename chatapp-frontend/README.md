# Quantum Chat Frontend

This is the frontend application for Quantum Chat, built with Svelte. It provides a user interface for secure messaging using quantum key distribution.

## Features

- Real-time chat interface
- Secure message encryption using AES
- Integration with Quantum Key Distribution backend
- Theme switching capability
- User authentication and conversation management

## Prerequisites

- Node.js (version 14 or later recommended)
- npm (usually comes with Node.js)

## Installation

1. Clone the repository if you haven't already:
   ```bash
   git clone https://github.com/CubeStar1/QuantumChat.git
   ```

2. Navigate to the frontend directory:
   ```bash
   cd QuantumChat/chatapp-frontend
   ```

3. Install dependencies:
   ```bash
   npm install
   ```

## Development

To start the development server:

```bash
npm run dev

# or to open it in a new browser tab automatically
npm run dev -- --open
```

The application will be available at `http://localhost:5173` (or another port if 5173 is in use).

## Building for Production

To create a production version of the app:

```bash
npm run build
```

You can preview the production build with:

```bash
npm run preview
```

## Project Structure

- `src/routes/`: Contains the main page components
- `src/lib/`: Houses reusable components and utility functions
- `src/lib/components/`: Includes individual UI components like ChatHeader, Sidebar, etc.

## Components

- `+page.svelte`: The main chat interface
- `DropDown.svelte`: User selection dropdown
- `ChatHeader.svelte`: Header component for the chat interface
- `ThemeSwitcher.svelte`: Component for switching between light and dark themes
- `Sidebar.svelte`: Sidebar component for navigation and user list

## Connecting to Backend

Ensure that the NodeJS backend and QKD server are running before starting the frontend. The WebSocket connection is typically established to `ws://localhost:3000`.

## Notes

- This frontend relies on the Quantum Chat backend for full functionality. Make sure to set up and run the backend servers as described in the main project README.
- For deploying to production, you may need to adjust the WebSocket connection URL and other environment-specific configurations.
