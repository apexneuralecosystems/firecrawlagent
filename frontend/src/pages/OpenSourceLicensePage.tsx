import { Link } from 'react-router-dom';
import { 
  Code2, Heart, GitBranch, Scale, Users, Sparkles, 
  ArrowLeft, ExternalLink, Github, Copy, Check, Zap
} from 'lucide-react';
import { useState } from 'react';

const MIT_LICENSE = `MIT License

Copyright (c) 2025 ApexNeural Private Limited

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.`;

const freedoms = [
  {
    icon: Code2,
    title: 'Use',
    description: 'Use the software for any purpose, including commercial applications',
    color: 'from-blue-500 to-cyan-500'
  },
  {
    icon: GitBranch,
    title: 'Modify',
    description: 'Modify the source code to suit your needs and create derivative works',
    color: 'from-purple-500 to-pink-500'
  },
  {
    icon: Users,
    title: 'Distribute',
    description: 'Share copies of the original software with others freely',
    color: 'from-green-500 to-emerald-500'
  },
  {
    icon: Sparkles,
    title: 'Sublicense',
    description: 'Grant sublicenses to others under the same permissive terms',
    color: 'from-amber-500 to-orange-500'
  }
];

const requirements = [
  {
    title: 'Include License',
    description: 'Include a copy of this license in all copies or substantial portions'
  },
  {
    title: 'Include Copyright',
    description: 'Keep the copyright notice intact in all distributions'
  }
];

export default function OpenSourceLicensePage() {
  const [copied, setCopied] = useState(false);

  const copyLicense = () => {
    navigator.clipboard.writeText(MIT_LICENSE);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="min-h-screen bg-[#030303] text-white">
      {/* Animated background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/3 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-1/4 right-1/4 w-80 h-80 bg-pink-500/10 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }} />
        <div className="absolute top-1/2 left-1/4 w-64 h-64 bg-violet-500/5 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '2s' }} />
        {/* Code pattern overlay */}
        <div className="absolute inset-0 opacity-[0.02]" style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='1'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`
        }} />
      </div>

      {/* Header */}
      <header className="sticky top-0 z-50 border-b border-white/10 bg-black/60 backdrop-blur-xl">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 py-4 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-3 group">
            <div className="w-10 h-10 bg-gradient-to-tr from-blue-600 to-indigo-600 rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/25 group-hover:shadow-blue-500/40 transition-shadow">
              <Zap className="w-5 h-5 text-white" />
            </div>
            <span className="text-lg font-bold tracking-tight">Firecrawl Agent</span>
          </Link>
          <Link 
            to="/" 
            className="flex items-center gap-2 px-4 py-2 rounded-full bg-white/5 hover:bg-white/10 border border-white/10 text-sm text-gray-300 hover:text-white transition-all"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to Home
          </Link>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative py-16 sm:py-24">
        <div className="max-w-6xl mx-auto px-4 sm:px-6">
          <div className="text-center mb-16">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-400 text-sm mb-6">
              <Heart className="w-4 h-4" />
              Open Source Software
            </div>
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold mb-4 bg-gradient-to-r from-white via-purple-200 to-pink-200 bg-clip-text text-transparent">
              Open Source License
            </h1>
            <p className="text-gray-400 text-lg max-w-2xl mx-auto">
              Firecrawl Agent is released under the MIT License, one of the most permissive and business-friendly open source licenses
            </p>
          </div>

          {/* MIT Badge */}
          <div className="flex justify-center mb-12">
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-r from-purple-500 to-pink-500 rounded-3xl blur-xl opacity-30" />
              <div className="relative flex items-center gap-4 px-8 py-6 rounded-3xl border border-white/20 bg-black/40 backdrop-blur-xl">
                <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center shadow-xl">
                  <Scale className="w-8 h-8 text-white" />
                </div>
                <div>
                  <h2 className="text-2xl font-bold text-white">MIT License</h2>
                  <p className="text-gray-400">A short and simple permissive license</p>
                </div>
              </div>
            </div>
          </div>

          {/* Freedoms Grid */}
          <div className="mb-12">
            <h3 className="text-center text-lg font-semibold text-gray-300 mb-6">What you can do</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {freedoms.map((freedom, i) => {
                const Icon = freedom.icon;
                return (
                  <div 
                    key={i} 
                    className="group relative rounded-2xl border border-white/10 bg-white/[0.02] hover:bg-white/[0.05] p-6 text-center transition-all duration-300"
                  >
                    <div className={`w-14 h-14 mx-auto mb-4 rounded-xl bg-gradient-to-br ${freedom.color} flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform`}>
                      <Icon className="w-7 h-7 text-white" />
                    </div>
                    <h4 className="text-lg font-semibold text-white mb-2">{freedom.title}</h4>
                    <p className="text-sm text-gray-400">{freedom.description}</p>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Requirements */}
          <div className="mb-12">
            <h3 className="text-center text-lg font-semibold text-gray-300 mb-6">Simple requirements</h3>
            <div className="max-w-2xl mx-auto grid gap-4 md:grid-cols-2">
              {requirements.map((req, i) => (
                <div key={i} className="flex items-start gap-4 p-4 rounded-xl border border-white/10 bg-white/[0.02]">
                  <div className="w-8 h-8 rounded-lg bg-green-500/20 flex items-center justify-center flex-shrink-0">
                    <Check className="w-4 h-4 text-green-400" />
                  </div>
                  <div>
                    <h4 className="font-medium text-white mb-1">{req.title}</h4>
                    <p className="text-sm text-gray-400">{req.description}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* License Text */}
          <div className="relative rounded-3xl border border-white/10 bg-gradient-to-br from-white/[0.05] to-transparent overflow-hidden">
            <div className="flex items-center justify-between px-6 py-4 border-b border-white/10 bg-white/[0.02]">
              <div className="flex items-center gap-3">
                <div className="flex gap-2">
                  <div className="w-3 h-3 rounded-full bg-red-500/80" />
                  <div className="w-3 h-3 rounded-full bg-yellow-500/80" />
                  <div className="w-3 h-3 rounded-full bg-green-500/80" />
                </div>
                <span className="text-sm text-gray-400 font-mono">LICENSE</span>
              </div>
              <button
                onClick={copyLicense}
                className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 text-sm text-gray-300 hover:text-white transition-all"
              >
                {copied ? (
                  <>
                    <Check className="w-4 h-4 text-green-400" />
                    Copied!
                  </>
                ) : (
                  <>
                    <Copy className="w-4 h-4" />
                    Copy
                  </>
                )}
              </button>
            </div>
            <pre className="p-6 text-sm text-gray-300 font-mono leading-relaxed overflow-x-auto">
          {MIT_LICENSE}
            </pre>
          </div>

          {/* GitHub CTA */}
          <div className="mt-12 text-center">
            <p className="text-gray-400 mb-4">View the source code and contribute</p>
            <a
              href="https://github.com/ApexNeural/firecrawl-agent"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-3 px-6 py-3 rounded-full bg-gradient-to-r from-purple-500 to-pink-500 text-white font-medium hover:opacity-90 transition-opacity shadow-lg shadow-purple-500/25"
            >
              <Github className="w-5 h-5" />
              View on GitHub
              <ExternalLink className="w-4 h-4" />
            </a>
          </div>

          {/* Footer note */}
          <div className="mt-16 text-center">
            <div className="inline-flex items-center gap-2 text-gray-500 text-sm">
              <Heart className="w-4 h-4 text-pink-500" />
              Made with love by ApexNeural Private Limited
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
