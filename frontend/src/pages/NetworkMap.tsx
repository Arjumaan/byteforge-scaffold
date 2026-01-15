import { useCallback } from 'react';
import ReactFlow, {
    Background,
    Controls,
    MiniMap,
    useNodesState,
    useEdgesState,
    addEdge,
    Connection,
    Edge,
    Node
} from 'reactflow';
import 'reactflow/dist/style.css';
import { useQuery } from '@tanstack/react-query';
import api from '../lib/api';

const initialNodes: Node[] = [];
const initialEdges: Edge[] = [];

export function NetworkMap() {
    const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
    const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

    const onConnect = useCallback((params: Connection) => setEdges((eds) => addEdge(params, eds)), [setEdges]);

    // Fetch Targets and Findings to build the graph
    const { isLoading } = useQuery({
        queryKey: ['network-graph'],
        queryFn: async () => {
            const targetsRes = await api.get('/targets/');
            const findingsRes = await api.get('/findings/');

            const newNodes: Node[] = [];
            const newEdges: Edge[] = [];

            // Add Targets (Level 0)
            targetsRes.data.forEach((t: any, i: number) => {
                newNodes.push({
                    id: `target-${t.id}`,
                    type: 'input',
                    data: { label: t.name },
                    position: { x: 250 * i, y: 0 },
                    style: { background: '#6366f1', color: 'white', border: 'none', width: 180 }
                });

                // Add Findings for this target (Level 1)
                const targetFindings = findingsRes.data.filter((f: any) => f.target_id === t.id);
                targetFindings.forEach((f: any, j: number) => {
                    const findingNodeId = `finding-${f.id}`;
                    newNodes.push({
                        id: findingNodeId,
                        data: { label: `${f.severity}: ${f.title}` },
                        position: { x: (250 * i) + (Math.random() * 100 - 50), y: 150 + (j * 60) },
                        style: {
                            background: f.severity === 'critical' ? '#dc2626' :
                                f.severity === 'high' ? '#ea580c' : '#1e293b',
                            color: 'white',
                            fontSize: '12px',
                            border: '1px solid rgba(255,255,255,0.2)',
                            width: 200
                        }
                    });

                    // Connect Target -> Finding
                    newEdges.push({
                        id: `e-${t.id}-${f.id}`,
                        source: `target-${t.id}`,
                        target: findingNodeId,
                        animated: true,
                        style: { stroke: '#475569' }
                    });
                });
            });

            setNodes(newNodes);
            setEdges(newEdges);
            return true;
        }
    });

    return (
        <div style={{ height: '80vh', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 12, overflow: 'hidden' }}>
            <ReactFlow
                nodes={nodes}
                edges={edges}
                onNodesChange={onNodesChange}
                onEdgesChange={onEdgesChange}
                onConnect={onConnect}
                fitView
            >
                <Background color="#aaa" gap={16} />
                <Controls />
                <MiniMap style={{ background: '#1e1b4b' }}
                    nodeColor={(n) => {
                        if (n.style?.background) return n.style.background as string;
                        return '#fff';
                    }}
                />
            </ReactFlow>
        </div>
    );
}
