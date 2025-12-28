import { Link } from 'react-router-dom';
import { 
  Shield, Database, Eye, Share2, Globe, Lock, Cookie, Clock, 
  UserCheck, Bell, Baby, User, Mail, Building2, ArrowLeft, 
  FileText, Brain, Server, Trash2, Zap
} from 'lucide-react';

const sections = [
  {
    id: 'collect',
    title: '1. Personal Data We Collect',
    icon: Database,
    color: 'from-blue-500 to-cyan-500',
    subsections: [
      {
        subtitle: 'Data Provided by You',
        items: ['Full name, email address, phone number', 'Login or account registration details', 'Billing and payment information', 'Files, documents, and content you upload']
      },
      {
        subtitle: 'Data Collected Automatically',
        items: ['IP address, device and browser type', 'Usage metrics and session duration', 'Cookies and tracking technologies']
      },
      {
        subtitle: 'AI-Generated Data',
        items: ['Inputs submitted to AI systems', 'Generated outputs and responses', 'Conversation history and preferences']
      }
    ]
  },
  {
    id: 'lawful',
    title: '2. Lawful Basis for Processing',
    icon: FileText,
    color: 'from-green-500 to-emerald-500',
    content: `Under the Digital Personal Data Protection Act, 2023 (DPDP Act), we process personal data based on:
• Your consent
• Performance of a contract or provision of requested Services
• Legitimate business purposes (security, analytics, fraud prevention)
• Compliance with legal or regulatory obligations`
  },
  {
    id: 'use',
    title: '4. How We Use Your Data',
    icon: Eye,
    color: 'from-purple-500 to-pink-500',
    content: `We use personal data to:
• Provide, operate, maintain and improve our Services
• Personalize user experience and AI outputs
• Manage payments, billing, and account services
• Communicate with you (support, alerts, updates)
• Monitor usage patterns and enhance performance
• Detect and prevent fraud, abuse, or security threats
• Train and improve AI/ML models
• Comply with applicable laws and regulations`
  },
  {
    id: 'ai-training',
    title: '5. Use of Data for AI Training',
    icon: Brain,
    color: 'from-indigo-500 to-violet-500',
    content: `By default, User Content may be used to train and improve our AI models. We take steps to avoid using directly identifying data.

You may opt out anytime by:
• Using account settings, or
• Emailing info@apexneural.com with subject: "Opt-Out of Model Training"

Anonymized or aggregated data may still be retained for improvement.`
  },
  {
    id: 'sharing',
    title: '7. Sharing & Disclosure',
    icon: Share2,
    color: 'from-amber-500 to-orange-500',
    content: `We do not sell personal data. We share data only with:
• Cloud hosting providers and data processors
• Payment processors and fraud prevention partners
• Professional advisors where necessary
• Governmental authorities if legally required
• Third parties in case of merger or acquisition

All third-party processors act only under our instructions.`
  },
  {
    id: 'transfers',
    title: '8. International Transfers',
    icon: Globe,
    color: 'from-teal-500 to-cyan-500',
    content: `Your data is primarily stored and processed in India. If transferred outside India, we ensure adequate safeguards consistent with DPDP Act standards and applicable international requirements.`
  },
  {
    id: 'security',
    title: '9. Data Security',
    icon: Lock,
    color: 'from-red-500 to-rose-500',
    content: `We implement industry-standard controls including:
• Encryption at rest (AES-256 where applicable)
• Encryption in transit (TLS/SSL)
• Access control and authentication procedures
• Regular vulnerability assessment and monitoring

However, no electronic transmission or storage is 100% secure.`
  },
  {
    id: 'cookies',
    title: '10. Cookies & Tracking',
    icon: Cookie,
    color: 'from-yellow-500 to-amber-500',
    content: `We use:
• Essential cookies (required for site functionality)
• Optional analytics cookies (e.g., Google Analytics)

Optional cookies are used only with your consent. You may manage preferences via browser settings or cookie banner.`
  },
  {
    id: 'retention',
    title: '11. Data Retention',
    icon: Clock,
    color: 'from-slate-500 to-gray-500',
    content: `Account data: Until deletion + up to 180 days
Billing & tax records: 8 years (legal requirement)
Inputs/Outputs: Until deleted or opt-out
Logs & analytics: Up to 12 months
Legal disputes: As required for protection`
  },
  {
    id: 'rights',
    title: '12. Your Rights Under DPDP Act',
    icon: UserCheck,
    color: 'from-emerald-500 to-green-500',
    content: `You have the right to:
• Access your personal data
• Request corrections of inaccurate data
• Withdraw consent (where applicable)
• Request deletion (subject to exceptions)
• Nominate a representative
• File a complaint with the Data Protection Board

To exercise rights, email: info@apexneural.com`
  },
  {
    id: 'breach',
    title: '13. Data Breach Notification',
    icon: Bell,
    color: 'from-rose-500 to-red-500',
    content: `In case of a personal data breach affecting your rights, we will notify you (where required by law) and the Data Protection Board of India, in accordance with legal obligations.`
  },
  {
    id: 'children',
    title: '14. Children\'s Privacy',
    icon: Baby,
    color: 'from-pink-500 to-rose-500',
    content: `Our Services are not intended for individuals under 18 years of age. We do not knowingly collect data from children. If inadvertently collected, we will delete it upon request.`
  }
];

