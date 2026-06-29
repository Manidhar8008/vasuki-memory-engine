import { useState } from "react";

export default function Search() {
  const [q, setQ] = useState("");
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  async function doSearch() {
    setLoading(true);

    try {
      const res = await fetch(
        `http://127.0.0.1:8000/founder/search?q=${encodeURIComponent(q)}`
      );

      const data = await res.json();
      setResults(data);
    } catch (err) {
      console.error(err);
    }

    setLoading(false);
  }

  return (
    <section
      style={{
        marginTop: "40px",
        padding: "20px",
        border: "1px solid #333",
        borderRadius: "12px"
      }}
    >
      <h2>Founder Search</h2>

      <input
        value={q}
        onChange={(e) => setQ(e.target.value)}
        placeholder="Search memories, files, ideas..."
        style={{
          width: "100%",
          padding: "12px",
          marginTop: "10px",
          color: "white",
          background: "#111",
          border: "1px solid #444"
        }}
      />

      <button
        onClick={doSearch}
        style={{
          marginTop: "10px",
          padding: "10px 20px",
          cursor: "pointer"
        }}
      >
        {loading ? "Searching..." : "Search"}
      </button>

      <div style={{ marginTop: "20px" }}>
        {results.map((r: any, i: number) => (
          <div
            key={i}
            style={{
              border: "1px solid #333",
              padding: "12px",
              marginBottom: "12px",
              borderRadius: "8px"
            }}
          >
            <h4>{r.filename}</h4>

            <pre
              style={{
                whiteSpace: "pre-wrap",
                overflowWrap: "break-word"
              }}
            >
              {r.preview}
            </pre>
          </div>
        ))}
      </div>
    </section>
  );
}
