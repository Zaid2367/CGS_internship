import os

def write_html_report(out_dir, title, profile, hypothesis, conclusions, key_points, tables, figures):
    html_path = os.path.join(out_dir, "report.html")
    concitems = ""
    for c, v in conclusions.items():
        concitems += f"<li>{c}: {v}</li>"
    kp = ""
    for k in key_points:
        kp += f"<li>{k}</li>"
    tab=""
    for name, table in tables.items():
        if table is not None and not table.empty:
            tab += f"<h3>{name}</h3>"
            tab += table.to_html()
    viz = ""
    for fig in figures:
        if fig:
            rel = os.path.relpath(fig, out_dir)
            viz += f'<img src="{rel}" width="800"><br><br>'
    hype = ""
    for k, v in hypothesis.items():
        hype+=f"<li>{k}: {v}</li>"
    html = f"""
    <html><head><meta charset="utf-8"/>
    <title>{title}</title>
    <style>
      body {{ font-family: Arial; margin: 30px; }}
      h1 {{ color:#666; }}
      table {{ border-collapse: collapse; }}
      th, td {{ padding: 6px 10px; border: 1px solid #ddd; }}
    </style></head><body>

    <h1>{title}</h1>
    
    <h2>Data Summary</h2>
    <ul>
        <li>Rows: {profile.get("rows")}</li>
        <li>Columns: {profile.get("cols")}</li>
        <li>Duplicates: {profile.get("duplicates")}</li>
    </ul>

    <h2>Hypothesis</h2>
    <p>{hype}</p>

    <h2>Conclusions</h2>
    <ul>{concitems}</ul>

    <h2>Key Points</h2>
    <ul>{kp}</ul>

    <h2>Tables</h2>
    <p>{tab}</p>

    <h2>Visualizations</h2>
    <p>{viz}</p>
    </body>
    </html>
    """
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    return html_path
