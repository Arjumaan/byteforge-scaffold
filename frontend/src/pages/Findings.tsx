import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import api from '../lib/api';
import { ShieldAlert, Info, AlertTriangle, Bug, Code2, X, Sparkles } from 'lucide-react';

interface Finding {
    id: number;
    title: string;
    severity: string;
    cwe?: string;
    description?: string;
}

export function Findings() {
    const [selectedRemediation, setSelectedRemediation] = useState<Finding | null>(null);

    const { data: findings, isLoading } = useQuery<Finding[]>({
        queryKey: ['findings'],
        queryFn: async () => {
            const res = await api.get('/findings/');
            return res.data;
        },
    });

    const getSeverityColor = (sev: string) => {
        switch (sev.toLowerCase()) {
            case 'critical': return 'var(--danger)';
            case 'high': return '#fb7185';
            case 'medium': return 'var(--warning)';
            case 'low': return '#34d399';
            default: return 'var(--text-muted)';
        }
    };

    const getAiRemediation = (finding: Finding) => {
        // Simulation of AI-generated patch
        const lowerTitle = finding.title.toLowerCase();

        if (lowerTitle.includes('xss') || lowerTitle.includes('script')) {
            return `// ByteForge AI Suggestion for XSS (React)
// VULNERABLE: <div dangerouslySetInnerHTML={{ __html: userInput }} />

// SECURE FIX: Use textContent or a sanitizer library
import DOMPurify from 'dompurify';

const SecureComponent = ({ userInput }) => {
    const clean = DOMPurify.sanitize(userInput);
    
    // SAFE approach
    return <div dangerouslySetInnerHTML={{ __html: clean }} />;
};`;
        }

        if (lowerTitle.includes('sql') || lowerTitle.includes('injection')) {
            return `# ByteForge AI Suggestion for SQL Injection (Python/SQLAlchemy)
# VULNERABLE: cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")

# SECURE FIX: Use parameterized queries
stmt = select(User).where(User.id == user_id)
result = session.execute(stmt)`;
        }

        return `// ByteForge AI Suggestion
// Analyzing patch strategies for ${finding.title}...
// Recommended: Review input validation and output encoding.

function secureFunction(input) {
  if (!isValid(input)) throw new Error("Invalid Input");
  return encodeHTML(input);
}`;
    };

    return (
        <div className="animate-in">
            <header style={{ marginBottom: 40 }}>
                <h1 style={{ fontSize: '2.5rem', marginBottom: 8 }}>Vulnerability Archive</h1>
                <p style={{ color: 'var(--text-muted)' }}>Consolidated findings from all security scans.</p>
            </header>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))', gap: 24 }}>
                {isLoading ? (
                    <p>Analyzing finding data...</p>
                ) : findings?.length === 0 ? (
                    <div className="card glass-panel" style={{ textAlign: 'center', gridColumn: '1/-1' }}>
                        <div style={{ marginBottom: 16 }}>
                            <ShieldAlert size={48} color="var(--text-muted)" style={{ margin: '0 auto' }} />
                        </div>
                        <h3>No vulnerabilities detected yet</h3>
                        <p style={{ color: 'var(--text-muted)' }}>New findings will appear here once scans are completed.</p>
                    </div>
                ) : findings?.map((f: any) => (
                    <div key={f.id} className="card" style={{ borderLeft: `4px solid ${getSeverityColor(f.severity)}` }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 12 }}>
                            <span className="badge" style={{ background: `${getSeverityColor(f.severity)}20`, color: getSeverityColor(f.severity) }}>
                                {f.severity}
                            </span>
                            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>CWE-{f.cwe || 'N/A'}</span>
                        </div>
                        <h3 style={{ marginBottom: 8 }}>{f.title}</h3>
                        <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)', marginBottom: 16 }}>
                            Potential {f.title.toLowerCase()} vulnerability found via automated scanning.
                        </p>
                        <div style={{ display: 'flex', gap: 12 }}>
                            <button className="btn-secondary" style={{ padding: '8px 16px', fontSize: '0.875rem', flex: 1 }}>Details</button>
                            <button
                                className="btn-primary"
                                style={{ padding: '8px 16px', fontSize: '0.875rem', flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 6 }}
                                onClick={() => setSelectedRemediation(f)}
                            >
                                <Sparkles size={14} />
                                <span>AI Fix</span>
                            </button>
                        </div>
                    </div>
                ))}
            </div>

            {/* AI Remediation Modal */}
            {selectedRemediation && (
                <div style={{
                    position: 'fixed', inset: 0,
                    background: 'rgba(0,0,0,0.8)', backdropFilter: 'blur(4px)',
                    zIndex: 1000, display: 'flex', alignItems: 'center', justifyContent: 'center'
                }} onClick={() => setSelectedRemediation(null)}>
                    <div style={{
                        width: '80%', maxWidth: '800px', background: 'var(--bg-card)',
                        borderRadius: '12px', border: '1px solid var(--border-color)',
                        display: 'flex', flexDirection: 'column', overflow: 'hidden',
                        boxShadow: '0 25px 50px -12px rgba(0,0,0,0.5)'
                    }} onClick={e => e.stopPropagation()}>
                        <div style={{
                            padding: '24px', borderBottom: '1px solid var(--border-color)',
                            display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                            background: 'rgba(255,255,255,0.02)'
                        }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                                <div style={{ padding: 8, background: 'linear-gradient(135deg, #6366f1, #a855f7)', borderRadius: 8, color: 'white' }}>
                                    <Sparkles size={20} />
                                </div>
                                <div>
                                    <h3 style={{ margin: 0 }}>AI Remediation Suggestion</h3>
                                    <span style={{ fontSize: '0.875rem', color: 'var(--text-muted)' }}>Auto-generated fix for {selectedRemediation.title}</span>
                                </div>
                            </div>
                            <button onClick={() => setSelectedRemediation(null)} style={{ background: 'none', border: 'none', color: 'var(--text-muted)' }}>
                                <X size={24} />
                            </button>
                        </div>

                        <div style={{ padding: '24px', background: '#0f172a' }}>
                            <div style={{
                                background: '#1e293b', borderRadius: '8px', padding: '16px',
                                fontFamily: 'monospace', fontSize: '0.9rem', lineHeight: '1.6',
                                border: '1px solid #334155', color: '#e2e8f0', overflowX: 'auto'
                            }}>
                                <pre style={{ margin: 0 }}>{getAiRemediation(selectedRemediation)}</pre>
                            </div>
                        </div>

                        <div style={{ padding: '24px', borderTop: '1px solid var(--border-color)', display: 'flex', justifyContent: 'flex-end', gap: 12 }}>
                            <button className="btn-secondary" onClick={() => setSelectedRemediation(null)}>Dismiss</button>
                            <button className="btn-primary" onClick={() => alert("Copied to clipboard!")}>Copy Code</button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
