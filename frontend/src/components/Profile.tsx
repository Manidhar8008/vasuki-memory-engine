import { useEffect, useState } from "react";

export default function Profile() {
  const [profile, setProfile] = useState<any>(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/founder/profile")
      .then(r => r.json())
      .then(setProfile);
  }, []);

  if (!profile) return <p>Loading profile...</p>;

  return (
    <section style={{ marginTop: "40px" }}>
      <h2>Founder Profile</h2>

      <h3>{profile.name}</h3>

      <p>{profile.title}</p>

      <p>{profile.mission}</p>

      <ul>
        {profile.focus.map((f: string, i: number) => (
          <li key={i}>{f}</li>
        ))}
      </ul>
    </section>
  );
}
