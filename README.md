# PDF水印工具

一个简单易用的PDF水印添加工具，支持自定义水印文本、字体大小、透明度、间距等参数。

## 功能特点

- 支持中文水印
- 可调整水印大小、透明度、间距
- 实时预览水印效果
- 自动生成带时间戳的输出文件
- 支持Windows和macOS系统

## 打包说明

### 环境要求

- Python 3.7+
- pip（Python包管理器）

### 打包步骤

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 生成图标：
```bash
python create_icon.py
```

3. 执行打包：
```bash
python build.py
```

打包完成后，可执行文件将位于 `dist/PDF水印工具` 目录下。

### Windows系统
- 运行 `dist/PDF水印工具/PDF水印工具.exe`

### macOS系统
- 运行 `dist/PDF水印工具.app`

## 使用说明

1. 点击"浏览"选择要添加水印的PDF文件
2. 输入水印文本
3. 调整水印参数：
   - 字体大小
   - 透明度
   - 水平间距
   - 垂直间距
   - 旋转角度
4. 点击"水印样式预览"查看效果
5. 点击"文件添加水印"生成带水印的PDF文件

## 注意事项

- 确保系统安装了中文字体
- macOS用户需要安装poppler：
  ```bash
  brew install poppler
  ```
- 生成的PDF文件会自动添加时间戳，格式为：原文件名_Watermarked_yyyyMMddHHmm.pdf 