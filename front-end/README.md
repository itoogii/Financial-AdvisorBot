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

# Chatbot Template

[Upgraded next.js to 16.1.6](https://nextjs.org/docs/app/getting-started/upgrading)
[Upgraded drizzle ORM](https://orm.drizzle.team/docs/get-started/postgresql-new)
[Replaced Next-auth with Better Auth](https://better-auth.com/docs/installation)
[Installed SQLite Better-SQL3](https://orm.drizzle.team/docs/get-started-sqlite)

## Prettier and TailwindCSS prettie

```bash
pnpm add --save-dev --save-exact prettier
pnpm add -D prettier-plugin-tailwindcss
```

## Better Auth

Added a new variable using

```bash
openssl rand -base64 32
```

```env
BETTER_AUTH_SECRET=
```

Generated the schema for better-auth using:

```bash
npm dlx auth@latest generate
```

Generated and migrated:

```bash
pnpm exec drizzle-kit generate
pnpm exec drizzle-kit migrate
```

pnpm add ai-sdk-ollama

Links:
https://github.com/seaweedfs/seaweedfs/wiki/nodejs-with-Seaweed-S3
AWS SDK Client Credentials
https://github.com/aws/aws-sdk-js-v3/blob/main/supplemental-docs/CLIENTS.md
https://docs.aws.amazon.com/AWSJavaScriptSDK/v3/latest/client/s3/command/PutObjectCommand/

### SQLite

The sqlite is initialized through the drizzle migration.

To remove the user and session database entries:

1. Installed the sqlite3 on local system

```shell
sudo apt install sqlite3
```

2. Used Sqlite3 to manage the database table entries for fresh start after tests.

```shell
SELECT * FROM user;
SELECT * FROM session;
DELETE FROM user;
DELETE FROM session;
.quit
```
