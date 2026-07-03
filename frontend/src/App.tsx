import Hero from "./components/Hero";
import Stats from "./components/Stats";
import Systems from "./components/Systems";
import Memory from "./components/Memory";
import Timeline from "./components/Timeline";
import VasukiCaseStudy from "./components/VasukiCaseStudy";
import Search from "./components/Search";

export default function App() {
  return (
    <main className="bg-black text-white">
      <Hero />
      <Stats />
      <Systems />
      <Memory />
      <Timeline />
      <VasukiCaseStudy />
      <Search />
    </main>
  );
}
