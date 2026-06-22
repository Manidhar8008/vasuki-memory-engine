import sqlite3

conn=sqlite3.connect("founder.db")

cur=conn.cursor()

projects=[

("vasuki","platform"),

("mw.ai","company"),

("janani","project")

]

for name,ptype in projects:

    cur.execute("""

    INSERT OR IGNORE INTO doctor_projects(

    name,
    project_type

    )

    VALUES(?,?)

    """,(name,ptype))

agents=[

("doctor_agent"),

("project_archaeologist"),

("founder_psychologist"),

("memory_builder")

]

for agent in agents:

    cur.execute("""

    INSERT OR IGNORE INTO doctor_agents(

    name

    )

    VALUES(?)

    """,(agent,))

conn.commit()

conn.close()

print("SEEDED")
