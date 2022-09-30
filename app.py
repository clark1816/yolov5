import string
from unicodedata import name
from wtforms.validators import InputRequired
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired
from werkzeug.utils import secure_filename
import pathlib
import os
import glob
import torch
import shutil
import cv2

#requirements--  pip install flask_wtf wtforms pathlib

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdf123'
app.config['UPLOAD_FOLDER'] = 'static/upload_images'
app.jinja_env.filters['zip'] = zip

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

@app.route('/', methods=['GET', "POST"])
def landingpage():
    form = UploadFileForm()
    #remove the files in the result folder 
    files = glob.glob('runs/detect/exp/*')
    upload_files = glob.glob('static/upload_images/*')
    for f in files:
        try:
            os.remove(f)
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))
    for fx in upload_files:
        try:
            os.remove(fx)
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))
    #now that is done succesful delete the folder 
    dir_path = 'runs/detect/exp'
    try:
        os.rmdir(dir_path)
    except OSError as e:
        print("Error: %s : %s" % (dir_path, e.strerror))
    return render_template('landingpage.html')
@app.route('/image', methods=['GET', "POST"])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
        file_name = (f"static/upload_images/{file.filename}")
        print(file_name)
        video = cv2.VideoCapture(file_name)
        file_extension = pathlib.Path(file_name).suffix
        if file_extension == '.mp4' or file_extension == ".mov":
            
            while True:
                video = cv2.VideoCapture(file_name)
                (sussessful_frame_read, frame) = video.read()
                if sussessful_frame_read:
                    print(frame)
                    # Inference
                    
                
                    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5n - yolov5x6, custom
                    results = model(frame)
                    # Images
                    img = file_name  # or file, Path, PIL, OpenCV, numpy, list

                    # Results
                    results.save()

                    path = "runs/detect/exp"
                    dir_list = os.listdir(path)
                    
                    print("Files and directories in '", path, "' :")
                    
                    # prints all files

                    #for fil in dir_list:
                        #file_path_list = (f"/root/yolov5_flask-app/runs/detect/exp/{fil}")
                    file_path = [i for i in dir_list]
                    print(file_path[0])
                    print(file_name)
                    #file_path_list = file_path
                
                    shutil.move(path + "/" + file_path[0], file_name)
                    
                    rl = results.xyxy[0].tolist()
                    print(rl)
                    return render_template('file_upload2.html', file_name=file_name, file_extension=file_extension)#, link_list=result_list_link, item_list = result_list_item, rl = rl)
        else:
            print(file_extension)
                
            model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5n - yolov5x6, custom

            # Images
            img = file_name  # or file, Path, PIL, OpenCV, numpy, list
            

            # Inference
            results = model(img)

            # Results
            results.save()

            path = "runs/detect/exp"
            dir_list = os.listdir(path)
            
            print("Files and directories in '", path, "' :")
            
            # prints all files

            #for fil in dir_list:
                #file_path_list = (f"/root/yolov5_flask-app/runs/detect/exp/{fil}")
            file_path = [i for i in dir_list]
            print(file_path[0])
            print(file_name)
            #file_path_list = file_path
        
            shutil.move(path + "/" + file_path[0], file_name)
            
            rl = results.xyxy[0].tolist()
            print(rl)

            #if any results do the following 
            result_list_link = []
            result_list_item = []
            rldisplay = []
            for x in rl:
                cords = ''
                for i in range(3):
                    cords+=str(x[i])+','
                cords+=str(x[3])




                
            #if the confidence is above 30%
                if rl[0][4] > .35:
                            #[0][5] is the class parameter. 
                            if x[5] == 61:
                                print("https://www.homedepot.com/p/Delta-Foundations-2-piece-1-1-GPF-1-6-GPF-Dual-Flush-Elongated-Toilet-in-White-Seat-Included-C43913D-WH/314293511?source=shoppingads&locale=en-US&&mtc=SHOPPING-RM-RMP-GGL-D29B-029_032_TOILET_SEATS-MB-DELTA-NA-SMART-NA-NA-MK560823300-9017946428-NBR-4-CON-NA-FY22_4_Toilets&cm_mmc=SHOPPING-RM-RMP-GGL-D29B-029_032_TOILET_SEATS-MB-DELTA-NA-SMART-NA-NA-MK560823300-9017946428-NBR-4-CON-NA-FY22_4_Toilets-71790000098969720-58790007973133485-92790072534693367&gclid=CjwKCAjwvsqZBhAlEiwAqAHElTm3DNRUb7jlOnlQGUoKD_b-WlAkMIW8EnXfZt-nwFrUfmvDlHUMGRoCqJkQAvD_BwE&gclsrc=aw.ds")
                            if x[5] == 1:
                                item = 'bike: '
                                link = 'https://www.amazon.com/s?k=bicycle&crid=ANGABQ99FK09&sprefix=bicycle%2Caps%2C65&ref=nb_sb_noss_1'
                                
                            if x[5] == 2:
                                item = 'car: '
                                link = 'https://www.amazon.com/s?k=car&crid=3NG8UMN3OSUCX&sprefix=car%2Caps%2C73&ref=nb_sb_noss_1'
                            if x[5] == 3:
                                item = 'motorcycle: '
                                link = 'https://www.amazon.com/s?k=motorcycle&sprefix=moto%2Caps%2C83&ref=nb_sb_ss_ts-doa-p_1_4'
                            if x[5] == 4:
                                item = 'airplane: '
                                link ='https://www.amazon.com/s?k=airplane&crid=2FR7BDB6NZB8R&sprefix=airplane%2Caps%2C87&ref=nb_sb_noss_1'
                            if x[5] == 5:
                                item = 'bus: '
                                link ='https://www.amazon.com/s?k=bus&crid=1I5VI3N938ZD1&sprefix=bus%2Caps%2C75&ref=nb_sb_noss_1'
                            if x[5] == 6:
                                item = 'train: '
                                link ='https://www.amazon.com/s?k=train&crid=ZFWPGOH7KLDO&sprefix=train%2Caps%2C82&ref=nb_sb_noss_1'
                                 
                            if x[5] == 7:
                                item = 'truck: '
                                link = 'https://www.amazon.com/s?k=truck&crid=2RJM319OPSTYO&sprefix=truck%2Caps%2C79&ref=nb_sb_noss_1'
                                 
                            if x[5] == 8:
                                item = 'boat: '
                                link = 'https://www.amazon.com/s?k=boat&crid=2N4QSE3C3S8C9&sprefix=boat%2Caps%2C76&ref=nb_sb_noss_1'
                                 
                            if x[5] == 9:
                                item = 'traffic light: '
                                link ='https://www.amazon.com/s?k=traffic+light&crid=25ZLOJJD4U3SG&sprefix=traffic+light%2Caps%2C79&ref=nb_sb_noss_1'
                                 
                            if x[5] == 10:
                                item = 'fire hydrant: '
                                link ='https://www.amazon.com/s?k=fire+hydrant&sprefix=fire+hyd%2Caps%2C77&ref=nb_sb_ss_ts-doa-p_2_8'
                                
                            if x[5] == 11:
                                item = 'stop sign: '
                                link = 'https://www.amazon.com/s?k=stop+sign&crid=2W6ZVD967WUK1&sprefix=stop+sign%2Caps%2C73&ref=nb_sb_noss_1'
                                
                            if x[5] == 12:
                                item = 'parking meter: '
                                link = 'https://www.amazon.com/s?k=parking+meter&crid=2UT9DCBZ0O800&sprefix=parking+meter%2Caps%2C73&ref=nb_sb_noss_1'
                                
                            if x[5] == 13:
                                item = 'bench: '
                                link = 'https://www.amazon.com/s?k=bench&crid=289TA6TP5B3E2&sprefix=bench%2Caps%2C126&ref=nb_sb_noss_1'
                                
                            if x[5] == 14:
                                item = 'bird: '
                                link = 'https://www.amazon.com/s?k=bird&crid=3CE3WA2PIXZ2L&sprefix=bird%2Caps%2C79&ref=nb_sb_noss_2'
                                
                            if x[5] == 15:
                                item = 'cat: '
                                link = 'https://www.amazon.com/s?k=cat&crid=Y19O1CW1C9JI&sprefix=ca%2Caps%2C315&ref=nb_sb_noss_2'
                                
                            if x[5] == 16:
                                item = 'dog: '
                                link = 'https://www.amazon.com/s?k=dog&crid=WVTLBDKN80DC&sprefix=dog%2Caps%2C90&ref=nb_sb_noss_2'
                                
                            if x[5] == 17:
                                item = 'horse: '
                                link = 'https://www.amazon.com/s?k=horse&crid=J1OLW7XNZ83Y&sprefix=horse%2Caps%2C74&ref=nb_sb_noss_1'
                                
                            if x[5] == 18:
                                item = 'sheep: '
                                link = 'https://www.amazon.com/s?k=sheep&crid=1I30FAU9YA0FO&sprefix=sheep%2Caps%2C76&ref=nb_sb_noss_1'
                                
                            if x[5] == 19:
                                item = 'cow: '
                                link = 'https://www.amazon.com/s?k=cow&crid=1MHKGZH7149QL&sprefix=cow%2Caps%2C73&ref=nb_sb_noss_1'
                                
                            if x[5] == 20:
                                item = 'elephant: '
                                link = 'https://www.amazon.com/s?k=elephant&crid=2JX33XDW7L5OG&sprefix=elephant%2Caps%2C68&ref=nb_sb_noss_1'
                                
                            if x[5] == 21:
                                item = 'bear: '
                                link = 'https://www.amazon.com/s?k=bear&crid=14C4XIANZ7R0H&sprefix=bear%2Caps%2C71&ref=nb_sb_noss_1'
                                
                            if x[5] == 22:
                                item  = 'zebra: '
                                link ='https://www.amazon.com/s?k=zebra&crid=1DFPJW7BP6ZJZ&sprefix=zebra%2Caps%2C71&ref=nb_sb_noss_1'
                                
                            if x[5] == 23:
                                item = 'giraffe: '
                                link ='https://www.amazon.com/s?k=giraffe&crid=P91FLJXQ40TB&sprefix=gir%2Caps%2C88&ref=nb_sb_ss_deep-retrain-ln-ops-acceptance_1_3'
                                
                            if x[5] == 24:
                                item = 'backpack: '
                                link = 'https://www.amazon.com/s?k=backpack&crid=3KKQ7QMX5VYSX&sprefix=backpack%2Caps%2C81&ref=nb_sb_noss_1'
                                
                            if x[5] == 25:
                                item = 'umbrella: '
                                link = 'https://www.amazon.com/s?k=umbrella&crid=24WIBP7L4R03H&sprefix=um%2Caps%2C75&ref=nb_sb_ss_deep-retrain-ln-ops-acceptance_1_2'
                                
                            if x[5] == 26:
                                item = 'handbag: '
                                link = 'https://www.amazon.com/s?k=handbag&crid=3IEXCZYSHJJ7O&sprefix=handbag%2Caps%2C81&ref=nb_sb_noss_1'
                                
                            if x[5] == 27:
                                item = 'tie: '
                                link ='https://www.amazon.com/s?k=tie&crid=2OBQFQO8S6DBQ&sprefix=tie%2Caps%2C81&ref=nb_sb_noss_1'
                                
                            if x[5] == 28:
                                item = 'suitcase: '
                                link = 'https://www.amazon.com/s?k=suitcas&crid=20JSEYXIIE60C&sprefix=suitcas%2Caps%2C127&ref=nb_sb_noss_2'
                                
                            if x[5] == 29:
                                item = 'frisbee: '
                                link = 'https://www.amazon.com/s?k=frisbee&crid=2DLXIM9OOTLMN&sprefix=frisbee%2Caps%2C78&ref=nb_sb_noss_1'
                                
                            if x[5] == 30:
                                item = 'skis: '
                                link = 'https://www.amazon.com/s?k=skis&crid=1O2PLARJGAS3H&sprefix=skis%2Caps%2C87&ref=nb_sb_noss_1'
                                
                            if x[5] == 31:
                                item = 'snowboard: '
                                link = 'https://www.amazon.com/s?k=snowboard&crid=2HVNNXNXX7W9N&sprefix=snowboard%2Caps%2C77&ref=nb_sb_noss_1'
                                
                            if x[5] == 32:
                                item = 'sports ball: '
                                link = 'https://www.amazon.com/s?k=sports+ball&crid=2GN1IUZCKYERZ&sprefix=sports+ball%2Caps%2C75&ref=nb_sb_noss_1'
                                
                            if x[5] == 33:
                                item = 'kite: '
                                link = 'https://www.amazon.com/s?k=kite&crid=2BB2WL82DNEGS&sprefix=kit%2Caps%2C132&ref=nb_sb_noss_2'
                                
                            if x[5] == 34:
                                item = 'baseball bat: '
                                link ='https://www.amazon.com/s?k=baseball+bat&crid=WBBWQ69HR0Z6&sprefix=baseball+bat%2Caps%2C76&ref=nb_sb_noss_1'
                                
                            if x[5] == 35:
                                item = 'baseball glove: '
                                link = 'https://www.amazon.com/s?k=baseball+glove&crid=13ZHP835AXUQ2&sprefix=baseball+glove%2Caps%2C79&ref=nb_sb_noss_1'
                                
                            if x[5] == 36:
                                item = 'skateboard: '
                                link ='https://www.amazon.com/s?k=skateboard&crid=3VDXY44ZWXXMT&sprefix=skateboard%2Caps%2C74&ref=nb_sb_noss_1'
                                
                            if x[5] == 37:
                                item = 'surfboard: '
                                link ='https://www.amazon.com/s?k=surfboard&crid=2QIR1LZ4MD3XC&sprefix=surfboard%2Caps%2C76&ref=nb_sb_noss_1'
                                
                            if x[5] == 38:
                                item = 'tennis racket: '
                                link ='https://www.amazon.com/s?k=tennis+racket&crid=6A3V9LOGQV0D&sprefix=tennis+racket%2Caps%2C77&ref=nb_sb_noss_1'
                                
                            if x[5] == 39:
                                item = 'bottle: '
                                link = 'https://www.amazon.com/s?k=bottle&crid=RGGVARKUFWL3&sprefix=bottle%2Caps%2C74&ref=nb_sb_noss_1'
                                
                            if x[5] == 40:
                                item = 'wine glass: '
                                link = 'https://www.amazon.com/s?k=wineglass&crid=3DAQ0CQ3SNYOJ&sprefix=wineglass%2Caps%2C73&ref=nb_sb_noss_2'
                                
                            if x[5] == 41:
                                item = 'cup: '
                                link = 'https://www.amazon.com/s?k=cup&crid=2GC2ZHSFLOTWE&sprefix=cup%2Caps%2C70&ref=nb_sb_noss_1'
                                
                            if x[5] == 42:
                                item = 'fork: '
                                link = 'https://www.amazon.com/s?k=fork&crid=YGMJVB2UI2N4&sprefix=fork%2Caps%2C73&ref=nb_sb_noss_1'
                                
                            if x[5] == 43:
                                item = 'knife: '
                                link = 'https://www.amazon.com/s?k=knife&crid=NZRKYL5D16U0&sprefix=knif%2Caps%2C68&ref=nb_sb_noss_2'
                                
                            if x[5] == 44:
                                item = 'spoon: '
                                link ='https://www.amazon.com/s?k=spoon&crid=1FZ6F18CBHXZC&sprefix=spoon%2Caps%2C78&ref=nb_sb_noss_1'
                                
                            if x[5] == 45:
                                item = 'bowl: '
                                link = 'https://www.amazon.com/s?k=bowl&crid=EK02SHJ77B98&sprefix=bowl%2Caps%2C95&ref=nb_sb_noss_1'
                                
                            if x[5] == 46:
                                item = 'banana: '
                                link = 'https://www.amazon.com/s?k=banana&crid=1BKG88YLJMC5X&sprefix=banana%2Caps%2C138&ref=nb_sb_noss_1'
                                
                            if x[5] == 47:
                                item = 'apple: '
                                link = 'https://www.amazon.com/s?k=apple&crid=300AEXGVMMK4R&sprefix=app%2Caps%2C101&ref=nb_sb_noss_2'
                                
                            if x[5] == 48:
                                item = 'sandwich: '
                                link ='https://www.amazon.com/s?k=sandwich&crid=3C3ZG5KC0FR33&sprefix=sandwich%2Caps%2C68&ref=nb_sb_noss_1'
                                
                            if x[5] == 49:
                                item = 'orange: '
                                link ='https://www.amazon.com/s?k=orange&crid=2M7ZKNPNRDVHQ&sprefix=orange%2Caps%2C69&ref=nb_sb_noss_1'
                                
                            if x[5] == 50:
                                item = 'broccoli: '
                                link = 'https://www.amazon.com/s?k=broccoli&crid=A0AZKMCJ0TIQ&sprefix=broccoli%2Caps%2C74&ref=nb_sb_noss_1'
                                
                            if x[5] == 51:
                                item = 'carrot: '
                                link = 'https://www.amazon.com/s?k=carrot&crid=VXLLW6SHKE8N&sprefix=carrot%2Caps%2C74&ref=nb_sb_noss_1'
                                
                            if x[5] == 52:
                                item = 'hot dog: '
                                link = 'https://www.amazon.com/s?k=hot+dog&crid=2CGWZMDRZOWIS&sprefix=hot+dog%2Caps%2C76&ref=nb_sb_noss_1'
                                
                            if x[5] == 53:
                                item = 'pizza: '
                                link = 'https://www.amazon.com/s?k=pizza&crid=265S1HUCRNLCO&sprefix=pizza%2Caps%2C74&ref=nb_sb_noss_1'
                                
                            if x[5] == 54:
                                item = 'donut: '
                                link = 'https://www.amazon.com/s?k=donut&crid=PY9LYHNZGY3V&sprefix=donut%2Caps%2C80&ref=nb_sb_noss_1'
                                
                            if x[5] == 55:
                                item = 'cake: '
                                link = 'https://www.amazon.com/s?k=cake&crid=IMCQ0OSX6XAQ&sprefix=cake%2Caps%2C72&ref=nb_sb_noss_1'
                                
                            if x[5] == 56:
                                item = 'chair: '
                                link = 'https://www.amazon.com/s?k=chair&crid=ET2N7H7TOXOJ&sprefix=chair%2Caps%2C69&ref=nb_sb_noss_1'
                                
                            if x[5] == 57:
                                item = 'couch: '
                                link ='https://www.amazon.com/s?k=couch&crid=2UJTC0GFERS53&sprefix=couch%2Caps%2C81&ref=nb_sb_noss_1'
                                
                            if x[5] == 58:
                                item = 'potted plant: '
                                link ='https://www.amazon.com/s?k=potted+plant&crid=3GRI7U1EYR4S5&sprefix=potted+plant%2Caps%2C69&ref=nb_sb_noss_1'
                                
                            if x[5] == 59:
                                item = 'bed: '
                                link ='https://www.amazon.com/s?k=bed&crid=292UTYQ8SJ3XJ&sprefix=bed%2Caps%2C73&ref=nb_sb_noss_1'
                                
                            if x[5] == 60:
                                item = 'dining table: '
                                link ='https://www.amazon.com/s?k=dining+table&crid=24MTTS3QDS9U9&sprefix=dining+table%2Caps%2C160&ref=nb_sb_noss_1'
                                
                            if x[5] == 61:
                                item = 'toilet: '
                                link ='https://www.amazon.com/s?k=toilet&crid=O17TQ894ON4F&sprefix=toilet%2Caps%2C120&ref=nb_sb_noss_1'
                                
                            if x[5] == 62:
                                item = 'tv: '
                                link ='https://www.amazon.com/s?k=tv&ref=nb_sb_noss'
                                
                            if x[5] == 63:
                                item = 'laptop: '
                                link = 'https://www.amazon.com/s?k=laptop&crid=2WP1BWXDV6PV8&sprefix=laptop%2Caps%2C73&ref=nb_sb_noss_1'
                                
                            if x[5] == 64:
                                item = 'mouse: '
                                link = 'https://www.amazon.com/s?k=mouse&crid=1LQTPA6RW0BK&sprefix=mous%2Caps%2C72&ref=nb_sb_noss_2'
                                
                            if x[5] == 65:
                                item = 'remote: '
                                link = 'https://www.amazon.com/s?k=remote&crid=T7GKMEG6DQY&sprefix=remote%2Caps%2C66&ref=nb_sb_noss_1'
                                
                            if x[5] == 66:
                                item = 'keyboard: '
                                link = 'https://www.amazon.com/s?k=keyboard&crid=3VLPLP1LRNJ0O&sprefix=keyboard%2Caps%2C76&ref=nb_sb_noss_1'
                                
                            if x[5] == 67:
                                item = 'cell phone: '
                                link = 'https://www.amazon.com/s?k=cell+phone&crid=3VPPZ15PK1LCM&sprefix=cell+phone%2Caps%2C71&ref=nb_sb_noss_1'
                                
                            if x[5] == 68:
                                item = 'microwave: '
                                link = 'https://www.amazon.com/s?k=microwave&crid=DP7W38YUYCC6&sprefix=microwave%2Caps%2C89&ref=nb_sb_noss_1'
                                
                            if x[5] == 69:
                                item = 'oven: '
                                link ='https://www.amazon.com/s?k=oven&crid=2DHYZNK4LLEXT&sprefix=oven%2Caps%2C79&ref=nb_sb_noss_1'
                                
                            if x[5] == 70:
                                item = 'toaster: '
                                link ='https://www.amazon.com/s?k=toaster&crid=FOV38NV3JF02&sprefix=toaster%2Caps%2C79&ref=nb_sb_noss_1'
                                
                            if x[5] == 71:
                                item = 'sink: '
                                link = 'https://www.amazon.com/s?k=sink&crid=22JXJBMLONG50&sprefix=sink%2Caps%2C81&ref=nb_sb_noss_1'
                                
                            if x[5] == 72:
                                item = 'refrigerator: '
                                link = 'https://www.amazon.com/s?k=refrigerator&crid=2WP2UFJ7HZV99&sprefix=refrigerator%2Caps%2C78&ref=nb_sb_noss_1'
                                
                            if x[5] == 73:
                                item = 'book: '
                                link ='https://www.amazon.com/b?node=283155'
                                
                            if x[5] == 74:
                                item = 'clock: '
                                link = 'https://www.amazon.com/s?k=clock&crid=B64RGUOJ4BMI&sprefix=clock%2Caps%2C82&ref=nb_sb_noss_1'
                                
                            if x[5] == 75:
                                item = 'vase: '
                                link ='https://www.amazon.com/s?k=vase&crid=2K0FQCDUAAQOR&sprefix=vase%2Caps%2C83&ref=nb_sb_noss_1'
                                
                            if x[5] == 76:
                                item = 'scissors: '
                                link ='https://www.amazon.com/s?k=scissors&crid=281TG3AAIKXKU&sprefix=scissors%2Caps%2C75&ref=nb_sb_noss_1'
                                
                            if x[5] == 77:
                                item = 'teddy bear: '
                                link = 'https://www.amazon.com/s?k=teddy+bear&crid=VLYQ44VUFKQ0&sprefix=teddy+bear%2Caps%2C72&ref=nb_sb_noss_1'
                                
                            if x[5] == 78:
                                item = 'hair drier: '
                                link ='https://www.amazon.com/s?k=hair+drier&crid=271RKG9W0FWU7&sprefix=hair+dryer%2Caps%2C73&ref=nb_sb_noss_1'
                                
                            if x[5] == 79:
                                item = 'toothbrush: '
                                link ='https://www.amazon.com/s?k=tooth+brush&crid=79GIB8AJYTQ6&sprefix=tooth%2Caps%2C71&ref=nb_sb_ss_deep-retrain-ln-ops-acceptance_5_5'
                            result_list_link.append(link)
                            result_list_item.append(item)
                            rldisplay.append([cords,link])   

                                
            # print(result_list_item)
            # print(result_list_link)     
            link_list = [*set(result_list_link)]
            item_list = [*set(result_list_item)]
            print(link_list)
            print(item_list)
            

            return render_template('file_upload2.html', file_name=file_name, file_extension=file_extension, link_list=result_list_link, item_list = result_list_item, rl = rl, rldisplay=rldisplay)
    return render_template('index.html', form=form)
        

