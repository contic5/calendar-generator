from datetime import datetime, timedelta
from PIL import Image
from PIL import ImageDraw,ImageFont
from pathlib import Path

image_names=["january","february","march","april","may","june","july","august","september","october","november","december"]
def get_images():
    path=Path("images")
    img_arr=[]

    for image_name in image_names:
        img=Image.open(f"images/{image_name}.png")
        img=img.resize((1980,1080))
        img_arr.append(img)
    return img_arr

def add_text(img, text, position, font_size, colour):
    font = ImageFont.truetype("fonts/Aptos-Mono.ttf", font_size)
    draw = ImageDraw.Draw(img)
    draw.text(position, text, font=font, fill=colour)
    return img

def main():
    background_images=get_images()
    background_images_index=0

    print(background_images_index)
    img_arr=[]
    img=Image.new("RGB", (1980, 1080*2), (255, 255, 255))
    img.paste(background_images[background_images_index],(0,0))

    date:datetime = datetime(2027, 1, 1)
    last_month=1
    week=0
    while date.year==2027:
        day=date.day
        weekday=date.weekday()
        month=date.month

        if month!=last_month:
            img_arr.append(img)
            img.save(f"output/Image {last_month}.jpg")
            print(f"Saved output/Image {last_month}.jpg")
            last_month=month
            week=0
            background_images_index+=1
            if background_images_index>=len(background_images):
                break
            
            img=Image.new("RGB", (1980, 1080*2), (255, 255, 255))
            img.paste(background_images[background_images_index],(0,0))

        if weekday==0:
            week+=1
        x=(weekday*img.width)//7
        y=img.height//2
        y+=(week)*(img.height//10)

        img=add_text(img,str(day),(x,y),64,(0,0,0))
        date=date+timedelta(days=1)
    img.save(f"output/Image {last_month}.jpg")
    print(f"Saved output/Image {last_month}.jpg")

if __name__=="__main__":
    main()