import { useQuery } from '@tanstack/react-query';
import axios from 'axios';
import { Zap, Clock, Terminal, CheckCircle2, AlertCircle } from 'lucide-react';

const api = axios.create({ baseURL: 'http://localhost:8000' });

export function Jobs() {
    const token = localStorage.getItem('token') || '';

    const { data: jobs, isLoading } = useQuery({
        queryKey: ['jobs', token],
        queryFn: async () => {
            const res = await api.get('/jobs/', { headers: { Authorization: `Bearer ${token}` } });
            return res.data;
        },
        enabled: !!token
    });

    const getStatusBadge = (status: string) => {
        switch (status) {
            case 'completed': return <span className="badge badge-success">Completed</span>;
            case 'running': return <span className="badge badge-info">Running</span>;
            case 'failed': return <span className="badge badge-danger">Failed</span>;
            default: return <span className="badge badge-warning">Queued</span>;
        }
    };

    return (
        <div className="animate-in">
            <header style={{ marginBottom: 40 }}>
                <h1 style={{ fontSize: '2.5rem', marginBottom: 8 }}>Job Console</h1>
                <p style={{ color: 'var(--text-muted)' }}>Monitor scanning activity and background tasks.</p>
            </header>

            <div className="card glass-panel" style={{ padding: 0, overflow: 'hidden' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                    <thead>
                        <tr style={{ textAlign: 'left', borderBottom: '1px solid var(--border-color)', background: 'rgba(255,255,255,0.02)' }}>
                            <th style={{ padding: '16px 24px', color: 'var(--text-muted)', fontWeight: 600 }}>ID</th>
                            <th style={{ padding: '16px 24px', color: 'var(--text-muted)', fontWeight: 600 }}>KIND</th>
                            <th style={{ padding: '16px 24px', color: 'var(--text-muted)', fontWeight: 600 }}>STATUS</th>
                            <th style={{ padding: '16px 24px', color: 'var(--text-muted)', fontWeight: 600 }}>CREATED</th>
                            <th style={{ padding: '16px 24px', color: 'var(--text-muted)', fontWeight: 600 }}>ACTION</th>
                        </tr>
                    </thead>
                    <tbody>
                        {isLoading ? (
                            <tr><td colSpan={5} style={{ padding: 24, textAlign: 'center' }}>Syncing with worker...</td></tr>
                        ) : jobs?.length === 0 ? (
                            <tr><td colSpan={5} style={{ padding: 24, textAlign: 'center' }}>No jobs recorded yet.</td></tr>
                        ) : jobs?.map((job: any) => (
                            <tr key={job.id} style={{ borderBottom: '1px solid var(--border-color)' }}>
                                <td style={{ padding: '16px 24px' }}>#{job.id}</td>
                                <td style={{ padding: '16px 24px' }}>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                                        <Zap size={16} color="var(--accent-primary)" />
                                        {job.kind.toUpperCase()}
                                    </div>
                                </td>
                                <td style={{ padding: '16px 24px' }}>{getStatusBadge(job.status)}</td>
                                <td style={{ padding: '16px 24px', color: 'var(--text-muted)' }}>{new Date(job.created_at).toLocaleString()}</td>
                                <td style={{ padding: '16px 24px' }}>
                                    <button style={{ background: 'none', border: 'none', color: 'var(--accent-primary)', display: 'flex', alignItems: 'center', gap: 4 }}>
                                        <Terminal size={14} />
                                        <span>View Log</span>
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
