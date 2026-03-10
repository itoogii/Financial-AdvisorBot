import { streamText, tool, UIMessage, convertToModelMessages } from 'ai';
import { ollama } from 'ai-sdk-ollama';
import { z } from 'zod';


export async function POST(req: Request) {
  const { messages }: { messages: UIMessage[] } = await req.json();

  const result = streamText({
    model: ollama("qwen3-unsloth-finadvisor"),
    messages: await convertToModelMessages(messages),
    tools: {
      oracle: tool({
        description: 'Predict the stock trend for a given stock symbol',
        inputSchema: z.object({
          stockSymbol: z.string().describe('The stock symbol to predict the trend for'),
        }),
        execute: async ({ stockSymbol }) => {
          // Call Backend API to get the stock trend prediction
          const signal = Math.random() > 0.5 ? 'up' : 'down';

          return {
            stockSymbol,
            signal,
          };
        },
      }),
    },
  });


  return result.toUIMessageStreamResponse();
}