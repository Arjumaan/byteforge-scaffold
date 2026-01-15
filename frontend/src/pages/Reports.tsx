import { useQuery } from '@tanstack/react-query';
import api from '../lib/api';
import { FileText, Download, Shield, AlertTriangle, CheckCircle } from 'lucide-react';

interface Report {
    id: number;
    job_id: number;
    log: string;
    created_at: string;
    status: string;
}

export function Reports() {
    const { data: jobs, isLoading } = useQuery<Report[]>({
        queryKey: ['reports'],
        queryFn: async () => {
            const res = await api.get('/jobs/');
            // Filter only report jobs
            return res.data.filter((j: any) => j.kind === 'report');
        },
    });

    const parseReport = (log: string) => {
        try {
            return JSON.parse(log);
        } catch {
            return null;
        }
    };

    return (
        <div className="animate-in">
            <header style={{ marginBottom: 40 }}>
                <h1 style={{ fontSize: '2.5rem', marginBottom: 8 }}>Security Reports</h1>
                <p style={{ color: 'var(--text-muted)' }}>Generated assessment reports and executive summaries.</p>
            </header>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))', gap: 24 }}>
                {isLoading ? (
                    <p>Loading reports...</p>
                ) : jobs?.length === 0 ? (
                    <div className="card glass-panel" style={{ textAlign: 'center', gridColumn: '1/-1', padding: 40 }}>
                        <FileText size={48} color="var(--text-muted)" style={{ margin: '0 auto 16px' }} />
                        <h3>No reports generated</h3>
                        <p style={{ color: 'var(--text-muted)' }}>Run a report job to generate security assessments.</p>
                    </div>
                ) : jobs?.map((job) => {
                    const reportData = parseReport(job.log);
                    if (!reportData) return null;

                    return (
                        <div key={job.id} className="card">
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 20 }}>
                                <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                                    <div style={{ padding: 10, background: 'rgba(99, 102, 241, 0.2)', borderRadius: 10, color: '#6366f1' }}>
                                        <FileText size={20} />
                                    </div>
                                    <div>
                                        <h3 style={{ margin: 0, fontSize: '1.1rem' }}>{reportData.report_id || `Report #${job.id}`}</h3>
                                        <span style={{ fontSize: '0.875rem', color: 'var(--text-muted)' }}>
                                            {new Date(job.created_at).toLocaleDateString()}
                                        </span>
                                    </div>
                                </div>
                                <span className={`badge ${job.status === 'completed' ? 'badge-success' : 'badge-warning'}`}>
                                    {job.status}
                                </span>
                            </div>

                            <div style={{ display: 'flex', gap: 16, marginBottom: 20 }}>
                                <div style={{ flex: 1, padding: 12, background: 'rgba(255,255,255,0.03)', borderRadius: 8, textAlign: 'center' }}>
                                    <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: reportData.risk_score > 70 ? '#ef4444' : reportData.risk_score > 40 ? '#eab308' : '#22c55e' }}>
                                        {reportData.risk_score || 0}
                                    </div>
                                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Risk Score</div>
                                </div>
                                <div style={{ flex: 1, padding: 12, background: 'rgba(255,255,255,0.03)', borderRadius: 8, textAlign: 'center' }}>
                                    <div style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>
                                        {reportData.total_findings || 0}
                                    </div>
                                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Findings</div>
                                </div>
                            </div>

                            <div style={{ display: 'flex', gap: 8 }}>
                                <button className="btn-primary" style={{ flex: 1 }} onClick={() => {
                                    const blob = new Blob([JSON.stringify(reportData, null, 2)], { type: 'application/json' });
                                    const url = URL.createObjectURL(blob);
                                    const a = document.createElement('a');
                                    a.href = url;
                                    a.download = `${reportData.report_id}.json`;
                                    a.click();
                                }}>
                                    <Download size={16} style={{ marginRight: 8 }} />
                                    JSON
                                </button>
                                <button className="btn-secondary" style={{ flex: 1 }} disabled>
                                    <FileText size={16} style={{ marginRight: 8 }} />
                                    PDF (Pro)
                                </button>
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
}
