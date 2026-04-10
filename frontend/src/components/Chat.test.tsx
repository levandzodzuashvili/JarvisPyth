import { fireEvent, render, screen } from "@testing-library/react";

import Chat from "@/components/Chat";
import { ApiRequestError, sendChatMessage } from "@/lib/api";
import { getApiConfig } from "@/lib/config";

jest.mock("@/lib/api", () => {
  class MockApiConfigError extends Error {}
  class MockApiRequestError extends Error {}

  return {
    ApiConfigError: MockApiConfigError,
    ApiRequestError: MockApiRequestError,
    sendChatMessage: jest.fn(),
  };
});

jest.mock("@/lib/config", () => ({
  getApiConfig: jest.fn(),
}));

const mockedSendChatMessage = sendChatMessage as jest.MockedFunction<
  typeof sendChatMessage
>;
const mockedGetApiConfig = getApiConfig as jest.MockedFunction<
  typeof getApiConfig
>;

describe("Chat", () => {
  let consoleErrorSpy: jest.SpyInstance;

  beforeEach(() => {
    consoleErrorSpy = jest.spyOn(console, "error").mockImplementation(() => {});
    mockedGetApiConfig.mockReturnValue({
      apiBaseUrl: "http://127.0.0.1:8000",
      configError: null,
    });
    mockedSendChatMessage.mockReset();
  });

  afterEach(() => {
    consoleErrorSpy.mockRestore();
  });

  it("renders the empty state and composer", () => {
    render(<Chat />);

    expect(screen.getByText("No messages yet")).toBeInTheDocument();
    expect(
      screen.getByPlaceholderText("Type your message here...")
    ).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Send" })).toBeInTheDocument();
  });

  it("appends the assistant reply after a successful send", async () => {
    mockedSendChatMessage.mockResolvedValue({ response: "Hello from Jarvis" });

    render(<Chat />);

    fireEvent.change(screen.getByPlaceholderText("Type your message here..."), {
      target: { value: "What is BM25?" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Send" }));

    expect(mockedSendChatMessage).toHaveBeenCalledWith("What is BM25?");
    expect(await screen.findByText("Hello from Jarvis")).toBeInTheDocument();
    expect(screen.getByText("What is BM25?")).toBeInTheDocument();
  });

  it("shows the generic error message when chat fails", async () => {
    mockedSendChatMessage.mockRejectedValue(
      new ApiRequestError("Groq request timed out")
    );

    render(<Chat />);

    fireEvent.change(screen.getByPlaceholderText("Type your message here..."), {
      target: { value: "Hello" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Send" }));

    expect(
      await screen.findByText(
        "Sorry, the chat service is unavailable right now. Please try again later."
      )
    ).toBeInTheDocument();
    expect(consoleErrorSpy).toHaveBeenCalled();
  });

  it("shows a configuration warning and disables the composer when config is missing", () => {
    mockedGetApiConfig.mockReturnValue({
      apiBaseUrl: null,
      configError:
        "NEXT_PUBLIC_API_BASE_URL is not set. Copy frontend/.env.example to frontend/.env.local and restart the Next.js dev server.",
    });

    render(<Chat />);

    expect(
      screen.getByText("Frontend configuration required")
    ).toBeInTheDocument();
    expect(
      screen.getByPlaceholderText("Type your message here...")
    ).toBeDisabled();
    expect(mockedSendChatMessage).not.toHaveBeenCalled();
  });
});
