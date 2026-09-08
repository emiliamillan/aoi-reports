#!/usr/bin/env python3
import pandas as pd
import sqlite3
import re
from pathlib import Path

DB_NAME = "lot_reports.db"

def parse_report(file_path):
    text = Path(file_path).read_text(errors="ignore")
    lot_match = re.search(r"Report For Lot -\s*([0-9.]+)", text)
    lot = lot_match.group(1) if lot_match else "UNKNOWN"

    def get_metric(name):
        m = re.search(rf"{re.escape(name)},([^\n\r]+)", text)
        return m.group(1).strip() if m else None

    rejected = get_metric("Rejected Dice")
    tray = get_metric("Tray Total")

    summary = {
        "lot": lot,
        "input_wafer_total": get_metric("Input Wafer Total"),
        "rejected_dice": rejected.split(',')[0] if rejected else None,
        "tray_total": tray.split(',')[0] if tray else None,
        "total_alarm": get_metric("Total Alarm"),
        "unplanned_downtime": get_metric("Total Unplanned Downtime")
    }

    alarms=[]
    in_alarm=False
    for line in text.splitlines():
        if 'Alarm List' in line:
            in_alarm=True
            continue
        if in_alarm:
            parts=[p.strip() for p in line.split(',')]
            if len(parts)>=4 and parts[0].isdigit():
                alarms.append({
                    'lot':lot,
                    'frequency':int(parts[0]),
                    'alarm_no':parts[2],
                    'description':','.join(parts[3:]).strip()
                })
    return summary, alarms

conn=sqlite3.connect(DB_NAME)
summary_rows=[]
alarm_rows=[]
for f in Path('.').glob('*.csv'):
    try:
        s,a=parse_report(f)
        summary_rows.append(s)
        alarm_rows.extend(a)
    except Exception as e:
        print(f'Failed {f}: {e}')

pd.DataFrame(summary_rows).to_sql('lot_summary',conn,if_exists='replace',index=False)
pd.DataFrame(alarm_rows).to_sql('alarm_details',conn,if_exists='replace',index=False)

query="""
SELECT description, SUM(frequency) AS total_freq
FROM alarm_details
GROUP BY description
ORDER BY total_freq DESC
LIMIT 15
"""
print(pd.read_sql(query,conn))
conn.close()
print('Database created:', DB_NAME)
