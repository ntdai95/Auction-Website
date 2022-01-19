import psycopg2 as pg
conn = pg.connect("dbname=auction_db user=docker password=auction host=172.17.0.2 port=5432")
cur = conn.cursor()
# cur.execute("\d")
# print(cur.fetchall())
cur.execute("insert into auctions values(default,'fb','item_123','on',now(),now() + interval '1 day')")
cur.execute("select * from auctions")
print(cur.fetchone())
cur.execute("delete from auctions")
