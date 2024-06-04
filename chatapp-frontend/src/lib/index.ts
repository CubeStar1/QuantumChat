import { writable } from "svelte/store";

export interface Message {
    timestamp: number;
    content: string;
    encrypted: boolean;
}

export const messagesStore = writable<Message[]>([]);

export const showLogs = writable(false);