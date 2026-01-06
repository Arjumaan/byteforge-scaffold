import { Sidebar } from './Sidebar';

export function Layout({ children }: { children: React.ReactNode }) {
    return (
        <div className="layout">
            <Sidebar />
            <main className="main-content">
                <div style={{ maxWidth: 1200, margin: '0 auto' }}>
                    {children}
                </div>
            </main>
        </div>
    );
}
