import { useEffect, useState } from "react";

export default function Explorer() {
  const [profile, setProfile] = useState<any>(null);
  const [projects, setProjects] = useState<any[]>([]);
  const [knowledge, setKnowledge] = useState<any[]>([]);

  useEffect(() => {
    fetch("http://localhost:8000/whoami")
      .then((r) => r.json())
      .then(setProfile);

    fetch("http://localhost:8000/projects")
      .then((r) => r.json())
      .then(setProjects);

    fetch("http://localhost:8000/knowledge")
      .then((r) => r.json())
      .then(setKnowledge);
  }, []);

  return (
    <div style={{ padding: "40px" }}>
      <h1>Who Is Manidhar?</h1>

      {profile && (
        <div>
          <h2>{profile.title}</h2>
          <p>{profile.focus}</p>
          <p>{profile.mission}</p>
        </div>
      )}

      <h2>Projects</h2>

      {projects.map((p, i) => (
        <div key={i}>
          <strong>{p.name}</strong>
          <p>{p.description}</p>
        </div>
      ))}

      <h2>Knowledge Domains</h2>

      <ul>
        {knowledge.map((k, i) => (
          <li key={i}>{k}</li>
        ))}
      </ul>
    </div>
  );
}
