import { useEffect, useRef, useState } from "react";
import cytoscape from "cytoscape";

function GraphView({ highlightIds = [] }) {
  const cyRef = useRef(null);
  const cyInstanceRef = useRef(null);
  const [nodeCount, setNodeCount] = useState(0);
  const [edgeCount, setEdgeCount] = useState(0);
  const [showLegend, setShowLegend] = useState(true);

  // Node colors based on type
  const getNodeColor = (type) => {
    const colors = {
      customer: "#10b981",  // Emerald
      order: "#3b82f6",     // Blue
      delivery: "#f59e0b",  // Amber
      invoice: "#8b5cf6",   // Purple
      payment: "#ef4444",   // Red
      default: "#6b7280"    // Gray
    };
    return colors[type] || colors.default;
  };

  // Initialize graph
  useEffect(() => {
    fetch("http://localhost:8000/graph")
      .then(res => res.json())
      .then(data => {
        setNodeCount(data.nodes.length);
        setEdgeCount(data.edges.length);

        const elements = [
          ...data.nodes.map(n => ({
            data: { 
              id: n.id, 
              label: n.label,
              type: n.id.split("_")[0],
              originalId: n.id.split("_")[1]
            }
          })),
          ...data.edges.map(e => ({
            data: {
              source: e.source,
              target: e.target,
              label: e.label
            }
          }))
        ];

        const cy = cytoscape({
          container: cyRef.current,
          elements: elements,
          style: [
            {
              selector: "node",
              style: {
                "label": "data(label)",
                "background-color": (ele) => getNodeColor(ele.data("type")),
                "width": 45,
                "height": 45,
                "font-size": "11px",
                "font-weight": "500",
                "color": "#fff",
                "text-valign": "center",
                "text-halign": "center",
                "text-wrap": "wrap",
                "text-max-width": "80px",
                "border-width": "2px",
                "border-color": "#fff",
                "border-opacity": 0.8,
                "shadow-blur": 8,
                "shadow-color": "rgba(0,0,0,0.2)",
                "shadow-offset-x": 2,
                "shadow-offset-y": 2,
                "transition-property": "background-color, width, height, shadow-blur",
                "transition-duration": "0.2s"
              }
            },
            {
              selector: "node.highlighted",
              style: {
                "background-color": "#ff4757",
                "border-width": 3,
                "border-color": "#ff0000",
                "border-opacity": 1,
                "width": 55,
                "height": 55,
                "font-weight": "bold",
                "font-size": "12px",
                "shadow-blur": 15,
                "shadow-color": "rgba(255,71,87,0.6)"
              }
            },
            {
              selector: "node.neighbor",
              style: {
                "background-color": "#ffa502",
                "border-width": 2,
                "border-color": "#ff8800"
              }
            },
            {
              selector: "node:hover",
              style: {
                "width": 52,
                "height": 52,
                "shadow-blur": 12,
                "font-size": "12px"
              }
            },
            {
              selector: "edge",
              style: {
                "label": "data(label)",
                "width": 2,
                "line-color": "#9ca3af",
                "target-arrow-color": "#9ca3af",
                "target-arrow-shape": "triangle",
                "curve-style": "bezier",
                "font-size": "9px",
                "color": "#6b7280",
                "text-rotation": "autorotate",
                "text-background-color": "#fff",
                "text-background-opacity": 0.8,
                "text-background-padding": "2px",
                "text-background-shape": "roundrectangle"
              }
            },
            {
              selector: "edge.highlighted",
              style: {
                "width": 3,
                "line-color": "#ff4757",
                "target-arrow-color": "#ff4757"
              }
            },
            {
              selector: "edge:hover",
              style: {
                "width": 3,
                "line-color": "#3b82f6"
              }
            }
          ],
          layout: {
            name: "cose",
            nodeRepulsion: 15000,
            idealEdgeLength: 180,
            edgeElasticity: 0.3,
            gravity: 0.2,
            numIter: 1500,
            padding: 50,
            animate: true,
            animationDuration: 800,
            fit: true
          },
          wheelSensitivity: 0.5,
          minZoom: 0.5,
          maxZoom: 2.5
        });

        cyInstanceRef.current = cy;

        // Node click handler
        cy.on("tap", "node", (evt) => {
          const node = evt.target;
          const nodeData = node.data();
          
          // Show tooltip/info
          const info = {
            id: nodeData.id,
            type: nodeData.type,
            label: nodeData.label,
            originalId: nodeData.originalId
          };
          
          // Optional: You can trigger a callback here
          console.log("Node clicked:", info);
        });

        // Fit after layout
        cy.ready(() => {
          setTimeout(() => {
            cy.fit();
            cy.center();
          }, 100);
        });

        return () => cy.destroy();
      })
      .catch(error => {
        console.error("Error loading graph:", error);
      });
  }, []);

  // Handle highlight updates
  useEffect(() => {
    const cy = cyInstanceRef.current;
    if (!cy) return;

    cy.elements().removeClass("highlighted neighbor");
    
    if (highlightIds.length > 0) {
      highlightIds.forEach(id => {
        const node = cy.$(`#${id}`);
        if (node.length > 0) {
          node.addClass("highlighted");
          node.connectedEdges().addClass("highlighted");
          node.neighborhood().nodes().addClass("neighbor");
        }
      });
      
      // Fit to highlighted nodes
      const highlightedNodes = cy.$("node.highlighted");
      if (highlightedNodes.length > 0) {
        cy.fit(highlightedNodes, 80);
      }
    }
  }, [highlightIds]);

  return (
    <div className="graph-container">
      {/* Graph Toolbar */}
      <div className="graph-toolbar">
        <div className="toolbar-left">
          
        </div>
        <div className="toolbar-right">
          <button 
            className="toolbar-button"
            onClick={() => setShowLegend(!showLegend)}
          >
            📖 Legend
          </button>
          <button 
            className="toolbar-button"
            onClick={() => {
              const cy = cyInstanceRef.current;
              if (cy) {
                cy.fit();
                cy.center();
              }
            }}
          >
            🎯 Fit View
          </button>
          <button 
            className="toolbar-button"
            onClick={() => {
              const cy = cyInstanceRef.current;
              if (cy) {
                cy.reset();
                cy.fit();
              }
            }}
          >
            ⟳ Reset
          </button>
        </div>
      </div>

      {/* Graph Canvas */}
      <div className="graph-canvas" ref={cyRef} />

      {/* Legend */}
      {showLegend && (
        <div className="graph-legend">
          <div className="legend-header">
            <strong>Legend</strong>
            <button onClick={() => setShowLegend(false)}>✕</button>
          </div>
          <div className="legend-items">
            <div className="legend-item">
              <div className="legend-color" style={{ background: "#10b981" }}></div>
              <span>Customer</span>
            </div>
            <div className="legend-item">
              <div className="legend-color" style={{ background: "#3b82f6" }}></div>
              <span>Order</span>
            </div>
            <div className="legend-item">
              <div className="legend-color" style={{ background: "#f59e0b" }}></div>
              <span>Delivery</span>
            </div>
            <div className="legend-item">
              <div className="legend-color" style={{ background: "#8b5cf6" }}></div>
              <span>Invoice</span>
            </div>
            <div className="legend-item">
              <div className="legend-color" style={{ background: "#ef4444" }}></div>
              <span>Payment</span>
            </div>
          </div>
          <div className="legend-note">
            <div className="legend-highlight"></div>
            <span>Highlighted nodes</span>
          </div>
        </div>
      )}
    </div>
  );
}

export default GraphView;