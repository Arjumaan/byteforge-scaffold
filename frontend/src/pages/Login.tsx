import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import api from '../lib/api';
import { useNavigate } from 'react-router-dom';
import { Zap, Shield, Mail, Lock } from 'lucide-react';

export function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const login = useMutation({
        mutationFn: async () => {
            const params = new URLSearchParams();
            params.append('username', email);
            params.append('password', password);
            const res = await api.post('/auth/token', params);
            localStorage.setItem('token', res.data.access_token);
            // Trigger storage listener in the same window
            window.dispatchEvent(new Event('storage'));
        },
        onSuccess: () => navigate('/')
    });

    const register = useMutation({
        mutationFn: async () => {
            await api.post('/auth/register', { email, password });
            // After successful registration, automatically log in
            const params = new URLSearchParams();
            params.append('username', email);
            params.append('password', password);
            const res = await api.post('/auth/token', params);
            localStorage.setItem('token', res.data.access_token);
            window.dispatchEvent(new Event('storage'));
        },
        onSuccess: () => navigate('/'),
        onError: (error: any) => {
            const message = error.response?.data?.detail || error.message || 'Registration failed. Check if backend is running.';
            alert(message);
        }
    });

    return (
        <div style={{
            minHeight: '100vh',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            background: 'radial-gradient(circle at top left, #1a1a2e 0%, #0a0a0c 100%)'
        }}>
            <div className="card glass-panel" style={{ width: 400, padding: 40 }}>
                <div style={{ textAlign: 'center', marginBottom: 32 }}>
                    <div style={{
                        width: 64,
                        height: 64,
                        background: 'var(--accent-primary)',
                        borderRadius: 16,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        margin: '0 auto 16px',
                        boxShadow: '0 0 20px var(--accent-glow)'
                    }}>
                        <Shield size={32} color="white" />
                    </div>
                    <h2 style={{ fontSize: '1.5rem', marginBottom: 8 }}>Vulnerability Portal</h2>
                    <p style={{ color: 'var(--text-muted)' }}>Secure access to ByteForge</p>
                </div>

                <div className="input-group">
                    <label className="input-label">Email Address</label>
                    <div style={{ position: 'relative' }}>
                        <Mail size={18} style={{ position: 'absolute', left: 12, top: 14, color: 'var(--text-muted)' }} />
                        <input
                            style={{ paddingLeft: 40 }}
                            placeholder="name@company.com"
                            value={email}
                            onChange={e => setEmail(e.target.value)}
                        />
                    </div>
                </div>

                <div className="input-group">
                    <label className="input-label">Security Key</label>
                    <div style={{ position: 'relative' }}>
                        <Lock size={18} style={{ position: 'absolute', left: 12, top: 14, color: 'var(--text-muted)' }} />
                        <input
                            type="password"
                            style={{ paddingLeft: 40 }}
                            placeholder="••••••••"
                            value={password}
                            onChange={e => setPassword(e.target.value)}
                        />
                    </div>
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
                    <button className="btn-primary" onClick={() => login.mutate()} disabled={login.isPending}>
                        {login.isPending ? 'Authenticating...' : 'Sign In'}
                    </button>
                    <button className="btn-secondary" onClick={() => register.mutate()}>
                        Create Free Account
                    </button>
                </div>
            </div>
        </div>
    );
}
