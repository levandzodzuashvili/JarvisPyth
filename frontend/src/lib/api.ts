import { getApiConfig } from "@/lib/config";

export interface ChatApiResponse {
  response: string;
}

export class ApiConfigError extends Error {}

export class ApiRequestError extends Error {}

export async function sendChatMessage(
  message: string
): Promise<ChatApiResponse> {
  const { apiBaseUrl, configError } = getApiConfig();

  if (!apiBaseUrl) {
    throw new ApiConfigError(configError ?? "Missing API configuration.");
  }

  const response = await fetch(`${apiBaseUrl}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message }),
  });

  if (!response.ok) {
    let detail = `Request failed with status ${response.status}`;

    try {
      const data = await response.json();
      if (typeof data.detail === "string") {
        detail = data.detail;
      }
    } catch {
      // Ignore JSON parsing errors and fall back to the HTTP status string.
    }

    throw new ApiRequestError(detail);
  }

  return response.json();
}