export default function PrivacyPolicyPage() {
  return (
    <div className="min-h-screen bg-[#030303] text-white">
      {/* Animated background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 right-1/4 w-96 h-96 bg-green-500/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-1/3 left-1/4 w-80 h-80 bg-emerald-500/10 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }} />
        <div className="absolute top-1/2 right-1/3 w-64 h-64 bg-teal-500/5 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '2s' }} />
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
          <div className="text-center mb-12">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-green-500/10 border border-green-500/20 text-green-400 text-sm mb-6">
              <Shield className="w-4 h-4" />
              Your Privacy Matters
            </div>
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold mb-4 bg-gradient-to-r from-white via-gray-200 to-gray-400 bg-clip-text text-transparent">
              Privacy Policy
            </h1>
            <p className="text-gray-400 text-lg max-w-2xl mx-auto">
              Learn how we collect, use, and protect your personal information
            </p>
            <p className="text-sm text-gray-500 mt-4">Last Updated: 15-Dec-2025</p>
          </div>

          {/* Introduction Card */}
          <div className="relative rounded-3xl border border-white/10 bg-gradient-to-br from-white/[0.05] to-transparent p-8 mb-12 overflow-hidden">
            <div className="absolute top-0 right-0 w-64 h-64 bg-gradient-to-br from-green-500/10 to-transparent rounded-full blur-2xl" />
            <div className="relative">
              <h2 className="text-xl font-semibold mb-4 flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-green-500 to-emerald-500 flex items-center justify-center">
                  <Shield className="w-5 h-5" />
                </div>
                Our Commitment
              </h2>
              <p className="text-gray-300 leading-relaxed">
                <span className="text-white font-medium">ApexNeural Private Limited</span> respects your privacy and is committed to protecting your personal data. 
                This Privacy Policy describes how we collect, use, store, share, and protect your information in accordance with the 
                Digital Personal Data Protection Act, 2023 (DPDP Act), the Information Technology Act, 2000, and other applicable laws.
              </p>
            </div>
          </div>

          {/* Quick Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-12">
            {[
              { icon: Server, label: 'Data stored in', value: 'India', color: 'from-blue-500 to-cyan-500' },
              { icon: Lock, label: 'Encryption', value: 'AES-256', color: 'from-green-500 to-emerald-500' },
              { icon: Clock, label: 'Response time', value: '7 days', color: 'from-purple-500 to-pink-500' },
              { icon: Trash2, label: 'Delete requests', value: '30 days', color: 'from-orange-500 to-red-500' }
            ].map((stat, i) => {
              const Icon = stat.icon;
              return (
                <div key={i} className="rounded-2xl border border-white/10 bg-white/[0.02] p-4 text-center">
                  <div className={`w-10 h-10 mx-auto mb-3 rounded-xl bg-gradient-to-br ${stat.color} flex items-center justify-center`}>
                    <Icon className="w-5 h-5 text-white" />
                  </div>
                  <p className="text-xs text-gray-500 mb-1">{stat.label}</p>
                  <p className="text-lg font-semibold text-white">{stat.value}</p>
                </div>
              );
            })}
          </div>

          {/* Sections */}
          <div className="space-y-6">
            {sections.map((section, index) => {
              const Icon = section.icon;
              return (
                <div
                  key={section.id}
                  className="group relative rounded-2xl border border-white/10 bg-white/[0.02] hover:bg-white/[0.04] p-6 transition-all duration-300 hover:border-white/20"
                >
                  <div className="flex items-start gap-4">
                    <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${section.color} flex items-center justify-center flex-shrink-0 shadow-lg`}>
                      <Icon className="w-6 h-6 text-white" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <h3 className="text-lg font-semibold text-white mb-3">
                        {section.title}
                      </h3>
                      {section.content && (
                        <p className="text-sm text-gray-400 leading-relaxed whitespace-pre-line">
                          {section.content}
                        </p>
                      )}
                      {section.subsections && (
                        <div className="grid gap-4 md:grid-cols-3 mt-4">
                          {section.subsections.map((sub, i) => (
                            <div key={i} className="rounded-xl bg-white/[0.03] border border-white/5 p-4">
                              <h4 className="text-sm font-medium text-white mb-2">{sub.subtitle}</h4>
                              <ul className="space-y-1">
                                {sub.items.map((item, j) => (
                                  <li key={j} className="text-xs text-gray-400 flex items-start gap-2">
                                    <span className="w-1 h-1 rounded-full bg-gray-500 mt-1.5 flex-shrink-0" />
                                    {item}
                                  </li>
                                ))}
                              </ul>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Grievance Officer */}
          <div className="mt-12 rounded-3xl border border-white/10 bg-gradient-to-br from-green-500/10 via-transparent to-emerald-500/10 p-8">
            <div className="grid md:grid-cols-2 gap-8">
              <div>
                <div className="flex items-center gap-4 mb-4">
                  <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-green-500 to-emerald-500 flex items-center justify-center shadow-xl shadow-green-500/25">
                    <User className="w-7 h-7 text-white" />
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold">Grievance Officer</h3>
                    <p className="text-gray-400 text-sm">For privacy concerns</p>
                  </div>
                </div>
                <div className="space-y-2 text-sm text-gray-300">
                  <p><span className="text-gray-500">Name:</span> S.B.Rao</p>
                  <p><span className="text-gray-500">Email:</span> <a href="mailto:grievance@apexneural.com" className="text-green-400 hover:text-green-300">grievance@apexneural.com</a></p>
                  <p><span className="text-gray-500">Phone:</span> +91-98499 49597</p>
                </div>
              </div>
              <div>
                <div className="flex items-center gap-4 mb-4">
                  <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-emerald-500 to-teal-500 flex items-center justify-center shadow-xl shadow-emerald-500/25">
                    <Building2 className="w-7 h-7 text-white" />
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold">Contact Us</h3>
                    <p className="text-gray-400 text-sm">General inquiries</p>
                  </div>
                </div>
                <div className="text-sm text-gray-300">
                  <p>ApexNeural Private Limited</p>
                  <p className="text-gray-400">5th Floor, Shantha Sriram Building, PRS Towers,<br />Gachibowli, Telangana - 500032</p>
                  <p className="mt-2"><a href="mailto:info@apexneural.com" className="text-green-400 hover:text-green-300 inline-flex items-center gap-1"><Mail className="w-3 h-3" /> info@apexneural.com</a></p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
