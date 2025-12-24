import { Bot, User } from 'lucide-react';
import { Message } from './DashboardLayout';

interface MessageBubbleProps {
  message: Message;
}

import { motion } from 'framer-motion';

export default function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === 'user';

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}
    >
      <div
        className={`flex gap-3 max-w-3xl ${isUser ? 'flex-row-reverse' : 'flex-row'
          }`}
      >
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.1, type: "spring" }}
          className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${isUser
              ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/30'
              : 'bg-white/5 border border-white/10 text-gray-300'
            }`}
        >
          {isUser ? (
            <User className="h-5 w-5" />
          ) : (
            <Bot className="h-5 w-5" />
          )}
        </motion.div>
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.15 }}
          className={`rounded-2xl px-4 py-3 backdrop-blur-sm ${isUser
              ? 'bg-blue-600 text-white rounded-tr-none shadow-lg shadow-blue-500/30'
              : 'bg-white/5 border border-white/10 text-gray-300 rounded-tl-none'
            }`}
        >
          <p className="whitespace-pre-wrap break-words">{message.content}</p>
        </motion.div>
      </div>
    </motion.div>
  );
}

