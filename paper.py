import tkinter as tk
import tkinter.ttk as ttk
import sqlite3

# 登録画面のGUI
def create_gui():
    # ----------------------------------------
    # コールバック関数群
    # ----------------------------------------    
    # 表示ボタンが押下されたときのコールバック関数
    def select_button():
        root.destroy()
        select_gui()
    # ----------------------------------------
    # 終了ボタンが押下されたときのコールバック関数
    def quit_button():
        root.destroy()
    # ----------------------------------------
    # 登録ボタンがクリックされた時にデータをDBに登録するコールバック関数
    def create_sql(item_company):

        # データベースに接続
        c = sqlite3.connect("paperdatabase.db")
        # item_nameをWHERE句に渡してitem_codeを取得する(メーカー名取得)
        item_code = c.execute("""
                    SELECT item_code FROM item
                    WHERE item_company = '{}'
                    """.format(item_company))
        item_code = item_code.fetchone()[0]

        #商品名の読み取り
        item_name = entry1.get()

        #品番の読み取り
        item_number = entry2.get()

        #表面の読み取り
        item_surface = entry3.get()

        #材質の読み取り
        item_material = entry4.get()

        #用途の読み取り
        item_use = entry5.get()


        # SQLを発行してDBへ登録
        # また、コミットする場合は、commitメソッドを用いる
        try:
            c.execute("""
            INSERT INTO acc_data(item_code,item_name,item_number,item_surface,item_material,item_use)
            VALUES('{}','{}','{}','{}','{}','{}');
            """.format(item_code,item_name,item_number,item_surface,item_material,item_use))
            c.execute("COMMIT;")
            print("1件登録しました")
        # ドメインエラーなどにより登録できなかった場合のエラー処理
        except:
            print("エラーにより登録できませんでした")
    # ----------------------------------------
    # 内訳テーブル(item)にあるitem_codeのタプルを作成する
    def createitemname():
        # データベースの接続
        c = sqlite3.connect("paperdatabase.db")
        # 空の「リスト型」を定義
        li = []
        # SELECT文を発行し、item_companyを取得し、for文で回す
        for r in c.execute("SELECT item_company FROM item"):
            # item_nameをリストに追加する
            li.append(r)
        # リスト型のliをタプル型に変換して、ファンクションに戻す
        return tuple(li)
    # ----------------------------------------
    
    # 空のデータベースを作成して接続する
    dbname = "paperdatabase.db"
    c = sqlite3.connect(dbname)
    c.execute("PRAGMA foreign_keys = 1")

    # 既にデータベースが登録されている場合は、ddlの発行でエラーが出るのでexceptブロックで回避する
    try:
        # itemテーブルの定義
        ddl = """
        CREATE TABLE item
        (
           item_code INTEGER PRIMARY KEY AUTOINCREMENT,
           item_company TEXT NOT NULL UNIQUE
        )
         """
        # SQLの発行
        c.execute(ddl)
        # acc_dataテーブルの定義    
        ddl = """
        CREATE TABLE acc_data
        ( 
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            acc_date DEFAULT CURRENT_TIMESTAMP, 
            item_code INTEGER NOT NULL,
            item_name TEXT NOT NULL,
            item_number TEXT NOT NULL,
            item_surface TEXT NOT NULL,
            item_material TEXT NOT NULL,
            item_use TEXT NOT NULL,
            
            FOREIGN KEY(item_code) REFERENCES item(item_code)
        )
        """
        # itemテーブルへリファレンスデータの登録
        c.execute(ddl)
        c.execute("INSERT INTO item VALUES(1,'富士フィルム')")
        c.execute("INSERT INTO item VALUES(2,'イルフォード')")
        c.execute("INSERT INTO item VALUES(3,'ケントメア')")
        c.execute("INSERT INTO item VALUES(4,'オリエンタル')")
        c.execute("INSERT INTO item VALUES(5,'ヤックス＆サンズ')")
        c.execute("INSERT INTO item VALUES(6,'ベルゲール')")
        c.execute("INSERT INTO item VALUES(7,'フォマ')")
        c.execute("INSERT INTO item VALUES(8,'コダック')")
        c.execute("INSERT INTO item VALUES(9,'ARISTA')")
        c.execute("INSERT INTO item VALUES(10,'ハネミューレ')")
        c.execute("INSERT INTO item VALUES(11,'フォルテ')")
        c.execute("INSERT INTO item VALUES(12,'DNP')")
        c.execute("INSERT INTO item VALUES(13,'ピクトリコ')")
        c.execute("COMMIT")
    except:
        pass

    # rootフレームの設定
    root = tk.Tk()
    root.title("印画紙")
    root.geometry("300x400")

    # メニューの設定
    frame = tk.Frame(root,bd=2,relief="ridge")
    frame.pack(fill="x")
    button1 = tk.Button(frame,text="入力")
    button1.pack(side="left")
    button2 = tk.Button(frame,text="表示",command=select_button)
    button2.pack(side="left")
    button3 = tk.Button(frame,text="終了",command=quit_button)
    button3.pack(side="right")

    # 入力画面ラベルの設定
    #label1 = tk.Label(root,text="【入力画面】",font=("",16),height=2)
    #label1.pack(fill="x")

    # 日付のラベルとエントリーの設定
    #frame1 = tk.Frame(root,pady=10)
    #frame1.pack()
    #label2 = tk.Label(frame1,font=("",14),text="日付")
    #label2.pack(side="left")
    #entry1 = tk.Entry(frame1,font=("",14),justify="center",width=15)
    #entry1.pack(side="left")

    #メーカーラベル
    frame1 = tk.Frame(root,pady=10)
    frame1.pack()
    label1 = tk.Label(frame1,font=("",14),text="メーカ")
    label1.pack(side="left")
    #メーカーコンボボックスの作成
    combo = ttk.Combobox(frame1, state='readonly',font=("",14),width=13)
    combo["values"] = createitemname()
    combo.current(0)
    combo.pack()

    #商品名のラベルとエントリーの設定
    frame2 = tk.Frame(root,pady=10)
    frame2.pack()
    label2 = tk.Label(frame2,font=("",14),text="商品名")
    label2.pack(side="left")
    entry1 = tk.Entry(frame2,font=("",14),justify="center",width=15)
    entry1.pack(side="left")

    #品番のラベルとエントリーの設定
    frame3 = tk.Frame(root,pady=10)
    frame3.pack()
    label3 = tk.Label(frame3,font=("",10),text="品番")
    label3.pack(side="left")
    entry2 = tk.Entry(frame3,font=("",14),justify="center",width=15)
    entry2.pack(side="left")

    #表面のラベルとエントリーの設定
    frame4 = tk.Frame(root,pady=10)
    frame4.pack()
    label4 = tk.Label(frame4,font=("",14),text="表面")
    label4.pack(side="left")
    entry3 = tk.Entry(frame4,font=("",14),justify="center",width=15)
    entry3.pack(side="left")

    #材質のラベルとエントリーの設定
    frame5 = tk.Frame(root,pady=10)
    frame5.pack()
    label5 = tk.Label(frame5,font=("",14),text="材質")
    label5.pack(side="left")
    entry4 = tk.Entry(frame5,font=("",14),justify="center",width=15)
    entry4.pack(side="left")

    #用途のラベルとエントリーの設定
    frame6 = tk.Frame(root,pady=10)
    frame6.pack()
    label6 = tk.Label(frame6,font=("",14),text="用途")
    label6.pack(side="left")
    entry5 = tk.Entry(frame6,font=("",14),justify="center",width=15)
    entry5.pack(side="left")

    # 登録ボタンの設定
    button4 = tk.Button(root,text="登録",
                        font=("",16),
                        width=10,bg="gray",
                        command=lambda:create_sql(combo.get()))
    button4.pack()
    
    root.mainloop()

