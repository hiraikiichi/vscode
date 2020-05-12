import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import sqlite3
import itertools


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
    # 編集ボタンが押下されたときのコールバック関数
    def Edit_button():
        root.destroy()
        Edit_gui()
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
            #print("1件登録しました")
        # ドメインエラーなどにより登録できなかった場合のエラー処理
        except:
            print("エラーにより登録できませんでした")
        #エントリー削除
        entry1.delete(0,tk.END)
        entry2.delete(0,tk.END)
        entry3.delete(0,tk.END)
        entry4.delete(0,tk.END)
        entry5.delete(0,tk.END)
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
    button4 = tk.Button(frame,text="編集",command=Edit_button)
    button4.pack(side="left")
    button3 = tk.Button(frame,text="終了",command=quit_button)
    button3.pack(side="right")

    #メーカーラベル
    frame1 = tk.Frame(root,pady=10)
    frame1.pack()
    label1 = tk.Label(frame1,text="メーカー",font=("HGPｺﾞｼｯｸM",12))
    label1.pack(side="left")
    
    #メーカーコンボボックスの作成
    combo = ttk.Combobox(frame1,state='readonly',width=13,font=("HGPｺﾞｼｯｸM",12))
    combo["values"] = createitemname()
    combo.current(0)
    combo.pack()

    #商品名のラベルとエントリーの設定
    frame2 = tk.Frame(root,pady=10)
    frame2.pack()
    label2 = tk.Label(frame2,text="商品名",font=("HGPｺﾞｼｯｸM",12))
    label2.pack(side="left")
    entry1 = tk.Entry(frame2,justify="center",width=15,font=("HGPｺﾞｼｯｸM",12))
    entry1.pack(side="left")

    #品番のラベルとエントリーの設定
    frame3 = tk.Frame(root,pady=10)
    frame3.pack()
    label3 = tk.Label(frame3,font=("HGPｺﾞｼｯｸM",12),text="品番")
    label3.pack(side="left")
    entry2 = tk.Entry(frame3,font=("HGPｺﾞｼｯｸM",12),justify="center",width=15)
    entry2.pack(side="left")

    #表面のラベルとエントリーの設定
    frame4 = tk.Frame(root,pady=10)
    frame4.pack()
    label4 = tk.Label(frame4,font=("HGPｺﾞｼｯｸM",12),text="表面")
    label4.pack(side="left")
    entry3 = tk.Entry(frame4,font=("HGPｺﾞｼｯｸM",12),justify="center",width=15)
    entry3.pack(side="left")

    #材質のラベルとエントリーの設定
    frame5 = tk.Frame(root,pady=10)
    frame5.pack()
    label5 = tk.Label(frame5,font=("HGPｺﾞｼｯｸM",12),text="材質")
    label5.pack(side="left")
    entry4 = tk.Entry(frame5,font=("HGPｺﾞｼｯｸM",12),justify="center",width=15)
    entry4.pack(side="left")

    #用途のラベルとエントリーの設定
    frame6 = tk.Frame(root,pady=10)
    frame6.pack()
    label6 = tk.Label(frame6,font=("HGPｺﾞｼｯｸM",12),text="用途")
    label6.pack(side="left")
    entry5 = tk.Entry(frame6,font=("HGPｺﾞｼｯｸM",12),justify="center",width=15)
    entry5.pack(side="left")

    # 登録ボタンの設定
    button4 = tk.Button(root,text="登録",
                        font=("HGPｺﾞｼｯｸM",12),
                        width=10,bg="gray",
                        command=lambda:create_sql(combo.get()))
    button4.pack()
    
    root.mainloop()

