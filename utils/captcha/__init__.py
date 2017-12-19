import random
import string
from PIL import Image, ImageDraw, ImageFont


class Captcha:
    # 验证码图片宽和高
    SIZE = (100, 40)
    # 生成几位数的验证码
    NUMBER = 4
    # 验证码字体大小
    FONTSIZE = 25
    # 加入干扰线的条数
    LINE_NUMBER = 3
    # 构建一个验证码源文本[a-zA-Z0-9]
    SPURCE = list(string.ascii_letters + string.digits)

    # 生成随机颜色
    @classmethod
    def __gene_random_color(cls, start=0, end=255):
        random.seed()
        return random.randint(start, end), random.randint(start, end), random.randint(start, end)

    # 随机选择一个字体
    @classmethod
    def __gene_random_font(cls):
        fonts = [
            'Apple Chancery.ttf',
            'Arial Bold Italic.ttf',
            'Luminari.ttf',
            'Malayalam MN.ttc'
        ]
        font = random.choice(fonts)
        return 'utils/captcha/fonts/' + font

    # 绘制干扰线
    @classmethod
    def __gene_line(cls, draw, width, height):
        begin = (random.randint(0, width), random.randint(0, height))
        end = (random.randint(0, width), random.randint(0, height))
        draw.line([begin, end], fill=cls.__gene_random_color(), width=2)

    # 绘制干扰噪点
    @classmethod
    def __gene_points(cls, draw, point_chance, width, height):
        chance = min(100, max(0, int(point_chance)))
        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill=cls.__gene_random_color())

    # 随机生成一个字符串
    @classmethod
    def __gene_text(cls, number):
        return ''.join(random.sample(cls.SPURCE, number))

    # 生成验证码
    @classmethod
    def gene_graph_captcha(cls):
        # 验证码图片宽和高
        width, height = cls.SIZE
        # 创建一个图片
        image = Image.new('RGBA', (width, height), cls.__gene_random_color(0, 100))
        # 验证码的字体
        font = ImageFont.truetype(cls.__gene_random_font(), cls.FONTSIZE)
        # 创建画笔
        draw = ImageDraw.Draw(image)
        # 生成字符串
        text = cls.__gene_text(cls.NUMBER)
        # 获取字体的宽和高
        font_width, font_height = font.getsize(text)
        # 填充字符串
        draw.text(((width - font_width) / 2, (height - font_height) / 2), text, font=font,
                  fill=cls.__gene_random_color(150, 255))
        # 绘制干扰线
        for x in range(0, cls.LINE_NUMBER):
            cls.__gene_line(draw, width, height)

        # 绘制噪点
        cls.__gene_points(draw, 10, width, height)
        # with open('captcha.png', 'wb') as fp:
        #     # print(fp)
        #     image.save(fp)

        return text, image


if __name__ == '__main__':
    Captcha.gene_graph_captcha()
