describe("getApiConfig", () => {
  const originalEnv = process.env;

  afterEach(() => {
    process.env = { ...originalEnv };
    jest.resetModules();
  });

  it("reports a missing NEXT_PUBLIC_API_BASE_URL", async () => {
    process.env = { ...originalEnv };
    delete process.env.NEXT_PUBLIC_API_BASE_URL;

    const { getApiConfig } = await import("@/lib/config");

    expect(getApiConfig()).toEqual({
      apiBaseUrl: null,
      configError:
        "NEXT_PUBLIC_API_BASE_URL is not set. Copy frontend/.env.example to frontend/.env.local and restart the Next.js dev server.",
    });
  });
});
