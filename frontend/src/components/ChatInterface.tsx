import { Loader2, Send } from 'lucide-react';
import { useLayoutEffect, useRef, useState } from 'react';
import { sendMessage } from '../services/api';
import { Message } from './DashboardLayout';
import MessageBubble from './MessageBubble';
import ProcessDetails from './ProcessDetails';

interface ChatInterfaceProps {
  sessionId: string;
  messages: Message[];
  setMessages: (messages: Message[]) => void;
  isProcessing: boolean;
  setIsProcessing: (processing: boolean) => void;
  workflowLogs: string[];
  setWorkflowLogs: (logs: string[]) => void;
}

export default function ChatInterface({
  sessionId,
  messages,
  setMessages,
  isProcessing,
  setIsProcessing,
  workflowLogs,
  setWorkflowLogs,
}: ChatInterfaceProps) {
  const [input, setInput] = useState('');
  const containerRef = useRef<HTMLDivElement>(null);

  useLayoutEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTop =
        containerRef.current.scrollHeight;
    }
  }, [messages, isProcessing]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isProcessing) return;

    const userMessage: Message = {
      role: 'user',
      content: input.trim(),
      logIndex: workflowLogs.length,
    };

    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInput('');
    setIsProcessing(true);

    try {
      const response = await sendMessage(sessionId, input.trim());

      if (response.logs) {
        setWorkflowLogs([...workflowLogs, response.logs]);
      }

      const assistantMessage: Message = {
        role: 'assistant',
        content: response.response,
        logIndex: userMessage.logIndex,
      };

      setMessages([...newMessages, assistantMessage]);
    } catch (error: any) {
      setMessages([
        ...newMessages,
        {
          role: 'assistant',
          content:
            error.response?.data?.detail ||
            error.message ||
            'Failed to process request',
        },
      ]);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="flex flex-col h-full relative">
      {/* Header */}
      <header className="bg-black/50 backdrop-blur-xl border-b border-white/10 p-6">
        <h1 className="text-3xl font-bold text-center text-white">
          🤖 IntelliChat Assistant
        </h1>
        <p className="text-center text-gray-400">
          Your intelligent document companion powered by RAG
        </p>
      </header>

      {/* Messages */}
      <div
        ref={containerRef}
        className="flex-1 min-h-0 overflow-y-auto p-6 space-y-4 scrollbar-hide"
      >
        {messages.length === 0 && (
          <p className="text-center text-gray-400 mt-12">
            Ask a question about your document to begin
          </p>
        )}

        {messages.map((message, index) => (
          <div key={index} className="space-y-2">
            <MessageBubble message={message} />

            {message.role === 'assistant' &&
              message.logIndex !== undefined &&
              workflowLogs[message.logIndex] && (
                <ProcessDetails
                  logIndex={message.logIndex}
                  logs={workflowLogs}
                />
              )}
          </div>
        ))}



        {isProcessing && (
          <div className="flex items-center gap-2 text-gray-400">
            <Loader2 className="h-5 w-5 animate-spin text-blue-500" />
            🤔 Thinking...
          </div>
        )}
      </div>

      {/* Input */}
      <form
        onSubmit={handleSubmit}
        className="p-6 border-t border-white/10 bg-black/50 backdrop-blur-xl"
      >
        <div className="flex gap-4 max-w-4xl mx-auto">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question about your document..."
            className="flex-1 px-4 py-3 rounded-xl bg-white/5 text-white border border-white/10 focus:ring-2 focus:ring-blue-500"
            disabled={isProcessing}
          />
          <button
            type="submit"
            disabled={!input.trim() || isProcessing}
            className="px-6 py-3 bg-blue-600 text-white rounded-xl disabled:opacity-50 flex items-center gap-2"
          >
            <Send className="h-5 w-5" />
            Send
          </button>
        </div>
      </form>
    </div>
  );
}
