import type { ChatResponse, Citation, StreamCompleteEvent } from "@/types/chat";
import { apiClient, ApiError } from "@/services/api-client";

interface StreamCallbacks {
  onToken: (token: string) => void;
  onComplete: (payload: StreamCompleteEvent) => void;
}

export class ChatService {
  async ask(question: string, signal?: AbortSignal) {
    return apiClient.post<ChatResponse>("/chat", { question }, signal);
  }

  async streamAnswer(question: string, callbacks: StreamCallbacks, signal?: AbortSignal) {
    const response = await fetch(`${apiClient.baseUrl}/chat/stream`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question }),
      signal,
    });

    if (!response.ok || !response.body) {
      throw new ApiError("Unable to stream response.", response.status);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const events = buffer.split("\n\n");
      buffer = events.pop() ?? "";

      for (const rawEvent of events) {
        const eventTypeMatch = rawEvent.match(/^event:\s*(.+)$/m);
        const dataMatch = rawEvent.match(/^data:\s*(.+)$/m);
        const eventType = eventTypeMatch?.[1]?.trim();
        const data = dataMatch?.[1]?.trim();

        if (!eventType || !data) continue;

        const parsed = JSON.parse(data) as { content?: string; citations?: Citation[] };

        if (eventType === "token" && parsed.content) {
          callbacks.onToken(parsed.content);
        }

        if (eventType === "complete") {
          callbacks.onComplete({ citations: parsed.citations });
        }
      }
    }
  }
}

export const chatService = new ChatService();
