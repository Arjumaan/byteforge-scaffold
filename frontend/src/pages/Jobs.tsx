import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import api from '../lib/api';
import { Zap, Terminal, X } from 'lucide-react';

interface Job {
    id: number;
    kind: string;
    status: string;
    log: string;
    created_at: string;
}

export function Jobs() {
    const [selectedJob, setSelectedJob] = useState<Job | null>(null);

    const { data: jobs, isLoading } = useQuery<Job[]>({
        queryKey: ['jobs'],
        queryFn: async () => {
            const res = await api.get('/jobs/');
            return res.data;
        },
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
                                    <button
                                        onClick={() => setSelectedJob(job)}
                                        style={{ background: 'none', border: 'none', color: 'var(--accent-primary)', display: 'flex', alignItems: 'center', gap: 4 }}
                                    >
                                        <Terminal size={14} />
                                        <span>View Log</span>
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {/* Live Terminal Modal */}
            {selectedJob && (
                <div style={{
                    position: 'fixed', inset: 0,
                    background: 'rgba(0,0,0,0.8)', backdropFilter: 'blur(4px)',
                    zIndex: 1000, display: 'flex', alignItems: 'center', justifyContent: 'center'
                }} onClick={() => setSelectedJob(null)}>
                    <div style={{
                        width: '80%', height: '80%', background: '#0f172a',
                        borderRadius: '12px', border: '1px solid #334155',
                        display: 'flex', flexDirection: 'column', overflow: 'hidden'
                    }} onClick={e => e.stopPropagation()}>
                        <div style={{
                            padding: '16px 24px', borderBottom: '1px solid #334155',
                            display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                            background: '#1e293b'
                        }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                                <Terminal size={18} color="#22c55e" />
                                <span style={{ fontWeight: 600, fontFamily: 'monospace' }}>job_{selectedJob.id}.log</span>
                            </div>
                            <button onClick={() => setSelectedJob(null)} style={{ background: 'none', border: 'none', color: '#94a3b8' }}>
                                <X size={20} />
                            </button>
                        </div>
                        <div style={{
                            padding: '24px', overflowY: 'auto', flex: 1,
                            fontFamily: 'monospace', fontSize: '0.9rem', lineHeight: '1.6',
                            color: '#e2e8f0', background: '#0f172a'
                        }}>
                            <div style={{ color: '#64748b' }}># Execution log for Job #{selectedJob.id} ({selectedJob.kind})</div>
                            <div style={{ color: '#64748b' }}># Started at {new Date(selectedJob.created_at).toISOString()}</div>
                            <br />
                            <pre style={{ margin: 0, whiteSpace: 'pre-wrap' }}>
                                {formatLog(selectedJob.log)}
                            </pre>
                            {selectedJob.status === 'running' && (
                                <div style={{ display: 'inline-block', width: 8, height: 16, background: '#22c55e', marginLeft: 4, animation: 'blink 1s infinite' }} />
                            )}
                        </div>
                    </div>
                </div>
            )}
            <style>{`
                @keyframes blink { 50% { opacity: 0; } }
            `}</style>
        </div>
    );
}

function formatLog(log: string) {
    if (!log) return "Waiting for logs...";
    try {
        const parsed = JSON.parse(log);
        return JSON.stringify(parsed, null, 2);
    } catch {
        return log;
    }
}
