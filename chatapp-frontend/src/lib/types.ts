export interface User {
  nickname: string;
  key: string;
}

export interface Message {
  timestamp: number;
  sender: string;
  receiver: string;
  encrypted: boolean;
  content: string;
  type?: string;
  data?: string;
  image?: string;
}


