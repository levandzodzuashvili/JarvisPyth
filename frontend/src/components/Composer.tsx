import { FormEvent } from "react";

interface ComposerProps {
  disabled?: boolean;
  input: string;
  loading: boolean;
  onInputChange: (value: string) => void;
  onSubmit: () => void;
}

export default function Composer({
  disabled = false,
  input,
  loading,
  onInputChange,
  onSubmit,
}: ComposerProps) {
  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    onSubmit();
  };

  return (
    <div className="border-t border-gray-300 bg-white p-6">
      <form className="flex gap-2" onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={(event) => onInputChange(event.target.value)}
          disabled={disabled || loading}
          placeholder="Type your message here..."
          className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
        />
        <button
          type="submit"
          disabled={disabled || loading || !input.trim()}
          className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white px-6 py-3 rounded-lg font-semibold transition-colors"
        >
          {loading ? "Sending..." : "Send"}
        </button>
      </form>
    </div>
  );
}
