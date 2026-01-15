import { useQuery } from '@tanstack/react-query';
import api from '../lib/api';
import { FileText, Camera, Code, MessageSquare, ExternalLink } from 'lucide-react';

interface Evidence {
    id: number;
    finding_id: number;
    kind: string;
    data: string;
    created_at: string;
}

export function Evidence() {
    const { data: evidences, isLoading } = useQuery<Evidence[]>({
        queryKey: ['evidence'],
        queryFn: async () => {
            const res = await api.get('/evidence/');
            return res.data;
        },
    });

    const getKindIcon = (kind: string) => {
        switch (kind) {
            case 'request': return <Code size={18} />;
            case 'response': return <Code size={18} />;
            case 'screenshot': return <Camera size={18} />;
            case 'note': return <MessageSquare size={18} />;
            default: return <FileText size={18} />;
        }
    };

    const getKindColor = (kind: string) => {
        switch (kind) {
            case 'request': return '#6366f1';
            case 'response': return '#22c55e';
            case 'screenshot': return '#f59e0b';
            case 'note': return '#ec4899';
            default: return 'var(--text-muted)';
        }
    };

    return (
        <div className="animate-in">
            <header style={{ marginBottom: 40 }}>
                <h1 style={{ fontSize: '2.5rem', marginBottom: 8 }}>Evidence Vault</h1>
                <p style={{ color: 'var(--text-muted)' }}>Forensic artifacts and proof-of-concept data.</p>
            </header>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(400px, 1fr))', gap: 24 }}>
                {isLoading ? (
                    <p>Loading evidence...</p>
                ) : evidences?.length === 0 ? (
                    <div className="card glass-panel" style={{ textAlign: 'center', gridColumn: '1/-1', padding: 40 }}>
                        <FileText size={48} color="var(--text-muted)" style={{ margin: '0 auto 16px' }} />
                        <h3>No evidence collected yet</h3>
                        <p style={{ color: 'var(--text-muted)' }}>Evidence will appear here after vulnerability scans.</p>
                    </div>
                ) : evidences?.map((e) => (
                    <div key={e.id} className="card" style={{ borderLeft: `4px solid ${getKindColor(e.kind)}` }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                                <div style={{ padding: 8, background: `${getKindColor(e.kind)}20`, borderRadius: 8, color: getKindColor(e.kind) }}>
                                    {getKindIcon(e.kind)}
                                </div>
                                <span className="badge" style={{ background: `${getKindColor(e.kind)}20`, color: getKindColor(e.kind), textTransform: 'uppercase' }}>
                                    {e.kind}
                                </span>
                            </div>
                            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                                Finding #{e.finding_id}
                            </span>
                        </div>

                        <pre style={{
                            background: 'rgba(0,0,0,0.3)',
                            padding: 16,
                            borderRadius: 8,
                            overflow: 'auto',
                            maxHeight: 200,
                            fontSize: '0.75rem',
                            fontFamily: 'monospace',
                            whiteSpace: 'pre-wrap',
                            wordBreak: 'break-all'
                        }}>
                            {e.data}
                        </pre>

                        <div style={{ marginTop: 16, display: 'flex', gap: 8 }}>
                            <button className="btn-secondary" style={{ padding: '8px 16px', fontSize: '0.875rem' }}>
                                <ExternalLink size={14} style={{ marginRight: 6 }} />
                                View Full
                            </button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
