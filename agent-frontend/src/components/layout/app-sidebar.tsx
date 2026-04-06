import { Landmark, Scale, ShieldCheck, Sparkles } from "lucide-react";
import { EXAMPLE_QUESTIONS } from "@/lib/constants";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
// import { Separator } from "@/components/ui/separator";

interface AppSidebarProps {
  onSelectQuestion: (question: string) => void;
}

export function AppSidebar({ onSelectQuestion }: AppSidebarProps) {
  return (
    <aside className="hidden w-[320px] shrink-0 xl:block">
      <div className="sticky top-6 space-y-4">
        <Card className="overflow-hidden">
          <CardHeader className="space-y-4">
            <div className="flex items-center gap-3">
              <div className="flex size-12 items-center justify-center rounded-2xl bg-linear-to-br from-blue-600 to-indigo-600 text-white shadow-lg">
                <Scale className="size-6" />
              </div>
              <div>
                <CardTitle className="text-xl">Katiba AI</CardTitle>
                <CardDescription>Constitution of Kenya assistant</CardDescription>
              </div>
            </div>
            <Badge variant="secondary" className="w-fit">Traceable constitutional answers</Badge>
          </CardHeader>
          <CardContent className="space-y-4 text-sm text-slate-600">
            <div className="flex items-start gap-3">
              <Landmark className="mt-0.5 size-4 text-indigo-600" />
              <p>Grounds answers in the Constitution of Kenya, 2010 and highlights supporting references.</p>
            </div>
            <div className="flex items-start gap-3">
              <ShieldCheck className="mt-0.5 size-4 text-indigo-600" />
              <p>Designed for precise, trustworthy responses rather than generic legal commentary.</p>
            </div>
            <div className="flex items-start gap-3">
              <Sparkles className="mt-0.5 size-4 text-indigo-600" />
              <p>Optimized for a mobile-friendly, ChatGPT-inspired conversational experience.</p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-base">Try these questions</CardTitle>
            <CardDescription>Quick prompts to help users get started.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            {EXAMPLE_QUESTIONS.map((question, index) => (
              <button
                key={question}
                type="button"
                onClick={() => onSelectQuestion(question)}
                className="w-full rounded-2xl border border-white/55 bg-white/65 px-4 py-3 text-left text-sm text-slate-700 transition hover:-translate-y-0.5 hover:bg-white"
              >
                <span className="mb-2 block text-xs font-medium uppercase tracking-[0.18em] text-slate-400">
                  Example {index + 1}
                </span>
                {question}
              </button>
            ))}
          </CardContent>
        </Card>

        {/*<Card>*/}
        {/*  <CardHeader>*/}
        {/*    <CardTitle className="text-base">Recommended response pattern</CardTitle>*/}
        {/*  </CardHeader>*/}
        {/*  <CardContent className="space-y-3 text-sm text-slate-600">*/}
        {/*    <p>Ask short, direct constitutional questions. The interface is ideal for rights, governance, devolution, public finance, and leadership queries.</p>*/}
        {/*    <Separator />*/}
        {/*    <p>For stronger legal traceability, keep the backend configured to return citations with article labels, page numbers, and excerpts.</p>*/}
        {/*  </CardContent>*/}
        {/*</Card>*/}
      </div>
    </aside>
  );
}
