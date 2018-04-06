from PIL import Image, ImageDraw, ImageFont



def mocked(string,output):
    image = Image.open("mock.jpg", 'r')
    width, height = image.size
    rell,tamstri = 0,0
    drawing = ImageDraw.Draw(image)

    def draw_shadow(off, argfont, estring, pix):
        drawing.text((off[0] - pix, off[1] - pix), estring, font=argfont, fill='black')
        drawing.text((off[0] + pix, off[1] - pix), estring, font=argfont, fill='black')
        drawing.text((off[0] - pix, off[1] + pix), estring, font=argfont, fill='black')
        drawing.text((off[0] + pix, off[1] + pix), estring, font=argfont, fill='black')

    if isinstance(string, u"".__class__):

        tamstri = len(string)
        rell = width // (int((tamstri) / 2.12))
        if rell > 200:
            rell = height // int(tamstri)
        offset = [width//rell, height - rell - 10]
        font = ImageFont.FreeTypeFont('impact.ttf', size=rell)
        draw_shadow(offset,font,string,2)
        drawing.text(offset, string, font=font)

    elif isinstance(string, list):
        offset = [20, height - height//4]
        maxlen = 0
        for elem in string:
            tamstri += len(elem)
            if maxlen < len(elem):
                maxlen = len(elem)
        rell = width // (int(maxlen/2.12))
        if rell > 90:
            rell = height // int(maxlen)
        font = ImageFont.FreeTypeFont('impact.ttf', size=rell)

        for line in string:
            draw_shadow(offset,font,line,2)
            drawing.text(offset, line, font=font)
            offset[1] += rell
    image.save(output)