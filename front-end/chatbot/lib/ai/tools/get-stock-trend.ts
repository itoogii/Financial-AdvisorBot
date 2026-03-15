import { tool } from "ai";
import { z } from "zod";

export const getStockTrend = tool({
  description:
    "Predict the stock trend (rise/fall/neutral signal) for a given stock ticker symbol like AAPL, TSLA, MSFT.",
  inputSchema: z.object({
    stockSymbol: z
      .string()
      .describe("Ticker symbol for the stock, such as AAPL"),
  }),
  strict: true,
  // inputExamples: [
  //   { input: { stockSymbol: 'AAPL' } },
  //   { input: { stockSymbol: 'googl' } },
  //   { input: { stockSymbol: 'Amzn' } },
  // ], oops only Anthropic support this. Keeping this as it looks cool :)
  execute: async ({ stockSymbol }) => {
    // A call to Backend API to get the stock trend prediction
    const signal = await fetch(`http://localhost:8000/estimate/${stockSymbol}`)
      .then((res) => res.json())
      .then((data) => data.response);
    return signal;
  },
});
