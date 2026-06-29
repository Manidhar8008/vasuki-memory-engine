while True:
    cmd = input("vasuki> ")

    if cmd == "screenshots":
        run_screenshot_agent()

    elif cmd == "pdfs":
        run_pdf_ingest()

    elif cmd == "relationships":
        run_relationship_miner()

    elif cmd == "graph":
        run_graph_builder()
