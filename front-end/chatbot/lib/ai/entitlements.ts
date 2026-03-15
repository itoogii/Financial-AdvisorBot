import { auth } from "@/app/lib/auth";
type UserType = typeof auth.$Infer.Session.user.type;

type Entitlements = {
  maxMessagesPerHour: number;
};

export const entitlementsByUserType: Record<UserType, Entitlements> = {
  /*
   * For users without an account
   */
  guest: {
    maxMessagesPerHour: 10,
  },

  /*
   * For users with an account
   */
  regular: {
    maxMessagesPerHour: 1000,
  },

  /*
   * TODO: For users with an account and a paid membership
   */
};
