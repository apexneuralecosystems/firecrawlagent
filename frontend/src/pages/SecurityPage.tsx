import { Zap } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function SecurityPage() {
  return (
    <div className="min-h-screen bg-[#050505] text-white">
      <header className="border-b border-white/10 bg-black/40 backdrop-blur-xl">
        <div className="max-w-5xl mx-auto px-4 py-4 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2">
            <div className="w-8 h-8 bg-gradient-to-tr from-blue-600 to-indigo-600 rounded-lg flex items-center justify-center">
              <Zap className="w-5 h-5 text-white" />
            </div>
            <span className="text-lg font-bold tracking-tight">Firecrawl Agent</span>
          </Link>
          <Link to="/" className="text-sm text-gray-400 hover:text-white transition-colors">
            Back to Home
          </Link>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-4 py-10">
        <h1 className="text-3xl sm:text-4xl font-bold mb-6">Security</h1>
        <div className="space-y-6 text-sm leading-relaxed text-gray-300">
          <p>
            We take reasonable measures to protect user accounts, uploaded content, and service infrastructure.
            No system is perfectly secure, but we continuously work to reduce risk through access controls,
            monitoring, and secure-by-default configuration.
          </p>

          <div className="rounded-2xl border border-white/10 bg-white/[0.02] p-6">
            <h2 className="text-base font-semibold text-white mb-3">Vulnerability Reporting</h2>
            <p className="text-gray-300">
              If you believe you have found a security vulnerability, please email <span className="text-white">info@apexneural.com</span> with the subject
              line <span className="text-white">“Security Vulnerability Report”</span>. Include steps to reproduce and any relevant logs/screenshots.
            </p>
          </div>

          <div className="rounded-2xl border border-white/10 bg-white/[0.02] p-6">
            <h2 className="text-base font-semibold text-white mb-3">Best Practices</h2>
            <ul className="list-disc pl-5 space-y-2 text-gray-300">
              <li>Use a strong, unique password for your account.</li>
              <li>Do not upload sensitive personal data unless you have a lawful basis and it is necessary.</li>
              <li>Review outputs before using them for important decisions.</li>
            </ul>
          </div>
        </div>
      </main>
    </div>
  );
}


