import { streamText, generateText, tool, UIMessage, convertToModelMessages } from 'ai';
import { ollama } from 'ai-sdk-ollama';


export async function POST(req: Request) {
  const { messages }: { messages: UIMessage[] } = await req.json();

  const result = streamText({
    model: ollama("qwen3-unsloth-finadvisor"),
    messages: await convertToModelMessages(messages),
  });
//  const { textStream } = await streamText({
//   model: ollama('llama3.2'),39
//   tools: { /* your tools */ },
//   prompt: 'Stream with tools'
// });

  return result.toUIMessageStreamResponse();
}