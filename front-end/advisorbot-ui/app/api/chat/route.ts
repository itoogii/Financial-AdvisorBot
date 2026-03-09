import { streamText, UIMessage, convertToModelMessages } from 'ai';
import { yourProvider } from "your-custom-provider";

export async function POST(req: Request) {
  const { messages }: { messages: UIMessage[] } = await req.json();

  const result = streamText({
    model: yourProvider("your-model-id"),
    messages: await convertToModelMessages(messages),
  });

  return result.toUIMessageStreamResponse();
}