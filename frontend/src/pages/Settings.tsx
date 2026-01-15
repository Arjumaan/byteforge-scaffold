import { useState } from 'react';
import { Save, Shield, Database, Bell, Lock, User } from 'lucide-react';
import api from '../lib/api';

export function Settings() {
    const [apiKey, setApiKey] = useState('********************************');
    const [notifications, setNotifications] = useState(true);
    const [theme, setTheme] = useState('dark');

    return (
        <div className="animate-in">
            <header style={{ marginBottom: 40 }}>
                <h1 style={{ fontSize: '2.5rem', marginBottom: 8 }}>Settings</h1>
                <p style={{ color: 'var(--text-muted)' }}>Manage system configuration and preferences.</p>
            </header>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: 24 }}>
                {/* Profile Section */}
                <div className="card">
                    <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 24 }}>
                        <div style={{ padding: 10, background: 'rgba(99, 102, 241, 0.2)', borderRadius: 10, color: '#6366f1' }}>
                            <User size={20} />
                        </div>
                        <h3 style={{ margin: 0 }}>Profile & Account</h3>
                    </div>

                    <div className="input-group">
                        <label className="input-label">Email Address</label>
                        <input value="admin@test.com" disabled style={{ opacity: 0.7 }} />
                    </div>

                    <div className="input-group">
                        <label className="input-label">Role</label>
                        <input value="Administrator" disabled style={{ opacity: 0.7 }} />
                    </div>
                </div>

                {/* Security Section */}
                <div className="card">
                    <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 24 }}>
                        <div style={{ padding: 10, background: 'rgba(34, 197, 94, 0.2)', borderRadius: 10, color: '#22c55e' }}>
                            <Shield size={20} />
                        </div>
                        <h3 style={{ margin: 0 }}>Security Configuration</h3>
                    </div>

                    <div className="input-group">
                        <label className="input-label">Master Encryption Key (AES-256)</label>
                        <div style={{ display: 'flex', gap: 8 }}>
                            <input type="password" value={apiKey} disabled style={{ flex: 1, fontFamily: 'monospace' }} />
                            <button className="btn-secondary" style={{ padding: '0 12px' }}>
                                <Lock size={16} />
                            </button>
                        </div>
                        <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: 8 }}>
                            Used to encrypt findings and evidence at rest. Managed in environment variables.
                        </p>
                    </div>
                </div>

                {/* Integrations Section */}
                <div className="card">
                    <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 24 }}>
                        <div style={{ padding: 10, background: 'rgba(59, 130, 246, 0.2)', borderRadius: 10, color: '#3b82f6' }}>
                            <Bell size={20} />
                        </div>
                        <h3 style={{ margin: 0 }}>Integrations</h3>
                    </div>

                    <div className="input-group">
                        <label className="input-label">Slack Webhook URL</label>
                        <input placeholder="https://hooks.slack.com/services/..." />
                    </div>

                    <div className="input-group">
                        <label className="input-label">Jira Domain</label>
                        <input placeholder="https://your-company.atlassian.net" />
                    </div>

                    <div style={{ display: 'flex', gap: 12 }}>
                        <div className="input-group" style={{ flex: 1 }}>
                            <label className="input-label">Jira Project Key</label>
                            <input placeholder="SEC" />
                        </div>
                        <div className="input-group" style={{ flex: 1 }}>
                            <label className="input-label">Jira Email</label>
                            <input placeholder="user@company.com" />
                        </div>
                    </div>
                </div>

                {/* System Section */}
                <div className="card">
                    <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 24 }}>
                        <div style={{ padding: 10, background: 'rgba(234, 179, 8, 0.2)', borderRadius: 10, color: '#eab308' }}>
                            <Database size={20} />
                        </div>
                        <h3 style={{ margin: 0 }}>System Preferences</h3>
                    </div>

                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
                        <div>
                            <div style={{ fontWeight: '500', marginBottom: 4 }}>Email Notifications</div>
                            <div style={{ fontSize: '0.875rem', color: 'var(--text-muted)' }}>Receive alerts for critical findings</div>
                        </div>
                        <label className="switch">
                            <input type="checkbox" checked={notifications} onChange={(e) => setNotifications(e.target.checked)} />
                            <span className="slider round"></span>
                        </label>
                    </div>

                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
                        <div>
                            <div style={{ fontWeight: '500', marginBottom: 4 }}>Dark Mode</div>
                            <div style={{ fontSize: '0.875rem', color: 'var(--text-muted)' }}>Toggle application theme</div>
                        </div>
                        <label className="switch">
                            <input
                                type="checkbox"
                                checked={theme === 'dark'}
                                onChange={(e) => {
                                    const newTheme = e.target.checked ? 'dark' : 'light';
                                    setTheme(newTheme);
                                    if (newTheme === 'light') {
                                        document.documentElement.setAttribute('data-theme', 'light');
                                    } else {
                                        document.documentElement.removeAttribute('data-theme');
                                    }
                                }}
                            />
                            <span className="slider round"></span>
                        </label>
                    </div>

                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <div>
                            <div style={{ fontWeight: '500', marginBottom: 4 }}>Audit Logging</div>
                            <div style={{ fontSize: '0.875rem', color: 'var(--text-muted)' }}>Log all security events (Enforced)</div>
                        </div>
                        <label className="switch">
                            <input type="checkbox" checked disabled />
                            <span className="slider round"></span>
                        </label>
                    </div>
                </div>
            </div>

            <div style={{ marginTop: 40, display: 'flex', justifyContent: 'flex-end' }}>
                <button className="btn-primary" style={{ padding: '12px 32px' }}>
                    <Save size={18} style={{ marginRight: 8 }} />
                    Save Changes
                </button>
            </div>

            <style>{`
                .switch {
                    position: relative;
                    display: inline-block;
                    width: 50px;
                    height: 26px;
                }
                .switch input {
                    opacity: 0;
                    width: 0;
                    height: 0;
                }
                .slider {
                    position: absolute;
                    cursor: pointer;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background-color: rgba(255,255,255,0.1);
                    transition: .4s;
                }
                .slider:before {
                    position: absolute;
                    content: "";
                    height: 18px;
                    width: 18px;
                    left: 4px;
                    bottom: 4px;
                    background-color: white;
                    transition: .4s;
                }
                input:checked + .slider {
                    background-color: var(--accent-primary);
                }
                input:checked + .slider:before {
                    transform: translateX(24px);
                }
                .slider.round {
                    border-radius: 34px;
                }
                .slider.round:before {
                    border-radius: 50%;
                }
            `}</style>
        </div>
    );
}