# 表示画面のGUI
def select_gui():
    # ----------------------------------------
    # コールバック関数群
    # ----------------------------------------    
    # 登録ボタンが押下されたときのコールバック関数
    def create_button():
        root.destroy()
        create_gui()
    # ----------------------------------------
    # 終了ボタンが押下されたときのコールバック関数
    def quit_button():
        root.destroy()   
    # ----------------------------------------
    # 表示ボタンが押下されたときのコールバック関数
    def select_sql(item_company):
        # treeviewのアイテムをすべて削除
        tree.delete(*tree.get_children())

        # item_companyをWHERE句に渡してitem_codeを取得する(メーカー名取得)
        item_code = c.execute("""
                    SELECT item_code FROM item
                    WHERE item_company = '{}'
                    """.format(item_company))
        item_code = item_code.fetchone()[0]

        #SELECT文の作成
        sql = """
        SELECT item_name,item_number,item_surface,item_material,item_use
        FROM acc_data as a,item as i
        WHERE a.item_code = i.item_code AND
        item_company = '{}'
        """.format(item_company)
        # ツリービューにアイテムの追加
        i=0
        for r in c.execute(sql):
            # ツリービューの要素に追加
            tree.insert("","end",values=r)
            if i & 1:
                tree.tag_configure(i,background="#CCFFFF")
            i+=1    
    # ----------------------------------------
    
    # 空のデータベースを作成して接続する
    dbname = "paperdatabase.db"
    c = sqlite3.connect(dbname)
    c.execute("PRAGMA foreign_keys = 1")

    # rootフレームの設定
    root = tk.Tk()
    root.title("印画紙")
    root.geometry("800x500")

    # メニューの設定
    frame = tk.Frame(root,bd=2,relief="ridge")
    frame.pack(fill="x")
    button1 = tk.Button(frame,text="入力",command=create_button)
    button1.pack(side="left")
    button2 = tk.Button(frame,text="表示")
    button2.pack(side="left")
    button3 = tk.Button(frame,text="終了",command=quit_button)
    button3.pack(side="right")

    # 内訳テーブル(item)にあるitem_nameのタプルを作成する
    def createitemname():
        # データベースの接続
        c = sqlite3.connect("paperdatabase.db")
        # 空の「リスト型」を定義
        li = []
        # SELECT文を発行し、item_companyを取得し、for文で回す
        for r in c.execute("SELECT item_company FROM item"):
            # item_nameをリストに追加する
            li.append(r)
        # リスト型のliをタプル型に変換して、ファンクションに戻す
        return tuple(li)
    # ----------------------------------------

    #メーカーラベル
    frame1 = tk.Frame(root,pady=10)
    frame1.pack()
    label1 = tk.Label(frame1,font=("",14),text="メーカ")
    label1.pack(side="left")
    #メーカーコンボボックスの作成
    combo = ttk.Combobox(frame1, state='readonly',font=("",14),width=18)
    combo["values"] = createitemname()
    combo.current(0)
    combo.pack()

    # 表示ボタンの設定
    button4 = tk.Button(root,text="表示",
                        font=("",16),
                        width=10,bg="gray",
                        command=lambda:select_sql(combo.get()))
    button4.pack()

    # ツリービューの作成
    tree = ttk.Treeview(root,padding=10)
    # 列インデックスの作成
    tree["columns"] = (1,2,3,4,5)
    # 表スタイルの設定(headingsはツリー形式ではない、通常の表形式)
    tree["show"] = "headings"
    # 各列の設定(インデックス,オプション(今回は幅を指定))
    tree.column(1,width=150)
    tree.column(2,width=150)
    tree.column(3,width=150)
    tree.column(4,width=150)
    tree.column(5,width=150)
    # 各列のヘッダー設定(インデックス,テキスト)
    tree.heading(1,text="商品名")
    tree.heading(2,text="品番")
    tree.heading(3,text="表面")
    tree.heading(4,text="材質")
    tree.heading(5,text="用途")

    # ツリービューのスタイル変更
    style = ttk.Style()
    # TreeViewの全部に対して、フォントサイズの変更
    style.configure("Treeview",font=("",12))
    # TreeViewのHeading部分に対して、フォントサイズの変更と太字の設定
    style.configure("Treeview.Heading",font=("",14))

    # SELECT文の作成
    sql = """
    SELECT item_name,item_number,item_surface,item_material,item_use
    FROM acc_data as a,item as i
    WHERE a.item_code = i.item_code
    ORDER BY item_name
    """

    # ツリービューにアイテムの追加
    i=0
    for r in c.execute(sql):
        tree.insert("","end",tags=i,values=r)
        if i & 1:
            tree.tag_configure(i,background="#CCFFFF")
        i+=1

    # ツリービューの配置
    tree.pack()

    # メインループ
    root.mainloop()


# GUI画面の表示
create_gui()