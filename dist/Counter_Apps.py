import tkinter as tk
from tkinter import font, simpledialog, messagebox, filedialog

class CounterApp:
    def __init__(self, master):
        self.master = master
        self.master.title("カウンターアプリ")        
        self.master.resizable(False, False)  # サイズ変更を無効化
        
        self.counters = []
        self.default_font = font.Font(family="Arial", size=18)
        self.shortcut_keys = {}

        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)
        
        # 設定メニュー
        self.settings_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="設定", menu=self.settings_menu)
        self.settings_menu.add_command(label="フォント設定", command=self.set_font)
        self.settings_menu.add_command(label="インフォメーション", command=self.show_info)

        # 操作メニュー
        self.operations_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="操作", menu=self.operations_menu)
        self.operations_menu.add_command(label="保存", command=self.save_counters)
        self.operations_menu.add_command(label="読み込み", command=self.load_counters)
        self.operations_menu.add_command(label="減少", command=self.remove_counter)

        self.counter_frame = tk.Frame(self.master)
        self.counter_frame.pack(pady=5)  # 上下の隙間を調整
        
        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack(pady=5)  # 上下の隙間を調整
        
        self.add_counter_button = tk.Button(self.button_frame, text="追加", command=self.add_counter)
        self.add_counter_button.pack(side=tk.LEFT, padx=5)
        
        self.remove_counter_button = tk.Button(self.button_frame, text="減少", command=self.remove_counter)
        self.remove_counter_button.pack(side=tk.LEFT, padx=5)
        
        self.add_counter()
        self.update_remove_button_visibility()
        
        # デフォルトのショートカットキー設定
        for i in range(1, 10):
            self.master.bind(f"<Key-{i}>", lambda event, i=i: self.increment_count_by_index(i-1))
        self.master.bind("<Control-r>", lambda event: self.reset_all_counts())

        # ウィンドウ全体にクリックイベントをバインド
        self.master.bind("<Button-1>", self.remove_focus)
        
    def set_font(self):
            font_dialog = tk.Toplevel(self.master)
            font_dialog.title("フォント設定")
            font_dialog.geometry("200x180")  
            font_dialog.resizable(False, False)  # サイズ変更を無効化
            font_dialog.attributes("-toolwindow", 1)  # 最小化ボタンを無効化
            
            tk.Label(font_dialog, text="フォントファミリを入力してください:").pack(pady=5)
            font_family_entry = tk.Entry(font_dialog)
            font_family_entry.pack(pady=5)
            font_family_entry.insert(0, "Arial")

            tk.Label(font_dialog, text="フォントサイズを入力してください:").pack(pady=5)
            font_size_entry = tk.Entry(font_dialog)
            font_size_entry.pack(pady=5)
            font_size_entry.insert(0, "18")
            
            def apply_font():
                font_family = font_family_entry.get()
                font_size = int(font_size_entry.get())
                if font_family and font_size:
                    self.default_font = font.Font(family=font_family, size=font_size)
                    for name_entry, count_label, key_button in self.counters:
                        count_label.config(font=self.default_font)
                font_dialog.destroy()
            
            tk.Button(font_dialog, text="適用", command=apply_font).pack(pady=10)
        
    def add_counter(self):
        frame = tk.Frame(self.counter_frame)
        frame.pack(fill=tk.X, pady=2)  # 上下の隙間を調整
        
        name_label = tk.Label(frame, text="メモ", width=5)
        name_label.pack(side=tk.LEFT, padx=1)
        
        name_entry = tk.Entry(frame)
        name_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        count_label = tk.Label(frame, text="0", font=self.default_font, width=5)
        count_label.pack(side=tk.LEFT, padx=5)
        
        increment_button = tk.Button(frame, text="追加", command=lambda: self.increment_count(count_label))
        increment_button.pack(side=tk.LEFT, padx=5)
        
        reset_button = tk.Button(frame, text="リセット", command=lambda: self.reset_count(count_label))
        reset_button.pack(side=tk.LEFT, padx=5)
        
        key_button = tk.Button(frame, text="キー設定", command=lambda: self.wait_for_key(count_label))
        key_button.pack(side=tk.LEFT, padx=10)
        
        self.counters.append((name_entry, count_label, key_button))
        self.update_remove_button_visibility()
        
    def remove_counter(self):
        if self.counters:
            frame = self.counters[-1][0].master
            frame.destroy()
            self.counters.pop()
        self.update_remove_button_visibility()

    def update_remove_button_visibility(self):
        if len(self.counters) > 1:
            self.remove_counter_button.pack(side=tk.LEFT, padx=5)
            self.operations_menu.entryconfig("減少", state=tk.NORMAL)
        else:
            self.remove_counter_button.pack_forget()
            self.operations_menu.entryconfig("減少", state=tk.DISABLED)
        
    def increment_count(self, count_label):
        current_count = int(count_label.cget("text"))
        count_label.config(text=str(current_count + 1))
    
    def increment_count_by_index(self, index):
        if index < len(self.counters):
            self.increment_count(self.counters[index][1])
        
    def reset_count(self, count_label):
        count_label.config(text="0")

    def reset_all_counts(self):
        for name_entry, count_label, key_button in self.counters:
            self.reset_count(count_label)
    
    def show_info(self):
        info_dialog = tk.Toplevel(self.master)
        info_dialog.title("インフォメーション")
        info_dialog.geometry("400x280")        
        info_dialog.resizable(False, False)  # サイズ変更を無効化
        info_dialog.attributes("-toolwindow", 1)  # 最小化ボタンを無効化
        
        info_text = (
            "カウンターアプリ 1.0.0 \n\n"
            "製作者: 黒髪零\n"
            "使用ツール: Python, Tkinter, ChatGPT\n\n"
            "当ツールをDLしていただきありがとうございます!\n"
            "便利なカウンターツールを作ろうと思いました\n\n"
            "機能の安易説明:\n"
            "・フォント設定やショートカットキーを使用できるよ！\n"
            "・不具合が発生した場合は、アプリケーションを再起動してね\n\n"
            "⚠ショートカットキーは9行まで数字キーで追加できます以降は自分で設定してね"
        )
        
        info_label = tk.Label(info_dialog, text=info_text, justify=tk.LEFT)
        info_label.pack(padx=10, pady=10)
        
        # リンクボタンを追加
        link_frame = tk.Frame(info_dialog)
        link_frame.pack(pady=10)
        
        link1_button = tk.Button(link_frame, text="BlueSky", fg="blue", cursor="hand2", command=lambda: self.open_link("https://bsky.app/profile/zeropso2.bsky.social"))
        link1_button.pack(side=tk.LEFT, padx=5)
        
        link2_button = tk.Button(link_frame, text="HomePage", fg="green", cursor="hand2", command=lambda: self.open_link("https://kurokamizero.jimdo.com/"))
        link2_button.pack(side=tk.LEFT, padx=5)
        
        link3_button = tk.Button(link_frame, text="Python", fg="#f312ff", cursor="hand2", command=lambda: self.open_link("https://www.python.org"))
        link3_button.pack(side=tk.LEFT, padx=5)
    
    def open_link(self, url):
        import webbrowser
        webbrowser.open_new(url)
    
    def save_counters(self):
        save_data = {
            "counters": [],
            "font": {"family": self.default_font.cget("family"), "size": self.default_font.cget("size")}
        }
        for name_entry, count_label, key_button in self.counters:
            save_data["counters"].append({
                "name": name_entry.get(),
                "count": count_label.cget("text"),
                "key": key_button.cget("text")
            })
        
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(save_data, file)
    
    def load_counters(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as file:
                load_data = json.load(file)
            
            self.default_font = font.Font(family=load_data["font"]["family"], size=load_data["font"]["size"])
            
            for counter in self.counters:
                counter[0].master.destroy()
            self.counters = []
            
            for counter_data in load_data["counters"]:
                self.add_counter()
                name_entry, count_label, key_button = self.counters[-1]
                name_entry.insert(0, counter_data["name"])
                count_label.config(text=counter_data["count"])
                count_label.config(font=self.default_font)
                key_button.config(text=counter_data["key"])
                self.bind_key(None, count_label, counter_data["key"])
            self.update_remove_button_visibility()
    
    def wait_for_key(self, count_label):
        dialog = tk.Toplevel(self.master)
        dialog.title("キー設定")
        dialog.geometry("300x100")
        
        label = tk.Label(dialog, text="キーを押してください")
        label.pack(pady=20)
        
        dialog.bind("<KeyPress>", lambda event: self.set_shortcut_key(event, count_label, dialog))
    
    def set_shortcut_key(self, event, count_label, dialog):
        key = event.keysym
        self.bind_key(None, count_label, key)
        self.get_key_button(count_label).config(text=key)
        dialog.destroy()
    
    def get_key_button(self, count_label):
        for name_entry, count_label_item, key_button in self.counters:
            if count_label_item == count_label:
                return key_button
    
    def bind_key(self, event, count_label, key):
        if key in self.shortcut_keys:
            self.master.unbind(f"<Key-{key}>")
        self.master.bind(f"<Key-{key}>", lambda event: self.increment_count(count_label))
        self.shortcut_keys[key] = count_label

    def remove_focus(self, event):
        widget = event.widget
        if not isinstance(widget, tk.Entry):
            self.master.focus_set()
        else:
            widget.focus_set()

if __name__ == "__main__":
    root = tk.Tk()
    app = CounterApp(root)
    root.mainloop()
