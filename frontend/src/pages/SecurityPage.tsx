import { Link } from 'react-router-dom';
import { 
  Shield, Lock, Eye, Server, Key, AlertTriangle, 
  CheckCircle2, ArrowLeft, Mail, Bug, FileWarning,
  Fingerprint, RefreshCcw, Database, Globe, Zap
} from 'lucide-react';

const securityFeatures = [
  {
    icon: Lock,
    title: 'Encryption in Transit',
    description: 'All data transmitted between your browser and our servers is encrypted using TLS/SSL protocols',
    color: 'from-blue-500 to-cyan-500'
  },
  {
    icon: Database,
    title: 'Encryption at Rest',
    description: 'Sensitive data is encrypted using AES-256 encryption when stored on our servers',
    color: 'from-purple-500 to-pink-500'
  },
  {
    icon: Fingerprint,
    title: 'Authentication',
    description: 'Secure JWT-based authentication with password hashing using industry-standard algorithms',
    color: 'from-green-500 to-emerald-500'
  },
  {
    icon: Key,
    title: 'Access Controls',
    description: 'Role-based access controls and least-privilege principles protect your data',
    color: 'from-amber-500 to-orange-500'
  },
  {
    icon: Eye,
    title: 'Monitoring',
    description: 'Continuous security monitoring and logging to detect and respond to threats',
    color: 'from-red-500 to-rose-500'
  },
  {
    icon: RefreshCcw,
    title: 'Regular Updates',
    description: 'Regular security patches and vulnerability assessments keep systems protected',
    color: 'from-indigo-500 to-violet-500'
  }
];

const bestPractices = [
  {
    icon: Key,
    title: 'Strong Passwords',
    description: 'Use a unique, strong password with at least 12 characters, including numbers and symbols'
  },
  {
    icon: FileWarning,
    title: 'Sensitive Data',
    description: 'Do not upload sensitive personal data unless necessary and you have a lawful basis'
  },
  {
    icon: CheckCircle2,
    title: 'Verify Outputs',
    description: 'Always review AI-generated outputs before using them for important decisions'
  },
  {
    icon: RefreshCcw,
    title: 'Regular Review',
    description: 'Periodically review your account activity and connected sessions'
  }
];

