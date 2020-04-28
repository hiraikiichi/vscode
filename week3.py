import tkinter as tk

root = tk.Tk()
#ウィンドウタイトル
root.title("名簿検索")
#ウィンドウサイズ指定
root.geometry("500x200")

#ラベル
enter_lbl = tk.Label(text = "名前を入力")
enter_lbl.place(x=30, y=40)
out_lbl = tk.Label(text = "検索結果")
out_lbl.place(x=30, y=80)

name_list = ["伊藤健一","高橋哲也","佐藤誠","田中直樹","鈴木剛"]

#テキストボックス
#入力
enter_txt = tk.Entry(width = 40)
enter_txt.place(x = 95, y = 40)
#出力
out_txt = tk.Entry(width = 40)
out_txt.place(x = 95, y = 80)

#検索
def btn_click():
    first_name2 = enter_txt.get()
    if first_name2 == "":
        out_txt.delete(0, tk.END)
        out_txt.insert(tk.END, "入力されていません")
        #out_txt.delete(0, tk.END)
        return
    #リスト内包表記
    name_list2 = list(filter(lambda x: first_name2 in x, name_list))
    if not name_list2:
        out_txt.delete(0, tk.END)
        out_txt.insert(tk.END, "リストにいません")
    else:
        out_txt.delete(0, tk.END)
        out_txt.insert(tk.END, name_list2)


#クリア
def delete_btn_click(): 
    out_txt.delete(0, tk.END)
    enter_txt.delete(0, tk.END)

#リスト表示
def list_btn_click():
    out_txt.delete(0, tk.END)
    out_txt.insert(tk.END, name_list)

#リスト登録
def list_add():
    add_name = enter_txt.get()
    if add_name == "":
        out_txt.delete(0, tk.END)
        out_txt.insert(tk.END, "入力されていません")
        #out_txt.delete(0, tk.END)
        return
    if add_name in name_list:
        out_txt.delete(0, tk.END)
        out_txt.insert(tk.END, add_name+"さんはすでに登録済です。")
    else:
        out_txt.delete(0, tk.END)
        out_txt.insert(tk.END, add_name+"さんが登録されました。")     
        #リストへの追加
        name_list.append(add_name)

#リストから削除
def list_clear():
    clear_name = enter_txt.get()
     #検索データがリストにいるか確認(lenを使いNULLか判定)
    if clear_name not in name_list: 
        out_txt.delete(0, tk.END)
        out_txt.insert(tk.END, "リストにいません")
    else: 
        name_list.remove(clear_name)
        out_txt.delete(0, tk.END)
        out_txt.insert(tk.END, clear_name+"さんをリストから削除しました")


#検索ボタン
btn = tk.Button(root, text='検索', command=btn_click)
btn.place(x=110, y=140)


#クリアボタン
delete_btn = tk.Button(root, text='クリア', command = delete_btn_click)
delete_btn.place(x=160, y=140)

#リスト表示ボタン
delete_btn = tk.Button(root, text='リスト表示', command = list_btn_click)
delete_btn.place(x=210, y=140)

#リスト登録ボタン
delete_btn = tk.Button(root, text='リスト登録', command = list_add)
delete_btn.place(x=280, y=140)

#リスト削除ボタン
delete_btn = tk.Button(root, text='リスト削除', command = list_clear)
delete_btn.place(x=350, y=140)

root.mainloop()