import { Loader2, Send } from 'lucide-react';
import { useEffect, useRef, useState } from 'react';
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
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
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

      // Store logs if available
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
      const errorMessage: Message = {
        role: 'assistant',
        content: `Error: ${error.response?.data?.detail || error.message || 'Failed to process request'}`,
      };
      setMessages([...newMessages, errorMessage]);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="flex flex-col h-full relative">
      {/* Header */}
      <header className="relative z-10 bg-black/50 backdrop-blur-xl border-b border-white/10 p-6 shadow-lg">
        <div className="text-center">
          <h1 className="text-3xl font-bold mb-2 bg-gradient-to-b from-white to-gray-400 bg-clip-text text-transparent">
            🤖 IntelliChat Assistant
          </h1>
          <p className="text-gray-400">Your intelligent document companion powered by RAG</p>
        </div>
      </header>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4 scrollbar-hide relative z-10">
        {messages.length === 0 && (
          <div className="text-center text-gray-400 mt-12">
            <p className="text-lg">Start a conversation by asking a question about your document!</p>
          </div>
        )}

        {messages.map((message, index) => (
          <div key={index} className="space-y-2">
            <MessageBubble message={message} />
            {message.logIndex !== undefined && workflowLogs[message.logIndex] && (
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
            <span>🤔 Thinking...</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <form onSubmit={handleSubmit} className="relative z-10 p-6 border-t border-white/10 bg-black/50 backdrop-blur-xl">
        <div className="flex gap-4 max-w-4xl mx-auto">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question about your document..."
            className="flex-1 px-4 py-3 border border-white/10 rounded-xl bg-white/5 backdrop-blur-sm text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 transition-all duration-200"
            disabled={isProcessing}
            autoFocus
          />
          <button
            type="submit"
            disabled={!input.trim() || isProcessing}
            className="px-6 py-3 bg-blue-600 hover:bg-blue-500 text-white rounded-xl disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 flex items-center gap-2 font-semibold shadow-lg shadow-blue-500/30 hover:shadow-xl hover:shadow-blue-500/40 hover:scale-[1.02] active:scale-[0.98]"
          >
            <Send className="h-5 w-5" />
            Send
          </button>
        </div>
      </form>
    </div>
  );
}

