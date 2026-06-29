import { useEffect, useState } from "react"

export default function Hero() {
  const [profile, setProfile] = useState<any>(null)

  useEffect(() => {
    fetch("http://192.168.0.104:8000/founder/profile")
      .then(r => r.json())
      .then(setProfile)
  }, [])

  if (!profile) return <h2>Loading...</h2>

  return (
    <section>
      <h1>{profile.name}</h1>
      <h2>{profile.title}</h2>
      <p>{profile.mission}</p>
    </section>
  )
}
