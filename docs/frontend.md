# Frontend Guide

The frontend is a Next.js 14 Pages Router application in `frontend/`. It no longer fetches the backend directly from the chat component; config and transport live in `src/lib/`.

## Project Structure

```text
frontend/
├── .env.example
├── .eslintrc.json
├── jest.config.js
├── jest.setup.ts
├── package.json
├── src/
│   ├── components/
│   │   ├── Chat.tsx
│   │   ├── Chat.test.tsx
│   │   ├── Composer.tsx
│   │   └── MessageList.tsx
│   ├── lib/
│   │   ├── api.ts
│   │   ├── config.test.ts
│   │   └── config.ts
│   ├── pages/
│   └── styles/
└── tsconfig.json
```

## UI Structure

### `Chat.tsx`

`Chat.tsx` is the stateful container. It owns:

- `input`
- `messages`
- `loading`
- frontend config checks via `getApiConfig()`

It does not perform raw `fetch()` calls directly.

### `Composer.tsx`

- wraps the input and send button in a `<form>`
- uses submit semantics instead of keypress-specific handling
- can be disabled when frontend config is missing

### `MessageList.tsx`

- renders the empty state
- renders user and assistant messages
- renders the loading indicator

## API and Config Boundary

### `src/lib/config.ts`

- reads `NEXT_PUBLIC_API_BASE_URL`
- trims trailing slashes
- returns `{ apiBaseUrl, configError }`

If the env var is missing, the UI shows a configuration banner and disables the composer.

### `src/lib/api.ts`

- exports `sendChatMessage(message)`
- throws `ApiConfigError` for missing frontend config
- throws `ApiRequestError` for non-2xx backend responses

## Scripts

| Command | Purpose |
| --- | --- |
| `npm run dev` | Start the Next.js dev server |
| `npm run build` | Build the production bundle |
| `npm start` | Start the production server |
| `npm run lint` | Run Next.js ESLint |
| `npm run test` | Run Jest in watch/default mode |
| `npm run test:ci` | Run Jest once for CI |

## Tests

Frontend tests use Jest + React Testing Library.

Current coverage includes:

- config helper behavior with missing env vars
- chat render
- successful send flow
- failed send flow
- missing-config UI behavior

## Environment

Create `frontend/.env.local` from `frontend/.env.example`:

```bash
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
```

Next.js reads this when the dev server starts or when the production bundle is built. Restart `npm run dev` after changing it.
