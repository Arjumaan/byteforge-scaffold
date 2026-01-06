import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import axios from 'axios';
import { Target, Globe, Plus, Search, ExternalLink } from 'lucide-react';

const api = axios.create({ baseURL: 'http://localhost:8000' });

export function Targets() {
    const qc = useQueryClient();
    const token = localStorage.getItem('token') || '';
    const [name, setName] = useState('');
    const [scope, setScope] = useState('');

    const { data: targets, isLoading } = useQuery({
        queryKey: ['targets', token],
        queryFn: async () => {
            const res = await api.get('/targets/', { headers: { Authorization: `Bearer ${token}` } });
            return res.data;
        },
        enabled: !!token
    });

    const createTarget = useMutation({
        mutationFn: async () => {
            await api.post('/targets/', { name, scope }, { headers: { Authorization: `Bearer ${token}` } });
        },
        onSuccess: () => {
            qc.invalidateQueries({ queryKey: ['targets'] });
            setName('');
            setScope('');
        }
    });

    return (
        <div className="animate-in">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 40 }}>
                <div>
                    <h1 style={{ fontSize: '2.5rem', marginBottom: 8 }}>Target Scopes</h1>
                    <p style={{ color: 'var(--text-muted)' }}>Manage your penetration testing boundaries and assets.</p>
                </div>
                <button className="btn-primary" style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    <Plus size={18} />
                    <span>Add Target</span>
                </button>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1fr) 350px', gap: 24 }}>
                <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
                    <div className="card" style={{ padding: '12px 20px', display: 'flex', alignItems: 'center', gap: 12 }}>
                        <Search size={20} color="var(--text-muted)" />
                        <input placeholder="Search targets..." style={{ border: 'none', background: 'transparent', padding: 0 }} />
                    </div>

                    {isLoading ? (
                        <p>Loading assets...</p>
                    ) : (
                        targets?.map((t: any) => (
                            <div key={t.id} className="card glass-panel" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
                                    <div style={{ padding: 10, background: 'rgba(99,102,241,0.1)', borderRadius: 10 }}>
                                        <Globe size={24} color="var(--accent-primary)" />
                                    </div>
                                    <div>
                                        <h4 style={{ fontSize: '1.1rem' }}>{t.name}</h4>
                                        <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)' }}>{t.scope}</p>
                                    </div>
                                </div>
                                <div style={{ display: 'flex', gap: 12 }}>
                                    <div className="badge badge-info">Active</div>
                                    <button style={{ background: 'none', border: 'none', color: 'var(--text-muted)' }}>
                                        <ExternalLink size={20} />
                                    </button>
                                </div>
                            </div>
                        ))
                    )}
                </div>

                <div className="card glass-panel" style={{ height: 'fit-content' }}>
                    <h3 style={{ marginBottom: 20 }}>Quick Connect</h3>
                    <div className="input-group">
                        <label className="input-label">Project Name</label>
                        <input value={name} onChange={e => setName(e.target.value)} placeholder="e.g. My Website" />
                    </div>
                    <div className="input-group">
                        <label className="input-label">Scope (Domain/IP)</label>
                        <input value={scope} onChange={e => setScope(e.target.value)} placeholder="e.g. example.com" />
                    </div>
                    <button
                        className="btn-primary"
                        style={{ width: '100%' }}
                        onClick={() => createTarget.mutate()}
                        disabled={createTarget.isPending}
                    >
                        {createTarget.isPending ? 'Saving...' : 'Register Scope'}
                    </button>
                </div>
            </div>
        </div>
    );
}
