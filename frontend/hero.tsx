export default function Hero() {
  return (
    <section className="min-h-screen flex flex-col justify-center px-8 max-w-6xl mx-auto">

      <p className="text-purple-400 uppercase tracking-widest">
        AI Systems Engineer
      </p>

      <h1 className="text-7xl font-bold mt-6">
        Building Personal
        <br />
        Intelligence Systems
      </h1>

      <p className="text-xl text-gray-400 mt-8 max-w-3xl">
        Creator of Vasuki Core —
        a personal intelligence system that transforms
        files, notes, PDFs, screenshots, and digital activity
        into searchable memory, knowledge graphs,
        timelines, and insights.
      </p>

      <div className="flex gap-4 mt-10">
        <button className="bg-purple-600 px-6 py-3 rounded-xl">
          Explore Vasuki
        </button>

        <button className="border border-white px-6 py-3 rounded-xl">
          View Architecture
        </button>
      </div>

    </section>
  );
}
