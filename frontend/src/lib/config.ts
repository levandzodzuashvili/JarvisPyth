export interface ApiConfigResult {
  apiBaseUrl: string | null;
  configError: string | null;
}

export function getApiConfig(): ApiConfigResult {
  const rawApiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL?.trim();

  if (!rawApiBaseUrl) {
    return {
      apiBaseUrl: null,
      configError:
        "NEXT_PUBLIC_API_BASE_URL is not set. Copy frontend/.env.example to frontend/.env.local and restart the Next.js dev server.",
    };
  }

  return {
    apiBaseUrl: rawApiBaseUrl.replace(/\/+$/, ""),
    configError: null,
  };
}
