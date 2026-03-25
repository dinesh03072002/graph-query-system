import { useState } from "react";

function QueryBox() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState(null);

  const handleSearch = async () => {
    const res = await fetch("http://localhost:8000/query", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ query })
    });

    const data = await res.json();
    setResult(data);
  };

  return (
    <div style={{ margin: "20px" }}>
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Ask something..."
        style={{ width: "300px", padding: "10px" }}
      />
      <button onClick={handleSearch}>Search</button>

      <pre>{JSON.stringify(result, null, 2)}</pre>
    </div>
  );
}

export default QueryBox;