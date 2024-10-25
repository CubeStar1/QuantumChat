import * as aesjs from 'aes-js';
import forge from 'node-forge';

export function decryptMessage(message, user) {
  if (!user || !message.encrypted) {
    return message;
  }

  let binaryKey = atob(user.key).split('').map(c => c.charCodeAt(0)).join('');
  let key = new Uint8Array(16);
  for (let i = 0; i < 16; i++) {
    key[i] = parseInt(binaryKey.substr(i * 8, 8), 2);
  }

  var aesCtr = new aesjs.ModeOfOperation.ctr(key, new aesjs.Counter(1));
  var encryptedBytes = aesjs.utils.hex.toBytes(message.content);
  var decryptedBytes = aesCtr.decrypt(encryptedBytes);
  var decryptedText = aesjs.utils.utf8.fromBytes(decryptedBytes);

  return {
    ...message,
    type: 'message',
    encrypted: false,
    content: decryptedText
  };
}

export async function generateKeyPair() {
  let keyPair = forge.pki.rsa.generateKeyPair(2048);
  let publicKey = forge.pki.publicKeyToPem(keyPair.publicKey);
  let privateKey = forge.pki.privateKeyToPem(keyPair.privateKey);
  return { publicKey, privateKey };
}

export async function decryptSymmetricKey(encryptedKey: string, privateKeyPem: string) {
  try {
    if (!(/^[A-Za-z0-9+/=]*$/.test(encryptedKey))) {
      throw new Error("Encrypted key is not a valid base64 string");
    }

    let encryptedKeyBytes = forge.util.decode64(encryptedKey);
    let privateKey = forge.pki.privateKeyFromPem(privateKeyPem);
    let decryptedKeyBytes = privateKey.decrypt(encryptedKeyBytes, 'RSA-OAEP');
    return btoa(decryptedKeyBytes);
  } catch (error) {
    console.error("Error decrypting symmetric key:", error);
    throw error;
  }
}