# 表示画面のGUI
def select_gui():
    # ----------------------------------------
    # コールバック関数群
    # ----------------------------------------    
    # 入力ボタンが押下されたときのコールバック関数
    def create_button():
        root.destroy()
        create_gui()
    # ----------------------------------------
    # 終了ボタンが押下されたときのコールバック関数
    def quit_button():
        root.destroy() 
    # ----------------------------------------
    # 編集ボタンが押下されたときのコールバック関数
    def Edit_button():
        root.destroy()
        Edit_gui()
    # ----------------------------------------
    # 表示ボタンが押下されたときのコールバック関数
    def select_sql(item_company):
        # treeviewのアイテムをすべて削除
        tree.delete(*tree.get_children())

        # item_companyをWHERE句に渡してitem_codeを取得する(メーカー名取得)
        #item_code = c.execute("""
        #            SELECT item_code FROM item
        #            WHERE item_company = '{}'
        #            """.format(item_company))
        #item_code = item_code.fetchone()[0]
        

        #print(item_company)
        #print(item_code)

        #SELECT文の作成
        sql = """
        SELECT item_company,item_name,item_number,item_surface,item_material,item_use
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

    def all_button():
        # treeviewのアイテムをすべて削除
        tree.delete(*tree.get_children())

        #SELECT文の作成
        sql = """
            SELECT item_company,item_name,item_number,item_surface,item_material,item_use
            FROM acc_data as a,item as i
            WHERE a.item_code = i.item_code
            ORDER BY item_company
            """
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
    root.title("印画紙-表示画面")
    root.geometry("1000x500")

    # メニューの設定
    frame = tk.Frame(root,bd=2,relief="ridge")
    frame.pack(fill="x")
    button1 = tk.Button(frame,text="入力",command=create_button)
    button1.pack(side="left")
    button2 = tk.Button(frame,text="表示")
    button2.pack(side="left")
    button4 = tk.Button(frame,text="編集",command=Edit_button)
    button4.pack(side="left")
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
    label1 = tk.Label(frame1,font=("HGPｺﾞｼｯｸM",12),text="メーカー")
    label1.pack(side="left")

    #メーカーコンボボックスの作成
    combo = ttk.Combobox(frame1, state='readonly',font=("HGPｺﾞｼｯｸM",12),width=18)
    combo["values"] = createitemname()
    combo.current(0)
    combo.pack()

    # 表示ボタンの設定
    frame2 = tk.Frame(root,pady=10)
    frame2.pack()
    button4 = tk.Button(frame2,text="表示",
                        font=("HGPｺﾞｼｯｸM",12),
                        width=10,bg="gray",
                        command=lambda:select_sql(combo.get()))
    button4.pack(side="left")

    # 全件表示ボタンの設定
    button5 = tk.Button(frame2,text="全件表示",
                        font=("HGPｺﾞｼｯｸM",12),
                        width=10,bg="gray",
                        command=all_button,
                        )
    button5.pack(side="left",padx=10)

    # ツリービューの作成
    tree = ttk.Treeview(root,padding=10)
    # 列インデックスの作成
    tree["columns"] = (1,2,3,4,5,6)
    # 表スタイルの設定(headingsはツリー形式ではない、通常の表形式)
    tree["show"] = "headings"
    # 各列の設定(インデックス,オプション(今回は幅を指定))
    tree.column(1,width=150)
    tree.column(2,width=150)
    tree.column(3,width=150)
    tree.column(4,width=150)
    tree.column(5,width=150)
    tree.column(6,width=150)
    # 各列のヘッダー設定(インデックス,テキスト)
    tree.heading(1,text="メーカー")
    tree.heading(2,text="商品名")
    tree.heading(3,text="品番")
    tree.heading(4,text="表面")
    tree.heading(5,text="材質")
    tree.heading(6,text="用途")

    # ツリービューのスタイル変更
    style = ttk.Style()
    # TreeViewの全部に対して、フォントサイズの変更
    style.configure("Treeview",font=("HGPｺﾞｼｯｸM",12))
    # TreeViewのHeading部分に対して、フォントサイズの変更設定
    style.configure("Treeview.Heading",font=("HGPｺﾞｼｯｸM",14))

    # SELECT文の作成
    sql = """
    SELECT item_company,item_name,item_number,item_surface,item_material,item_use
    FROM acc_data as a,item as i
    WHERE a.item_code = i.item_code
    ORDER BY item_company
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

