import { betterAuth } from "better-auth";
import { drizzleAdapter } from "better-auth/adapters/drizzle";
import { db } from "@/lib/db/client"; // drizzle database client
import * as schema from "@/lib/db/schema/auth-schema";
import { nextCookies } from "better-auth/next-js";
import { anonymous } from "better-auth/plugins"; // https://better-auth.com/docs/plugins/anonymous
//
export const auth = betterAuth({
  database: drizzleAdapter(db, {
    provider: "sqlite", // or "mysql", "pg"
    schema: schema,
  }),
  emailAndPassword: {
    enabled: true,
    autoSignIn: false, //defaults to true
  },
  user: {
    additionalFields: {
      type: {
        type: "string",
        required: true,
        defaultValue: "regular",
      },
    },
  },
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days
    updateAge: 60 * 60 * 24, // 1 day (every 1 day the session expiration is updated)
    freshAge: 0, // Disable freshness check
    cookieCache: {
      enabled: true,
      maxAge: 5 * 60, // Cache duration in seconds (5 minutes)
      strategy: "jwt", // "compact" or "jwe"
      // refreshCache: {
      //   updateAge: 60, // Refresh when 60 seconds remain before expiry
      // },
    },
  },
  plugins: [anonymous(), nextCookies()],
});
