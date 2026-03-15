import { createAuthClient } from "better-auth/react";
import { anonymousClient } from "better-auth/client/plugins";
import { nextCookies } from "better-auth/next-js";

export const authClient = createAuthClient({
  //   baseURL: "http://localhost:3000",
  plugins: [anonymousClient(), nextCookies()],
});
export type Session = typeof authClient.$Infer.Session;
export type User = typeof authClient.$Infer.Session.user;
