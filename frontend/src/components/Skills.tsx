export default function Skills() {

  const skills = [
    "Python",
    "SQLite",
    "FastAPI",
    "React",
    "Git",
    "GitHub",
    "AI Agents",
    "Knowledge Graphs",
    "Prompt Engineering"
  ];

  return (
    <section style={{ marginTop: "40px" }}>
      <h2>Skills</h2>

      <div>
        {skills.map((skill, i) => (
          <span
            key={i}
            style={{
              border: "1px solid #333",
              padding: "8px",
              margin: "4px",
              display: "inline-block"
            }}
          >
            {skill}
          </span>
        ))}
      </div>
    </section>
  );
}
