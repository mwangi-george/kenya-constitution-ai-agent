export interface Citation {
  chunk_id: string;
  article_label?: string | null;
  page_number?: number | null;
  excerpt: string;
}

export interface ChatRequest {
  question: string;
}

export interface ChatResponse {
  answer: string;
  citations: Citation[];
}

export type MessageRole = "user" | "assistant";

export interface ChatMessage {
  id: string;
  role: MessageRole;
  content: string;
  citations?: Citation[];
  isStreaming?: boolean;
  createdAt: string;
}

export interface StreamCompleteEvent {
  citations?: Citation[];
}