@app.route('/video', methods=['GET', "POST"])
def video():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
        file_name = (f"static/upload_images/{file.filename}")
        print(file_name)
        file_extension = pathlib.Path(file_name).suffix
        os.system("python3 detect.py")
        path = "runs/detect/exp"
        dir_list = os.listdir(path)      
  
        print("Files and directories in '", path, "' :")
        
        # prints all files

        #for fil in dir_list:
            #file_path_list = (f"/root/yolov5_flask-app/runs/detect/exp/{fil}")
        file_path = [i for i in dir_list]
        print(file_path[0])
        print(file_name)
	    #file_path_list = file_path
	
        shutil.move(path + "/" + file_path[0], file_name)
        return render_template('golfvideo.html', file_name=file_name, file_extension=file_extension, file_path=file_path[0])
    return render_template('index.html', form=form)

@app.route('/bathroom', methods=['GET', "POST"])
def bathroom():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
        file_name = (f"static/upload_images/{file.filename}")
        print(file_name)
        file_extension = pathlib.Path(file_name).suffix
        os.system("python3 bathroom_detect.py")
        path = "runs/detect/exp"
        dir_list = os.listdir(path)      
  
        print("Files and directories in '", path, "' :")
        
        # prints all files

        #for fil in dir_list:
            #file_path_list = (f"/root/yolov5_flask-app/runs/detect/exp/{fil}")
        file_path = [i for i in dir_list]
        print(file_path[0])
        print(file_name)
	    #file_path_list = file_path
	
        shutil.move(path + "/" + file_path[0], file_name)
	    
	
        return render_template('golfvideo.html', file_name=file_name, file_extension=file_extension, file_path=file_path[0])
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
