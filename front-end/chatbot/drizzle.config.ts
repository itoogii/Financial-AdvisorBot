import { config } from "dotenv";
import { defineConfig } from "drizzle-kit";

config({
  path: ".env",
});

if (!process.env.DATABASE_URL) {
  throw new Error("env.process.DATABASE_URL is not set");
}

export default defineConfig({
  schema: "./lib/db/schema",
  out: "./lib/db/migrations",
  dialect: "sqlite",
  dbCredentials: {
    // biome-ignore lint: Forbidden non-null assertion.
    url: process.env.DATABASE_URL,
  },
});
