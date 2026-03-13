# AdvisorBot UI

I used nvm to manage my local node version installation. 
```shell
nvm install -lts
```

Installed the pnpm:
```shell
npm install -g pnpm
```

## Next.js and AI-SDK

### Installation

Follow along quickstart tutorial &#128073; [link](https://ai-sdk.dev/docs/getting-started/nextjs-app-router)

Added the Ollama provider:
```shell
pnpm add ai-sdk-ollama
```

Added AI Elements. Apparently, it added all components. 

```bash
pnpm dlx ai-elements@latest
```

AI Elements documentation shows that individual components installation as:
```bash
npx ai-elements@latest add prompt-input
```

Install better-auth
```bash
pnpm add better-auth
```

Install theme
https://ui.shadcn.com/docs/dark-mode/next
```bash
pnpm add next-themes
pnpm dlx shadcn@latest add sidebar
pnpm dlx shadcn@latest add sonner
```