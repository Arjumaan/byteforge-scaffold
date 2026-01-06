import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Target, Zap, FileText, Settings, ShieldAlert } from 'lucide-react';

export function Sidebar() {
    const links = [
        { title: 'Dashboard', icon: LayoutDashboard, path: '/' },
        { title: 'Targets', icon: Target, path: '/targets' },
        { title: 'Jobs', icon: Zap, path: '/jobs' },
        { title: 'Findings', icon: ShieldAlert, path: '/findings' },
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
                        className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
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
