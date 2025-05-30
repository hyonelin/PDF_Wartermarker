from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from PyPDF2 import PdfWriter, PdfReader
import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
import shutil
from PIL import Image, ImageTk
import io
from reportlab.pdfbase.pdfmetrics import stringWidth
import tempfile

class PDFWatermarker:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("PDF水印工具")
        self.window.geometry("800x900")
        
        # 注册中文字体
        self.register_chinese_font()
        
        # 创建主框架
        self.main_frame = ttk.Frame(self.window, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 文件选择
        ttk.Label(self.main_frame, text="选择PDF文件:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.file_path = tk.StringVar()
        ttk.Entry(self.main_frame, textvariable=self.file_path, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(self.main_frame, text="浏览", command=self.browse_file).grid(row=0, column=2)
        
        # 水印文本
        ttk.Label(self.main_frame, text="水印文本:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.watermark_text = tk.StringVar(value="这是水印文案")
        ttk.Entry(self.main_frame, textvariable=self.watermark_text, width=50).grid(row=1, column=1, columnspan=2, sticky=tk.W)
        
        # 水印设置
        settings_frame = ttk.LabelFrame(self.main_frame, text="水印设置", padding="5")
        settings_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # 字体大小
        ttk.Label(settings_frame, text="字体大小:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.font_size = tk.IntVar(value=30)
        ttk.Spinbox(settings_frame, from_=10, to=100, textvariable=self.font_size, width=10).grid(row=0, column=1, padx=5)
        
        # 透明度
        opacity_frame = ttk.Frame(settings_frame)
        opacity_frame.grid(row=0, column=2, columnspan=2, sticky=tk.W, pady=5, padx=10)
        ttk.Label(opacity_frame, text="透明度:").pack(side=tk.LEFT)
        self.opacity = tk.DoubleVar(value=0.2)
        self.opacity_scale = ttk.Scale(opacity_frame, from_=0.1, to=1.0, variable=self.opacity, 
                                     orient=tk.HORIZONTAL, length=150, command=self.update_opacity_label)
        self.opacity_scale.pack(side=tk.LEFT, padx=5)
        self.opacity_label = ttk.Label(opacity_frame, text="20%")
        self.opacity_label.pack(side=tk.LEFT)
        
        # 水平间距
        ttk.Label(settings_frame, text="水平间距(cm):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.horizontal_gap = tk.DoubleVar(value=1.5)
        ttk.Spinbox(settings_frame, from_=0.1, to=10.0, increment=0.1, textvariable=self.horizontal_gap, width=10).grid(row=1, column=1, padx=5)
        
        # 垂直间距
        ttk.Label(settings_frame, text="垂直间距比例:").grid(row=1, column=2, sticky=tk.W, pady=5, padx=10)
        self.vertical_gap_ratio = tk.DoubleVar(value=0.2)
        ttk.Spinbox(settings_frame, from_=0.1, to=1.0, increment=0.1, textvariable=self.vertical_gap_ratio, width=10).grid(row=1, column=3)
        
        # 旋转角度
        ttk.Label(settings_frame, text="旋转角度:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.rotation = tk.IntVar(value=45)
        ttk.Spinbox(settings_frame, from_=0, to=360, textvariable=self.rotation, width=10).grid(row=2, column=1, padx=5)
        
        # 预览和生成按钮
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=20)
        ttk.Button(button_frame, text="水印样式预览", command=self.preview_watermark).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="文件添加水印", command=self.generate_watermark).pack(side=tk.LEFT, padx=5)
        
        # 预览区域
        preview_frame = ttk.LabelFrame(self.main_frame, text="预览", padding="5")
        preview_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        self.preview_canvas = tk.Canvas(preview_frame, width=600, height=400, bg='white')
        self.preview_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 状态栏
        self.status_var = tk.StringVar()
        ttk.Label(self.main_frame, textvariable=self.status_var).grid(row=5, column=0, columnspan=3, sticky=tk.W)
        
        # 配置网格权重
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(4, weight=1)
        preview_frame.grid_columnconfigure(0, weight=1)
        preview_frame.grid_rowconfigure(0, weight=1)
    
    def update_opacity_label(self, *args):
        opacity_value = int(self.opacity.get() * 100)
        self.opacity_label.config(text=f"{opacity_value}%")
    
    def create_preview_image(self):
        # 创建临时PDF
        temp_pdf = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
        temp_pdf.close()
        
        # 创建水印PDF
        self.create_watermark(self.watermark_text.get(), temp_pdf.name)
        
        # 将PDF转换为图像
        from pdf2image import convert_from_path
        images = convert_from_path(temp_pdf.name, first_page=1, last_page=1)
        
        # 清理临时文件
        os.unlink(temp_pdf.name)
        
        return images[0]
    
    def preview_watermark(self):
        try:
            # 创建预览图像
            preview_image = self.create_preview_image()
            
            # 调整图像大小以适应预览区域
            canvas_width = self.preview_canvas.winfo_width()
            canvas_height = self.preview_canvas.winfo_height()
            
            # 计算缩放比例
            img_width, img_height = preview_image.size
            scale = min(canvas_width/img_width, canvas_height/img_height)
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            
            # 调整图像大小
            preview_image = preview_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # 转换为PhotoImage
            self.photo = ImageTk.PhotoImage(preview_image)
            
            # 清除画布并显示新图像
            self.preview_canvas.delete("all")
            self.preview_canvas.create_image(
                canvas_width//2, 
                canvas_height//2, 
                image=self.photo, 
                anchor=tk.CENTER
            )
            
            self.status_var.set("预览已更新")
            
        except Exception as e:
            messagebox.showerror("预览错误", f"生成预览时出错: {str(e)}")
            self.status_var.set("预览失败")
    
    def register_chinese_font(self):
        system_fonts = [
            '/System/Library/Fonts/PingFang.ttc',  # macOS
            '/System/Library/Fonts/STHeiti Light.ttc',  # macOS
            '/System/Library/Fonts/STHeiti Medium.ttc',  # macOS
            '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf',  # Linux
            'C:/Windows/Fonts/simhei.ttf',  # Windows
        ]
        
        for font_path in system_fonts:
            if os.path.exists(font_path):
                pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
                return True
        
        messagebox.showerror("错误", "未找到可用的中文字体，请确保系统安装了中文字体")
        return False
    
    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="选择PDF文件",
            filetypes=[("PDF文件", "*.pdf")]
        )
        if filename:
            self.file_path.set(filename)
    
    def create_watermark(self, watermark_text, output_file):
        c = canvas.Canvas(output_file)
        width, height = c._pagesize
        
        # 设置透明度
        c.setFillAlpha(self.opacity.get())
        c.setFont("ChineseFont", self.font_size.get())
        
        # 倾斜文本
        c.rotate(self.rotation.get())
        
        # 创建重复水印文本覆盖整页
        text_width = c.stringWidth(watermark_text, "ChineseFont", self.font_size.get())
        gap = text_width + self.horizontal_gap.get()*cm
        
        # 扩展覆盖范围确保旋转后仍覆盖整页
        expanded_width = (width + height) * 1.5
        expanded_height = expanded_width
        
        # 绘制水印网格
        y = -height
        while y < expanded_height:
            x = -width
            while x < expanded_width:
                c.drawString(x, y, watermark_text)
                x += gap
            y += gap * self.vertical_gap_ratio.get()
        
        c.save()
    
    def add_watermark(self, input_pdf, output_pdf, watermark_file):
        watermark = PdfReader(watermark_file)
        pdf_reader = PdfReader(input_pdf)
        pdf_writer = PdfWriter()
        
        for i in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[i]
            page.merge_page(watermark.pages[0])
            pdf_writer.add_page(page)
        
        with open(output_pdf, 'wb') as out:
            pdf_writer.write(out)
    
    def generate_watermark(self):
        input_file = self.file_path.get()
        if not input_file:
            messagebox.showerror("错误", "请选择PDF文件")
            return
        
        if not os.path.exists(input_file):
            messagebox.showerror("错误", "选择的文件不存在")
            return
        
        watermark_text = self.watermark_text.get()
        if not watermark_text:
            messagebox.showerror("错误", "请输入水印文本")
            return
        
        try:
            # 创建临时水印文件
            watermark_file = "temp_watermark.pdf"
            self.create_watermark(watermark_text, watermark_file)
            
            # 生成输出文件名
            input_filename = os.path.splitext(os.path.basename(input_file))[0]
            timestamp = datetime.now().strftime("%Y%m%d%H%M")
            output_file = f"{input_filename}_Watermarked_{timestamp}.pdf"
            
            # 添加水印
            self.add_watermark(input_file, output_file, watermark_file)
            
            # 清理临时文件
            os.remove(watermark_file)
            
            self.status_var.set(f"水印已生成: {output_file}")
            messagebox.showinfo("成功", f"水印已生成: {output_file}")
            
        except Exception as e:
            messagebox.showerror("错误", f"生成水印时出错: {str(e)}")
            self.status_var.set("生成失败")
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = PDFWatermarker()
    app.run()