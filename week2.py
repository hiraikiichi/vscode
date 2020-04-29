import tkinter as tk
root = tk.Tk()
#ウィンドウタイトル
root.title("名簿検索")
#ウィンドウサイズ指定
root.geometry("640x480")

#ラベルを追加
label = tk.Label(root, text="Hello,World")
#表示
label.grid()

Static1 = tk.Label(root,text=u'test', foreground='#ff0000', background='#ffaacc')
Static1.place(x=150, y=228)

def pushed(b):
 #print("clicked") #ターミナルに表示される
 b["text"] = "変更したぜ"

button = tk.Button(root, text="ボタン", command=lambda: pushed(button))

button.grid()

root.mainloop()
