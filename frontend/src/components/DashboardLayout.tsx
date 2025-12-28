import { useState } from 'react';
import ChatInterface from './ChatInterface';
import Sidebar from './Sidebar';
import WelcomeScreen from './WelcomeScreen';

export interface Message {
    role: 'user' | 'assistant';
    content: string;
    logIndex?: number;
}

export default function DashboardLayout() {
    const [sessionId, setSessionId] = useState<string | null>(null);
    const [messages, setMessages] = useState<Message[]>([]);
    const [isProcessing, setIsProcessing] = useState(false);
    const [workflowLogs, setWorkflowLogs] = useState<string[]>([]);

    const handleDocumentUpload = (newSessionId: string) => {
        setSessionId(newSessionId);
        setMessages([]);
        setWorkflowLogs([]);
    };

    const handleReset = () => {
        setSessionId(null);
        setMessages([]);
        setWorkflowLogs([]);
    };

    return (
        <div className="flex h-screen bg-[#050505] overflow-hidden">
            <Sidebar
                onDocumentUpload={handleDocumentUpload}
                onReset={handleReset}
                sessionId={sessionId}
            />
            <main className="flex-1 flex flex-col overflow-hidden relative">
                {/* Animated background gradients */}
                <div className="absolute inset-0 overflow-hidden pointer-events-none">
                    <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[600px] bg-blue-600/10 blur-[120px] rounded-full" />
                    <div className="absolute bottom-0 right-0 w-[500px] h-[500px] bg-indigo-600/10 blur-[120px] rounded-full" />
                </div>
                <div className="relative z-10 flex-1 flex flex-col min-h-0">

                    {!sessionId ? (
                        <WelcomeScreen />
                    ) : (
                        <ChatInterface
                            sessionId={sessionId}
                            messages={messages}
                            setMessages={setMessages}
                            isProcessing={isProcessing}
                            setIsProcessing={setIsProcessing}
                            workflowLogs={workflowLogs}
                            setWorkflowLogs={setWorkflowLogs}
                        />
                    )}
                </div>
            </main>
        </div>
    );
}