#編集画面のGUI
def Edit_gui():
    # ----------------------------------------
    # コールバック関数群
    # ----------------------------------------    
    # 入力ボタンが押下されたときのコールバック関数
    def create_button():
        root.destroy()
        create_gui()
    # ----------------------------------------
    # 終了ボタンが押下されたときのコールバック関数
    def quit_button():
        root.destroy() 
    # ----------------------------------------
    # 表示ボタンが押下されたときのコールバック関数
    def select_button():
        root.destroy()
        select_gui()
    # ----------------------------------------
    # 空のデータベースを作成して接続する
    dbname = "paperdatabase.db"
    c = sqlite3.connect(dbname)
    c.execute("PRAGMA foreign_keys = 1")

    # rootフレームの設定
    root = tk.Tk()
    root.title("印画紙-編集画面")
    root.geometry("400x300")

    # メニューの設定
    frame = tk.Frame(root,bd=2,relief="ridge")
    frame.pack(fill="x")
    button1 = tk.Button(frame,text="入力",command=create_button)
    button1.pack(side="left")
    button2 = tk.Button(frame,text="表示",command=select_button)
    button2.pack(side="left")
    button4 = tk.Button(frame,text="編集")
    button4.pack(side="left")
    button3 = tk.Button(frame,text="終了",command=quit_button)
    button3.pack(side="right") 
    
