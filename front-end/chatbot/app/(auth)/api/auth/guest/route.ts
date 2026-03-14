import { auth } from "@/app/lib/auth";
import { NextResponse } from "next/server";
import { headers } from "next/headers";

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const redirectUrl = searchParams.get("redirectUrl") || "/";

  const session = await auth.api.getSession({
    headers: await headers(),
  });

  if (session) {
    return NextResponse.redirect(new URL("/", request.url));
  }

  try {
    await auth.api.signInAnonymous({
      headers: await headers(),
    });

    return NextResponse.redirect(new URL(redirectUrl, request.url));
  } catch (error) {
    console.error("Guest login failed:", error);
    return NextResponse.redirect(new URL("/login", request.url));
  }
}
