import { ChatView } from "@/components/chat/chat-view";

interface ConversationPageProps {
  params: Promise<{ id: string }>;
}

/** A single conversation thread (PRD P2). Deep-linkable by id. */
export default async function ConversationPage({
  params,
}: ConversationPageProps) {
  const { id } = await params;
  return <ChatView conversationId={id} />;
}
