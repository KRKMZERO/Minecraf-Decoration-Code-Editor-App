import tkinter as tk
from tkinter import ttk

class MinecraftCodeEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Minecraft Decoration Code Editor")

        # メインフレーム
        self.frame = tk.Frame(root)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        # 上部に配置するボタンフレーム
        self.button_frame = tk.Frame(self.frame)
        self.button_frame.grid(row=0, column=0, columnspan=3, sticky="ew", pady=5)

        # カラーコードのプルダウンメニュー
        self.color_codes = [
            "§0 (Black)", "§1 (Dark Blue)", "§2 (Dark Green)", "§3 (Dark Aqua)",
            "§4 (Dark Red)", "§5 (Dark Purple)", "§6 (Gold)", "§7 (Gray)",
            "§8 (Dark Gray)", "§9 (Blue)", "§a (Green)", "§b (Aqua)",
            "§c (Red)", "§d (Light Purple)", "§e (Yellow)", "§f (White)"
        ]
        self.color_code_var = tk.StringVar(value=self.color_codes[0])  # 初期値

        self.color_code_menu = ttk.OptionMenu(
            self.button_frame, self.color_code_var, *self.color_codes
        )
        self.color_code_menu.grid(row=0, column=0, padx=5, pady=5)

        # 「カラーコードを追加」ボタン
        self.add_color_button = tk.Button(self.button_frame, text="Add Color Code", command=self.add_color_code)
        self.add_color_button.grid(row=0, column=1, padx=5, pady=5)

        # フォーマットコードボタン
        format_codes = [
            ("§k (Obfuscated)", "§k"),
            ("§l (Bold)", "§l"),
            ("§m (Strikethrough)", "§m"),
            ("§n (Underline)", "§n"),
            ("§o (Italic)", "§o"),
            ("§r (Reset)", "§r"),
        ]
        for idx, (label, code) in enumerate(format_codes):
            button = tk.Button(self.button_frame, text=label, command=lambda c=code: self.add_format_code(c))
            button.grid(row=0, column=2 + idx, padx=5, pady=5)

        # テキストクリアボタン
        self.clear_button = tk.Button(self.button_frame, text="Clear Text", command=self.clear_text)
        self.clear_button.grid(row=0, column=2 + len(format_codes), padx=5, pady=5)

        # テキストボックス
        self.text_box = tk.Text(self.frame, wrap="word", height=20, width=50)
        self.text_box.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)

        # グリッドの調整
        self.frame.rowconfigure(1, weight=1)
        self.frame.columnconfigure(0, weight=1)

    def add_color_code(self):
        """選択されたカラーコードをテキストボックスに追加"""
        selected_code = self.color_code_var.get().split()[0]  # コード部分だけを抽出
        self.text_box.insert(tk.END, selected_code)

    def add_format_code(self, code):
        """指定されたフォーマットコードをテキストボックスに追加"""
        self.text_box.insert(tk.END, code)

    def clear_text(self):
        """テキストボックスの内容をクリアする"""
        self.text_box.delete(1.0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = MinecraftCodeEditor(root)
    root.mainloop()
