import { motion } from 'framer-motion';
import { Outlet } from 'react-router-dom';
import { Zap } from 'lucide-react';

export const AuthLayout = () => {
    return (
        <div className="flex min-h-screen w-full bg-[#050505] overflow-hidden">
            {/* Left side - Login Form */}
            <div className="flex w-full flex-col justify-center px-4 py-12 sm:px-6 lg:flex-none lg:px-20 xl:px-24 relative z-10">
                <div className="mx-auto w-full max-w-sm lg:w-96">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.6 }}
                    >
                        <Outlet />
                    </motion.div>
                </div>
            </div>

            {/* Right side - Abstract Art / Branding */}
            <div className="relative hidden w-0 flex-1 lg:block">
                <div className="absolute inset-0 h-full w-full overflow-hidden">
                    {/* Animated gradient background */}
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ duration: 1 }}
                        className="absolute inset-0 bg-gradient-to-br from-blue-600/20 via-indigo-600/20 to-purple-600/20"
                    />
                    
                    {/* Animated blur circles */}
                    <motion.div
                        animate={{
                            scale: [1, 1.2, 1],
                            opacity: [0.3, 0.5, 0.3],
                        }}
                        transition={{
                            duration: 8,
                            repeat: Infinity,
                            ease: "easeInOut"
                        }}
                        className="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-600/30 rounded-full blur-[120px]"
                    />
                    <motion.div
                        animate={{
                            scale: [1, 1.3, 1],
                            opacity: [0.2, 0.4, 0.2],
                        }}
                        transition={{
                            duration: 10,
                            repeat: Infinity,
                            ease: "easeInOut",
                            delay: 1
                        }}
                        className="absolute bottom-1/4 right-1/4 w-[500px] h-[500px] bg-indigo-600/30 rounded-full blur-[120px]"
                    />
                    
                    {/* Content */}
                    <div className="relative h-full flex flex-col items-center justify-center text-white p-12 text-center z-10">
                        <motion.div
                            initial={{ scale: 0, rotate: -180 }}
                            animate={{ scale: 1, rotate: 0 }}
                            transition={{ 
                                type: "spring",
                                stiffness: 200,
                                damping: 15,
                                delay: 0.3
                            }}
                            className="mb-8"
                        >
                            <div className="w-16 h-16 bg-gradient-to-tr from-blue-600 to-indigo-600 rounded-2xl flex items-center justify-center shadow-2xl shadow-blue-500/50">
                                <Zap className="w-8 h-8 text-white" />
                            </div>
                        </motion.div>
                        
                        <motion.h1
                            initial={{ y: 20, opacity: 0 }}
                            animate={{ y: 0, opacity: 1 }}
                            transition={{ delay: 0.5, duration: 0.6 }}
                            className="text-5xl font-bold mb-4 bg-gradient-to-b from-white to-gray-400 bg-clip-text text-transparent"
                        >
                            FireCrawl Agent
                        </motion.h1>
                        <motion.p
                            initial={{ y: 20, opacity: 0 }}
                            animate={{ y: 0, opacity: 1 }}
                            transition={{ delay: 0.7, duration: 0.6 }}
                            className="text-lg text-gray-400 max-w-md"
                        >
                            Intelligent Document RAG & Analysis
                        </motion.p>
                        
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            transition={{ delay: 1, duration: 1 }}
                            className="mt-12 flex gap-4"
                        >
                            {['LlamaIndex', 'Firecrawl', 'FastAPI'].map((tech, i) => (
                                <motion.span
                                    key={tech}
                                    initial={{ opacity: 0, y: 10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    transition={{ delay: 1.2 + i * 0.1 }}
                                    className="px-4 py-2 rounded-full bg-white/5 border border-white/10 text-sm text-gray-300 backdrop-blur-sm"
                                >
                                    {tech}
                                </motion.span>
                            ))}
                        </motion.div>
                    </div>
                </div>
            </div>
        </div>
    );
};
