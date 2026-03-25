import { useState, useRef, useEffect } from "react";

function ChatInterface({ onQueryResult }) {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: "bot",
      content: "Hi! I can help you analyze the Order to Cash process. Ask me about customers, orders, deliveries, invoices, or payments!"
    }
  ]);
  const [inputValue, setInputValue] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!inputValue.trim() || loading) return;

    const userMessage = {
      id: messages.length + 1,
      type: "user",
      content: inputValue
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInputValue("");
    setLoading(true);

    try {
      const response = await fetch("http://localhost:8000/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ query: inputValue })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Query failed");
      }

      const data = await response.json();
      
      // Pass highlight IDs to parent
      if (onQueryResult && data.highlight_ids) {
        onQueryResult(data);
      }

      // Format bot response
      let botResponse = "";
      if (data.result && data.result.length > 0) {
        botResponse = `Found ${data.result.length} result(s).`;
        
        // Add summary for common queries
        if (inputValue.toLowerCase().includes("customer") && data.result[0].customer_name) {
          botResponse += ` Here's what I found for customer ${data.result[0].customer_name}.`;
        } else if (inputValue.toLowerCase().includes("total") || inputValue.toLowerCase().includes("amount")) {
          const total = data.result.reduce((sum, row) => {
            const amount = row.total_amount || row.amount || 0;
            return sum + parseFloat(amount);
          }, 0);
          botResponse += ` Total amount: ₹${total.toFixed(2)}.`;
        }
        
        botResponse += ` The relevant nodes are highlighted in the graph.`;
      } else {
        botResponse = "No results found for your query. Try asking about specific customers, orders, or invoices.";
      }

      const botMessage = {
        id: messages.length + 2,
        type: "bot",
        content: botResponse,
        sql: data.sql,
        resultCount: data.result?.length || 0
      };
      
      setMessages(prev => [...prev, botMessage]);
      
    } catch (error) {
      const errorMessage = {
        id: messages.length + 2,
        type: "bot",
        content: `Sorry, I encountered an error: ${error.message}. Please try asking a different question.`,
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
      inputRef.current?.focus();
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const exampleQueries = [
    "Show orders for customer 310000108",
    "Which products have the highest invoice amounts?",
    "Show incomplete flows (delivered but not invoiced)",
    "What's the total payment amount for customer 320000083?"
  ];

  return (
    <div className="chat-interface">
      {/* Header */}
      <div className="chat-header">
        <div className="chat-header-icon">🤖</div>
        <div className="chat-header-info">
          <h3>Dodge AI</h3>
          <p>Graph Agent</p>
        </div>
      </div>

      {/* Messages */}
      <div className="chat-messages">
        {messages.map((message) => (
          <div key={message.id} className={`message ${message.type}`}>
            <div className="message-avatar">
              {message.type === "bot" ? "🤖" : "👤"}
            </div>
            <div className={`message-content ${message.isError ? "error" : ""}`}>
              <p>{message.content}</p>
              {message.sql && (
                <details className="sql-details">
                  <summary>View generated SQL</summary>
                  <pre><code>{message.sql}</code></pre>
                </details>
              )}
              {message.resultCount > 0 && (
                <div className="result-badge">
                  📊 {message.resultCount} records found
                </div>
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div className="message bot">
            <div className="message-avatar">🤖</div>
            <div className="message-content loading">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Example Queries */}
      <div className="example-queries">
        <p>Try asking:</p>
        <div className="query-chips">
          {exampleQueries.map((query, index) => (
            <button
              key={index}
              className="query-chip"
              onClick={() => {
                setInputValue(query);
                inputRef.current?.focus();
              }}
            >
              {query}
            </button>
          ))}
        </div>
      </div>

      {/* Input Area */}
      <div className="chat-input-area">
        <textarea
          ref={inputRef}
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask about orders, customers, invoices..."
          rows={2}
          disabled={loading}
        />
        <button 
          onClick={handleSend} 
          disabled={loading || !inputValue.trim()}
          className="send-button"
        >
          {loading ? "..." : "Send"}
        </button>
      </div>
    </div>
  );
}

export default ChatInterface;