import os
import cv2
from flask import Flask, render_template, request, redirect, url_for
from ultralytics import YOLO
from PIL import Image
import numpy as np

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
PROCESSED_FOLDER = 'static/processed'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

model = YOLO('best.pt')  # Load your trained YOLO model

# Hasta details dictionary
hasta_details = {
    'ANJALI': {
        'MEANING': 'Salutation',
        'SHLOKA': 'Devataguru Vipranaam\nNamaskaraepyanukramaat\nKaryas shiromukhorastho\nViniyoganjali karaha',
        'HAND_POSITIONING': 'Hold Pataka in both the hands & join the palms to show Anjali Hasta.',
        'USAGE': 'Anjali hasta is used for the salutation to God, Teacher, and the Learned. We hold the anjali hasta above the head for the Gods, in front of the face for the teachers & in front of chest for the learned.'
    },
    'AVAHITTHA': {
        'MEANING': 'Secrecy',
        'SHLOKA': 'Srungara Natanechiva Leelaa\nKanduka dharane Kucharthe\nYujyate Soyamavahitthakaraabhidhaha',
        'HAND_POSITIONING': 'Hold Alapadma in both the hands, cross them at the wrist, place them near chest to show Avahittha hasta.',
        'USAGE': 'Avahittha Hasta is used to show Love, Catching the ball, Breasts.'
    },
    'BERUNDA': {
        'MEANING': 'Twin birds',
        'SHLOKA': 'Berundapakshi Dampatyorbherundhaka Eteeritaha',
        'HAND_POSITIONING': 'Hold Kapitha Hasta & cross them at the wrist to show Berunda Hasta.',
        'USAGE': 'Berunda hasta is used to show a bird couple.'
    },
    'CHAKRA': {
        'MEANING': 'Wheel',
        'SHLOKA': 'Chakrahastassa vigneyachakrarthe viniyujyate',
        'HAND_POSITIONING': 'Hold Ardhachandra hasta in both the hands, place them one above the other like a Plus(+) mark to show Chakra Hasta.',
        'USAGE': 'This Hasta is used to show Chakra, the weapon of Lord Vishnu.'
    },
    'DOLA': {
        'MEANING': 'Neutral hand position',
        'SHLOKA': 'Naatyarambhe Prayoktavyam Iti Natyavidovidhuhu',
        'HAND_POSITIONING': 'Hold Pataka Hasta, stretch the arms & keep the hasta upside down along the hip line to show Dola Hasta.',
        'USAGE': 'This hasta is used in the beginning of a dance.'
    },
    'GARUDA': {
        'MEANING': 'Eagle',
        'SHLOKA': 'Garudo Garudarthe cha Yujyate Baratagame',
        'HAND_POSITIONING': 'Hold Ardhachandra in both the hands, turn them & hold them with the thumbs to show Garuda Hasta.',
        'USAGE': 'This Hasta is used to show a bird called Garuda.'
    },
    'KAPOTA': {
        'MEANING': 'Humility',
        'SHLOKA': 'Pranaamae Gurusambhashae\nVinayangi kritaeshwayam',
        'HAND_POSITIONING': 'In Anjali Hasta, only the borders of the hands are joined (Inside face of the Palm should not touch one another) to show Kapota Hasta.',
        'USAGE': 'Kapota hasta is used to show respectful salutation to the teachers, as a mark of acceptance and to show politeness (vinayam).'
    },
    'KARKATA': {
        'MEANING': 'Group gathering',
        'SHLOKA': 'Samoohaa gamanae Tundadarshanae\nShankhapoorane Angaanaam Motane\nShaakhonnamaanecha Niyujyate',
        'HAND_POSITIONING': 'Bring the fingers of both the hands between one another to show Karkata Hasta.',
        'USAGE': 'Karkata hasta is used to show the arrival of a crowd, showing the belly, blowing the shanku (conch), twisting and stretching the limbs, and bending branch of a tree.'
    },
    'KARTARISWASTIKA': {
        'MEANING': 'Branches, trees',
        'SHLOKA': 'Shakhaasucha Adri Shikhare\nVruksheshucha Niyujyate',
        'HAND_POSITIONING': 'Hold Kartareemukha Hasta in both the hands & cross the hands at the wrist to show Kartareeswastika Hasta.',
        'USAGE': 'To show the branches of a tree, tip of Mountains, Trees this hasta is used.'
    },
    'KATAKAVARDHANA': {
        'MEANING': 'Bond, agreement',
        'SHLOKA': 'Pattabhishaekae Poojayam Vivahadishu Yujyate',
        'HAND_POSITIONING': 'Hold Katakamukha Hasta in both hands, cross the hands at the wrist to show Katakavardhana Hasta.',
        'USAGE': 'To show Coronation, to worship and to show weddings this hasta is used.'
    },
    'KEELAKA': {
        'MEANING': 'Affection, love',
        'SHLOKA': 'Snehecha Narmalaapecha\nViniyogosya Sammataha',
        'HAND_POSITIONING': 'Hold Mrugasheersha Hasta in both hands, bend the little finger a little & join these fingers like a chain to show Keelaka Hasta.',
        'USAGE': 'To show friendly talk this hasta is used.'
    },
    'KHATWA': {
        'MEANING': 'Cot, bed',
        'SHLOKA': 'Khatva Hasta\nKhatvahastobhavedeshaha\nKhatvaadishu Niyujyate',
        'HAND_POSITIONING': 'Hold Chatura Hasta in both hands, place the hands one above the other, stretch the index fingers down to show Khatwa Hasta.',
        'USAGE': 'Khatwa hasta is used to show Bed.'
    },
    'KURMA': {
        'MEANING': 'Turtle',
        'SHLOKA': 'Koormahastasyavigneyaha\nKoormarthe Viniyujyate',
        'HAND_POSITIONING': 'Opposite of Chakra Hasta is Kurma Hasta i.e Stretch the thumb & little fingers & fold the other fingers in Chakra Hasta to show Kurma Hasta.',
        'USAGE': 'This Hasta is used to show Turtle, Tortoise.'
    },
    'MATHSYA': {
        'MEANING': 'Fish',
        'SHLOKA': 'Etasya Viniyogastu\nMatsyarthe Sammatobhavet',
        'HAND_POSITIONING': 'Hold Pataka hasta in both the hands, place them one above the other, stretch the thumb a bit (like fins of fish) to show Mathsya Hasta.',
        'USAGE': 'This hasta is used to show Fish.'
    },
    'NAGABANDHA': {
        'MEANING': 'Snakes entwined',
        'SHLOKA': 'Bhujagadampatee Bhaave\nNikunchanaamcha darshane\nAthrvanasya mantreshu\nYojyo Bharatakovidhihi',
        'HAND_POSITIONING': 'Hold Sarpasheersha in both the hands & cross them at the wrist to show Nagabandha Hasta.',
        'USAGE': 'This hasta is used to show Snakes, Creeper, Chamber and Atharva Veda Shlokas.'
    },
    'PAASHA': {
        'MEANING': 'Bondage, conflict',
        'SHLOKA': 'Anyonyakalahe Paashe\nShynkhalaayaam Niyujyate',
        'HAND_POSITIONING': 'Hold Suchi Hasta in both hands, bend the index finger a little & join these fingers like a chain to show Paasha Hasta.',
        'USAGE': 'To show Playful Quarrel, Rope, Chains this hasta is used.'
    },
    'PUSHPAPUTA': {
        'MEANING': 'Holding flowers',
        'SHLOKA': 'Neeraajenavidhou baala\nvaari Phaladikrehanaepicha\nSandhyayaam marghyadaanecha\nMantrapushpecha yujyathae',
        'HAND_POSITIONING': 'Hold Sarpasheersha in both the hands & join them at the wrist to show Pushpaputa Hasta.',
        'USAGE': 'Pushpaputa hasta is used to show Lamp Offering, Children, Accept Fruits, Offering to the Sun in the evenings, and Chant Holy prayers.'
    },
    'SAMPUTA': {
        'MEANING': 'Concealment',
        'SHLOKA': 'Vastvaacchchade Samputecha\nSamputahkara Eeritaha',
        'HAND_POSITIONING': 'Hold Pataka Hasta, bent the palm a little in both the hands and place one above the other such that inside of the palm face each other to show Samputa Hasta.',
        'USAGE': 'To cover things and to show the sacred box in which the idols are placed this Samputa Hasta is used.'
    },
    'SHAKATA': {
        'MEANING': 'Demon',
        'SHLOKA': 'Raakshasaabhinayechaayam\nNiyukto Bharatadibhihi',
        'HAND_POSITIONING': 'Leave the thumb & the middle fingers in Bhramara Hasta. Hold like this in both the hands & cross at the wrist to show Shakata Hasta. Another way of showing Shakata Hasta is to cross the Arala Hastas at the wrist.',
        'USAGE': 'This hasta is used to show Demons.'
    },
    'SHIVALINGA': {
        'MEANING': 'Representation of Shiva',
        'SHLOKA': 'Viniyogastu tatsyva Shivalingasya darshanae',
        'HAND_POSITIONING': 'Hold Ardhachandra Hasta in the left hand (palm up), keep shikhara Hasta in right hand & place it on the left hand to show Shivalinga Hasta.',
        'USAGE': 'This Hasta is used to show Shivalinga (Lord Shiva).'
    },
    'SHANKHA': {
        'MEANING': 'Conch shell',
        'SHLOKA': 'Shankhaadishuniyujyoya\nMityevam Bharataadayaha',
        'HAND_POSITIONING': 'Hold the Left thumb with the last three fingers of the right hand, stretch the other fingers of the left hand, stretch & touch the thumb & index fingers of the right hand with the stretched fingers of the left hand to show Shankha Hasta.',
        'USAGE': 'This hasta is used to show Shanku (Conch).'
    },
    'SWASTIKA': {
        'MEANING': 'Denotes crossing',
        'SHLOKA': 'Samyogena Swastikakhyo Makarae viniyujyate\nBhayavade Vivadecha Keertane Swastikobhavet',
        'HAND_POSITIONING': 'Hold Pataka Hands & cross the hands at the wrist so that the hands are opposite to each other to show Swastika Hasta.',
        'USAGE': 'Swastika hasta is used to show Alligator (a crocodilian), talking with fear, to show an argument and to praise.'
    },
    'UTHSUNGA': {
        'MEANING': 'Modesty',
        'SHLOKA': 'Aalinganaecha lajjayaam\nAngadaadipradarshanae\nBaalanaamshikshanechayaam\nUtsango yujyatae karaha',
        'HAND_POSITIONING': 'Hold Mrugasheersha Hasta in both the hands, cross the hands, touch opposite shoulders to show Utsunga Hasta.',
        'USAGE': 'Utsunga hasta is used to show embracing someone, shyness, show one’s body, and to show teaching discipline to children.'
    },
    'VARAHA': {
        'MEANING': 'Boar',
        'SHLOKA': 'Etasyaviniyogastu Varaharthe tu Yujyate',
        'HAND_POSITIONING': 'Hold Mrugasheersha hasta in both hands,place the other hand on top of it to show Varaha Hasta.',
        'USAGE': 'Varaha Hasta is used to show a boar.'
    }
}

