export default function Systems() {
  return (
    <section className="py-32 max-w-6xl mx-auto">

      <h2 className="text-5xl font-bold">
        What Vasuki Does
      </h2>

      <div className="grid md:grid-cols-4 gap-6 mt-12">

        <div>
          <h3>Capture</h3>
          <ul>
            <li>Files</li>
            <li>PDFs</li>
            <li>Notes</li>
            <li>Screenshots</li>
          </ul>
        </div>

        <div>
          <h3>Understand</h3>
          <ul>
            <li>Entities</li>
            <li>Relationships</li>
            <li>Metadata</li>
          </ul>
        </div>

        <div>
          <h3>Organize</h3>
          <ul>
            <li>Memory</li>
            <li>Timeline</li>
            <li>Knowledge Graph</li>
          </ul>
        </div>

        <div>
          <h3>Retrieve</h3>
          <ul>
            <li>Search</li>
            <li>Insights</li>
            <li>Reports</li>
          </ul>
        </div>

      </div>

    </section>
  );
}