export default function SecurityPage() {
  return (
    <div className="min-h-screen bg-[#030303] text-white">
      {/* Animated background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-1/3 right-1/4 w-80 h-80 bg-blue-500/10 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }} />
        <div className="absolute top-1/2 right-1/3 w-64 h-64 bg-indigo-500/5 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '2s' }} />
        {/* Shield pattern */}
        <div className="absolute inset-0 opacity-[0.015]" style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='80' height='80' viewBox='0 0 24 24' fill='none' stroke='%23ffffff' stroke-width='0.5'%3E%3Cpath d='M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10'/%3E%3C/svg%3E")`,
          backgroundSize: '80px 80px'
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
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 text-sm mb-6">
              <Shield className="w-4 h-4" />
              Your Security is Our Priority
            </div>
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold mb-4 bg-gradient-to-r from-white via-cyan-200 to-blue-200 bg-clip-text text-transparent">
              Security
            </h1>
            <p className="text-gray-400 text-lg max-w-2xl mx-auto">
              We take reasonable measures to protect user accounts, uploaded content, and service infrastructure
            </p>
          </div>

          {/* Security Shield Animation */}
          <div className="flex justify-center mb-16">
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-full blur-3xl opacity-20 animate-pulse" />
              <div className="relative w-32 h-32 rounded-full bg-gradient-to-br from-cyan-500/20 to-blue-500/20 border border-white/10 flex items-center justify-center">
                <div className="w-24 h-24 rounded-full bg-gradient-to-br from-cyan-500/30 to-blue-500/30 border border-white/10 flex items-center justify-center">
                  <div className="w-16 h-16 rounded-full bg-gradient-to-br from-cyan-500 to-blue-500 flex items-center justify-center shadow-xl shadow-cyan-500/30">
                    <Shield className="w-8 h-8 text-white" />
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Security Features Grid */}
          <div className="mb-16">
            <h2 className="text-2xl font-bold text-center mb-8">How We Protect You</h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {securityFeatures.map((feature, i) => {
                const Icon = feature.icon;
                return (
                  <div
                    key={i}
                    className="group relative rounded-2xl border border-white/10 bg-white/[0.02] hover:bg-white/[0.05] p-6 transition-all duration-300 hover:border-white/20"
                  >
                    <div className={`w-14 h-14 mb-4 rounded-xl bg-gradient-to-br ${feature.color} flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform`}>
                      <Icon className="w-7 h-7 text-white" />
                    </div>
                    <h3 className="text-lg font-semibold text-white mb-2">{feature.title}</h3>
                    <p className="text-sm text-gray-400">{feature.description}</p>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Vulnerability Reporting */}
          <div className="relative rounded-3xl border border-white/10 bg-gradient-to-br from-red-500/10 via-transparent to-orange-500/10 p-8 mb-16 overflow-hidden">
            <div className="absolute top-0 right-0 w-64 h-64 bg-gradient-to-br from-red-500/10 to-transparent rounded-full blur-2xl" />
            <div className="relative flex flex-col md:flex-row items-start md:items-center gap-6">
              <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-red-500 to-orange-500 flex items-center justify-center shadow-xl shadow-red-500/25 flex-shrink-0">
                <Bug className="w-10 h-10 text-white" />
              </div>
              <div className="flex-1">
                <h2 className="text-2xl font-bold mb-3">Vulnerability Reporting</h2>
                <p className="text-gray-400 mb-4">
                  If you believe you have found a security vulnerability, please report it to us responsibly. 
                  We appreciate your help in keeping our platform secure.
                </p>
                <div className="flex flex-wrap gap-4">
                  <a
                    href="mailto:info@apexneural.com?subject=Security%20Vulnerability%20Report"
                    className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-red-500 to-orange-500 text-white font-medium hover:opacity-90 transition-opacity shadow-lg shadow-red-500/25"
                  >
                    <Mail className="w-4 h-4" />
                    Report Vulnerability
                  </a>
                  <div className="flex items-center gap-2 text-sm text-gray-400">
                    <AlertTriangle className="w-4 h-4 text-amber-500" />
                    Include steps to reproduce and relevant logs/screenshots
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Best Practices */}
          <div className="mb-16">
            <h2 className="text-2xl font-bold text-center mb-2">Best Practices</h2>
            <p className="text-gray-400 text-center mb-8">Recommended security practices for users</p>
            <div className="grid md:grid-cols-2 gap-4">
              {bestPractices.map((practice, i) => {
                const Icon = practice.icon;
                return (
                  <div
                    key={i}
                    className="flex items-start gap-4 p-5 rounded-2xl border border-white/10 bg-white/[0.02] hover:bg-white/[0.04] transition-all"
                  >
                    <div className="w-12 h-12 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center flex-shrink-0">
                      <Icon className="w-6 h-6 text-cyan-400" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-white mb-1">{practice.title}</h3>
                      <p className="text-sm text-gray-400">{practice.description}</p>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Trust Indicators */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-16">
            {[
              { icon: Lock, label: 'TLS/SSL', value: 'Encrypted', color: 'text-green-400' },
              { icon: Server, label: 'Data Center', value: 'India', color: 'text-blue-400' },
              { icon: Globe, label: 'Compliance', value: 'DPDP Act', color: 'text-purple-400' },
              { icon: Zap, label: 'Uptime', value: '99.9%', color: 'text-amber-400' }
            ].map((item, i) => {
              const Icon = item.icon;
              return (
                <div key={i} className="rounded-2xl border border-white/10 bg-white/[0.02] p-4 text-center">
                  <Icon className={`w-6 h-6 mx-auto mb-2 ${item.color}`} />
                  <p className="text-xs text-gray-500 mb-1">{item.label}</p>
                  <p className="text-lg font-semibold text-white">{item.value}</p>
                </div>
              );
            })}
          </div>

          {/* Disclaimer */}
          <div className="rounded-2xl border border-white/10 bg-white/[0.02] p-6">
            <div className="flex items-start gap-4">
              <div className="w-10 h-10 rounded-lg bg-amber-500/10 flex items-center justify-center flex-shrink-0">
                <AlertTriangle className="w-5 h-5 text-amber-500" />
              </div>
              <div>
                <h3 className="font-semibold text-white mb-2">Security Disclaimer</h3>
                <p className="text-sm text-gray-400">
                  No system is perfectly secure, but we continuously work to reduce risk through access controls, 
                  monitoring, and secure-by-default configuration. We follow industry best practices and regularly 
                  update our security measures to address emerging threats.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