def draw_yolo_output(img_path, results):
    image = cv2.imread(img_path)
    for result in results:
        boxes = result.boxes
        for box in boxes:
            cls_id = int(box.cls[0])
            label = result.names[cls_id]
            conf = box.conf[0]
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, f"{label} {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (36, 255, 12), 2)
    return image

def apply_clahe(image_path):
    image = cv2.imread(image_path)
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))
    final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    return final

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)

        if file:
            filename = file.filename
            original_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(original_path)

            # Apply CLAHE
            clahe_img = apply_clahe(original_path)
            clahe_path = os.path.join(PROCESSED_FOLDER, 'clahe_' + filename)
            cv2.imwrite(clahe_path, clahe_img)

            # YOLO Detection
            results = model(clahe_img)
            output_img = draw_yolo_output(original_path, results)
            output_path = os.path.join(PROCESSED_FOLDER, 'yolo_' + filename)
            cv2.imwrite(output_path, output_img)

            # Get detected Hasta details
            detected_hastas = set()
            for result in results:
                for box in result.boxes:
                    class_id = int(box.cls[0])
                    hasta_name = result.names[class_id].upper()
                    if hasta_name in hasta_details:
                        detected_hastas.add(hasta_name)

            hasta_info = {hasta: hasta_details[hasta] for hasta in detected_hastas}

            return render_template('result.html',
                                   original=url_for('static', filename='uploads/' + filename),
                                   clahe=url_for('static', filename='processed/clahe_' + filename),
                                   output=url_for('static', filename='processed/yolo_' + filename),
                                   hasta_info=hasta_info)

    return render_template('index.html')


if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(PROCESSED_FOLDER, exist_ok=True)
    app.run(debug=True)
