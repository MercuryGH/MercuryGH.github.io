from PIL import Image
import sys

def concatenate_images_horizontally(image1_path, image2_path, output_path):
    """
    将两张高度相同的图片水平拼接并保存
    
    参数:
        image1_path (str): 第一张图片的路径
        image2_path (str): 第二张图片的路径
        output_path (str): 输出图片的路径
    """
    try:
        # 打开两张图片
        image1 = Image.open(image1_path)
        image2 = Image.open(image2_path)
        
        # 检查两张图片的高度是否相同
        if image1.height != image2.height:
            raise ValueError("两张图片的高度不一致，无法水平拼接")
        
        # 创建一个新图片，宽度为两张图片宽度之和，高度与输入图片相同
        new_width = image1.width + image2.width
        new_image = Image.new('RGB', (new_width, image1.height))
        
        # 将两张图片粘贴到新图片中
        new_image.paste(image1, (0, 0))
        new_image.paste(image2, (image1.width, 0))
        
        # 保存输出图片
        new_image.save(output_path)
        print(f"图片拼接成功，已保存到 {output_path}")
        
    except Exception as e:
        print(f"发生错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # 检查命令行参数
    if len(sys.argv) != 4:
        print("用法: python concatenate_images.py 图片1路径 图片2路径 输出图片路径")
        sys.exit(1)
    
    image1_path = sys.argv[1]
    image2_path = sys.argv[2]
    output_path = sys.argv[3]
    
    concatenate_images_horizontally(image1_path, image2_path, output_path)
