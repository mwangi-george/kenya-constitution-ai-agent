import type { FormEvent, KeyboardEvent } from "react";
import { LoaderCircle, Square, ArrowUp } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";

interface ChatComposerProps {
    value: string;
    onChange: (value: string) => void;
    onSubmit: () => void;
    onStop: () => void;
    canSubmit: boolean;
    isLoading: boolean;
}

export function ChatComposer({
                                 value,
                                 onChange,
                                 onSubmit,
                                 onStop,
                                 canSubmit,
                                 isLoading,
                             }: ChatComposerProps) {

    const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        if (!canSubmit || isLoading) return;
        onSubmit();
    };

    /**
     * Handle Enter key submission
     * - Enter → submit
     * - Shift + Enter → new line
     */
    const handleKeyDown = (event: KeyboardEvent<HTMLTextAreaElement>) => {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();

            if (!canSubmit || isLoading) return;

            onSubmit();
        }
    };

    return (
        <form
            onSubmit={handleSubmit}
            className="rounded-[30px] border border-green-500 bg-white/80 p-4 shadow-[0_20px_70px_-35px_rgba(15,23,42,0.4)] backdrop-blur-xl"
        >
            <Textarea
                value={value}
                onChange={(event) => onChange(event.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask a question about the Constitution of Kenya, 2010..."
                className="min-h-29 resize-none border-0 bg-transparent px-0 py-4 text-[15px] leading-7 shadow-none focus-visible:ring-0"
            />

            <div className="mt-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                <p className="text-xs leading-5 text-slate-500">
                    Responses should be grounded in the indexed constitutional text and returned with citations.
                </p>

                {isLoading ? (
                    <Button type="button" variant="outline" onClick={onStop} className="min-w-30">
                        <Square className="size-4 fill-current" />
                        Stop
                    </Button>
                ) : (
                    <Button type="submit" size="lg" disabled={!canSubmit} className="min-w-35">
                        {isLoading ? (
                            <LoaderCircle className="size-4 animate-spin" />
                        ) : (
                            <ArrowUp className="size-4" />
                        )}
                        Ask Katiba AI
                    </Button>
                )}
            </div>
        </form>
    );
}
