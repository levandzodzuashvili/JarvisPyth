# Frontend Guide

The frontend is a Next.js 14 application with TypeScript and Tailwind CSS, located in `frontend/`.

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   └── Chat.tsx          # Main chat UI (client component)
│   ├── pages/
│   │   ├── _app.tsx          # App wrapper, global CSS import
│   │   └── index.tsx         # Home page (renders Chat)
│   └── styles/
│       └── globals.css       # Tailwind directives, base reset
├── package.json
├── tsconfig.json             # TypeScript config (strict mode)
├── tailwind.config.js        # Tailwind content paths
├── postcss.config.js         # PostCSS with Tailwind + Autoprefixer
├── next.config.js            # Next.js config (default)
└── next-env.d.ts             # Next.js TypeScript definitions
```

## Chat Component (`src/components/Chat.tsx`)

This is the core UI component — a `"use client"` React component that manages the entire chat experience.

### State

| State Variable | Type        | Purpose                       |
| -------------- | ----------- | ----------------------------- |
| `input`        | `string`    | Current text in the input box |
| `messages`     | `Message[]` | Full conversation history     |
| `loading`      | `boolean`   | Whether an API call is active |

The `Message` interface:
```typescript
interface Message {
  role: "user" | "assistant";
  content: string;
}
```

### API Communication

The component sends POST requests to `http://127.0.0.1:8001/chat` with:
- Headers: `Content-Type: application/json`
- Body: `{ message: string }`
- Expected response: `{ response: string }`

On success, the assistant's reply is appended to `messages`. On failure, an error message is displayed as an assistant message.

### UI Sections

1. **Header** — Gradient blue bar with title "Python Jarvis" and subtitle
2. **Messages area** — Scrollable container showing the conversation
   - User messages: right-aligned, blue background, white text
   - Assistant messages: left-aligned, gray background, dark text
   - Empty state: centered prompt to start chatting
3. **Loading indicator** — Three animated bouncing dots (shown while waiting for API)
4. **Input area** — Text input + Send button at the bottom
   - Enter key sends the message
   - Input and button are disabled during loading

## Styling

- **Tailwind CSS 3** via PostCSS — configured in `tailwind.config.js`
- Content scanning: `./src/**/*.{js,ts,jsx,tsx}`
- Global reset in `globals.css`: border-box sizing, full-height html/body, system font stack
- No custom Tailwind theme extensions or plugins

## TypeScript Configuration

Key `tsconfig.json` settings:
- **Target:** ES2020
- **Strict mode:** enabled
- **Path alias:** `@/*` maps to `src/*` (e.g., `import Chat from "@/components/Chat"`)
- **JSX:** preserve (Next.js handles compilation)
- **Source maps:** enabled

## Adding a New Page

1. Create a file in `src/pages/`:
   ```typescript
   // src/pages/about.tsx
   export default function About() {
     return <main><h1>About</h1></main>;
   }
   ```
2. The page is automatically available at `/about` (Next.js file-based routing).

## Adding a New Component

1. Create a file in `src/components/`:
   ```typescript
   // src/components/SearchBar.tsx
   interface SearchBarProps {
     onSearch: (query: string) => void;
   }

   export default function SearchBar({ onSearch }: SearchBarProps) {
     // Component logic
   }
   ```
2. Import it in any page or component:
   ```typescript
   import SearchBar from "@/components/SearchBar";
   ```

> **Note on `"use client"`:** The existing `Chat.tsx` includes the `"use client"` directive, but this project uses the **Pages Router** (not App Router), where all components are client-rendered by default. The directive is harmless but unnecessary for Pages Router components.

## Available Scripts

| Command         | Description                |
| --------------- | -------------------------- |
| `npm run dev`   | Start development server   |
| `npm run build` | Create production build    |
| `npm start`     | Start production server    |
| `npm run lint`  | Run Next.js ESLint checks  |

## Dependencies

| Package      | Version  | Purpose                    |
| ------------ | -------- | -------------------------- |
| react        | ^18.2.0  | UI library                 |
| react-dom    | ^18.2.0  | React DOM renderer         |
| next         | ^14.0.0  | React framework            |
| tailwindcss  | ^3.3.0   | Utility-first CSS          |
| typescript   | ^5.3.0   | Type safety                |
| postcss      | ^8.4.31  | CSS post-processing        |
| autoprefixer | ^10.4.16 | Vendor prefix automation   |

## See Also

- [Architecture](architecture.md) — How frontend communicates with backend
- [Configuration](configuration.md) — TypeScript and Tailwind config details
- [Getting Started](getting-started.md) — Running the frontend locally
