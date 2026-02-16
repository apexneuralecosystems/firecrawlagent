import { useEffect, useState } from 'react';
import { checkBackendHealth, getApiBaseUrl } from '../services/api';

type Status = 'checking' | 'connected' | 'error';

export function BackendStatus() {
  const [status, setStatus] = useState<Status>('checking');
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function run() {
      const result = await checkBackendHealth();
      if (cancelled) return;
      if (result.ok) {
        setStatus('connected');
        setErrorMessage(null);
      } else {
        setStatus('error');
        setErrorMessage(result.error ?? 'Backend did not respond.');
      }
    }

    run();
    return () => {
      cancelled = true;
    };
  }, []);

  const baseUrl = getApiBaseUrl();

  if (status === 'checking') {
    return (
      <div
        className="flex items-center justify-center gap-2 px-3 py-2 text-sm bg-slate-700/80 text-slate-200"
        role="status"
        aria-live="polite"
      >
        <span className="inline-block w-3 h-3 rounded-full border-2 border-slate-400 border-t-transparent animate-spin" />
        Checking backend at {baseUrl}…
      </div>
    );
  }

  if (status === 'error') {
    return (
      <div
        className="flex flex-wrap items-center justify-center gap-2 px-3 py-2 text-sm bg-red-900/90 text-red-100"
        role="alert"
      >
        <span className="font-medium">Backend unreachable</span>
        <span className="opacity-90">
          ({baseUrl}) — {errorMessage ?? 'Is the server running?'}
        </span>
      </div>
    );
  }

  return (
    <div
      className="flex items-center justify-center gap-2 px-3 py-2 text-sm bg-emerald-900/60 text-emerald-100"
      role="status"
    >
      <span className="inline-block w-2 h-2 rounded-full bg-emerald-400" />
      Backend connected ({baseUrl})
    </div>
  );
}
