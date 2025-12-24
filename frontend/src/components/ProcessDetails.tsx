import { motion, AnimatePresence } from 'framer-motion';
import { useState } from 'react';
import { ChevronDown, ChevronUp, FileText } from 'lucide-react';

interface ProcessDetailsProps {
  logIndex: number;
  logs: string[];
}

export default function ProcessDetails({ logIndex, logs }: ProcessDetailsProps) {
  const [isExpanded, setIsExpanded] = useState(false);
  const logContent = logs[logIndex];

  if (!logContent) return null;

  return (
    <div className="max-w-3xl mx-auto">
      <motion.button
        whileHover={{ scale: 1.01 }}
        whileTap={{ scale: 0.99 }}
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full flex items-center justify-between px-4 py-2 bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl transition-all duration-300 text-sm text-gray-300"
      >
        <div className="flex items-center gap-2">
          <FileText className="h-4 w-4 text-blue-400" />
          <span>View Process Details</span>
        </div>
        <motion.div
          animate={{ rotate: isExpanded ? 180 : 0 }}
          transition={{ duration: 0.3 }}
        >
          <ChevronDown className="h-4 w-4" />
        </motion.div>
      </motion.button>
      <AnimatePresence>
        {isExpanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3 }}
            className="overflow-hidden"
          >
            <div className="mt-2 p-4 bg-black/40 border border-white/10 rounded-xl overflow-x-auto backdrop-blur-sm">
              <pre className="text-xs text-gray-300 font-mono whitespace-pre-wrap">
                {logContent}
              </pre>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

