import { streamText, tool, UIMessage, convertToModelMessages, stepCountIs } from 'ai';
import { ollama } from 'ai-sdk-ollama';
import { z } from 'zod';


export async function POST(req: Request) {
  const { messages }: { messages: UIMessage[] } = await req.json();

  const result = streamText({
    model: ollama("qwen3-unsloth-finadvisor"),
    system: [
      'You are Hermes, a financial advisor.',
      'If user asks stock direction/performance/trend/signal/forecast for a symbol/ticker, call the StockTrend tool first.',
      'Do not guess a trend when StockTrend is available.',
      'If you do call a tool, do not output interim text like "let me check"; call the tool immediately.',
      "If you don't have a stock symbol, ask for the ticker symbol.",
    ].join('\n'),
    messages: await convertToModelMessages(messages),
    tools: {
      StockTrend: tool({
        description: 'Predict the stock trend (rise/fall/neutral signal) for a given stock ticker symbol like AAPL, TSLA, MSFT.',
        inputSchema: z.object({
          stockSymbol: z.string().describe('Stock ticker symbol, e.g., AAPL'),
        }),
        strict: true,
        // inputExamples: [
        //   { input: { stockSymbol: 'AAPL' } },
        //   { input: { stockSymbol: 'googl' } },
        //   { input: { stockSymbol: 'Amzn' } },
        // ], oops only Anthropic support this. Keeping this as it looks cool :)
        execute: async ({ stockSymbol }) => {
          // Call Backend API to get the stock trend prediction
          const signal = await fetch(`http://localhost:8000/estimate/${stockSymbol}`)
            .then(res => res.json())
            .then(data => data.signal);
          return {
            stockSymbol,
            signal,
          };
        },
      }),
    },
    stopWhen: stepCountIs(5),
    toolChoice: 'auto',
  });


  return result.toUIMessageStreamResponse();
}