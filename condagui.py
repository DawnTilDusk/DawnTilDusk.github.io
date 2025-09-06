import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import sys
import os
import pygame

class VSCodeCondaConfigurator:
    def __init__(self, root):
        self.root = root
        self.root.title("VSCode Conda 环境配置指南")
        self.root.geometry("900x700")
        self.create_widgets()
    
    def create_widgets(self):
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 标题
        title = ttk.Label(main_frame, text="在 VSCode 中配置 Conda 环境", font=("Arial", 16, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=10)
        
        # 创建标签页控件
        notebook = ttk.Notebook(main_frame)
        notebook.grid(row=1, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 创建各个标签页
        self.setup_tab(notebook)
        self.extension_tab(notebook)
        self.select_tab(notebook)
        self.troubleshoot_tab(notebook)
        
        # 状态栏
        self.status = ttk.Label(main_frame, text="就绪", relief=tk.SUNKEN, anchor=tk.W)
        self.status.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # 配置网格权重
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def setup_tab(self, notebook):
        # 设置标签页
        setup_frame = ttk.Frame(notebook, padding="10")
        notebook.add(setup_frame, text="1. 前期准备")
        
        content = """
在 VSCode 中使用 Conda 环境前的准备工作：

1. 确保已安装以下软件：
   - Anaconda 或 Miniconda
   - Visual Studio Code

2. 创建 Conda 环境（如果尚未创建）：
   打开终端/命令提示符，运行：
   
   conda create -n myenv python=3.8
   
   将 "myenv" 替换为您的环境名称，3.8 替换为所需的 Python 版本。

3. 激活环境以验证安装：
   
   conda activate myenv
   python --version
   
   应该显示您选择的 Python 版本。
        """
        
        text = scrolledtext.ScrolledText(setup_frame, width=85, height=20, wrap=tk.WORD)
        text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        text.insert(tk.INSERT, content)
        text.config(state=tk.DISABLED)
        
        # 按钮框架
        btn_frame = ttk.Frame(setup_frame)
        btn_frame.grid(row=1, column=0, pady=10)
        
        ttk.Button(btn_frame, text="检查 Conda 安装", command=self.check_conda).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="检查 VSCode 安装", command=self.check_vscode).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="复制创建环境命令", command=lambda: self.copy_command("conda create -n myenv python=3.8")).pack(side=tk.LEFT, padx=5)
        
        setup_frame.columnconfigure(0, weight=1)
        setup_frame.rowconfigure(0, weight=1)
    
    def extension_tab(self, notebook):
        # 扩展标签页
        extension_frame = ttk.Frame(notebook, padding="10")
        notebook.add(extension_frame, text="2. 安装扩展")
        
        content = """
在 VSCode 中配置 Conda 环境需要安装 Python 扩展：

1. 打开 VSCode
2. 点击左侧活动栏中的扩展图标 (或按 Ctrl+Shift+X)
3. 搜索 "Python"
4. 找到由 Microsoft 发布的 "Python" 扩展并安装

此外，推荐安装以下扩展以增强体验：

- "Pylance" - 提供出色的语言支持
- "Jupyter" - 如果您使用 Jupyter 笔记本
- "Python Extension Pack" - 包含多个有用的 Python 工具

安装扩展后，重新启动 VSCode 以确保扩展正确加载。
        """
        
        text = scrolledtext.ScrolledText(extension_frame, width=85, height=20, wrap=tk.WORD)
        text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        text.insert(tk.INSERT, content)
        text.config(state=tk.DISABLED)
        
        # 按钮框架
        btn_frame = ttk.Frame(extension_frame)
        btn_frame.grid(row=1, column=0, pady=10)
        
        ttk.Button(btn_frame, text="打开 VSCode 扩展面板", command=self.open_vscode_extensions).pack(side=tk.LEFT, padx=5)
        
        extension_frame.columnconfigure(0, weight=1)
        extension_frame.rowconfigure(0, weight=1)
    
    def select_tab(self, notebook):
        # 选择解释器标签页
        select_frame = ttk.Frame(notebook, padding="10")
        notebook.add(select_frame, text="3. 选择解释器")
        
        content = """
在 VSCode 中选择 Conda 环境作为 Python 解释器：

方法 1：使用命令面板
1. 打开 VSCode 和一个 Python 文件
2. 按 Ctrl+Shift+P (或 Cmd+Shift+P on Mac) 打开命令面板
3. 输入 "Python: Select Interpreter" 并选择该命令
4. 从列表中选择您的 Conda 环境（通常以 'envs/环境名' 形式显示）

方法 2：使用状态栏
1. 打开一个 Python 文件
2. 查看 VSCode 窗口左下角，应该显示当前 Python 解释器
3. 点击解释器名称，会弹出选择菜单
4. 从列表中选择您的 Conda 环境

方法 3：手动配置
1. 在项目文件夹中创建或编辑 .vscode/settings.json 文件
2. 添加以下内容（根据您的实际路径调整）：
   
   {
       "python.defaultInterpreterPath": "C:\\\\Users\\\\用户名\\\\anaconda3\\\\envs\\\\环境名\\\\python.exe"
   }
   
   或者在 Linux/Mac 上：
   
   {
       "python.defaultInterpreterPath": "/home/用户名/anaconda3/envs/环境名/bin/python"
   }
        """
        
        text = scrolledtext.ScrolledText(select_frame, width=85, height=20, wrap=tk.WORD)
        text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        text.insert(tk.INSERT, content)
        text.config(state=tk.DISABLED)
        
        select_frame.columnconfigure(0, weight=1)
        select_frame.rowconfigure(0, weight=1)
    
    def troubleshoot_tab(self, notebook):
        # 故障排除标签页
        troubleshoot_frame = ttk.Frame(notebook, padding="10")
        notebook.add(troubleshoot_frame, text="4. 故障排除")
        
        content = """
常见问题及解决方案：

1. VSCode 找不到 Conda 环境
   - 确保 Conda 已正确安装
   - 尝试在 VSCode 的集成终端中运行 "conda activate 环境名"
   - 重启 VSCode

2. Conda 环境不在解释器列表中
   - 手动输入解释器路径（见上一标签页的方法3）
   - 确保 Conda 环境已创建且可用

3. VSCode 终端无法激活 Conda 环境
   - 检查 VSCode 的终端设置，可能需要更改默认终端
   - 在设置中搜索 "terminal.integrated.shell.windows" (Windows) 或 
     "terminal.integrated.shell.osx" (Mac) 或 "terminal.integrated.shell.linux" (Linux)

4. 扩展无法正常工作
   - 确保已安装 Python 扩展
   - 尝试重新加载 VSCode 窗口 (Ctrl+Shift+P, 输入 "Developer: Reload Window")
   - 检查扩展是否已启用

5. 路径问题
   - 确保 Conda 的路径已添加到系统 PATH 环境变量中
   - 在 Windows 上，默认路径通常是 "C:\\\\Users\\\\用户名\\\\anaconda3\\\\Scripts" 和 "C:\\\\Users\\\\用户名\\\\anaconda3"
   - 在 Linux/Mac 上，通常是 "/home/用户名/anaconda3/bin"

如果问题仍然存在，可以尝试：
- 更新 Conda: conda update conda
- 更新 VSCode 和所有扩展
- 重新安装 Python 扩展
        """
        
        text = scrolledtext.ScrolledText(troubleshoot_frame, width=85, height=20, wrap=tk.WORD)
        text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        text.insert(tk.INSERT, content)
        text.config(state=tk.DISABLED)
        
        troubleshoot_frame.columnconfigure(0, weight=1)
        troubleshoot_frame.rowconfigure(0, weight=1)
    
    def check_conda(self):
        try:
            result = subprocess.run(["conda", "--version"], capture_output=True, text=True, check=True)
            self.status.config(text=f"找到 Conda: {result.stdout.strip()}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.status.config(text="未找到 Conda，请先安装 Anaconda 或 Miniconda")
            messagebox.showerror("错误", "未检测到 Conda 安装。请先安装 Anaconda 或 Miniconda。")
    
    def check_vscode(self):
        try:
            if sys.platform == "win32":
                result = subprocess.run(["code", "--version"], capture_output=True, text=True, check=True)
            else:
                result = subprocess.run(["which", "code"], capture_output=True, text=True, check=True)
            self.status.config(text="找到 VSCode 安装")
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.status.config(text="未找到 VSCode 或未添加到 PATH")
            messagebox.showwarning("警告", "未找到 VSCode 或未添加到 PATH。请确保已安装 VSCode 并将其添加到系统路径。")
    
    def copy_command(self, command):
        self.root.clipboard_clear()
        self.root.clipboard_append(command)
        self.status.config(text="命令已复制到剪贴板")
    
    def open_vscode_extensions(self):
        try:
            subprocess.Popen(["code", "--extensions-dir"])
            self.status.config(text="已尝试打开 VSCode 扩展面板")
        except FileNotFoundError:
            self.status.config(text="无法打开 VSCode，请检查安装")
            messagebox.showerror("错误", "无法启动 VSCode。请确保已安装并正确配置。")

if __name__ == "__main__":
    root = tk.Tk()
    app = VSCodeCondaConfigurator(root)
    root.mainloop()