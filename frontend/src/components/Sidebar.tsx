import { NavLink } from 'react-router-dom';
import { LucideIcon, LayoutDashboard, Target, Zap, FileText, Settings, ShieldAlert, Cpu, FolderOpen, Network } from 'lucide-react';

export function Sidebar() {
    const links: { title: string; icon: LucideIcon; path: string }[] = [
        { title: 'Dashboard', icon: LayoutDashboard, path: '/' },
        { title: 'Forge-Agent', icon: Cpu, path: '/ai' },
        { title: 'Targets', icon: Target, path: '/targets' },
        { title: 'Jobs', icon: Zap, path: '/jobs' },
        { title: 'Findings', icon: ShieldAlert, path: '/findings' },
        { title: 'Evidence', icon: FolderOpen, path: '/evidence' },
        { title: 'Network Map', icon: Network, path: '/network' },
        { title: 'Reports', icon: FileText, path: '/reports' },
        { title: 'Settings', icon: Settings, path: '/settings' },
    ];

    return (
        <aside className="sidebar">
            <div style={{ marginBottom: 40, display: 'flex', alignItems: 'center', gap: 12 }}>
                <div style={{ padding: 8, background: 'var(--accent-primary)', borderRadius: 8 }}>
                    <Zap size={24} color="white" />
                </div>
                <h2 className="gradient-text">ByteForge</h2>
            </div>
            <nav style={{ flex: 1 }}>
                {links.map((link) => (
                    <NavLink
                        key={link.path}
                        to={link.path}
                        className={({ isActive }: { isActive: boolean }) => `nav-link ${isActive ? 'active' : ''}`}
                    >
                        <link.icon size={20} />
                        <span>{link.title}</span>
                    </NavLink>
                ))}
            </nav>
            <div style={{ borderTop: '1px solid var(--border-color)', paddingTop: 20 }}>
                <div className="nav-link">
                    <Settings size={20} />
                    <span>v0.1.0-alpha</span>
                </div>
            </div>
        </aside>
    );
}
