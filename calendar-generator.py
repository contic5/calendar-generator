from datetime import datetime, timedelta
from PIL import Image
from PIL import ImageDraw,ImageFont
from pathlib import Path

def get_images():
    path=Path("images")
    img_arr=[]

    for image_file in path.iterdir():
        # 1. Open an image from disk
        with Image.open(image_file.absolute()) as img:
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

    
    img_arr=[]
    img=Image.new("RGB", (1980, 1080*2), (255, 255, 255))
    img.paste(background_images[background_images_index],(0,0))

    date:datetime = datetime(2027, 1, 1)
    last_month=-1
    while date.year==2027:
        day=date.day
        weekday=date.weekday()
        month=date.month
        print(f"{weekday}: {month}/{day}")

        if month!=last_month:
            img_arr.append(img)
            img.save(f"output/Image {last_month}.jpg")
            last_month=month
            background_images_index+=1
            if background_images_index>=len(background_images):
                break
            
            img=Image.new("RGB", (1980, 1080*2), (255, 255, 255))
            img.paste(background_images[background_images_index],(0,0))

        x=(weekday*img.width)/7
        y=img.height/2
        y+=(day/7)*(img.height/10)

        add_text(img,day,(x,y),14,"black")
        date=date+timedelta(days=1)

if __name__=="__main__":
    main()