# -*- coding: utf-8 -*-
# filename: database.py

import sqlite3

# 空のデータベースを作成して接続する
dbname = "database.db"
c = sqlite3.connect(dbname)
# 外部キー制約のオプションは、デフォルトでは無効になっているため、これを有効にする
c.execute("PRAGMA foreign_keys = 1")
# itemテーブルの定義
ddl = """
CREATE TABLE item
(
   item_code INTEGER PRIMARY KEY,
   item_name TEXT NOT NULL UNIQUE
);
 """
# SQLの発行
c.execute(ddl)

# acc_dataテーブルの定義    
ddl = """
CREATE TABLE acc_data
( 
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    acc_date DATE NOT NULL,
    item_code INTEGER NOT NULL,
    amount INTEGER,
    FOREIGN KEY(item_code) REFERENCES item(item_code)
);
"""
#sqlの発行
c.execute(ddl)
# itemテーブル登録のテスト
c.execute("INSERT INTO item VALUES(1,'食費');")
c.execute("INSERT INTO item VALUES(2,'住宅費');")
c.execute("INSERT INTO item VALUES(3,'光熱費');")
c.execute("COMMIT;")

# acc_dateテーブル登録のテスト
c.execute("""
    INSERT INTO acc_data(acc_date,item_code,amount)
    VALUES('2017-3-1',1,1000);
""")
c.execute("COMMIT;")

# acc_dateテーブル登録のテスト（次は変数を使った登録）
date = "'{}-{}-{}'".format(2017,3,5)
code = 2
amount = 2000

c.execute("""
    INSERT INTO acc_data(acc_date,item_code,amount)
    VALUES({},{},{});""".format(date,code,amount)
    )
c.execute("COMMIT;")

# 最後に登録されているデータの表示して確認する。
# itemテーブルの表示
result = c.execute("SELECT * FROM item;")
for row in result:
    print(row)
# 結果として３レコード登録されているのが確認できた。
# (1, '食費')
# (2, '住宅費')
# (3, '光熱費')

# acc_dataテーブルの表示
result = c.execute("SELECT * FROM acc_data;")
for row in result:
    print(row)
# 結果として２レコード登録されているのが確認できた。
# (1, '2017-3-1', 1, 1000)
# (2, '2017-3-5', 2, 2000)

# acc_dataテーブルとitemテーブルを結合して表示する
result = c.execute("""
    SELECT a.acc_date, i.item_name, a.amount
     FROM acc_data as a,item as i
      WHERE a.item_code = i.item_code;
""")
for row in result:
    print(row)