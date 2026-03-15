import { tool } from "ai";
import { z } from "zod";

export const getPrice = tool({
  description: "Get the last closing price of the stock ticker.",
  inputSchema: z.object({
    ticker: z.string().describe("Ticker symbol for the stock, such as AAPL"),
  }),
  strict: true,
  execute: async ({ ticker }) => {
    // A call to Backend API to get the stock price
    const price_info = await fetch(`http://localhost:8000/last_price/${ticker}`)
      .then((res) => res.json())
      .then((data) => data.response);
    return price_info;
  },
});
