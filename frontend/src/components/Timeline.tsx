export default function Timeline() {

  const events = [
    "Built Vasuki",
    "Created Founder Memory System",
    "Started Janani",
    "Built MW.AI",
    "Created Founder Explorer"
  ];

  return (
    <section style={{ marginTop: "40px" }}>
      <h2>Timeline</h2>

      {events.map((e, i) => (
        <div key={i}>
          <strong>2026</strong> — {e}
        </div>
      ))}
    </section>
  );
}
