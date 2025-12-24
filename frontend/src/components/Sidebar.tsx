import { AlertCircle, ArrowUp, CheckCircle2, Info, LogOut, RotateCcw, Upload, User } from 'lucide-react';
import { motion } from 'framer-motion';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { deleteSession, uploadDocument } from '../services/api';

interface SidebarProps {
  onDocumentUpload: (sessionId: string) => void;
  onReset: () => void;
  sessionId: string | null;
}

export default function Sidebar({ onDocumentUpload, onReset, sessionId }: SidebarProps) {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (!file.name.endsWith('.pdf')) {
      setError('Only PDF files are supported');
      setSuccess(false);
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      setError('File size must be less than 10MB');
      setSuccess(false);
      return;
    }

    setUploading(true);
    setError(null);
    setSuccess(false);

    try {
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await uploadDocument(formData);
      onDocumentUpload(response.session_id);
      setSuccess(true);
      setError(null);
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to upload document';
      setError(errorMessage);
      setSuccess(false);
    } finally {
      setUploading(false);
    }
  };

  const handleReset = async () => {
    if (sessionId) {
      try {
        await deleteSession(sessionId);
      } catch (err) {
        console.error('Failed to delete session:', err);
      }
    }
    onReset();
    setError(null);
    setSuccess(false);
  };

  return (
    <aside className="w-80 bg-black/50 backdrop-blur-xl border-r border-white/10 flex flex-col shadow-lg relative z-10">
      {/* Header */}
      <div className="p-6 border-b border-white/10">
        <motion.h2
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-xl font-bold text-white text-center mb-4"
        >
          Document Assistant
        </motion.h2>
        {user && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="flex items-center gap-2 px-3 py-2.5 bg-white/5 rounded-xl border border-white/10"
          >
            <User className="h-4 w-4 text-gray-400 flex-shrink-0" />
            <span className="text-sm text-gray-300 truncate font-medium">
              {user.email}
            </span>
          </motion.div>
        )}
      </div>

      {/* Upload Section */}
      <div className="p-6 flex-1 overflow-y-auto scrollbar-hide">
        <motion.label
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="block group cursor-pointer"
        >
          <div className="flex flex-col items-center justify-center rounded-2xl border-2 border-dashed border-white/10 px-6 py-12 hover:border-blue-500/50 transition-all duration-300 bg-white/5 hover:bg-white/[0.08] backdrop-blur-sm group-hover:scale-[1.02]">
            <div className="text-center">
              <motion.div
                animate={{ y: [0, -5, 0] }}
                transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
              >
                <ArrowUp className="mx-auto h-10 w-10 text-gray-400 group-hover:text-blue-400 transition-colors duration-300 mb-4" />
              </motion.div>
              <div className="flex items-center justify-center gap-1 text-sm leading-6 text-gray-400">
                <span className="font-semibold text-blue-400 hover:text-blue-300 transition-colors">
                  Upload a PDF
                </span>
                <span>or drag and drop</span>
              </div>
              <p className="text-xs text-gray-500 mt-2">
                PDF up to 10MB
              </p>
            </div>
          </div>
          <input
            type="file"
            className="sr-only"
            accept=".pdf"
            onChange={handleFileUpload}
            disabled={uploading}
          />
        </motion.label>

        {error && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="mt-4 p-3.5 bg-red-500/10 border border-red-500/20 rounded-xl"
          >
            <div className="flex items-start gap-2.5 text-red-400 text-sm">
              <AlertCircle className="h-4 w-4 flex-shrink-0 mt-0.5" />
              <span className="flex-1">{error}</span>
            </div>
          </motion.div>
        )}

        {uploading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="mt-4 text-center"
          >
            <div className="inline-flex items-center gap-2.5 text-sm text-gray-400">
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                className="rounded-full h-4 w-4 border-2 border-blue-500 border-t-transparent"
              />
              <span className="font-medium">Processing document...</span>
            </div>
          </motion.div>
        )}

        {success && sessionId && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="mt-4 p-3.5 bg-green-500/10 border border-green-500/20 rounded-xl"
          >
            <div className="flex items-center gap-2.5 text-green-400 text-sm">
              <CheckCircle2 className="h-4 w-4 flex-shrink-0" />
              <span className="font-medium">Ready to Chat!</span>
            </div>
          </motion.div>
        )}
      </div>

      {/* Footer Section */}
      <div className="p-6 border-t border-white/10 space-y-3">
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="mb-4"
        >
          <h3 className="text-sm font-semibold text-white mb-3 flex items-center gap-2">
            <Info className="h-4 w-4 text-blue-400" />
            About This Tool
          </h3>
          <ul className="space-y-2 text-xs text-gray-400 leading-relaxed">
            <li className="flex items-start gap-2">
              <span className="text-blue-400 mt-0.5">•</span>
              <span>Document analysis</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-blue-400 mt-0.5">•</span>
              <span>Web search capabilities</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-blue-400 mt-0.5">•</span>
              <span>Advanced AI reasoning</span>
            </li>
          </ul>
        </motion.div>
        
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={handleReset}
          className="w-full flex items-center justify-center gap-2 px-4 py-2.5 bg-white/5 hover:bg-white/10 text-gray-300 rounded-xl transition-all duration-300 font-medium border border-white/10 hover:border-white/20"
        >
          <RotateCcw className="h-4 w-4" />
          Reset Conversation
        </motion.button>
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={handleLogout}
          className="w-full flex items-center justify-center gap-2 px-4 py-2.5 bg-red-500/10 hover:bg-red-500/20 text-red-400 rounded-xl transition-all duration-300 font-medium border border-red-500/20 hover:border-red-500/30"
        >
          <LogOut className="h-4 w-4" />
          Logout
        </motion.button>
      </div>
    </aside>
  );
}

