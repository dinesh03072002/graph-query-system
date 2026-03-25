import { useState } from 'react';
import GraphView from './components/GraphView';
import ChatInterface from './components/ChatInterface';
import './App.css';

function App() {
  const [highlightIds, setHighlightIds] = useState([]);
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const handleQueryResult = (result) => {
    if (result && result.highlight_ids) {
      setHighlightIds(result.highlight_ids);
    }
  };

  const clearHighlights = () => {
    setHighlightIds([]);
  };

  return (
    <div className="app">


      {/* Main Content */}
      <div className="main-container">
        {/* Sidebar - Chat Interface */}
        <div className={`sidebar ${sidebarOpen ? 'open' : 'closed'}`}>
          <ChatInterface onQueryResult={handleQueryResult} />
        </div>

        {/* Graph Area */}
        <div className="graph-area">
          <GraphView highlightIds={highlightIds} />
        </div>
      </div>
    </div>
  );
}

export default App;