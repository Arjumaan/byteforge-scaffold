import { useState, useEffect } from 'react';
import { Search, Command, ArrowRight, Zap, Play, FileText } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../lib/api';

interface CommandItem {
    id: string;
    name: string;
    icon: any;
    action: () => void;
    group: 'Navigation' | 'Actions' | 'Targets';
}

export function CommandPalette() {
    const [open, setOpen] = useState(false);
    const [query, setQuery] = useState('');
    const navigate = useNavigate();
    const queryClient = useQueryClient();

    // Fetch targets for quick actions
    const { data: targets } = useQuery({
        queryKey: ['targets'],
        queryFn: async () => (await api.get('/targets/')).data,
        enabled: open, // Only fetch when open
    });

    // Scan mutation
    const scanMutation = useMutation({
        mutationFn: async ({ targetId, kind }: { targetId: number, kind: string }) => {
            await api.post('/jobs/', { target_id: targetId, kind });
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['jobs'] });
            navigate('/jobs');
            setOpen(false);
        }
    });

    useEffect(() => {
        const down = (e: KeyboardEvent) => {
            if (e.key === 'k' && (e.metaKey || e.ctrlKey)) {
                e.preventDefault();
                setOpen((open) => !open);
            }
            if (e.key === 'Escape') {
                setOpen(false);
            }
        };

        document.addEventListener('keydown', down);
        return () => document.removeEventListener('keydown', down);
    }, []);

    const commands: CommandItem[] = [
        // Navigation
        { id: 'nav-dash', name: 'Go to Dashboard', icon: Command, group: 'Navigation', action: () => navigate('/') },
        { id: 'nav-targets', name: 'Go to Targets', icon: Command, group: 'Navigation', action: () => navigate('/targets') },
        { id: 'nav-jobs', name: 'Go to Jobs', icon: Command, group: 'Navigation', action: () => navigate('/jobs') },
        { id: 'nav-find', name: 'Go to Findings', icon: Command, group: 'Navigation', action: () => navigate('/findings') },
        { id: 'nav-evid', name: 'Go to Evidence', icon: Command, group: 'Navigation', action: () => navigate('/evidence') },
        { id: 'nav-rep', name: 'Go to Reports', icon: Command, group: 'Navigation', action: () => navigate('/reports') },
        { id: 'nav-set', name: 'Go to Settings', icon: Command, group: 'Navigation', action: () => navigate('/settings') },

        // General Actions
        { id: 'act-rep', name: 'Generate New Report', icon: FileText, group: 'Actions', action: () => navigate('/reports') }, // Ideally triggers generation modla
    ];

    // Dynamic Target Actions
    const targetCommands: CommandItem[] = targets?.flatMap((t: any) => [
        {
            id: `scan-nuc-${t.id}`,
            name: `Scan ${t.name} (Nuclei)`,
            icon: Zap,
            group: 'Targets',
            action: () => scanMutation.mutate({ targetId: t.id, kind: 'nuclei' })
        },
        {
            id: `scan-crawl-${t.id}`,
            name: `Crawl ${t.name} (Katana)`,
            icon: Play,
            group: 'Targets',
            action: () => scanMutation.mutate({ targetId: t.id, kind: 'crawl' })
        }
    ]) || [];

    const allCommands = [...commands, ...targetCommands];
    const filtered = allCommands.filter(c => c.name.toLowerCase().includes(query.toLowerCase()));

    if (!open) return null;

    return (
        <div style={{
            position: 'fixed', inset: 0,
            background: 'rgba(0,0,0,0.6)', backdropFilter: 'blur(4px)',
            display: 'flex', justifyContent: 'center', alignItems: 'flex-start', paddingTop: '15vh',
            zIndex: 9999
        }} onClick={() => setOpen(false)}>
            <div style={{
                width: '100%', maxWidth: '600px',
                background: '#1e1b4b', border: '1px solid rgba(255,255,255,0.1)',
                borderRadius: '12px', boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.5)',
                overflow: 'hidden'
            }} onClick={e => e.stopPropagation()}>
                <div style={{
                    display: 'flex', alignItems: 'center', padding: '16px',
                    borderBottom: '1px solid rgba(255,255,255,0.1)'
                }}>
                    <Search color="var(--text-muted)" size={20} />
                    <input
                        autoFocus
                        placeholder="Type a command or search..."
                        value={query}
                        onChange={e => setQuery(e.target.value)}
                        style={{
                            background: 'transparent', border: 'none', color: 'white',
                            fontSize: '1.1rem', marginLeft: '12px', flex: 1, outline: 'none'
                        }}
                    />
                    <div style={{ display: 'flex', alignItems: 'center', gap: 4, padding: '4px 8px', background: 'rgba(255,255,255,0.1)', borderRadius: 6, fontSize: '12px' }}>
                        <span style={{ fontSize: '0.8rem' }}>ESC</span>
                    </div>
                </div>

                <div style={{ maxHeight: '400px', overflowY: 'auto', padding: '8px' }}>
                    {['Navigation', 'Actions', 'Targets'].map(group => {
                        const groupItems = filtered.filter(c => c.group === group);
                        if (groupItems.length === 0) return null;

                        return (
                            <div key={group}>
                                <div style={{
                                    padding: '8px 12px', fontSize: '0.75rem',
                                    fontWeight: 600, color: 'var(--text-muted)',
                                    textTransform: 'uppercase', letterSpacing: '0.05em'
                                }}>
                                    {group}
                                </div>
                                {groupItems.map(item => (
                                    <div
                                        key={item.id}
                                        onClick={() => {
                                            item.action();
                                            setOpen(false);
                                        }}
                                        className="command-item"
                                        style={{
                                            display: 'flex', alignItems: 'center', padding: '12px 16px',
                                            borderRadius: '8px', cursor: 'pointer',
                                            color: 'var(--text-secondary)'
                                        }}
                                        onMouseEnter={e => e.currentTarget.style.backgroundColor = 'rgba(255,255,255,0.05)'}
                                        onMouseLeave={e => e.currentTarget.style.backgroundColor = 'transparent'}
                                    >
                                        <item.icon size={16} style={{ marginRight: 12, opacity: 0.5 }} />
                                        <span style={{ flex: 1 }}>{item.name}</span>
                                        {item.group === 'Targets' && <ArrowRight size={14} style={{ opacity: 0.3 }} />}
                                    </div>
                                ))}
                            </div>
                        );
                    })}

                    {filtered.length === 0 && (
                        <div style={{ padding: '20px', textAlign: 'center', color: 'var(--text-muted)' }}>
                            No results found.
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
