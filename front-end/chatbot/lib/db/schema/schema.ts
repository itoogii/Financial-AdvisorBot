import { type InferSelectModel } from "drizzle-orm";
import {
  sqliteTable,
  text,
  integer,
  primaryKey,
  foreignKey,
} from "drizzle-orm/sqlite-core";
import { user } from "./auth-schema";

export const chat = sqliteTable("Chat", {
  id: text("id").primaryKey().notNull(),
  createdAt: integer("createdAt", { mode: "timestamp" }).notNull(),
  title: text("title").notNull(),
  userId: text("userId")
    .notNull()
    .references(() => user.id, { onDelete: "cascade" }),
  visibility: text("visibility")
    .$type<"public" | "private">()
    .notNull()
    .default("private"),
});

export type Chat = InferSelectModel<typeof chat>;

export const message = sqliteTable("Message_v2", {
  id: text("id").primaryKey().notNull(),
  chatId: text("chatId")
    .notNull()
    .references(() => chat.id),
  role: text("role").notNull(),
  // SQLite doesn't have a native JSON type, Drizzle stores it as text
  parts: text("parts", { mode: "json" }).notNull(),
  attachments: text("attachments", { mode: "json" }).notNull(),
  createdAt: integer("createdAt", { mode: "timestamp" }).notNull(),
});

export type DBMessage = InferSelectModel<typeof message>;

export const vote = sqliteTable(
  "Vote_v2",
  {
    chatId: text("chatId")
      .notNull()
      .references(() => chat.id),
    messageId: text("messageId")
      .notNull()
      .references(() => message.id),
    isUpvoted: integer("isUpvoted", { mode: "boolean" }).notNull(),
  },
  (t) => [primaryKey({ columns: [t.chatId, t.messageId] })],
);

export type Vote = InferSelectModel<typeof vote>;

export const document = sqliteTable(
  "Document",
  {
    id: text("id").notNull(),
    createdAt: integer("createdAt", { mode: "timestamp" }).notNull(),
    title: text("title").notNull(),
    content: text("content"),
    kind: text("kind")
      .$type<"text" | "code" | "image" | "sheet">()
      .notNull()
      .default("text"),
    userId: text("userId")
      .notNull()
      .references(() => user.id, { onDelete: "cascade" }),
  },
  (t) => [primaryKey({ columns: [t.id, t.createdAt] })],
);

export type Document = InferSelectModel<typeof document>;

export const suggestion = sqliteTable(
  "Suggestion",
  {
    id: text("id").primaryKey().notNull(),
    documentId: text("documentId").notNull(),
    documentCreatedAt: integer("documentCreatedAt", {
      mode: "timestamp",
    }).notNull(),
    originalText: text("originalText").notNull(),
    suggestedText: text("suggestedText").notNull(),
    description: text("description"),
    isResolved: integer("isResolved", { mode: "boolean" })
      .notNull()
      .default(false),
    userId: text("userId")
      .notNull()
      .references(() => user.id, { onDelete: "cascade" }),
    createdAt: integer("createdAt", { mode: "timestamp" }).notNull(),
  },
  (t) => [
    primaryKey({ columns: [t.id] }),
    foreignKey({
      columns: [t.documentId, t.documentCreatedAt],
      foreignColumns: [document.id, document.createdAt],
    }),
  ],
);

export type Suggestion = InferSelectModel<typeof suggestion>;

export const stream = sqliteTable("Stream", {
  id: text("id").primaryKey().notNull(),
  chatId: text("chatId")
    .notNull()
    .references(() => chat.id),
  createdAt: integer("createdAt", { mode: "timestamp" }).notNull(),
});

export type Stream = InferSelectModel<typeof stream>;
