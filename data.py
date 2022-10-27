import sqlite3
import json
conn = sqlite3.connect("data.db")
with open("skee.json", "r", encoding="utf-8" ) as f:
    x = json.load(f)  

i = 0
for z in x:
    
    c = conn.execute(f"INSERT INTO locations_db (ID,city, lat, lon) VALUES({i}, '{z['city']}', '{z['lat']}', '{z['lng']}')")
    i+=1
    conn.commit()

#
#
#