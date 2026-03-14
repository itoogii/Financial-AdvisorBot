// Curated list of top models from Vercel AI Gateway
export const DEFAULT_CHAT_MODEL = "qwen3-unsloth-finadvisor:latest";

export type ChatModel = {
  id: string;
  name: string;
  provider: string;
  description: string;
};

export const chatModels: ChatModel[] = [
  // Anthropic
  {
    id: "qwen3-unsloth-finadvisor:latest",
    name: "Financial Advisor model",
    provider: "FinAdvisor",
    description: "Great for financial consultations and advice.",
  },

];

// Group models by provider for UI
export const allowedModelIds = new Set(chatModels.map((m) => m.id));

export const modelsByProvider = chatModels.reduce(
  (acc, model) => {
    if (!acc[model.provider]) {
      acc[model.provider] = [];
    }
    acc[model.provider].push(model);
    return acc;
  },
  {} as Record<string, ChatModel[]>
);