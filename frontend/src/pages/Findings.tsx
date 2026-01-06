import { useQuery } from '@tanstack/react-query';
import axios from 'axios';
import { ShieldAlert, Info, AlertTriangle, Bug } from 'lucide-react';

const api = axios.create({ baseURL: 'http://localhost:8000' });

export function Findings() {
    const token = localStorage.getItem('token') || '';

    const { data: findings, isLoading } = useQuery({
        queryKey: ['findings', token],
        queryFn: async () => {
            const res = await api.get('/findings/', { headers: { Authorization: `Bearer ${token}` } });
            return res.data;
        },
        enabled: !!token
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
                            <button className="btn-secondary" style={{ padding: '8px 16px', fontSize: '0.875rem' }}>Details</button>
                            <button className="btn-secondary" style={{ padding: '8px 16px', fontSize: '0.875rem' }}>Evidence</button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
