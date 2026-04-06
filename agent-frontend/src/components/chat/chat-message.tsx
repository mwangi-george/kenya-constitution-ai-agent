import { Bot, FileText, User } from "lucide-react";
import type { ChatMessage as ChatMessageType } from "@/types/chat";
import { formatCitationLabel } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";

interface ChatMessageProps {
  message: ChatMessageType;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isAssistant = message.role === "assistant";

  return (
    <div className={`flex w-full ${isAssistant ? "justify-start" : "justify-end"}`}>
      <div className={`flex w-full max-w-4xl gap-3 ${isAssistant ? "" : "flex-row-reverse"}`}>
        <div className={`mt-1 flex size-10 shrink-0 items-center justify-center rounded-2xl ${isAssistant ? "bg-slate-900 text-white" : "bg-linear-to-br from-blue-600 to-indigo-600 text-white"}`}>
          {isAssistant ? <Bot className="size-5" /> : <User className="size-5" />}
        </div>

        <Card className={`w-full px-5 py-4 ${isAssistant ? "bg-white/78" : "bg-linear-to-br from-indigo-600 to-blue-600 text-white"}`}>
          <div className="space-y-4">
            <div className={`whitespace-pre-wrap text-sm leading-7 ${isAssistant ? "text-slate-700" : "text-white"}`}>
              {message.content || (message.isStreaming ? "Thinking…" : "")}
            </div>

            {message.isStreaming ? (
              <div className="flex items-center gap-2 text-xs text-slate-500">
                <span className="inline-flex size-2 animate-pulse rounded-full bg-indigo-500" />
              </div>
            ) : null}

            {isAssistant && message.citations && message.citations.length > 0 ? (
              <div className="space-y-3 pt-2">
                <div className="flex items-center gap-2">
                  <FileText className="size-4 text-indigo-600" />
                  <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">Supporting citations</p>
                </div>

                <div className="grid gap-3 md:grid-cols-2">
                  {message.citations.map((citation) => (
                    <div key={citation.chunk_id} className=" border border-slate-200/70 bg-slate-50/80 p-0">
                      <Badge variant="secondary" className="">
                        {formatCitationLabel(citation.article_label, citation.page_number)}
                      </Badge>
                      {/*<p className="text-sm leading-6 text-slate-600">{citation.excerpt}</p>*/}
                    </div>
                  ))}
                </div>
              </div>
            ) : null}
          </div>
        </Card>
      </div>
    </div>
  );
}
