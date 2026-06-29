import Hero from "./components/Hero"
import Stats from "./components/Stats"
import VasukiCaseStudy from "./components/VasukiCaseStudy"
import Search from "./components/Search"
import Evidence from "./components/Evidence"
import Systems from "./components/Systems"
import HowIThink from "./components/HowIThink"
import CurrentFocus from "./components/CurrentFocus"

export default function App() {
  return (
    <main className="max-w-6xl mx-auto p-6">

      <Hero />

      <Stats />

      <VasukiCaseStudy />

      <Search />

      <Evidence />

      <Systems />

      <HowIThink />

      <CurrentFocus />

    </main>
  )
}
