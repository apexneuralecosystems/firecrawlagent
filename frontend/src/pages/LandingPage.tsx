import { AnimatePresence, motion } from 'framer-motion';
import {
    ArrowRight,
    CheckCircle2,
    Cpu,
    Database,
    // Github,
    Globe,
    Linkedin,
    Menu,
    Minus,
    Play,
    Plus,
    Search,
    Sparkles,
    Star,
    // Twitter,
    X,
    Zap
} from 'lucide-react';
import { useState } from 'react';
import { Link } from 'react-router-dom';
import { subscribeNewsletter } from '../services/api';

const LandingPage = () => {
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const [activeFaq, setActiveFaq] = useState<number | null>(null);
    const [newsletterEmail, setNewsletterEmail] = useState('');
    const [newsletterStatus, setNewsletterStatus] = useState<{ type: 'success' | 'error' | null; message: string }>({ type: null, message: '' });
    const [newsletterLoading, setNewsletterLoading] = useState(false);

    const navLinks = [
        { name: 'Features', href: '#features' },
        { name: 'Workflow', href: '#workflow' },
        { name: 'Technology', href: '#technology' },
        { name: 'Pricing', href: '#pricing' },
        { name: 'FAQ', href: '#faq' },
    ];

    const technologies = [
        'LlamaIndex', 'Firecrawl', 'FastAPI', 'React', 'OpenAI', 'Gemini', 'Milvus', 'Qdrant', 'ChromaDB'
    ];

    const benefits = [
        {
            title: 'Agentic RAG Engine',
            description: 'Advanced multi-agent workflow that coordinates retrieval and generation for superior accuracy.',
            icon: <Cpu className="w-6 h-6 text-blue-500" />,
            className: 'md:col-span-2 md:row-span-1',
        },
        {
            title: 'Web Search Integration',
            description: 'Beyond local documents. Real-time web context via Firecrawl API when static data isn\'t enough.',
            icon: <Globe className="w-6 h-6 text-green-500" />,
            className: 'md:col-span-1 md:row-span-1',
        },
        {
            title: 'LlamaIndex Powered',
            description: 'Production-grade document processing, chunking, and indexing for complex PDF structures.',
            icon: <Database className="w-6 h-6 text-purple-500" />,
            className: 'md:col-span-1 md:row-span-1',
        },
        {
            title: 'Intelligent Filtering',
            description: 'Automated relevance filtering ensures your LLM only sees the most important context.',
            icon: <Search className="w-6 h-6 text-yellow-500" />,
            className: 'md:col-span-2 md:row-span-1',
        },
    ];

    const pricing = [
        {
            name: 'Community',
            price: '$0',
            description: 'Perfect for local development and individuals.',
            features: ['Local LLM Support', 'Standard Indexing', 'Core Agentic Workflow', 'Community Support'],
            cta: 'Explore Community',
            popular: false,
        },
        {
            name: 'Pro',
            price: '$49',
            description: 'For power users needing real-time web context.',
            features: ['Firecrawl Integration', 'Advanced Filtering', 'Priority Support', 'Cloud LLM Direct Access', 'Unlimited Sessions'],
            cta: 'Get Started with Pro',
            popular: true,
        },
        {
            name: 'Enterprise',
            price: 'Custom',
            description: 'Scaleable RAG infrastructure for large datasets.',
            features: ['Milvus/Qdrant Clusters', 'Custom Agent Logic', 'Dedicated Infrastructure', 'SLA Guarantee', 'SSO Integration'],
            cta: 'Contact Sales',
            popular: false,
        },
    ];

    const testimonials = [
        {
            name: 'Dr. Sarah James',
            role: 'AI Research Lead',
            content: 'The combination of LlamaIndex and Firecrawl is genius. It bridges the gap between static private data and the ever-changing web.',
            avatar: 'https://i.pravatar.cc/150?u=sarah',
        },
        {
            name: 'Marcus Thorne',
            role: 'Full Stack Engineer',
            content: 'The agentic workflow handling search and retrieval autonomously saves so much prompt engineering time.',
            avatar: 'https://i.pravatar.cc/150?u=marcus',
        },
        {
            name: 'Elena Vance',
            role: 'Knowledge Manager',
            content: 'Finally a RAG system that doesn\'t just hallucinate when it lacks info—it actually goes out and searches for it.',
            avatar: 'https://i.pravatar.cc/150?u=elena',
        },
    ];

    const faqs = [
        {
            question: 'How does the web search integration work?',
            answer: 'Our Web Search Agent uses Firecrawl to perform real-time searches when local document retrieval doesn\'t yield high-confidence answers, ensuring your responses are always up-to-date.',
        },
        {
            question: 'Which LLMs can I use with Firecrawl Agent?',
            answer: 'We support any LLM via LiteLLM, including OpenAI, OpenRouter (Gemini, Claude), and local models through Ollama and LMStudio.',
        },
        {
            question: 'Is my document data private?',
            answer: 'Yes. Documents are processed and stored in your choice of vector database (Milvus, Qdrant, or ChromaDB). We support 100% private deployments.',
        },
        {
            question: 'Can I use this for complex PDF structures?',
            answer: 'Absolutely. Leveraging LlamaIndex\'s advanced parsing, we can handle complex layouts, tables, and multi-page documents effectively.',
        },
    ];

    return (
        <div className="min-h-screen bg-[#050505] text-white selection:bg-blue-500/30 selection:text-blue-200 overflow-x-hidden">
            {/* Navbar */}
            <nav className="fixed top-0 w-full z-50 border-b border-white/10 bg-black/50 backdrop-blur-xl">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between items-center h-16">
                        <div className="flex items-center gap-2">
                            <div className="w-8 h-8 bg-gradient-to-tr from-blue-600 to-indigo-600 rounded-lg flex items-center justify-center">
                                <Zap className="w-5 h-5 text-white" />
                            </div>
                            <span className="text-xl font-bold tracking-tight">Firecrawl Agent</span>
                        </div>

                        {/* Desktop Nav */}
                        <div className="hidden md:flex items-center gap-8">
                            {navLinks.map((link) => (
                                <a
                                    key={link.name}
                                    href={link.href}
                                    className="text-sm font-medium text-gray-400 hover:text-white transition-colors"
                                >
                                    {link.name}
                                </a>
                            ))}
                            <Link
                                to="/login"
                                className="px-5 py-2 text-sm font-semibold text-white bg-blue-600 hover:bg-blue-500 rounded-full transition-all duration-300 shadow-lg shadow-blue-500/20"
                            >
                                Sign In
                            </Link>
                        </div>

                        {/* Mobile Nav Toggle */}
                        <div className="md:hidden">
                            <button
                                onClick={() => setIsMenuOpen(!isMenuOpen)}
                                className="p-2 text-gray-400 hover:text-white transition-colors"
                            >
                                {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
                            </button>
                        </div>
                    </div>
                </div>

                {/* Mobile Menu */}
                <AnimatePresence>
                    {isMenuOpen && (
                        <motion.div
                            initial={{ opacity: 0, height: 0 }}
                            animate={{ opacity: 1, height: 'auto' }}
                            exit={{ opacity: 0, height: 0 }}
                            className="md:hidden border-b border-white/10 bg-black/95 backdrop-blur-2xl overflow-hidden"
                        >
                            <div className="px-4 pt-2 pb-6 space-y-1">
                                {navLinks.map((link) => (
                                    <a
                                        key={link.name}
                                        href={link.href}
                                        onClick={() => setIsMenuOpen(false)}
                                        className="block px-3 py-4 text-base font-medium text-gray-400 hover:text-white hover:bg-white/5 rounded-xl transition-all"
                                    >
                                        {link.name}
                                    </a>
                                ))}
                                <div className="pt-4">
                            <Link
                                to="/login"
                                onClick={() => setIsMenuOpen(false)}
                                className="block w-full text-center px-5 py-4 text-base font-semibold text-white bg-blue-600 hover:bg-blue-500 rounded-xl transition-all"
                            >
                                Sign In
                            </Link>
                                </div>
                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>
            </nav>

            <main className="pt-24">
                {/* Hero Section */}
                <section className="relative px-4 pt-20 pb-32 sm:pt-32 sm:pb-40 overflow-hidden">
                    <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[600px] bg-blue-600/10 blur-[120px] -z-10 rounded-full" />
                    <div className="absolute bottom-0 right-0 w-[500px] h-[500px] bg-indigo-600/10 blur-[120px] -z-10 rounded-full" />

                    <div className="max-w-5xl mx-auto text-center">
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.6 }}
                            className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-blue-400 text-xs font-semibold uppercase tracking-wider mb-8"
                        >
                            <Sparkles className="w-3.5 h-3.5" />
                            <span>Intelligent Agentic RAG System</span>
                        </motion.div>

                        <motion.h1
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.6, delay: 0.1 }}
                            className="text-5xl sm:text-7xl font-bold tracking-tight mb-8 bg-gradient-to-b from-white to-gray-400 bg-clip-text text-transparent lg:leading-[1.1]"
                        >
                            Universal Retrieval Meet <br /> Real-Time Search
                        </motion.h1>

                        <motion.p
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.6, delay: 0.2 }}
                            className="text-lg sm:text-xl text-gray-400 max-w-2xl mx-auto mb-10 leading-relaxed"
                        >
                            Combine local document intelligence with the breadth of the internet. Our agent-based RAG workflow retrieves what you have and searches for what you lack.
                        </motion.p>

                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.6, delay: 0.3 }}
                            className="flex flex-col sm:flex-row items-center justify-center gap-4 px-4"
                        >
                            <Link
                                to="/login"
                                className="w-full sm:w-auto px-8 py-4 text-base font-bold text-white bg-blue-600 hover:bg-blue-500 rounded-full transition-all duration-300 shadow-2xl shadow-blue-500/40 hover:scale-105 active:scale-95"
                            >
                                Get Started
                            </Link>
                            <a
                                href="https://website.apexneural.cloud/case-studies/firecrawl-agentic-rag"
                                target="_blank"
                                rel="noopener noreferrer"
                                className="w-full sm:w-auto px-8 py-4 text-base font-bold text-gray-300 hover:text-white bg-white/5 hover:bg-white/10 rounded-full border border-white/10 transition-all duration-300 backdrop-blur-sm flex items-center justify-center gap-2 group"
                            >
                                <Play className="w-4 h-4 fill-current group-hover:scale-110 transition-transform" />
                                View Architecture
                            </a>
                        </motion.div>
                    </div>

                    <motion.div
                        initial={{ opacity: 0, y: 100 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 1, delay: 0.4, ease: [0.16, 1, 0.3, 1] }}
                        className="mt-20 max-w-6xl mx-auto p-2 sm:p-4 rounded-[2rem] bg-gradient-to-b from-white/10 to-transparent border border-white/10 shadow-2xl shadow-black"
                    >
                        <div className="aspect-[16/10] bg-black rounded-[1.5rem] overflow-hidden border border-white/5 relative group">
                            <img
                                src="https://images.unsplash.com/photo-1639322537228-f710d846310a?auto=format&fit=crop&q=80&w=2000"
                                alt="Agentic Visualization"
                                className="w-full h-full object-cover opacity-60 group-hover:scale-105 transition-transform duration-700"
                            />
                            <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent" />
                        </div>
                    </motion.div>
                </section>

                {/* Tech Stack Marquee */}
                <section id="technology" className="py-20 border-y border-white/5 bg-white/[0.02]">
                    <div className="max-w-7xl mx-auto px-4 text-center mb-10">
                        <p className="text-sm font-medium text-gray-500 uppercase tracking-widest">Built with state-of-the-art tech</p>
                    </div>
                    <div className="relative flex overflow-hidden">
                        <div className="flex animate-marquee whitespace-nowrap py-4 gap-20 items-center">
                            {[...technologies, ...technologies].map((tech, i) => (
                                <span key={i} className="text-2xl sm:text-4xl font-black text-white/20 hover:text-white/40 transition-colors cursor-default">
                                    {tech}
                                </span>
                            ))}
                        </div>
                        <div className="absolute left-0 top-0 bottom-0 w-40 bg-gradient-to-r from-[#050505] to-transparent z-10" />
                        <div className="absolute right-0 top-0 bottom-0 w-40 bg-gradient-to-l from-[#050505] to-transparent z-10" />
                    </div>
                </section>

                {/* Features (Bento Grid) */}
                <section id="features" className="py-32 px-4">
                    <div className="max-w-7xl mx-auto">
                        <div className="text-center mb-20">
                            <h2 className="text-3xl sm:text-5xl font-bold mb-6">Autonomous Knowledge Intelligence</h2>
                            <p className="text-gray-400 max-w-xl mx-auto text-lg text-balance">The system coordinates multiple agents to ensure your answers are anchored in truth.</p>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 auto-rows-[250px]">
                            {benefits.map((benefit, i) => (
                                <motion.div
                                    key={i}
                                    initial={{ opacity: 0, scale: 0.95 }}
                                    whileInView={{ opacity: 1, scale: 1 }}
                                    transition={{ duration: 0.4, delay: i * 0.1 }}
                                    viewport={{ once: true }}
                                    className={`${benefit.className} group relative overflow-hidden p-8 rounded-3xl bg-white/[0.03] border border-white/10 hover:border-blue-500/50 transition-all duration-500`}
                                >
                                    <div className="absolute inset-0 bg-gradient-to-br from-blue-600/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
                                    <div className="relative h-full flex flex-col justify-between">
                                        <div className="inline-flex p-3 rounded-2xl bg-black/40 border border-white/5 w-fit h-fit">
                                            {benefit.icon}
                                        </div>
                                        <div>
                                            <h3 className="text-xl font-bold mb-2">{benefit.title}</h3>
                                            <p className="text-gray-400 text-sm leading-relaxed">{benefit.description}</p>
                                        </div>
                                    </div>
                                </motion.div>
                            ))}
                        </div>
                    </div>
                </section>

                {/* How it Works / Workflow */}
                <section id="workflow" className="py-32 bg-white/[0.02] border-y border-white/5">
                    <div className="max-w-7xl mx-auto px-4 text-center">
                        <h2 className="text-3xl sm:text-5xl font-bold mb-20">The Agentic Pipeline</h2>

                        <div className="grid grid-cols-1 md:grid-cols-3 gap-12 relative">
                            <div className="hidden md:block absolute top-[60px] left-[15%] right-[15%] h-px bg-gradient-to-r from-transparent via-blue-500/30 to-transparent" />

                            {[
                                { step: '01', title: 'Document Ingestion', desc: 'LlamaIndex processes your PDFs into high-dimensional vector embeddings.' },
                                { step: '02', title: 'Multi-Agent Search', desc: 'Retrieve agent looks into local store, while Web Search agent queries Firecrawl.' },
                                { step: '03', title: 'Synthesis & Generation', desc: 'Final response is filtered for relevance and synthesized by your chosen LLM.' },
                            ].map((item, i) => (
                                <motion.div
                                    key={i}
                                    initial={{ opacity: 0, y: 20 }}
                                    whileInView={{ opacity: 1, y: 0 }}
                                    transition={{ duration: 0.5, delay: i * 0.2 }}
                                    viewport={{ once: true }}
                                    className="relative z-10 group"
                                >
                                    <div className="w-16 h-16 mx-auto mb-8 rounded-2xl bg-blue-600 flex items-center justify-center text-xl font-black shadow-lg shadow-blue-500/40 group-hover:scale-110 transition-transform duration-300">
                                        {item.step}
                                    </div>
                                    <h3 className="text-xl font-bold mb-4">{item.title}</h3>
                                    <p className="text-gray-400 leading-relaxed max-w-[250px] mx-auto">{item.desc}</p>
                                </motion.div>
                            ))}
                        </div>
                    </div>
                </section>

                {/* Pricing Selection */}
                <section id="pricing" className="py-32 px-4">
                    <div className="max-w-7xl mx-auto">
                        <div className="text-center mb-20">
                            <p className="text-blue-500 font-bold mb-4 uppercase tracking-[0.2em] text-sm">Pricing Plans</p>
                            <h2 className="text-4xl sm:text-6xl font-bold mb-6 text-balance">Infrastructure That Scales</h2>
                            <p className="text-gray-400 max-w-xl mx-auto text-lg">Choose the right tier for your data retrieval needs.</p>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                            {pricing.map((plan, i) => (
                                <div
                                    key={i}
                                    className={`relative p-8 rounded-[2.5rem] border ${plan.popular ? 'border-blue-500 bg-blue-500/[0.02] shadow-[0_0_50px_-12px_rgba(59,130,246,0.3)]' : 'border-white/10 bg-white/[0.02]'} transition-all hover:translate-y-[-8px]`}
                                >
                                    {plan.popular && (
                                        <div className="absolute -top-4 left-1/2 -translate-x-1/2 px-4 py-1.5 bg-blue-600 rounded-full text-xs font-bold uppercase tracking-widest flex items-center gap-1.5 shadow-lg shadow-blue-600/40">
                                            <Sparkles className="w-3 h-3" />
                                            Recommended
                                        </div>
                                    )}
                                    <h3 className="text-xl font-bold mb-2">{plan.name}</h3>
                                    <div className="flex items-baseline gap-1 mb-4">
                                        <span className="text-5xl font-black">{plan.price}</span>
                                        <span className="text-gray-500 text-sm">{plan.price !== 'Custom' && '/month'}</span>
                                    </div>
                                    <p className="text-gray-400 text-sm mb-8 min-h-[40px]">{plan.description}</p>

                                    <Link
                                        to="/login"
                                        className={`block w-full py-4 rounded-2xl text-center font-bold transition-all mb-8 ${plan.popular ? 'bg-blue-600 text-white hover:bg-blue-500 shadow-xl shadow-blue-500/20' : 'bg-white/5 text-white hover:bg-white/10 border border-white/10'}`}
                                    >
                                        {plan.cta}
                                    </Link>

                                    <div className="space-y-4">
                                        {plan.features.map((feature, idx) => (
                                            <div key={idx} className="flex items-center gap-3 text-sm text-gray-300">
                                                <CheckCircle2 className="w-5 h-5 text-blue-500 flex-shrink-0" />
                                                {feature}
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </section>

                {/* Testimonials */}
                <section id="testimonials" className="py-32 bg-blue-600/5 overflow-hidden">
                    <div className="max-w-7xl mx-auto px-4">
                        <div className="text-center mb-20">
                            <h2 className="text-3xl sm:text-5xl font-bold mb-6">Expert Perspectives</h2>
                            <p className="text-gray-400 max-w-xl mx-auto text-lg underline decoration-blue-500/50 decoration-2 underline-offset-8">
                                What the community says about Firecrawl Agent
                            </p>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                            {testimonials.map((t, i) => (
                                <div key={i} className="p-8 rounded-3xl bg-black/40 border border-white/5 backdrop-blur-sm relative group">
                                    <div className="flex gap-1 mb-6">
                                        {[1, 2, 3, 4, 5].map((s) => (
                                            <Star key={s} className="w-4 h-4 text-yellow-500 fill-current" />
                                        ))}
                                    </div>
                                    <p className="text-gray-300 mb-8 italic leading-relaxed">"{t.content}"</p>
                                    <div className="flex items-center gap-4">
                                        <img src={t.avatar} alt={t.name} className="w-12 h-12 rounded-full border border-white/10" />
                                        <div>
                                            <h4 className="font-bold text-white">{t.name}</h4>
                                            <p className="text-sm text-gray-500">{t.role}</p>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </section>

                {/* FAQ Section */}
                <section id="faq" className="py-32 px-4 max-w-3xl mx-auto">
                    <div className="text-center mb-20">
                        <h2 className="text-3xl sm:text-5xl font-bold mb-6 tracking-tight">Technical FAQ</h2>
                        <p className="text-gray-400">Deep dive into the architecture and capabilities.</p>
                    </div>

                    <div className="space-y-4">
                        {faqs.map((faq, i) => (
                            <div
                                key={i}
                                className={`rounded-2xl border transition-all duration-300 ${activeFaq === i ? 'border-blue-500 bg-blue-500/[0.03]' : 'border-white/10 bg-white/[0.02] hover:bg-white/[0.05]'}`}
                            >
                                <button
                                    onClick={() => setActiveFaq(activeFaq === i ? null : i)}
                                    className="w-full px-6 py-6 flex items-center justify-between text-left"
                                >
                                    <span className="font-semibold text-lg">{faq.question}</span>
                                    <div className={`p-1 rounded-full transition-transform duration-300 ${activeFaq === i ? 'rotate-180 bg-blue-500 text-white' : 'text-gray-500'}`}>
                                        {activeFaq === i ? <Minus className="w-5 h-5" /> : <Plus className="w-5 h-5" />}
                                    </div>
                                </button>
                                <AnimatePresence>
                                    {activeFaq === i && (
                                        <motion.div
                                            initial={{ height: 0, opacity: 0 }}
                                            animate={{ height: 'auto', opacity: 1 }}
                                            exit={{ height: 0, opacity: 0 }}
                                            className="overflow-hidden"
                                        >
                                            <div className="px-6 pb-6 text-gray-400 leading-relaxed">
                                                {faq.answer}
                                            </div>
                                        </motion.div>
                                    )}
                                </AnimatePresence>
                            </div>
                        ))}
                    </div>
                </section>

                {/* Final CTA */}
                <section className="py-20 px-4">
                    <div className="max-w-6xl mx-auto">
                        <div className="relative rounded-[3rem] bg-blue-600 p-12 sm:p-20 overflow-hidden text-center shadow-2xl shadow-blue-500/20">
                            <div className="absolute top-0 right-0 -mr-20 -mt-20 w-80 h-80 bg-white/10 blur-[80px] rounded-full" />
                            <div className="absolute bottom-0 left-0 -ml-20 -mb-20 w-80 h-80 bg-black/10 blur-[80px] rounded-full" />

                            <div className="relative z-10">
                                <h2 className="text-3xl sm:text-6xl font-black text-white mb-8">Ready to deploy your <br /> private RAG agent?</h2>
                                <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                                    <Link
                                        to="/login"
                                        className="w-full sm:w-auto px-10 py-5 text-lg font-bold text-blue-600 bg-white hover:bg-gray-100 rounded-full transition-all shadow-xl hover:scale-105 active:scale-95"
                                    >
                                        Get Started Now
                                    </Link>
                                </div>
                                <p className="mt-8 text-blue-100/60 text-sm font-medium">Open Source Core • Modular Vector Storage • Multi-Provider Support</p>
                            </div>
                        </div>
                    </div>
                </section>
            </main>

            {/* Footer */}
            <footer className="bg-black border-t border-white/5 py-20 px-4">
                <div className="max-w-7xl mx-auto">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-12 mb-16">
                        <div className="col-span-1 md:col-span-1">
                            <div className="flex items-center gap-2 mb-6">
                                <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                                    <Zap className="w-5 h-5 text-white" />
                                </div>
                                <span className="text-xl font-bold tracking-tight">Firecrawl Agent</span>
                            </div>
                            <p className="text-gray-500 text-sm leading-relaxed mb-8 text-balance">
                                Pioneering the hybrid RAG architecture. Combining document embeddings with web-scale search for unparalleled AI context.
                            </p>
                            <div className="flex gap-4">
                                {/* {[Twitter, Github].map((Icon, i) => (
                                    <a key={i} href="#" className="w-10 h-10 rounded-xl bg-white/5 flex items-center justify-center text-gray-400 hover:text-white hover:bg-blue-600 transition-all">
                                        <Icon className="w-5 h-5" />
                                    </a>
                                ))} */}
                                <a 
                                    href="https://www.linkedin.com/company/apexneural/posts/?feedView=all" 
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="w-10 h-10 rounded-xl bg-white/5 flex items-center justify-center text-gray-400 hover:text-white hover:bg-blue-600 transition-all"
                                >
                                    <Linkedin className="w-5 h-5" />
                                </a>
                            </div>
                        </div>

                        <div>
                            <h4 className="font-bold mb-6">Legal</h4>
                            <ul className="space-y-4 text-sm text-gray-500">
                                <li>
                                    <Link to="/terms" className="hover:text-blue-500 transition-colors">
                                        Terms of Use
                                    </Link>
                                </li>
                                <li>
                                    <Link to="/privacy" className="hover:text-blue-500 transition-colors">
                                        Privacy Policy
                                    </Link>
                                </li>
                                <li>
                                    <Link to="/open-source-license" className="hover:text-blue-500 transition-colors">
                                        Open Source License
                                    </Link>
                                </li>
                                <li>
                                    <Link to="/security" className="hover:text-blue-500 transition-colors">
                                        Security
                                    </Link>
                                </li>
                            </ul>
                        </div>

                        <div>
                            <h4 className="font-bold mb-6">Stay Updated</h4>
                            <p className="text-sm text-gray-500 mb-6">Get the latest on agentic RAG and AI search.</p>
                            <form
                                className="flex flex-col gap-2"
                                onSubmit={async (e) => {
                                    e.preventDefault();
                                    setNewsletterLoading(true);
                                    setNewsletterStatus({ type: null, message: '' });
                                    
                                    try {
                                        const result = await subscribeNewsletter(newsletterEmail);
                                        if (result.success) {
                                            setNewsletterStatus({ type: 'success', message: result.message });
                                            setNewsletterEmail('');
                                        } else {
                                            setNewsletterStatus({ type: 'error', message: result.message });
                                        }
                                    } catch (error: any) {
                                        setNewsletterStatus({ 
                                            type: 'error', 
                                            message: error.response?.data?.message || 'Failed to subscribe. Please try again.' 
                                        });
                                    } finally {
                                        setNewsletterLoading(false);
                                    }
                                }}
                            >
                                <div className="flex gap-2">
                                    <input
                                        name="email"
                                        type="email"
                                        required
                                        value={newsletterEmail}
                                        onChange={(e) => setNewsletterEmail(e.target.value)}
                                        placeholder="name@email.com"
                                        disabled={newsletterLoading}
                                        className="bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-blue-500 transition-colors w-full disabled:opacity-50"
                                    />
                                    <button
                                        type="submit"
                                        disabled={newsletterLoading}
                                        className="p-3 bg-blue-600 hover:bg-blue-500 rounded-xl transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                                    >
                                        {newsletterLoading ? (
                                            <motion.div
                                                animate={{ rotate: 360 }}
                                                transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                                                className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full"
                                            />
                                        ) : (
                                            <ArrowRight className="w-5 h-5" />
                                        )}
                                    </button>
                                </div>
                                {newsletterStatus.type && (
                                    <motion.div
                                        initial={{ opacity: 0, y: -10 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        className={`text-sm p-3 rounded-xl ${
                                            newsletterStatus.type === 'success'
                                                ? 'bg-green-500/10 border border-green-500/20 text-green-400'
                                                : 'bg-red-500/10 border border-red-500/20 text-red-400'
                                        }`}
                                    >
                                        {newsletterStatus.message}
                                    </motion.div>
                                )}
                            </form>
                        </div>
                    </div>

                    <div className="pt-8 border-t border-white/5 flex flex-col md:flex-row justify-between items-center gap-6">
                        <p className="text-sm text-gray-600">© 2025 Firecrawl Agentic Pipeline. All rights reserved.</p>
                        <div className="flex gap-8 text-sm text-gray-600">
                            <Link to="/terms" className="hover:text-gray-400 transition-colors">Terms of Use</Link>
                            <Link to="/privacy" className="hover:text-gray-400 transition-colors">Privacy Policy</Link>
                            <Link to="/open-source-license" className="hover:text-gray-400 transition-colors">Open Source License</Link>
                            <Link to="/security" className="hover:text-gray-400 transition-colors">Security</Link>
                        </div>
                    </div>
                </div>
            </footer>
        </div>
    );
};

export default LandingPage;
