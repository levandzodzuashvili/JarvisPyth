"use client";

import { useState } from "react";

import Composer from "@/components/Composer";
import MessageList, { Message } from "@/components/MessageList";
import { ApiConfigError, ApiRequestError, sendChatMessage } from "@/lib/api";
import { getApiConfig } from "@/lib/config";

const GENERIC_CHAT_ERROR =
  "Sorry, the chat service is unavailable right now. Please try again later.";

export default function Chat() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  const { configError } = getApiConfig();

  const sendMessage = async () => {
    const trimmedInput = input.trim();
    if (!trimmedInput || loading) return;

    if (configError) {
      console.error(configError);
      return;
    }

    setLoading(true);
    const userMessage: Message = { role: "user", content: trimmedInput };
    setMessages((prev) => [...prev, userMessage]);

    try {
      const data = await sendChatMessage(trimmedInput);
      const assistantMessage: Message = {
        role: "assistant",
        content: data.response,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error("Failed to send chat message", error);

      const errorMessage: Message = {
        role: "assistant",
        content: error instanceof ApiConfigError ? error.message : GENERIC_CHAT_ERROR,
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setInput("");
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      <div className="bg-gradient-to-r from-blue-600 to-blue-800 text-white p-6 shadow-lg">
        <h1 className="text-3xl font-bold">Python Jarvis</h1>
        <p className="text-blue-100 mt-1">AI-powered document analysis & chat</p>
      </div>

      {configError && (
        <div className="mx-6 mt-6 rounded-lg border border-amber-300 bg-amber-50 px-4 py-3 text-amber-900">
          <p className="font-semibold">Frontend configuration required</p>
          <p className="mt-1 text-sm">{configError}</p>
        </div>
      )}

      <MessageList loading={loading} messages={messages} />

      <Composer
        disabled={Boolean(configError)}
        input={input}
        loading={loading}
        onInputChange={setInput}
        onSubmit={sendMessage}
      />
    </div>
  );
}
