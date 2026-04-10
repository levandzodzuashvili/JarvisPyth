export interface Message {
  role: "user" | "assistant";
  content: string;
}

interface MessageListProps {
  loading: boolean;
  messages: Message[];
}

export default function MessageList({
  loading,
  messages,
}: MessageListProps) {
  return (
    <div className="flex-1 overflow-y-auto p-6 space-y-4">
      {messages.length === 0 ? (
        <div className="flex items-center justify-center h-full">
          <div className="text-center">
            <p className="text-gray-400 text-lg">No messages yet</p>
            <p className="text-gray-300 mt-2">Start by typing a message below</p>
          </div>
        </div>
      ) : (
        messages.map((message, index) => (
          <div
            key={`${message.role}-${index}`}
            className={`flex ${
              message.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`max-w-xs lg:max-w-md px-4 py-3 rounded-lg ${
                message.role === "user"
                  ? "bg-blue-600 text-white rounded-br-none"
                  : "bg-gray-200 text-gray-800 rounded-bl-none"
              }`}
            >
              <p className="break-words">{message.content}</p>
            </div>
          </div>
        ))
      )}

      {loading && (
        <div className="flex justify-start">
          <div className="bg-gray-200 text-gray-800 px-4 py-3 rounded-lg rounded-bl-none">
            <div className="flex space-x-2">
              <div
                className="w-2 h-2 bg-gray-600 rounded-full animate-bounce"
                style={{ animationDelay: "0ms" }}
              ></div>
              <div
                className="w-2 h-2 bg-gray-600 rounded-full animate-bounce"
                style={{ animationDelay: "150ms" }}
              ></div>
              <div
                className="w-2 h-2 bg-gray-600 rounded-full animate-bounce"
                style={{ animationDelay: "300ms" }}
              ></div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
