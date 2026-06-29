import { useEffect, useState } from "react"

export default function Stats() {

  const [stats,setStats] = useState<any>(null)

  useEffect(() => {
    fetch("http://127.0.0.1:8000/founder/stats")
      .then(r => r.json())
      .then(setStats)
  }, [])

  if(!stats) return <p>Loading stats...</p>

  return (
    <section style={{marginTop:"40px"}}>

      <h2>Founder Archive Stats</h2>

      <ul>
        <li>Artifacts: {stats.artifacts}</li>
        <li>Content: {stats.content}</li>
        <li>Core Files: {stats.core_files}</li>
        <li>Visions: {stats.visions}</li>
        <li>Memories: {stats.memories}</li>
      </ul>

    </section>
  )
}
