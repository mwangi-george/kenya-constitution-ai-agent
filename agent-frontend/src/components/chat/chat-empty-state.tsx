import { MessageSquareMore } from "lucide-react";
import { EXAMPLE_QUESTIONS } from "@/lib/constants";

interface ChatEmptyStateProps {
  onSelectQuestion: (question: string) => void;
}

export function ChatEmptyState({ onSelectQuestion }: ChatEmptyStateProps) {
  return (
    <div className="flex h-full flex-col items-center justify-center rounded-4xl border border-dashed border-white/60 bg-white/45 px-6 py-1 text-center backdrop-blur-sm">
      <div className="mb-5 flex size-16 items-center justify-center rounded-3xl bg-linear-to-br from-sky-500 to-indigo-600 text-white shadow-[0_16px_36px_-20px_rgba(79,70,229,0.8)]">
        <MessageSquareMore className="size-8" />
      </div>
      <h2 className="text-2xl font-semibold text-slate-900">Start a constitutional conversation</h2>
      <p className="mt-3 max-w-xl text-sm leading-6 text-slate-600">
        Ask about rights, devolution, Parliament, public participation, leadership and integrity, or any other part of the Constitution.
      </p>
      <div className="mt-2 grid w-full max-w-3xl gap-3 md:grid-cols-2">
        {EXAMPLE_QUESTIONS.map((question) => (
          <button
            key={question}
            type="button"
            onClick={() => onSelectQuestion(question)}
            className="rounded-3xl border border-white/60 bg-white/75 px-4 py-4 text-left text-sm text-slate-700 transition hover:-translate-y-0.5 hover:bg-white"
          >
            {question}
          </button>
        ))}
      </div>
    </div>
  );
}
