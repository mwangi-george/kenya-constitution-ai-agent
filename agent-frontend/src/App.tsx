import { Toaster } from "sonner";
import { ChatShell } from "@/components/chat/chat-shell";

export default function App() {
  return (
    <>
      <ChatShell />
      <Toaster richColors position="top-right" />
    </>
  );
}
