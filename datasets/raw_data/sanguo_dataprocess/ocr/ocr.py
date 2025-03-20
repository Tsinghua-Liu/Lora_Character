from pdf2image import convert_from_path
import pytesseract
import cv2
import numpy as np
from PIL import Image
import os


def pdf_to_text(pdf_path,
                output_txt,
                dpi=350,
                lang='chi_sim',
                # 图像预处理参数
                gray_mode=True,
                threshold_type='adaptive',
                denoise=True,
                sharpen=True,
                denoise_h=30,
                denoise_template=5,
                denoise_search=11,
                sharpen_kernel=None,
                # 系统参数
                poppler_path= r"E:\softwares\poppler-24.08.0\Library\bin",
                tesseract_config = r"E:\softwares\Tesseract-OCR\tesseract.exe"):

    """
    PDF扫描件转文本核心函数
    参数：
        pdf_path: PDF文件路径
        output_txt: 输出文本路径
        dpi: 图像分辨率(200-600)
        lang: OCR语言(默认中英混合)
        gray_mode: 是否灰度化
        threshold_type: 阈值类型(adaptive/otsu)
        denoise: 是否去噪
        sharpen: 是否锐化
        denoise_h: 去噪强度
        denoise_template: 去噪模板窗口
        denoise_search: 去噪搜索窗口  
        sharpen_kernel: 自定义锐化核
        poppler_path: Poppler工具路径
        tesseract_config: Tesseract额外配置
    """
    # 默认锐化核
    if sharpen_kernel is None:
        sharpen_kernel = np.array([[0, -1, 0], [-1, 6, -1], [0, -1, 0]])

    # 转换PDF为图像
    images = convert_from_path(pdf_path,
                               dpi=dpi,
                               poppler_path=poppler_path,
                               fmt='jpeg',
                               thread_count=4)

    with open(output_txt, 'w', encoding='utf-8') as f:
        for page_num, image in enumerate(images, 1):
            # 图像预处理
            _, processed_img = preprocess_image(
                image,
                gray_mode=gray_mode,
                threshold_type=threshold_type,
                denoise=denoise,
                sharpen=sharpen,
                denoise_h=denoise_h,
                denoise_template=denoise_template,
                denoise_search=denoise_search,
                sharpen_kernel=sharpen_kernel
            )

            # OCR识别
            text = pytesseract.image_to_string(
                processed_img,
                lang=lang,
                config=tesseract_config
            )

            # 写入分页内容
            f.write(f"\n=== PAGE {page_num} ===\n")
            f.write(text)
            f.write("\n" + "=" * 40 + "\n")

            # 进度提示
            if page_num % 10 == 0:
                print(f"Processed {page_num} pages...")

            if page_num>0:
                break
    print(f"OCR完成！输出文件：{os.path.abspath(output_txt)}")


# 修改后的预处理函数（参数兼容）
def preprocess_image(image,
                     gray_mode=True,
                     threshold_type='adaptive',
                     denoise=True,
                     sharpen=True,
                     denoise_h=30,
                     denoise_template=5,
                     denoise_search=11,
                     sharpen_kernel=None,
                     debug=False):
    img = np.array(image)

    # 灰度转换
    if gray_mode and len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # 阈值处理
    if threshold_type == 'adaptive':
        img = cv2.adaptiveThreshold(img, 255,
                                    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                    cv2.THRESH_BINARY, 21, 5)
    elif threshold_type == 'otsu':
        _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 去噪处理
    if denoise:
        img = cv2.fastNlMeansDenoising(
            img,
            h=denoise_h,
            templateWindowSize=denoise_template,
            searchWindowSize=denoise_search
        )

    # 锐化处理
    if sharpen and sharpen_kernel is not None:
        img = cv2.filter2D(img, -1, sharpen_kernel)

    return image, Image.fromarray(img)


# 使用示例
if __name__ == "__main__":
    pytesseract.pytesseract.tesseract_cmd = r'E:\softwares\Tesseract-OCR\tesseract.exe'
    pdf_to_text(
        pdf_path="sanguo1-10.pdf",
        output_txt="sanguo1-10.txt",
        dpi=500,
        lang='chi_sim',
        gray_mode=True,
        threshold_type='otsu',
        denoise=True,
        denoise_h=25,  # 增强去噪力度
        sharpen_kernel=np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]],),  # 强化锐化
        poppler_path=r"E:\softwares\poppler-24.08.0\Library\bin",
    )