import { useState, useEffect } from 'react';
import { CreditCard, CheckCircle2, AlertCircle, Loader2, Lock } from 'lucide-react';
import { createPaymentOrder, capturePaymentOrder, PaymentOrder } from '../services/api';

interface PaymentComponentProps {
  planName?: string;
  amount: number;
  currency?: string;
  description?: string;
  onSuccess?: () => void;
}

export default function PaymentComponent({
  planName = 'Pro Plan',
  amount,
  currency = 'USD',
  description,
  onSuccess
}: PaymentComponentProps) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const [processingReturn, setProcessingReturn] = useState(false);

  // Check if returning from PayPal
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('token');
    const payerId = urlParams.get('PayerID');

    if (token && payerId && !processingReturn) {
      setProcessingReturn(true);
      handlePayPalReturn(token);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handlePayPalReturn = async (orderId: string) => {
    setLoading(true);
    setError(null);
    try {
      const captureResult = await capturePaymentOrder({ order_id: orderId });
      if (captureResult) {
        setSuccess(true);
        if (onSuccess) onSuccess();
        // Clean up URL
        window.history.replaceState({}, document.title, window.location.pathname);
      }
    } catch (err: any) {
      console.error('Payment capture error:', err);
      setError(err.response?.data?.detail || err.message || 'Failed to capture payment');
    } finally {
      setLoading(false);
      setProcessingReturn(false);
    }
  };

  const handlePayment = async () => {
    setLoading(true);
    setError(null);
    setSuccess(false);

    try {
      // Create PayPal order
      const order: PaymentOrder = await createPaymentOrder({
        amount,
        currency,
        description: description || `${planName} Subscription`
      });

      // Find approval URL from PayPal response
      const approvalUrl = order.order?.links?.find(
        (link: any) => link.rel === 'approve'
      )?.href;

      if (approvalUrl) {
        // Redirect to PayPal for approval
        window.location.href = approvalUrl;
      } else {
        // If no approval URL, try to capture directly (for testing)
        if (order.order_id || order.order?.id) {
          const captureResult = await capturePaymentOrder({
            order_id: order.order_id || order.order?.id
          });
          
          if (captureResult) {
            setSuccess(true);
            if (onSuccess) onSuccess();
          }
        } else {
          throw new Error('No order ID received');
        }
      }
    } catch (err: any) {
      console.error('Payment error:', err);
      console.error('Error response:', err.response?.data);
      const errorMessage = err.response?.data?.detail || err.response?.data?.message || err.message || 'Payment failed';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  // Show processing state if returning from PayPal
  if (processingReturn) {
    return (
      <div className="p-6 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
        <div className="text-center">
          <Loader2 className="h-8 w-8 animate-spin mx-auto text-blue-600 mb-4" />
          <p className="text-gray-600 dark:text-gray-400">
            Processing your payment...
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
      <div className="flex items-center gap-3 mb-4">
        <div className="p-2 bg-blue-100 dark:bg-blue-900/30 rounded-lg">
          <CreditCard className="h-5 w-5 text-blue-600 dark:text-blue-400" />
        </div>
        <div>
          <h3 className="font-semibold text-gray-900 dark:text-gray-100">
            {planName}
          </h3>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Secure payment via PayPal
          </p>
        </div>
      </div>

      <div className="mb-6">
        <div className="flex justify-between items-baseline mb-2">
          <span className="text-gray-600 dark:text-gray-400">Amount</span>
          <span className="text-2xl font-bold text-gray-900 dark:text-gray-100">
            {currency} {amount.toFixed(2)}
          </span>
        </div>
        {description && (
          <p className="text-sm text-gray-500 dark:text-gray-500 mt-2">
            {description}
          </p>
        )}
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
          <div className="flex items-center gap-2 text-red-700 dark:text-red-400 text-sm">
            <AlertCircle className="h-4 w-4 flex-shrink-0" />
            <span>{error}</span>
          </div>
        </div>
      )}

      {success && (
        <div className="mb-4 p-3 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg">
          <div className="flex items-center gap-2 text-green-700 dark:text-green-400 text-sm">
            <CheckCircle2 className="h-4 w-4 flex-shrink-0" />
            <span>Payment successful!</span>
          </div>
        </div>
      )}

      <button
        onClick={handlePayment}
        disabled={loading || success}
        className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white rounded-lg transition-colors font-medium shadow-sm"
      >
        {loading ? (
          <>
            <Loader2 className="h-4 w-4 animate-spin" />
            Processing...
          </>
        ) : success ? (
          <>
            <CheckCircle2 className="h-4 w-4" />
            Paid
          </>
        ) : (
          <>
            <Lock className="h-4 w-4" />
            Pay with PayPal
          </>
        )}
      </button>

      <p className="mt-4 text-xs text-center text-gray-500 dark:text-gray-500">
        Your payment is secured by PayPal
      </p>
    </div>
  );
}

