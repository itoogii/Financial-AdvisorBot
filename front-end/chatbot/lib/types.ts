import type { InferUITool, UIMessage } from "ai";
import { z } from "zod";
import type { ArtifactKind } from "@/components/artifact";

import type { getPrice } from "./ai/tools/get-stock-price";
import type { getStockTrend } from "./ai/tools/get-stock-trend";

import type { Suggestion } from "./db/schema/schema";

export type DataPart = { type: "append-message"; message: string };

export const messageMetadataSchema = z.object({
  createdAt: z.string(),
});

export type MessageMetadata = z.infer<typeof messageMetadataSchema>;

type getPriceTool = InferUITool<typeof getPrice>;
type getStockTrendTool = InferUITool<typeof getStockTrend>;

export type ChatTools = {
  getPrice: getPriceTool;
  getStockTrend: getStockTrendTool;
};

export type CustomUIDataTypes = {
  textDelta: string;
  imageDelta: string;
  sheetDelta: string;
  codeDelta: string;
  suggestion: Suggestion;
  appendMessage: string;
  id: string;
  title: string;
  kind: ArtifactKind;
  clear: null;
  finish: null;
  "chat-title": string;
};

export type ChatMessage = UIMessage<
  MessageMetadata,
  CustomUIDataTypes,
  ChatTools
>;

export type Attachment = {
  name: string;
  url: string;
  contentType: string;
};
