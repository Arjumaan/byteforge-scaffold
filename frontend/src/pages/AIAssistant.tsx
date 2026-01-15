import { useState, useRef, useEffect } from 'react';
import api from '../lib/api';
import { motion, AnimatePresence } from 'framer-motion';
import { Shield, Terminal, Send, Cpu, Sparkles, Command } from 'lucide-react';

interface Message {
    role: 'user' | 'agent';
    content: string;
    suggestions?: string[];
    agent?: string;
}

export function AIAssistant() {
    const [input, setInput] = useState('');
    const [history, setHistory] = useState<Message[]>([]);
    const [isTyping, setIsTyping] = useState(false);
    const scrollRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [history, isTyping]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userQuery = input;
        setInput('');
        setHistory(prev => [...prev, { role: 'user', content: userQuery }]);
        setIsTyping(true);

        try {
            const res = await api.post('/ai/query', { prompt: userQuery });

            setHistory(prev => [...prev, {
                role: 'agent',
                content: res.data.message,
                suggestions: res.data.suggestions,
                agent: res.data.agent
            }]);
        } catch (err) {
            setHistory(prev => [...prev, { role: 'agent', content: 'Connection to Forge-Agent lost. Re-establishing link...' }]);
        } finally {
            setIsTyping(false);
        }
    };

    return (
        <div className="animate-in" style={{ height: 'calc(100vh - 120px)', display: 'flex', flexDirection: 'column' }}>
            <header style={{ marginBottom: 24, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
                    <div style={{ padding: 12, background: 'linear-gradient(135deg, #6366f1, #a855f7)', borderRadius: 12, boxShadow: '0 0 20px rgba(99, 102, 241, 0.3)' }}>
                        <Cpu color="white" size={24} />
                    </div>
                    <div>
                        <h1 style={{ fontSize: '1.875rem' }}>Forge-Agent</h1>
                        <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>Combining Antigravity Speed & Claude Logic</p>
                    </div>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '6px 12px', background: 'rgba(52, 211, 153, 0.1)', borderRadius: 20, border: '1px solid rgba(52, 211, 153, 0.2)' }}>
                    <Shield size={14} color="#34d399" />
                    <span style={{ fontSize: '0.75rem', color: '#34d399', fontWeight: 600, letterSpacing: '0.05em' }}>AES-256 SECURE SESSION</span>
                </div>
            </header>

            <div className="card glass-panel" style={{ flex: 1, display: 'flex', flexDirection: 'column', padding: 0, overflow: 'hidden', borderBottomLeftRadius: 0, borderBottomRightRadius: 0 }}>
                <div ref={scrollRef} style={{ flex: 1, overflowY: 'auto', padding: 24, display: 'flex', flexDirection: 'column', gap: 20 }}>
                    {history.length === 0 && (
                        <div style={{ textAlign: 'center', marginTop: 100, color: 'var(--text-muted)' }}>
                            <Sparkles size={48} style={{ margin: '0 auto 16px', opacity: 0.5 }} />
                            <h3>Intelligence Ready</h3>
                            <p>Ask me to analyze targets, suggest scans, or explain findings.</p>
                        </div>
                    )}

                    {history.map((msg, i) => (
                        <motion.div
                            key={i}
                            initial={{ opacity: 0, x: msg.role === 'user' ? 20 : -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            style={{
                                alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
                                maxWidth: '80%',
                                display: 'flex',
                                gap: 12,
                                flexDirection: msg.role === 'user' ? 'row-reverse' : 'row'
                            }}
                        >
                            <div style={{
                                padding: '12px 18px',
                                borderRadius: 16,
                                background: msg.role === 'user' ? 'var(--accent-primary)' : 'rgba(255,255,255,0.05)',
                                border: msg.role === 'user' ? 'none' : '1px solid var(--border-color)',
                                color: 'white',
                                position: 'relative'
                            }}>
                                {msg.agent && <span style={{ fontSize: '0.65rem', position: 'absolute', top: -18, left: 10, color: 'var(--accent-secondary)', fontWeight: 700 }}>{msg.agent.toUpperCase()}</span>}
                                {msg.content}

                                {msg.suggestions && (
                                    <div style={{ display: 'flex', gap: 8, marginTop: 12, flexWrap: 'wrap' }}>
                                        {msg.suggestions.map((s: string) => (
                                            <button
                                                key={s}
                                                onClick={() => setInput(s)}
                                                style={{
                                                    fontSize: '0.75rem',
                                                    padding: '4px 10px',
                                                    borderRadius: 99,
                                                    background: 'rgba(255,255,255,0.1)',
                                                    border: 'none',
                                                    color: 'var(--text-main)'
                                                }}
                                            >
                                                {s}
                                            </button>
                                        ))}
                                    </div>
                                )}
                            </div>
                        </motion.div>
                    ))}

                    {isTyping && (
                        <div style={{ alignSelf: 'flex-start', padding: 12, background: 'rgba(255,255,255,0.05)', borderRadius: 16 }}>
                            <div className="typing-indicator">
                                <span></span><span></span><span></span>
                            </div>
                        </div>
                    )}
                </div>

                <form onSubmit={handleSubmit} style={{ padding: 20, borderTop: '1px solid var(--border-color)', background: 'rgba(0,0,0,0.2)' }}>
                    <div style={{ position: 'relative' }}>
                        <Terminal size={18} style={{ position: 'absolute', left: 16, top: 18, color: 'var(--text-muted)' }} />
                        <input
                            value={input}
                            onChange={e => setInput(e.target.value)}
                            placeholder="Type your security directive..."
                            style={{
                                paddingLeft: 48,
                                paddingRight: 60,
                                height: 54,
                                background: 'rgba(0,0,0,0.3)',
                                fontSize: '1rem'
                            }}
                        />
                        <button
                            type="submit"
                            className="btn-primary"
                            style={{ position: 'absolute', right: 8, top: 8, padding: '8px 12px' }}
                        >
                            <Send size={18} />
                        </button>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginTop: 12, fontSize: '0.7rem', color: 'var(--text-muted)' }}>
                        <Command size={12} />
                        <span>K + Enter to quickly dispatch command</span>
                    </div>
                </form>
            </div>

            <style>{`
        .typing-indicator span {
          height: 8px; width: 8px; background: var(--text-muted); display: inline-block; border-radius: 50%; margin: 0 2px;
          animation: bounce 1.4s infinite ease-in-out both; opacity: 0.6;
        }
        .typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
        .typing-indicator span:nth-child(2) { animation-delay: -0.16s; }
        @keyframes bounce { 0%, 80%, 100% { transform: scale(0); } 40% { transform: scale(1.0); } }
      `}</style>
        </div>
    );
}
