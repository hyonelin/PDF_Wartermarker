from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    # 创建一个 1024x1024 的图像
    size = 1024
    image = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    
    # 绘制圆形背景
    circle_color = (41, 128, 185)  # 蓝色
    draw.ellipse([50, 50, size-50, size-50], fill=circle_color)
    
    # 添加文字
    try:
        # 尝试使用系统字体
        font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 400)
    except:
        # 如果找不到系统字体，使用默认字体
        font = ImageFont.load_default()
    
    text = "PDF"
    text_color = (255, 255, 255)  # 白色
    
    # 计算文字位置使其居中
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    # 绘制文字
    draw.text((x, y), text, font=font, fill=text_color)
    
    # 保存为不同格式
    # Windows 图标
    image.save('icon.ico', format='ICO', sizes=[(256, 256)])
    
    # macOS 图标
    image.save('icon.icns', format='ICNS')

if __name__ == '__main__':
    create_icon() 