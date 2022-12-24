from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\\tesseract.exe'
def read_text(text_path):

    im = Image.open(text_path)
    imgry = im.convert("L")
    threshold = 140
    table = []
    for j in range(256):
        if j < threshold:
            table.append(1)
        else:
            table.append(0)    

    out = imgry.point(table, '1')
    text = pytesseract.image_to_string(out, lang="eng",config='--psm 6')
    out.save("aa.png")
    return text

if  __name__ == '__main__':
    print(read_text("captcha.png"))
    