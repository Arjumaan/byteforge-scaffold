import { motion } from 'framer-motion';
import { LucideIcon, Target, Zap, ShieldAlert, CheckCircle2 } from 'lucide-react';

export function Dashboard() {
    const stats: { label: string; value: string; icon: LucideIcon; trend: string }[] = [
        { label: 'Active Targets', value: '12', icon: Target, trend: '+2 this week' },
        { label: 'Jobs Running', value: '4', icon: Zap, trend: 'High load' },
        { label: 'Vulnerabilities', value: '87', icon: ShieldAlert, trend: '12 Critical' },
        { label: 'Reports Ready', value: '45', icon: CheckCircle2, trend: 'All synced' },
    ];

    return (
        <div className="animate-in">
            <header style={{ marginBottom: 40 }}>
                <h1 style={{ fontSize: '2.5rem', marginBottom: 8 }}>Security Overview</h1>
                <p style={{ color: 'var(--text-muted)' }}>Welcome back, administrator. Here's what's happening today.</p>
            </header>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: 24, marginBottom: 40 }}>
                {stats.map((stat, i) => (
                    <motion.div
                        key={stat.label}
                        className="card"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: i * 0.1 }}
                    >
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 16 }}>
                            <div style={{ padding: 12, background: 'rgba(255,255,255,0.05)', borderRadius: 12 }}>
                                <stat.icon size={24} color="var(--accent-primary)" />
                            </div>
                            <span style={{ fontSize: '0.75rem', color: 'var(--accent-primary)', fontWeight: 600 }}>{stat.trend}</span>
                        </div>
                        <h3 style={{ fontSize: '0.875rem', color: 'var(--text-muted)', marginBottom: 4 }}>{stat.label}</h3>
                        <p style={{ fontSize: '1.875rem', fontWeight: 700 }}>{stat.value}</p>
                    </motion.div>
                ))}
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: 24 }}>
                <div className="card glass-panel" style={{ minHeight: 400 }}>
                    <h3 style={{ marginBottom: 20 }}>Recent Activity</h3>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
                        {[1, 2, 3].map(i => (
                            <div key={i} style={{ display: 'flex', gap: 16, padding: '12px 0', borderBottom: '1px solid var(--border-color)' }}>
                                <div style={{ width: 8, height: 8, borderRadius: '50%', background: 'var(--accent-primary)', marginTop: 6 }} />
                                <div>
                                    <p style={{ fontWeight: 500 }}>Nuclei scan completed for production-api.env</p>
                                    <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)' }}>2 hours ago • 4 new findings</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="card glass-panel">
                    <h3 style={{ marginBottom: 20 }}>Quick Actions</h3>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
                        <button className="btn-primary" onClick={() => window.location.href = '/targets'}>New Target Scan</button>
                        <button className="btn-secondary" onClick={() => window.location.href = '/reports'}>Export Latest Report</button>
                        <button className="btn-secondary" onClick={() => window.location.href = '/settings'}>User Settings</button>
                    </div>
                </div>
            </div>
        </div>
    );
}
