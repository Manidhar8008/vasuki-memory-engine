import { useEffect, useState } from "react";

export default function Memory() {
  const [memory, setMemory] = useState<any>(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/founder/memory")
      .then(r => r.json())
      .then(setMemory);
  }, []);

  if (!memory) return <p>Loading memory...</p>;

  return (
    <section style={{ marginTop: "40px" }}>
      <h2>Founder Memory</h2>

      <h3>{memory.title}</h3>

      <pre
        style={{
          whiteSpace: "pre-wrap",
          border: "1px solid #333",
          padding: "12px",
          maxHeight: "400px",
          overflowY: "auto"
        }}
      >
        {memory.content}
      </pre>
    </section>
  );
}
