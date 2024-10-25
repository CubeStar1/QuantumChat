import { toast } from "svelte-sonner";

export function copyMessage(content: string) {
  navigator.clipboard.writeText(content).then(() => {
    console.log('Message copied to clipboard');
    toast.success("Message copied to clipboard");
  }).catch(err => {
    console.error('Could not copy text: ', err);
    toast.error("Failed to copy message");
  });
}

export function deleteMessage(timestamp: number, db, decryptedMessages) {
  decryptedMessages = decryptedMessages.filter(message => message.timestamp !== timestamp);
  db.transaction(["messages"], "readwrite").objectStore("messages").delete(timestamp);
  toast.success("Message deleted", {
    description: `Message has been deleted from your chat history.`,
    action: {
      label: "Undo",
      onClick: () => console.info("Undo")
    }
  });
}

export function forwardMessage(content: string) {
  console.log('Forwarding message:', content);
  toast.info("Forwarding not implemented yet");
}
