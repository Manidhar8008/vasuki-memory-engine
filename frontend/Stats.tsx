const stats = [
  ["Files Indexed", "41,802"],
  ["PDFs Processed", "595"],
  ["Entities", "44,444"],
  ["Mentions", "545,000"],
];

export default function Stats() {
  return (
    <section className="py-24">
      <div className="max-w-6xl mx-auto grid md:grid-cols-4 gap-6">

        {stats.map(([title,value])=>(
          <div
            key={title}
            className="bg-zinc-900 p-8 rounded-2xl"
          >
            <h3 className="text-4xl font-bold">
              {value}
            </h3>

            <p className="text-gray-400 mt-2">
              {title}
            </p>
          </div>
        ))}

      </div>
    </section>
  );
}
