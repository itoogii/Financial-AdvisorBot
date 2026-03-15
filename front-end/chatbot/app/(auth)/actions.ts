"use server";

import { z } from "zod";

import { auth } from "@/app/lib/auth";
import { redirect } from "next/navigation";

const loginSchema = z.object({
  email: z.email(),
  password: z.string().min(6),
});
const signupSchema = z.object({
  name: z.string().min(2).max(100),
  email: z.email(),
  password: z.string().min(6),
});

export type LoginActionState = {
  status: "idle" | "in_progress" | "success" | "failed" | "invalid_data";
};

export const login = async (
  _: LoginActionState,
  formData: FormData,
): Promise<LoginActionState> => {
  try {
    const validatedData = loginSchema.parse({
      email: formData.get("email"),
      password: formData.get("password"),
    });

    await auth.api.signInEmail({
      body: {
        email: validatedData.email,
        password: validatedData.password,
      },
    });

    return { status: "success" };
  } catch (error) {
    if (error instanceof z.ZodError) {
      return { status: "invalid_data" };
    }

    return { status: "failed" };
  }
};

export type RegisterActionState = {
  status:
    | "idle"
    | "in_progress"
    | "success"
    | "failed"
    | "user_exists"
    | "invalid_data";
};

export const register = async (
  _: RegisterActionState,
  formData: FormData,
): Promise<RegisterActionState> => {
  try {
    const validatedData = signupSchema.parse({
      name: formData.get("name"),
      email: formData.get("email"),
      password: formData.get("password"),
    });

    await auth.api.signUpEmail({
      body: {
        name: validatedData.name, // required
        email: validatedData.email, // required
        password: validatedData.password, // required
      },
    });
    // await auth.api.signInEmail(
    //       {
    //           body: {
    //               email: validatedData.email,
    //               password: validatedData.password,
    //           }
    //       } );

    return { status: "success" };
  } catch (error: any) {
    if (error instanceof z.ZodError) {
      return { status: "invalid_data" };
    }
    if (error.code === "USER_ALREADY_EXISTS") {
      return { status: "user_exists" };
    }

    return { status: "failed" };
  }
};
