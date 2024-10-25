import * as aesjs from 'aes-js';
import axios from 'axios';

export function handleSubmit(messageText, selectedUser, socket, logEncryptMessages) {
  if (!messageText || !(messageText = messageText.trim()) || !selectedUser) {
    return messageText;
  }

  let binaryKey = atob(selectedUser.key).split('').map(c => c.charCodeAt(0)).join('');
  let key = new Uint8Array(16);
  for (let i = 0; i < 16; i++) {
    key[i] = parseInt(binaryKey.substr(i * 8, 8), 2);
  }

  var aesCtr = new aesjs.ModeOfOperation.ctr(key, new aesjs.Counter(1));
  var textBytes = aesjs.utils.utf8.toBytes(messageText);
  var encryptedBytes = aesCtr.encrypt(textBytes);
  var encryptedHex = aesjs.utils.hex.fromBytes(encryptedBytes);

  let message = {
    encrypted: true,
    content: encryptedHex,
    timestamp: Date.now(),
    receiver: selectedUser.nickname,
    sender: socket.nickname // Make sure this is set correctly
  };

  logEncryptMessages += `Timestamp: ${new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}\n`;
  logEncryptMessages += `Symmetric Key: ${selectedUser.key}\n`;
  logEncryptMessages += `Message encrypted: ${message.content}\n`;

  let payload = {
    type: 'message',
    data: message
  };

  socket.send(JSON.stringify(payload));
  return '';
}

export function handleInput(typing, nickname, socket, typingTimeout, stopTyping) {
  clearTimeout(typingTimeout);
  if (!typing) {
    typing = true;
    socket.send(JSON.stringify({ type: 'typing', data: {user: nickname, typing: true }})); 
  }
  return setTimeout(() => stopTyping(nickname, socket), 1000);
}

export function stopTyping(nickname, socket) {
  socket.send(JSON.stringify({ type: 'typing', data: {user: nickname, typing: false }}));
}

export async function sendImage(API_URLS, selectedUser, nickname, socket) {
  const fileInput = document.getElementById('fileInput') as HTMLInputElement;
  var file = fileInput.files?.[0];
  if (!file) return;

  const reader = new FileReader();
  let patientInfo = null;

  if (file.name.toLowerCase().endsWith('.dcm')) {
    const formData = new FormData();
    formData.append('file', file);
    const response = await axios.post(API_URLS.CONVERT, formData, {
      responseType: 'blob',
    });

    const blob = new Blob([response.data], { type: 'image/jpeg' });
    file = new File([blob], file.name.replace('.dcm', '.jpg'), { type: 'image/jpeg' });

    const patientInfoResponse = await axios.post(API_URLS.EXTRACT_PATIENT_INFO, formData);
    patientInfo = patientInfoResponse.data.patient_info;
  }

  reader.onload = async (event) => {
    const dataUrl = event.target?.result as string;
    const message = {
      type: 'image',
      data: {
        type: 'image',
        image: dataUrl,
        sender: nickname,
        receiver: selectedUser?.nickname,
        timestamp: Date.now(),
        encrypted: false
      }
    };

    socket.send(JSON.stringify(message));

    if (patientInfo) {
      const patientSummaryResponse = await axios.post(API_URLS.GET_PATIENT_SUMMARY, { patient_info: patientInfo });
      const patientVitals = await axios.get(API_URLS.GET_PATIENT_VITALS);
      const patientSummary = patientSummaryResponse.data.patient_summary;

      const summaryMessage = {
        type: 'message',
        data: {
          type: 'message',
          encrypted: false,
          content: patientSummary,
          timestamp: Date.now(),
          sender: nickname,
          receiver: selectedUser?.nickname
        }
      };

      const contentString = "**Patient vitals:** "  + "\n\n" + "Heart rate: " + patientVitals.data.average_heart_rate + " bpm\n\n" + "Temperature: " + patientVitals.data.average_temperature + "º F";

      const vitalsMessage = {
        type: 'message',
        data: {
          type: 'message',
          encrypted: false,
          content: contentString,
          timestamp: Date.now() + 1,
          sender: nickname,
          receiver: selectedUser?.nickname
        }
      };
      socket.send(JSON.stringify(summaryMessage));
      socket.send(JSON.stringify(vitalsMessage));
    }
    
    fileInput.value = '';
  };

  reader.readAsDataURL(file);
}
