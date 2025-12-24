import { clsx } from 'clsx';
import { motion } from 'framer-motion';
import { ArrowLeft, ArrowRight, Lock, Mail, User, Zap } from 'lucide-react';
import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { twMerge } from 'tailwind-merge';
import { useAuth } from '../context/AuthContext';

function cn(...inputs: (string | undefined | null | false)[]) {
    return twMerge(clsx(inputs));
}

export default function SignupPage() {
    const [formData, setFormData] = useState({
        email: '',
        password: '',
        first_name: '',
        last_name: ''
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const { signup } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setLoading(true);
        try {
            await signup(formData);
            navigate('/login');
        } catch (err: any) {
            console.error(err);
            setError('Signup failed. Email might be in use.');
        } finally {
            setLoading(false);
        }
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
            className="relative"
        >
            {/* Background glow effect */}
            <div className="absolute -inset-4 bg-blue-600/5 rounded-3xl blur-2xl -z-10" />
            
            {/* Back Button */}
            <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.5, delay: 0.1 }}
                className="mb-6"
            >
                <Link
                    to="/"
                    className="inline-flex items-center gap-2 text-gray-400 hover:text-white transition-colors duration-300 group"
                >
                    <motion.div
                        whileHover={{ x: -3 }}
                        className="flex items-center gap-2"
                    >
                        <ArrowLeft className="h-5 w-5 group-hover:text-blue-400 transition-colors" />
                        <span className="text-sm font-medium group-hover:text-blue-400 transition-colors">Back to Home</span>
                    </motion.div>
                </Link>
            </motion.div>
            
            {/* Firecrawl Agent Logo */}
            <motion.div
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.15 }}
                className="mb-8 flex justify-center lg:justify-start"
            >
                <Link
                    to="/"
                    className="flex items-center gap-3 group cursor-pointer"
                >
                    <motion.div
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        className="w-10 h-10 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-lg flex items-center justify-center shadow-lg shadow-blue-500/30 group-hover:shadow-blue-500/50 transition-all duration-300"
                    >
                        <Zap className="w-6 h-6 text-white" />
                    </motion.div>
                    <span className="text-xl font-bold text-white tracking-tight group-hover:text-blue-400 transition-colors duration-300">
                        Firecrawl Agent
                    </span>
                </Link>
            </motion.div>
            
            <div className="text-center lg:text-left mb-8">
                <motion.h2
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1 }}
                    className="text-4xl font-bold text-white mb-2"
                >
                    Create Account
                </motion.h2>
                <motion.p
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 }}
                    className="text-sm text-gray-400"
                >
                    Start building intelligent agents today
                </motion.p>
            </div>

            <div className="mt-8">
                <div className="mt-6">
                    <form onSubmit={handleSubmit} className="space-y-6">

                        <motion.div
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: 0.3 }}
                            className="flex gap-4"
                        >
                            <div className="flex-1">
                                <label htmlFor="first_name" className="block text-sm font-medium text-gray-300 mb-2">First Name</label>
                                <div className="mt-1 relative rounded-xl">
                                    <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                                        <User className="h-5 w-5 text-gray-500" />
                                    </div>
                                    <input
                                        name="first_name"
                                        id="first_name"
                                        required
                                        value={formData.first_name}
                                        onChange={handleChange}
                                        className="block w-full pl-12 pr-4 py-3 border border-white/10 rounded-xl bg-white/5 backdrop-blur-sm text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 transition-all duration-200 sm:text-sm"
                                        placeholder="John"
                                    />
                                </div>
                            </div>
                            <div className="flex-1">
                                <label htmlFor="last_name" className="block text-sm font-medium text-gray-300 mb-2">Last Name</label>
                                <div className="mt-1 relative rounded-xl">
                                    <input
                                        name="last_name"
                                        id="last_name"
                                        required
                                        value={formData.last_name}
                                        onChange={handleChange}
                                        className="block w-full px-4 py-3 border border-white/10 rounded-xl bg-white/5 backdrop-blur-sm text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 transition-all duration-200 sm:text-sm"
                                        placeholder="Doe"
                                    />
                                </div>
                            </div>
                        </motion.div>

                        <motion.div
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: 0.4 }}
                        >
                            <label htmlFor="email" className="block text-sm font-medium text-gray-300 mb-2">
                                Email address
                            </label>
                            <div className="mt-1 relative rounded-xl">
                                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                                    <Mail className="h-5 w-5 text-gray-500" aria-hidden="true" />
                                </div>
                                <input
                                    id="email"
                                    name="email"
                                    type="email"
                                    autoComplete="email"
                                    required
                                    value={formData.email}
                                    onChange={handleChange}
                                    className="block w-full pl-12 pr-4 py-3 border border-white/10 rounded-xl bg-white/5 backdrop-blur-sm text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 transition-all duration-200 sm:text-sm"
                                    placeholder="name@example.com"
                                />
                            </div>
                        </motion.div>

                        <motion.div
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: 0.5 }}
                        >
                            <label htmlFor="password" className="block text-sm font-medium text-gray-300 mb-2">
                                Password
                            </label>
                            <div className="mt-1 relative rounded-xl">
                                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                                    <Lock className="h-5 w-5 text-gray-500" aria-hidden="true" />
                                </div>
                                <input
                                    id="password"
                                    name="password"
                                    type="password"
                                    autoComplete="new-password"
                                    required
                                    value={formData.password}
                                    onChange={handleChange}
                                    className="block w-full pl-12 pr-4 py-3 border border-white/10 rounded-xl bg-white/5 backdrop-blur-sm text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 transition-all duration-200 sm:text-sm"
                                    placeholder="••••••••"
                                />
                            </div>
                        </motion.div>

                        {error && (
                            <motion.div
                                initial={{ opacity: 0, scale: 0.95 }}
                                animate={{ opacity: 1, scale: 1 }}
                                className="p-3 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm"
                            >
                                {error}
                            </motion.div>
                        )}

                        <motion.div
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.6 }}
                        >
                            <button
                                type="submit"
                                disabled={loading}
                                className={cn(
                                    "w-full flex justify-center items-center gap-2 py-3.5 px-4 border border-transparent rounded-xl text-sm font-semibold text-white bg-blue-600 hover:bg-blue-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-300 shadow-lg shadow-blue-500/30 hover:shadow-xl hover:shadow-blue-500/40 hover:scale-[1.02] active:scale-[0.98]",
                                    loading && "opacity-70 cursor-not-allowed"
                                )}
                            >
                                {loading ? (
                                    <>
                                        <motion.div
                                            animate={{ rotate: 360 }}
                                            transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                                            className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full"
                                        />
                                        <span>Creating account...</span>
                                    </>
                                ) : (
                                    <>
                                        Sign Up <ArrowRight className="h-4 w-4" />
                                    </>
                                )}
                            </button>
                        </motion.div>
                    </form>
                </div>

                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.7 }}
                    className="mt-6 text-center"
                >
                    <p className="text-sm text-gray-400">
                        Already have an account?{' '}
                        <Link to="/login" className="font-medium text-blue-400 hover:text-blue-300 transition-colors">
                            Sign in
                        </Link>
                    </p>
                </motion.div>

            </div>
        </motion.div>
    );
}
