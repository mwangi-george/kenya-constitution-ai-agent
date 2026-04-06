import { Badge } from "@/components/ui/badge";

export function ChatHeader() {
  return (
    <header className="flex flex-col gap-3 rounded-[28px] border border-white/55 bg-white/70 p-5 shadow-[0_12px_50px_-30px_rgba(15,23,42,0.35)] backdrop-blur-xl sm:flex-row sm:items-center sm:justify-between">
      <div>
        <p className="text-xs font-semibold uppercase tracking-[0.24em] text-indigo-500">Constitution assistant</p>
        <h1 className="mt-1 text-2xl font-semibold tracking-tight text-slate-900">Ask anything about the Constitution of Kenya, 2010</h1>
        <p className="mt-2 max-w-2xl text-sm text-slate-600">
          Get grounded answers with supporting citations from your indexed constitutional document.
        </p>
      </div>
      <Badge variant="secondary" className="self-start sm:self-auto">FastAPI + Pydantic AI</Badge>
    </header>
  );
}
