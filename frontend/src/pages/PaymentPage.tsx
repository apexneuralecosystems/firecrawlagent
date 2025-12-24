import { motion } from 'framer-motion';
import { ArrowLeft, CreditCard } from 'lucide-react';
import { Link } from 'react-router-dom';
import PaymentComponent from '../components/PaymentComponent';
import Sidebar from '../components/Sidebar';

export default function PaymentPage() {
  return (
    <div className="flex h-screen bg-gray-50 dark:bg-gray-900">
      <Sidebar
        onDocumentUpload={() => {}}
        onReset={() => {}}
        sessionId={null}
      />
      <main className="flex-1 flex flex-col overflow-hidden">
        <div className="flex-1 overflow-y-auto p-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="max-w-2xl mx-auto"
          >
            {/* Header */}
            <div className="mb-8">
              <Link
                to="/dashboard"
                className="inline-flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 mb-4 transition-colors"
              >
                <ArrowLeft className="h-4 w-4" />
                Back to Dashboard
              </Link>
              <div className="flex items-center gap-3 mb-2">
                <div className="p-3 bg-blue-100 dark:bg-blue-900/30 rounded-lg">
                  <CreditCard className="h-6 w-6 text-blue-600 dark:text-blue-400" />
                </div>
                <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">
                  Payment & Subscription
                </h1>
              </div>
              <p className="text-gray-600 dark:text-gray-400 mt-2">
                Choose a plan that fits your needs and unlock all features
              </p>
            </div>

            {/* Payment Plans */}
            <div className="space-y-6">
              {/* Pro Plan */}
              <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6 shadow-sm">
                <PaymentComponent
                  planName="Pro Plan"
                  amount={49}
                  currency="USD"
                  description="Unlimited access to all features including Firecrawl integration, advanced filtering, priority support, cloud LLM direct access, and unlimited sessions"
                  onSuccess={() => {
                    console.log('Payment successful!');
                    // Could redirect to dashboard or show success message
                  }}
                />
              </div>

              {/* Additional Plans */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Community Plan */}
                <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6 shadow-sm">
                  <h3 className="text-xl font-bold text-gray-900 dark:text-gray-100 mb-2">
                    Community
                  </h3>
                  <div className="mb-4">
                    <span className="text-3xl font-bold text-gray-900 dark:text-gray-100">$0</span>
                    <span className="text-gray-600 dark:text-gray-400 text-sm ml-2">/month</span>
                  </div>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                    Perfect for local development and individuals
                  </p>
                  <ul className="space-y-2 mb-6 text-sm text-gray-600 dark:text-gray-400">
                    <li className="flex items-center gap-2">
                      <span className="text-green-500">✓</span>
                      Local LLM Support
                    </li>
                    <li className="flex items-center gap-2">
                      <span className="text-green-500">✓</span>
                      Standard Indexing
                    </li>
                    <li className="flex items-center gap-2">
                      <span className="text-green-500">✓</span>
                      Core Agentic Workflow
                    </li>
                    <li className="flex items-center gap-2">
                      <span className="text-green-500">✓</span>
                      Community Support
                    </li>
                  </ul>
                  <button
                    disabled
                    className="w-full py-2 px-4 bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400 rounded-lg font-medium cursor-not-allowed"
                  >
                    Current Plan
                  </button>
                </div>

                {/* Enterprise Plan */}
                <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6 shadow-sm">
                  <h3 className="text-xl font-bold text-gray-900 dark:text-gray-100 mb-2">
                    Enterprise
                  </h3>
                  <div className="mb-4">
                    <span className="text-3xl font-bold text-gray-900 dark:text-gray-100">Custom</span>
                  </div>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                    Scalable RAG infrastructure for large datasets
                  </p>
                  <ul className="space-y-2 mb-6 text-sm text-gray-600 dark:text-gray-400">
                    <li className="flex items-center gap-2">
                      <span className="text-green-500">✓</span>
                      Milvus/Qdrant Clusters
                    </li>
                    <li className="flex items-center gap-2">
                      <span className="text-green-500">✓</span>
                      Custom Agent Logic
                    </li>
                    <li className="flex items-center gap-2">
                      <span className="text-green-500">✓</span>
                      Dedicated Infrastructure
                    </li>
                    <li className="flex items-center gap-2">
                      <span className="text-green-500">✓</span>
                      SLA Guarantee
                    </li>
                    <li className="flex items-center gap-2">
                      <span className="text-green-500">✓</span>
                      SSO Integration
                    </li>
                  </ul>
                  <button className="w-full py-2 px-4 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 rounded-lg font-medium transition-colors">
                    Contact Sales
                  </button>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </main>
    </div>
  );
}

