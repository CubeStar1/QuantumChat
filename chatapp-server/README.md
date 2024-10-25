# ChatApp Server

## Overview

This is the backend server for the ChatApp application, built using TypeScript and Node.js. It provides RESTful APIs to handle chat functionalities and manage user interactions.

## Prerequisites

- **Node.js**: Ensure you have Node.js installed on your machine. You can download it from [here](https://nodejs.org/).
- **TypeScript**: This project uses TypeScript, so make sure to have it installed globally:
  ```bash
  npm install -g typescript
  ```

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/CubeStar1/QuantumChat.git
   cd chatapp-server
   ```

2. **Install Dependencies:**
   Run the following command to install all necessary packages:
   ```bash
   npm install
   ```

## Running the Server

1. **Start the Server:**
   Use `ts-node` to run the server:
   ```bash
   ts-node server-v3.ts
   ```

2. **Access the Server:**
   The server will be running on `http://localhost:3000` (or your specified port).

## API Endpoints

- **GET /api/messages**: Retrieve all chat messages.
- **POST /api/messages**: Send a new chat message.
- **GET /api/users**: Retrieve user information.

## Notes

- Ensure that the ports are available and not blocked by any firewall settings.
- You can configure environment variables in a `.env` file for settings like the server port and database connections.


