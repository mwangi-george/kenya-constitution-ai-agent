import { useMemo, useRef, useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { toast } from "sonner";
import { chatService } from "@/services/chat-service";
import type { ChatMessage, Citation } from "@/types/chat";
import { generateMessageId } from "@/lib/utils";

function createMessage(
  role: ChatMessage["role"],
  content: string,
  options?: { citations?: Citation[]; isStreaming?: boolean },
): ChatMessage {
  return {
    id: generateMessageId(),
    role,
    content,
    citations: options?.citations,
    isStreaming: options?.isStreaming,
    createdAt: new Date().toISOString(),
  };
}

export function useChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const abortControllerRef = useRef<AbortController | null>(null);

  const askMutation = useMutation({
    mutationFn: async (question: string) => {
      abortControllerRef.current?.abort();
      abortControllerRef.current = new AbortController();

      const userMessage = createMessage("user", question);
      const assistantMessage = createMessage("assistant", "", { isStreaming: true });

      setMessages((current) => [...current, userMessage, assistantMessage]);

      await chatService.streamAnswer(
        question,
        {
          onToken: (token) => {
            setMessages((current) => {
              const updated = [...current];
              const lastMessage = updated[updated.length - 1];
              if (!lastMessage || lastMessage.role !== "assistant") return current;
              updated[updated.length - 1] = {
                ...lastMessage,
                content: `${lastMessage.content}${token}`,
              };
              return updated;
            });
          },
          onComplete: ({ citations }) => {
            setMessages((current) => {
              const updated = [...current];
              const lastMessage = updated[updated.length - 1];
              if (!lastMessage || lastMessage.role !== "assistant") return current;
              updated[updated.length - 1] = {
                ...lastMessage,
                citations,
                isStreaming: false,
              };
              return updated;
            });
          },
        },
        abortControllerRef.current.signal,
      );
    },
    onError: (error) => {
      setMessages((current) => {
        const updated = [...current];
        const lastMessage = updated[updated.length - 1];
        if (lastMessage?.role === "assistant") {
          updated[updated.length - 1] = {
            ...lastMessage,
            content:
              "Sorry, I could not complete your request. Please confirm the backend is running and try again.",
            isStreaming: false,
          };
        }
        return updated;
      });

      toast.error(error instanceof Error ? error.message : "Failed to get a response.");
    },
  });

  const submitQuestion = async (question: string) => {
    const trimmedQuestion = question.trim();
    if (!trimmedQuestion || askMutation.isPending) return;

    setInput("");
    await askMutation.mutateAsync(trimmedQuestion);
  };

  const stopStreaming = () => {
    abortControllerRef.current?.abort();
    setMessages((current) => {
      const updated = [...current];
      const lastMessage = updated[updated.length - 1];
      if (lastMessage?.role === "assistant") {
        updated[updated.length - 1] = { ...lastMessage, isStreaming: false };
      }
      return updated;
    });
  };

  const canSubmit = useMemo(() => input.trim().length > 0 && !askMutation.isPending, [input, askMutation.isPending]);

  return {
    messages,
    input,
    setInput,
    canSubmit,
    isLoading: askMutation.isPending,
    submitQuestion,
    stopStreaming,
  };
}
