import { compare } from "bcrypt-ts";
// import NextAuth, { type DefaultSession } from "next-auth";
import { betterAuth } from "better-auth";
import { drizzleAdapter } from "better-auth/adapters/drizzle";
import { db } from "@/lib/db/client"; // your drizzle instance
import { nextCookies } from "better-auth/next-js";


export const auth = betterAuth({
  database: drizzleAdapter(db, {
        provider: "sqlite", // or "mysql", "pg"
    }),
  emailAndPassword: {    
        enabled: true,
        autoSignIn: false //defaults to true
    },
  user: {
      additionalFields: {
        type: {
          type: "string", 
          required: true,
          defaultValue: "regular"
        }
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
            refreshCache: {
                updateAge: 60 // Refresh when 60 seconds remain before expiry
            }
        },
    },
    plugins: [nextCookies()] 
});
