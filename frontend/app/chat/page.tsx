"use client";

import { useState, useRef, useEffect } from "react";
import { motion } from "framer-motion";
import { sendChat } from "@/lib/api";
import { Send, Bot, User, MessageSquare, Sparkles } from "lucide-react";
import { cn } from "@/lib/utils";

interface Message {
  role: "user" | "bot";
  content: string;
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "bot",
      content:
        "Hello! I'm your AI Health Assistant. Ask me anything about health, symptoms, or vitals.",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function handleSend(e: React.FormEvent) {
    e.preventDefault();
    const text = input.trim();
    if (!text || loading) return;

    setMessages((prev) => [...prev, { role: "user", content: text }]);
    setInput("");
    setLoading(true);

    try {
      const res = await sendChat(text);
      setMessages((prev) => [
        ...prev,
        { role: "bot", content: res.bot_response },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          content: `Error: ${err instanceof Error ? err.message : "Failed to reach server"}`,
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex h-[calc(100vh-6rem)] flex-col">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="mb-4 flex items-center gap-3"
      >
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-violet-500/10 border border-violet-500/20">
          <MessageSquare className="h-5 w-5 text-violet-400" />
        </div>
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-white">
            Health Chat
          </h1>
          <p className="text-sm text-white/50">
            Talk to the AI health assistant
          </p>
        </div>
      </motion.div>

      {/* Messages area */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.1 }}
        className="flex-1 overflow-hidden rounded-xl border border-white/[0.08] bg-white/[0.02] backdrop-blur-sm"
      >
        <div className="flex h-full flex-col">
          <div className="flex-1 space-y-4 overflow-y-auto p-5">
            {messages.map((msg, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
                className={cn(
                  "flex items-start gap-3",
                  msg.role === "user" ? "flex-row-reverse" : "flex-row",
                )}
              >
                {/* Avatar */}
                <div
                  className={cn(
                    "flex h-8 w-8 shrink-0 items-center justify-center rounded-full",
                    msg.role === "user"
                      ? "bg-teal-500/20 text-teal-400"
                      : "bg-violet-500/20 text-violet-400",
                  )}
                >
                  {msg.role === "user" ? (
                    <User className="h-4 w-4" />
                  ) : (
                    <Bot className="h-4 w-4" />
                  )}
                </div>

                {/* Bubble */}
                <div
                  className={cn(
                    "max-w-[75%] rounded-2xl px-4 py-2.5 text-sm leading-relaxed",
                    msg.role === "user"
                      ? "bg-teal-500/15 border border-teal-500/20 text-white/90"
                      : "bg-white/[0.05] border border-white/[0.08] text-white/80",
                  )}
                >
                  {msg.content}
                </div>
              </motion.div>
            ))}

            {loading && (
              <div className="flex items-start gap-3">
                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-violet-500/20 text-violet-400">
                  <Bot className="h-4 w-4" />
                </div>
                <div className="rounded-2xl bg-white/[0.05] border border-white/[0.08] px-4 py-2.5 text-sm text-white/40">
                  <span className="inline-flex gap-1">
                    <span className="animate-bounce">●</span>
                    <span
                      className="animate-bounce"
                      style={{ animationDelay: "0.1s" }}
                    >
                      ●
                    </span>
                    <span
                      className="animate-bounce"
                      style={{ animationDelay: "0.2s" }}
                    >
                      ●
                    </span>
                  </span>
                </div>
              </div>
            )}
            <div ref={bottomRef} />
          </div>

          {/* Input */}
          <div className="border-t border-white/[0.08] p-4">
            <form onSubmit={handleSend} className="flex gap-3">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask about symptoms, vitals, health tips…"
                className="flex-1 rounded-xl border border-white/[0.1] bg-white/[0.05] px-4 py-3 text-sm text-white placeholder:text-white/30 focus:border-teal-500/50 focus:outline-none focus:ring-1 focus:ring-teal-500/30 transition-colors"
              />
              <motion.button
                type="submit"
                disabled={loading || !input.trim()}
                whileHover={{ scale: 1.04 }}
                whileTap={{ scale: 0.96 }}
                className="flex items-center gap-2 rounded-xl px-5 py-3 text-sm font-medium text-white transition-all disabled:opacity-40"
                style={{
                  background:
                    "linear-gradient(135deg, #14B8A6 0%, #0D9488 100%)",
                  boxShadow: "0 4px 16px rgba(20,184,166,0.25)",
                }}
              >
                <Send className="h-4 w-4" />
                Send
              </motion.button>
            </form>
            <div className="mt-2 flex items-center gap-1.5 text-[10px] text-white/25">
              <Sparkles className="h-3 w-3" />
              Powered by AI Health Assistant
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
