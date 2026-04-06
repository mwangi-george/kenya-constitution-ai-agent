import { useEffect, useMemo, useRef } from "react";
import { AppSidebar } from "@/components/layout/app-sidebar";
import { ChatComposer } from "@/components/chat/chat-composer";
import { ChatEmptyState } from "@/components/chat/chat-empty-state";
import { ChatHeader } from "@/components/chat/chat-header";
import { ChatMessage } from "@/components/chat/chat-message";
import { ScrollArea } from "@/components/ui/scroll-area";
import { useChat } from "@/hooks/use-chat";

export function ChatShell() {
  const { messages, input, setInput, canSubmit, isLoading, submitQuestion, stopStreaming } = useChat();
  const messagesContainerRef = useRef<HTMLDivElement | null>(null);

  const hasMessages = useMemo(() => messages.length > 0, [messages.length]);

  useEffect(() => {
    const element = messagesContainerRef.current;
    if (!element) return;
    element.scrollTo({ top: element.scrollHeight, behavior: "smooth" });
  }, [messages]);

  return (
    <div className="min-h-screen px-4 py-4 sm:px-6 lg:px-8">
      <div className="mx-auto flex max-w-7xl gap-6">
        <AppSidebar onSelectQuestion={(question) => void submitQuestion(question)} />

        <main className="flex min-h-[calc(100vh-2rem)] flex-1 flex-col gap-4">
          <ChatHeader />

          <div className="flex min-h-0 flex-1 flex-col rounded-4xl border border-white/55 bg-white/60 p-3 shadow-[0_24px_90px_-45px_rgba(15,23,42,0.45)] backdrop-blur-xl sm:p-4">
            <ScrollArea className="min-h-0 flex-1">
              <div ref={messagesContainerRef} className="space-y-2 p-2 sm:p-4">
                {hasMessages ? (
                  messages.map((message) => <ChatMessage key={message.id} message={message} />)
                ) : (
                  <ChatEmptyState onSelectQuestion={(question) => void submitQuestion(question)} />
                )}
              </div>
            </ScrollArea>

            <div className="mt-2 border border-gray-200">
              <ChatComposer
                value={input}
                onChange={setInput}
                onSubmit={() => void submitQuestion(input)}
                onStop={stopStreaming}
                canSubmit={canSubmit}
                isLoading={isLoading}
              />
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
