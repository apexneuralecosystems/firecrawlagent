import { motion } from 'framer-motion';

export default function WelcomeScreen() {
  return (
    <div className="flex-1 flex items-center justify-center p-8 relative z-10">
      <div className="text-center max-w-2xl">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="mb-8"
        >
          <h1 className="text-5xl font-bold text-white mb-4 bg-gradient-to-b from-white to-gray-400 bg-clip-text text-transparent">
            🤖 IntelliChat Assistant
          </h1>
          <p className="text-xl text-gray-400">
            Your intelligent document companion powered by RAG
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="relative bg-white/[0.03] backdrop-blur-sm rounded-3xl border border-white/10 p-12 shadow-2xl"
        >
          {/* Glow effect */}
          <div className="absolute -inset-1 bg-blue-600/10 rounded-3xl blur-xl -z-10" />
          
          <motion.h2
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="text-2xl font-semibold text-white mb-4"
          >
            👋 Welcome to IntelliChat!
          </motion.h2>
          <motion.p
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="text-lg text-gray-400 mb-6 leading-relaxed"
          >
            To get started, please upload a PDF document using the sidebar on the left.
            <br />
            Once uploaded, you can ask questions about your document and I'll help you find answers.
          </motion.p>
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.6, type: "spring" }}
            className="text-6xl mb-6"
          >
            📄💬🔍
          </motion.div>
          
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.7 }}
            className="mt-8 pt-8 border-t border-white/10"
          >
            <div className="flex justify-center items-center gap-8 flex-wrap">
              {[
                { name: 'FireCrawl', logo: 'https://mintlify.s3.us-west-1.amazonaws.com/firecrawl/logo/logo-dark.png' },
                { name: 'Beam', logo: 'https://i.ibb.co/m5RtcvnY/beam-logo.png' },
                { name: 'Milvus', logo: 'https://milvus.io/images/layout/milvus-logo.svg' }
              ].map((tech, i) => (
                <motion.div
                  key={tech.name}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.8 + i * 0.1 }}
                  whileHover={{ scale: 1.1 }}
                  className="text-center"
                >
                  <div className="bg-white/5 rounded-xl p-3 mb-2 border border-white/10">
                    <img 
                      src={tech.logo} 
                      alt={tech.name} 
                      className="h-12 mx-auto"
                    />
                  </div>
                  <p className="text-xs text-gray-500">{tech.name}</p>
                </motion.div>
              ))}
            </div>
          </motion.div>
        </motion.div>
      </div>
    </div>
  );
}

