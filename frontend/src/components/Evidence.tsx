import { useEffect, useState } from "react";

export default function Evidence() {

  const [items, setItems] = useState<any[]>([]);

  useEffect(() => {

    fetch("http://127.0.0.1:8000/founder/evidence")
      .then(r => r.json())
      .then(setItems);

  }, []);

  return (

    <section style={{marginTop:"40px"}}>

      <h2>Evidence Archive</h2>

      {items.map((x,i) => (

        <div
          key={i}
          style={{
            border:"1px solid #333",
            padding:"12px",
            marginBottom:"12px"
          }}
        >

          <h4>{x.filename}</h4>

          <pre
            style={{
              whiteSpace:"pre-wrap"
            }}
          >
            {x.preview}
          </pre>

        </div>

      ))}

    </section>

  );
}
