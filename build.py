import os
import platform
import subprocess
import sys

def install_requirements():
    """安装必要的依赖"""
    requirements = [
        'reportlab',
        'PyPDF2',
        'Pillow',
        'pdf2image',
        'pyinstaller'
    ]
    
    for req in requirements:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', req])

def build_executable():
    """构建可执行文件"""
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 基本参数
    icon_path = os.path.join(current_dir, 'icon.ico' if platform.system() == 'Windows' else 'icon.icns')
    name = 'PDF水印工具'
    
    # PyInstaller 命令
    cmd = [
        'pyinstaller',
        '--name', name,
        '--windowed',  # 不显示控制台窗口
        '--clean',     # 清理临时文件
        '--noconfirm', # 不确认覆盖
        '--add-data', f'{current_dir}/pdf.py:.',  # 添加主程序文件
    ]
    
    # 添加图标（如果存在）
    if os.path.exists(icon_path):
        cmd.extend(['--icon', icon_path])
    
    # 添加主程序
    cmd.append('pdf.py')
    
    # 执行打包命令
    subprocess.check_call(cmd)
    
    print(f"打包完成！可执行文件位于 dist/{name} 目录下")

if __name__ == '__main__':
    # 安装依赖
    install_requirements()
    
    # 构建可执行文件
    build_executable() 