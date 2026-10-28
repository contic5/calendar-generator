from datetime import datetime, timedelta
from PIL import Image
from PIL import ImageDraw,ImageFont
from pathlib import Path

image_names=["january","february","march","april","may","june","july","august","september","october","november","december"]
def get_images(folder):
    path=Path("images")
    img_arr=[]

    for image_name in image_names:
        img=Image.open(f"images/{folder}/{image_name}.png")
        img=img.resize((1980,1080))
        img_arr.append(img)
    return img_arr

def add_text(img, text, position, font_size, colour,anchor="lt"):
    font = ImageFont.truetype("fonts/Aptos-Mono.ttf", font_size)
    draw = ImageDraw.Draw(img)
    draw.text(position, text, font=font, fill=colour,anchor=anchor)
    return img

def setup_image(top_images,bottom_images,images_index,date):
    weekday_initials=["S","M","Tu","W","Th","F","S"]

    img=Image.new("RGBA", (1980, 1080*2), (255, 255, 255))
    img.paste(bottom_images[images_index],(0,1080))

    overlay_img=Image.new("RGBA", (1980, 1080*2), (255, 255, 255,255))
    draw = ImageDraw.Draw(overlay_img)
    draw.rectangle((0,1080,1980,1080*2), fill=(255,255,255,64))
    draw.rectangle((0,8*img.height/16,1980,10*img.height/16), fill=(255,255,255,128))
    img = Image.alpha_composite(img, overlay_img)

    img.paste(top_images[images_index],(0,0))

    img=add_text(img,date.strftime("%B").upper(),(0,img.height/2),128,(0,0,0))
    for i in range(len(weekday_initials)):
        x=i*img.width/7+img.width/14
        img=add_text(img,weekday_initials[i],(x,9*img.height/16),128,(0,0,0),anchor="mt")
    return img

def main():
    top_images=get_images("top")
    bottom_images=get_images("bottom")
    images_index=0

    date:datetime = datetime(2027, 1, 1)
    last_month=1
    week=0
    
    img_arr=[]
    img=setup_image(top_images,bottom_images,images_index,date)
    
    while date.year==2027:
        day=date.day
        weekday=date.weekday()
        weekday=(weekday+1)%7 #Sunday should be 0, Monday should be 1, etc
        month=date.month

        if month!=last_month:
            img_arr.append(img)
            outfile_name=f"output/({last_month}) {image_names[last_month-1].title()}.png"
            img.save(outfile_name)
            print(f"Saved {outfile_name}")

            last_month=month
            week=0
            images_index+=1
            if images_index>=len(bottom_images):
                break
            
            img=setup_image(top_images,bottom_images,images_index,date)

        if weekday==0 and day>1:
            week+=1

        x=(weekday*img.width)//7
        y=(10*img.height)//16
        y+=(week)*(img.height//16)

        img=add_text(img,str(day),(x+img.width/14,y+img.height/32),64,(0,0,0),anchor="mt")
        draw = ImageDraw.Draw(img)

        next_date=date+timedelta(days=1)
        if day%2==0:
            draw.rectangle((x,y,x+img.width/7,y+img.height/16),fill=None,outline="white",width=15)
        else:
            draw.rectangle((x,y,x+img.width/7,y+img.height/16),fill=None,outline="lightgray",width=15)
        date=next_date

    outfile_name=f"output/({last_month}) {image_names[last_month-1].title()}.png"
    img.save(outfile_name)
    print(f"Saved {outfile_name}")

if __name__=="__main__":
    main()