#もし同じ商品名があったらIDが更新されない。
    def select_now(event):
        if len(lb.curselection()) == 0:
            return

        #選択された場所の番号(インデックス)を取得
        index = lb.curselection()[0]
        #インデックスから要素を取得
        element = lb.get(index)
        #タプル型なので要素だけを取得
        element2 = element[0]

        sql = ("""
        select item_company,item_name,item_number,item_surface,item_material,item_use,id
        from acc_data as a,item as i  
        where a.item_code = i.item_code and 
        item_name = '{}'
        """).format(element2)
        #SQL文にする
        r = c.execute(sql)
        list_data = r.fetchall()
        #itertools.chain.from_iterable()で2次元のリストを平坦化
        list_data2 = list(itertools.chain.from_iterable(list_data))

        #メーカーエントリーに挿入
        entry2.configure(state='normal')
        entry2.delete(0,tk.END)
        entry2.insert(0,list_data2[0])
        entry2.configure(state='readonly')
        #商品名エントリーに挿入
        entry3.delete(0,tk.END)
        entry3.insert(0,list_data2[1])
        #品番エントリーに挿入
        entry4.delete(0,tk.END)
        entry4.insert(0,list_data2[2])
        #表面エントリーに挿入
        entry5.delete(0,tk.END)
        entry5.insert(0,list_data2[3])
        #材質エントリーに挿入
        entry6.delete(0,tk.END)
        entry6.insert(0,list_data2[4])
        #用途エントリーに挿入
        entry7.delete(0,tk.END)
        entry7.insert(0,list_data2[5])
        #IDエントリーに挿入
        entry8.configure(state='normal')
        entry8.delete(0,tk.END)
        entry8.insert(0,list_data2[6])
        entry8.configure(state='readonly')

    #削除ボタンが押されたら
    def delete():
        #商品名の読み取り
        item_name = entry3.get()
        #品番の読み取り
        item_number = entry4.get()
        #表面の読み取り
        item_surface = entry5.get()
        #材質の読み取り
        item_material = entry6.get()
        #用途の読み取り
        item_use = entry7.get()
        #IDの読み取り
        item_id = entry8.get()

        # リストボックスが選択されていない時
        if item_id == "":
        #if item_name == "" and item_number == "" and item_surface == "" and item_material == "" and item_use == "":
            messagebox.showwarning("エラー", "選択されていません")
            return
        # messageboxで確認
        f = messagebox.askokcancel("削除", "本当に削除しますか？")
        if f:
            pass
        else:
            return
        # SQLを発行してDBへ登録
        # また、コミットする場合は、commitメソッドを用いる
        try:
            c.execute("""
            delete from acc_data where item_name = '{}' and item_number = '{}' and item_surface = '{}' and
            item_material = '{}' and item_use = '{}' and id = '{}'
            """.format(item_name,item_number,item_surface,item_material,item_use,item_id))
            c.execute("COMMIT;")
            #print("1件削除しました")
        # ドメインエラーなどにより登録できなかった場合のエラー処理
        except:
            print("エラーにより登録できませんでした")
        #リストボックス更新
        # SELECT文の作成
        sql = """
        SELECT item_name
        FROM acc_data as a,item as i
        WHERE a.item_code = i.item_code
        ORDER BY item_company
        """
        #エントリー削除
        entry2.configure(state='normal')
        entry2.delete(0,tk.END)
        entry2.configure(state='readonly')
        entry3.delete(0,tk.END)
        entry4.delete(0,tk.END)
        entry5.delete(0,tk.END)
        entry6.delete(0,tk.END)
        entry7.delete(0,tk.END)
        entry8.configure(state='normal')
        entry8.delete(0,tk.END)
        entry8.configure(state='readonly')
        #リストボックス削除
        lb.delete(0, tk.END)
        # リストボックスに商品名挿入
        for r in c.execute(sql):
            lb.insert(tk.END,r)
    
    #更新ボタンが押されたら
    def update():
        #商品名の読み取り
        item_name = entry3.get()
        #品番の読み取り
        item_number = entry4.get()
        #表面の読み取り
        item_surface = entry5.get()
        #材質の読み取り
        item_material = entry6.get()
        #用途の読み取り
        item_use = entry7.get()
        #IDの読み取り
        item_id = entry8.get()

        # リストボックスが選択されていない時
        if item_name == "" and item_number == "" and item_surface == "" and item_material == "" and item_use == "":
            messagebox.showwarning("エラー", "選択されていません")
            return
        # messageboxで確認
        f = messagebox.askokcancel("確認", "更新しますか？")
        if f:
            pass
        else:
            return
        # SQLを発行してDBへ登録
        # また、コミットする場合は、commitメソッドを用いる
        try:
            c.execute("""
            update acc_data set item_name = '{}',item_number = '{}',item_surface = '{}',
            item_material = '{}',item_use = '{}' where id ='{}' 
            """.format(item_name,item_number,item_surface,item_material,item_use,item_id))
            c.execute("COMMIT;")
            #print("1件更新しました")
        # ドメインエラーなどにより登録できなかった場合のエラー処理
        except:
            print("エラーにより登録できませんでした")
        #リストボックス更新
        # SELECT文の作成
        sql = """
        SELECT item_name
        FROM acc_data as a,item as i
        WHERE a.item_code = i.item_code
        ORDER BY item_company
        """
        #リストボックス削除
        lb.delete(0, tk.END)
        # リストボックスに商品名挿入
        for r in c.execute(sql):
            lb.insert(tk.END,r)
        #エントリー削除
        entry2.configure(state='normal')
        entry2.delete(0,tk.END)
        entry2.configure(state='readonly')
        entry3.delete(0,tk.END)
        entry4.delete(0,tk.END)
        entry5.delete(0,tk.END)
        entry6.delete(0,tk.END)
        entry7.delete(0,tk.END)
        entry8.configure(state='normal')
        entry8.delete(0,tk.END)
        entry8.configure(state='readonly')
        

    # SELECT文の作成
    sql = """
    SELECT item_name
    FROM acc_data as a,item as i
    WHERE a.item_code = i.item_code
    ORDER BY item_company
    """
    # リストボックス作成
    lb = tk.Listbox(root, width=20,selectmode=tk.SINGLE,font=("HGPｺﾞｼｯｸM",12))

    # リストボックスに商品名入れる
    for r in c.execute(sql):
        lb.insert(tk.END,r)
    
    # 項目が選択されたときの処理
    lb.bind('<<ListboxSelect>>', select_now)
    #リストボックス配置
    lb.pack(side=tk.LEFT,fill=tk.Y)
    
    #メーカーラベルとエントリー
    frame2 = tk.Frame(root,pady=4)
    frame2.pack(anchor=tk.W)
    label2 = tk.Label(frame2,text="メーカー",font=("HGPｺﾞｼｯｸM",12))
    label2.pack(side=tk.LEFT,padx=5)

    entry2 = tk.Entry(frame2,width=20,font=("HGPｺﾞｼｯｸM",12))
    entry2.pack(side=tk.LEFT,padx=10)
    entry2.configure(state='readonly')

    #商品名ラベルとエントリー
    frame3 = tk.Frame(root,pady=4)
    frame3.pack(anchor=tk.W)
    label3 = tk.Label(frame3,text="商品名 ",font=("HGPｺﾞｼｯｸM",12))
    label3.pack(side=tk.LEFT,padx=5)

    entry3 = tk.Entry(frame3,width=20,font=("HGPｺﾞｼｯｸM",12))
    entry3.pack(side=tk.LEFT,padx=10)

    #品番ラベルとエントリー
    frame4 = tk.Frame(root,pady=4)
    frame4.pack(anchor=tk.W)
    label4 = tk.Label(frame4,text="品番",font=("HGPｺﾞｼｯｸM",12))
    label4.pack(side=tk.LEFT,padx=5)

    entry4 = tk.Entry(frame4,width=20,font=("HGPｺﾞｼｯｸM",12))
    entry4.pack(side=tk.LEFT,padx=10)

    #表面ラベルとエントリー
    frame5 = tk.Frame(root,pady=4)
    frame5.pack(anchor=tk.W)
    label5 = tk.Label(frame5,text="表面",font=("HGPｺﾞｼｯｸM",12))
    label5.pack(side=tk.LEFT,padx=5)

    entry5 = tk.Entry(frame5,width=20,font=("HGPｺﾞｼｯｸM",12))
    entry5.pack(side=tk.LEFT,padx=10)

    #材質ラベルとエントリー
    frame6 = tk.Frame(root,pady=2)
    frame6.pack(anchor=tk.W)
    label6 = tk.Label(frame6,text="材質",font=("HGPｺﾞｼｯｸM",12))
    label6.pack(side=tk.LEFT,padx=5)

    entry6 = tk.Entry(frame6,width=20,font=("HGPｺﾞｼｯｸM",12))
    entry6.pack(side=tk.LEFT,padx=10)

    #用途ラベルとエントリー
    frame7 = tk.Frame(root,pady=2)
    frame7.pack(anchor=tk.W)
    label7 = tk.Label(frame7,text="用途",font=("HGPｺﾞｼｯｸM",12))
    label7.pack(side=tk.LEFT,padx=5)

    entry7 = tk.Entry(frame7,width=20,font=("HGPｺﾞｼｯｸM",12))
    entry7.pack(side=tk.LEFT,padx=10)

    #IDラベルとエントリー
    frame8 = tk.Frame(root,pady=2)
    frame8.pack(anchor=tk.W)
    label8 = tk.Label(frame8,text="番号",font=("HGPｺﾞｼｯｸM",12))
    label8.pack(side=tk.LEFT,padx=5)

    entry8 = tk.Entry(frame8,width=20,font=("HGPｺﾞｼｯｸM",12))
    entry8.pack(side=tk.LEFT,padx=10)
    entry8.configure(state='readonly')

    # 削除ボタンの設定
    button1 = tk.Button(root,text="削除",
                        font=("HGPｺﾞｼｯｸM",12),
                        width=7,bg="gray",
                        command=delete)
    button1.pack(side=tk.LEFT,padx=10)

    # 更新ボタンの設定
    button2 = tk.Button(root,text="更新",
                        font=("HGPｺﾞｼｯｸM",12),
                        width=7,bg="gray",
                        command=update)
    button2.pack(side=tk.LEFT,padx=10)

    #スクロールバーの生成・配置
    #scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=lb.yview)
    #scrollbar.pack(fill='y', side=tk.RIGHT)

    # メインループ
    root.mainloop()

# GUI画面の表示
create_gui()


#問題442行目
#ID検索にする