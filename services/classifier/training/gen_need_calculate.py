import os
import random
import argparse
from PIL import Image,ImageDraw,ImageFont,ImageFilter


parser = argparse.ArgumentParser(description="Generating Calculation Needed Images")

parser.add_argument("-c","--count",type=int,default=1000)
parser.add_argument("-l","--log-file",type=str,default="need_calculation.log")
parser.add_argument("-o","--output-dir",type=str,default="need")
parser.add_argument("-f","--format",type=str,default="jpeg")

args=parser.parse_args()

font_paths=["font1.ttf","font2.ttf","font3.ttf","font4.ttf"]
image_size = (1300,600)

log_file = open(args.log_file,"w")

def generate_random_calculation():
    num1 = str(random.choice([random.randint(0,100),random.randint(100,10000),random.randint(10000,10000000)]))
    num2 = str(random.choice([random.randint(0,100),random.randint(100,10000),random.randint(10000,10000000)]))
    n_op_space = random.randint(1,2)
    operator = random.choice(['+', '-', '*','x'])
    return [f"{num1}{n_op_space*" "}{operator}",f"{num2}"]


def draw_curved_line(image,start_pos,end_pos):
    curve_height = random.randint(-40,40)
    print(f"\tcurve height : {curve_height} ")
    log_file.write(f"\tcurve height : {curve_height}\n")
    line_width = random.randint(1,3)
    print(f"\tline width : {line_width}")
    log_file.write(f"\tline width : {line_width}\n")
    draw = ImageDraw.Draw(image)
    control_x = (start_pos[0]+end_pos[0])/2
    control_y = (start_pos[1]+end_pos[1])/2-curve_height
    curve_points = []
    for t in range(101):
        t /= 100.0
        x = (1-t)**2*start_pos[0]+2*(1-t)*t*control_x + t**2 * end_pos[0]
        y = (1-t)**2*start_pos[1]+2*(1-t)*t*control_y + t**2 * end_pos[1]
        curve_points.append((int(x),int(y)))
        draw.line(curve_points,fill = 'black',width=line_width)


def create_image_with_calc(calc):
    font_size = random.randint(7,100)
    print(f"\tfont size : {font_size}")
    log_file.write(f"\tfont size : {font_size}\n")
    fonts = [ImageFont.truetype(font_path,font_size) for font_path in font_paths]
    font = random.choice(fonts)
    print(f"\tfont : {font.getname()}")
    log_file.write(f"\tfont : {font.getname()}\n")
    image = Image.new('RGB',image_size,color='white')
    draw = ImageDraw.Draw(image)
    offset_height = random.randint(-200,200)
    offset_width = random.randint(-200,200)
    i = 0
    for text in calc:
        text_bbox = draw.textbbox((0,0),text,font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        position = (((image_size[0] - text_width)//2)+offset_width,((image_size[1] - text_height)//2)+(offset_height+(i*40)))
        if i == 0:
            print(f"\tposition : {position}")
            log_file.write(f"\tposition : {position}\n")
        draw.text(position,text,fill="black",font=font)
        if i == 1:
            draw_curved_line(image,
                             (((image_size[0] - text_width)//2)+offset_width-random.randint(75,100),((image_size[1] - text_height)//2)+(offset_height+(100+random.randint(0,20)))),
                             (((image_size[0] - text_width)//2)+offset_width+random.randint(75,100),((image_size[1] - text_height)//2)+(offset_height+(100+random.randint(0,20)))))

        i+=1
    return image


def augment_image(image):
    blur_level = random.randint(1,3)
    print(f"\tblur level : {blur_level}")
    log_file.write(f"\tblur level : {blur_level}\n")
    image = image.filter(ImageFilter.GaussianBlur(radius=blur_level))
    angle = random.uniform(-95,95)
    print(f"\tangle : f{angle}")
    log_file.write(f"\tangle : f{angle}\n")
    image = image.rotate(angle,expand=0,fillcolor='white')
    return image



for i in range(args.count//2):
    random_calc = generate_random_calculation()
    print(f"{i+1} : \n\tcalc : {" ".join(random_calc)}")
    log_file.write(f"{i+1} : \n\tcalc : {" ".join(random_calc)}\n")
    create_image_with_calc(random_calc).save(os.getcwd()+"/"+args.output_dir+"/calc-"+str(i+1),args.format)

for i in range((args.count//2)+1,args.count):
    random_calc = generate_random_calculation()
    print(f"{i+1} : \n\tcalc : {" ".join(random_calc)}")
    log_file.write(f"{i+1} : \n\tcalc : {" ".join(random_calc)}\n")
    augment_image(create_image_with_calc(random_calc)).save(os.getcwd()+"/"+args.output_dir+"/augmented_calc-"+str(i+1),args.format)

print("Normal Images :"+str(args.count//2))
print("Augmented Images :"+str(args.count-(args.count//2)))
log_file.write("Normal Images :"+str(args.count//2)+"\n")
log_file.write("Augmented Images :"+str(args.count-(args.count//2)))
log_file.close()

