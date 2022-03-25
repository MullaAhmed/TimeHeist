# app.py
from distutils.log import error
from flask import *
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import exists
import re

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///registration.db"
db = SQLAlchemy(app)


class UserRegister(db.Model):
    name = db.Column(db.String, nullable=False)
    user_email = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    user_password = db.Column(db.String, nullable=False)
    

    def __init__(self, name, email, password):
        self.name = name
        self.user_email = email
        self.user_password = password


def check_none():
    temp_attempt = request.cookies.get("Attempt")
    if temp_attempt == None:
        temp_attempt = 0

    elif temp_attempt != None:
        temp_attempt = int(temp_attempt)

    return temp_attempt


def question(option, answer, que_page, to_page):

    if option == answer:
        attempt = 0
        resp = make_response(redirect(to_page))
        resp.set_cookie("Attempt", json.dumps(attempt))
        resp.set_cookie("Link", json.dumps(to_page))

        return resp

    else:
        attempt = request.cookies.get("Attempt")
        if attempt != None:
            attempt = int(attempt)
            resp = make_response(render_template(que_page))
            resp.set_cookie("Attempt", json.dumps(attempt))
            resp.set_cookie("Link", json.dumps(que_page))
            return resp

        elif attempt == None:
            attempt = 1
            resp = make_response(render_template(que_page))
            resp.set_cookie("Attempt", json.dumps(attempt))
            resp.set_cookie("Link", json.dumps(que_page))
            return resp


# Pages


@app.route("/", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        name = name.lower()
        email = request.form["email"]
        email = email.lower()
        password = request.form["password"]
        password = password.lower()
        regex_email = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
        if (
            not re.search(regex_email, email)
            # or not re.search(regex_password, password)
            # or not re.search(regex_name, name)
        ):
            return render_template(
                "register.html", message="Invalid email or password or name"
            )
        exists = (
            db.session.query(UserRegister.user_email)
            .filter_by(user_email=email)
            .first()
            is not None
        )
        if not exists:
            user = UserRegister(name=name, email=email, password=password)
            db.session.add(user)
            db.session.commit()
        else:
            return render_template("register.html", message="Email already exists")
        return redirect("/main")

    return render_template("register.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    try:
        if request.method == "POST":
            email = request.form["email"]
            email = email.lower()
            password = request.form["password"]
            password = password.lower()
            exists = (
                db.session.query(UserRegister.user_email)
                .filter_by(user_email=email)
                .first()
                is not None
            )
            if exists:
                user = UserRegister.query.filter_by(user_email=email).first()
                print(user)
                if user.user_email == email and user.user_password == password:
                    return redirect("/main")
            else:
                return redirect("/")
    except:
        return render_template("login.html")

    return render_template("login.html")


@app.route("/main", methods=["POST", "GET"])
def main():
    return render_template("main.html")


@app.route("/rules", methods=["POST", "GET"])
def rules():
    rule_link = "https://drive.google.com/file/d/1-FYyO2BVAaioXFOo15CaX-dW3-QGPHVU/view?usp=drivesdk"
    return render_template("rules.html",rule_link=rule_link)


@app.route("/thanks", methods=["POST", "GET"])
def thanks():
    return render_template("thanks.html")


@app.route("/level/<int:level>/question/<int:Number>", methods=["POST"])
def redirects(level, Number):
    if request.method == "POST":
        option = request.form["answer"]
        option=str(option).lower()
        answer_dict = {
            1: {1: ["momentum"], 2: ["momentum"], 3: ["1","one"], 4: ["0","zero"]},
            2: {1: ["10301"], 2: ["vision told this in conference","vision"], 3: ["3125"], 4: ["Doctor Strange","Dr. Strange","doctor strange"], 5: ["101000"]},
            3: {1: ["control pad"], 2: ["control board"], 3: ["microcontroller"], 4: ["integrated development enviroment"],5: ["compile"], 6: ["loop"]},
            4: {1:["captain america","steve rogers"],2:["the stork club"],3:["bucky barnes"],4:["hydra"],5:["scepter"],6:["vision"],7:["scarlet witch","wanda maximoff"],8:["pietro maximoff"],9:["sokovia"],10:["friday"],11:["11"],12:["kamar taj"],13:["14000605"],14:["avengers assemble"],15:["3000"]},
            5: {1:["130"],2: ["One rotation by 10° & 13 rotations by 130°"], 3: ["same as mirror"], 4: ["refractive index"],5:["heroes"]},
        }
        question_dict = {
            1:4,
            2:5,
            3:6,
            4:15,
            5:3
        }
        print(option, answer_dict[level][Number])
        if option in answer_dict[level][Number]:
            if question_dict[level] > Number:
                Number += 1
            elif Number == question_dict[level]:
                level += 1
                Number = 1
            return redirect(f"/level/{level}/question/{Number}")
        else:
            return redirect(f"/level/{level}/question/{Number}")

@app.route("/level/<int:level>/question/<int:Number>", methods=["GET"])
def answers(level, Number):

    points_dict = {
        1: {1: "0", 2: "1", 3: "2", 4: "3"},
        2: {1: "4", 2: "5", 3: "6", 4: "7", 5: "8"},
        3: {1: "9", 2: "10", 3: "11", 4: "12",5: "13", 6: "14"},
        4: {1:"15",2:"16",3:"17",4:"18",5:"19",6:"20",7:"21",8:"22",9:"23",10:"24",11:"25",12:"26",13:"27",14:"28",15:"29"},
        5: {1: "30", 2: "31", 3: "32"},
    }
    image_dict= {
        # https://drive.google.com/file/d/1BLzgtSKLbqDDT-7qkV2u0lv72a7DGeZR/view?usp=sharing
        1: { 3: "https://drive.google.com/uc?export=view&id=1iOntsdnYmZoVbi1RHq2XfZiBdSfUYcmJ"},
        2: {1: "https://drive.google.com/uc?export=view&id=1qCyXkVx58bSYPTuFSj_vfGenC0-7IFzC", 
            2: "https://drive.google.com/uc?export=view&id=18hDjNzg6MzHyjIhyGlKka3xAK0DCjn17", 
            3: "https://drive.google.com/uc?export=view&id=1WqX4I17WcwkBC3lZZZ5rryN78AKonAUJ", 
            4: "https://drive.google.com/uc?export=view&id=1V7Z2LhZOpjwoG61L3YST8bKPmcgYi91a", 
            5: "https://drive.google.com/uc?export=view&id=1Xrk5OcOGA5HVi4OBtj6R4u0wSGjGCRRk"},
        3: {1: "https://drive.google.com/uc?export=view&id=1iec0XfuRt0Kw0t5vGEDeWp5L07Ta5XL2", 
            2: "https://drive.google.com/uc?export=view&id=100h3dLLxEXOotogtMZKaPANAh25uQ8nt"},
        5: {1: "https://drive.google.com/uc?export=view&id=1BLzgtSKLbqDDT-7qkV2u0lv72a7DGeZR"},
    }

    question_dict = {
        1: {
            1: [
                "Introduction: iron man, hulk, spiderman and Antman are on their way to retrieve space stone from hydra. They have divided themselves into two teams which are respectively iron man and hulk and spiderman and Antman.",
                "Spider man and Antman reached a path where they saw the Heli carriers in the air.",
                "Spider man: “What are those?”",
                "Antman: “They are the vehicles that hydra used was insight Heli carriers. They were designed to be capable of sustained, independently powered flight via massive turbines engines that provided the lift to keep them in air. Tony stark upgraded them so that they relied on repulsor technology rather than turbines, allowing them to stay in air indefinity.",
                "Spider: “this means the repulsors converts electrical power into ____ and also can be used as a weapon.",
            ],
            2: [
                "Simultaneously at another planet:",
                "Thor is currently convincing Odin to give him the reality stone.",
                "Odin: “Son, you do know the implications of wielding the stone and using it.",
                "Odin: “The Reality stone enables whoever wields it to change our Earth to another in the multiverse and is thus the manifestation of the quantum nature the physical universe. there are an infinite number of parallel universes, and that the probability of a particular quantum event is reflected in the alternate histories and futures of these parallel universes. Many of these parallel Earths are very similar to our own (with perhaps a few notable differences) while others may vary greatly from our world.",
                "Jane foster: “This means that the basic equations of quantum physics instruct us how to calculate the probability that an electron in an atom will be found at a given position or with a particular _____ but not exactly where it is or how fast it is moving. Quantum Mechanics, the field of physics that describes the properties of atoms and how they interact with light, is itself a subject of probabilities.",
            ],
            3: [
                "Back to earth, where ironman and hulk are fighting with hydra:",
                "While fighting, a powerful blow strikes down ironman.",
                "Friday: “sir, the suit is malfunctioning. It can be fixed only physically.”",
                "Tony Stark: “What’s the problem?”",
                "Friday: “The circuit connecting the arc is malfunctioning! There is a disturbance in the potential difference of the circuit.”",
                "Tony stark: “Assuming point A is to be at zero potential, Lets use Kirchhoff’s rules to determine the potential at point B!”",
                "Spiderman from behind: “Mr. Stark, it seems easy. You do know that we are taught about this in Highschool?”",
                "Tony Stark: “Who else knows? Anybody?” “Nobody.” “Not even your unusually attractive aunt?”",
                "Spiderman: ……",
                "Friday: “Sir, there is no time to dawdle!”",
            ],
            4: [
                "Friday: “Sir we have only fixed the circuit, we are yet to fix the solenoid in the suit!",
                "Friday: “There is a solenoid of length 1.0 m has a radius of 1 cm and has a total of 1000 turns wound on it. It carries a current of 5 A.”",
                "Tony Stark: “Then we must calculate the magnitude of the axial magnetic field inside the solenoid. If an electron was to move with a speed of 104 m/s along the axis of this current carrying solenoid, what would be the force experienced by this electron?”",
            ],
        },
        2: {
            1: [
                "*We welcome you to the timeline where Loki invades earth and the war between the Avengers and Loki takes place*",
                "The avengers defeat Loki’s army and takes hold of his scepter. Later they discover that the scepter contains the Mind Stone. Tony Stark, aka Iron Man, starts to study the Mind Stone and a series of thoughts occur to him.",
                "He starts questioning the universe and the creatures that exist in it. To prevent further incidents that would endanger earth from the aliens, he makes an AI Defense Mechanism which will form a barrier around the earth using the prowess of the mind stone.",
                "But the dilemma occurs as his knowledge is limited to the current era of earth and requires the help of you guys in creating it.",
                "The scepter is found to be enclosed in a protective shield which requires a five-digit password to disarm the shield. Help tony stark in cracking up this problem:",
                "* The five-digit password is in the result of the below mentioned pseudo code: - *",
                
            ],
            2: [
                "Well Done!",
                "Tony stark gets the access of the scepter which helps him proceed his plan to make an AI defense mechanism, which will later be known as ‘Ultron’.",
                "But but but Ultron turns out to be a good guy and not evil.",
                "Ultron is now helping Tony create VISION using Jarvis as the soul. While integrating the mind stone to vision, a problem occurs. Help them in successfully creating vision by cracking this code: -",
            ],
            3: [
                "Time flies and events occurs which leads to thanos invading earth.",
                "Ultron gets damaged by thanos trying to prevent him from invading earth.",
                "Now after knowing that thanos has arrived and wants the mind stone, avengers decide to ask for Shuri’s help to remove the mind stone in such a way that vision will still live.",
                "Shuri requires the access of Ultron’s knowledge as he knows more about vision than anyone else, but as Ultron was damaged the system wouldn’t open unless the right code was entered.",
                "Help the avengers to crack the code to make it possible to save vision:",
            ],
            4: [
                " Bravo!! Shuri successfully gets access to Ultron’s vast knowledge and makes it possible to remove the mind stone from vision safely and securely",
                "Now it’s time to get hold of the time stone.",
                "After solving the vision crisis, the avengers go to Dr. Strange to take the Time Stone from him for safekeeping until Tony Stark creates the Nano Gauntlet.",
                "Doctor Strange opens The Eyes of Agamotto using the time stone and sees the possible futures. Out of all of them only one future depicts that the avengers can defeat thanos and survive successfully.",
                "To test whether this future is the one with hope, he gives the avengers a riddle.",
                "Only if they crack the code will he give them the time stone.",
                "Help the avengers in cracking the code successfully to receive the time stone.",
            ],
            5: [
                "Amazing!! They cracked the code and received the time stone without any problems.",
                "But they weren’t aware that Dr. Strange had hidden another question casted in the form of a spell that sealed The Eye of Agamotto. If only they crack the code, the Eye will open revealing the Stone in it.",
                "Help the avengers in solving the riddle.",
                "The riddle consists of a pseudo code which has the pass code. Can you guess what that pass code is?",
            ],
        },
        3: {
            1: [
                "In the mean time while the avengers were recovering the mind stone and time stone, the guardians of the galaxy are in the progress of protecting the Power stone.",
                "Thanos has noticed their movements and his minions are after them to prevent them from escaping his grasp and unite with the other avengers.",
                "The Guardians of the galaxy’s spaceship “Milano” has been damaged by the collectors sent by thanos.",
                "While their ship was being repaired rocket and peter quill have their usual banter but this time a bit technical.",
                "The quarrel starts with peter ridiculing rockets knowledge.",
                "Peter: “Lets have a competition, who fixes the ship first!”",
                "Rocket: “You maniac! The whole ship is gonna blow, you got issues quill!”",
                "*Peter fixes the front of the ship*",
                "Peter: To open the dashboard, one part of the Arduino based component is missing. Find out which part is not mentioned in the below figure:",
            ],
            2: [
                "*Simultaneously Rocket’s fixing the rear of the ship*",
                "Rocket: There are two different boards on the Robot: The Control Board (top) and the Motor Board (bottom). If you're just getting started with electronics and programming, you should work with the",
            ],
            3: [
                "Rocket to peter: “Are you going to finish or should we abort the ship, cause I can lose one friend today but not my life” BWHAHAHAHAHAHA",
                "Peter replies cheekily: ‘Ain’t nothing like me 'cept me!!’",
                "Rocket: “Blah, Blah, Blah. We're All Very Fascinated, Whitey.”",
                "Rocket: “We have to repair other parts too, time’s ticking.”",
                "Peter: After writing the Arduino Code in the IDE, where should it be uploaded which eventually executes the code, interacting with the input and output such as sensor, motors, and lights.",
            ],
            4: ["Rocket: “Whitey, do you know what IDE stands for?”"],
            5: [
                "Peter: “Who do you think you’re challenging? Your turn!”",
                "Peter: “Before your program “code” can be sent to the board, it needs to be converted into instructions that the board understands. This process is called _______.”",
            ],
            6: [
                "Rocket: “HAHAHAHA, guess who is right again? As we are already talking about codes:”",
                "Q6 Rocket: “Which command is called repetitively over and over again as long as the Arduino has power.”",
            ],
        },
        4: {
            1: [
                "Now our heroes have received all the infinity stone except one. The SOUL stone. So, Natasha and Hawkeye have travelled to the past to get the stone from Vormir.",
                "But there they meet red skull who tells them the whole thing about how to get the soul stone by sacrificing a precious life. But none of them is ready to do it, even all the avengers deny the idea.",
                "Will you sacrifice your life for helping Avengers and the whole Universe?",
                "No, no, no don't think about that because there’s a twist in that story. Red Skull has been hiding the truth this whole time. There isn't only one way possible.",
                "There is another way through which you can get the SOUL stone. Red skull never told anyone the other solution because he never thought that anyone was worthy enough.",
                "The latter method is harder than the former because it requires a person, not to sacrifice a soul, but a mind instead. Even a person with IQ 1000 wouldn't be a perfect fit.",
                "But you, you have been chosen to help the Avengers and save the world.",
                "Now you have to travel all the way to Brooklyn where an avenger A was born. This is the same avenger who was thought to be dead, but he/she isn't. Who’s the Avenger A?",
            ],
            2: [
                "A lost love of his/her life to time. A finds a way to travel to the past to a place B where A and his/her lover were supposed to meet. What’s the name of the place B?"
            ],
            3: [
                "A has many friends but his/her best friend is a person C, who A used to work with but later they were both separated in a train incident and C was believed to be dead. Who’s C in the above context?"
            ],
            4: [
                "Later it was found that C is alive but lost something precious to life and got an artificially replaced by a powerful and dangerous organization D whose motto is, “If a head is cut off, two more shall take its place.”"
            ],
            5: [
                "This organization D was successful in getting their hands on a powerful weapon E from between a war, but was later acquired by a well-known group of people."
            ],
            6: [
                "This weapon E was used to create a strong and powerful personality F."
            ],
            7: [
                "Later F fell in love with G. G possesses abilities to alter reality in unspecified ways and is a powerful sorceress."
            ],
            8: [
                "G has a brother H and most people know H by his superhero name. What’s the real name of H?"
            ],
            9: [
                "Both G and H are originally from a place I. Can you guess where I is?"
            ],
            10: [
                "Now that you have solve the first mystery, let’s check your knowledge about the man behind all the WHAT IF theories, DR. STRANGE.",
                "Dr. Stephen Strange was a neurosurgeon. But on a particular day, he met with an intense accident. This was a planned accident by one of his nurse named Billy.",
                "From this day everything shifted in MCU because it changed the life of Strange himself and many others. ",
                "The date was May 6th, 2012. Can you guess which day it was? ",
                "[Hint2: Use today’s day!]",
            ],
            11: [
                "Strange thought his whole life was gone due to this accident because he wouldn’t be able to practice neurosurgeries after this.",
                "He had a major surgery on his hands where a number of stainless steels pins were fitted in his bones. He doesn’t know about that yet.",
                "Strange wants to know the number of steel pins in his hands but his Christine is afraid to tell him so she tells him in a form of riddle.",
                "Find the answer however you may, but help Christine Palmer, Strange’s girlfriend, in telling strange about his surgery.",
            ],
            12: [
                "7+4, 11+16, 27+64, 91+256",
                "“What!” Yes that was his reaction after knowing about the surgery.",
                "After this tragedy, Strange was lost. He didn’t know what to do, where to go, how to live a life!",
                "He was searching for a man who would have gone through the same situation to help him.",
                "Then he found Jonathan Pangborn, the man to learned to walk again after a similar tragedy occurred with him.",
                "So he talked with him and got to know about the place where Jonathan got the therapy. Its location is kept secrecy so that only the desired can find it.",
                "He was desperate to find the place, but given his situation, he wasn’t able to. Would you help him find that place?",
                "I Y K Y P    R Y H   L C N Y J",
                "                      ↓       ",
                "_ _ _ _ _     _ _ _    N E P A L",
            ],
            13: [
                "Strange didn’t knew his life wasn’t going to be the same as before, after reaching there.",
                "He got so much more than the therapy he needed. It’s like he got his life back, but only to save other’s.",
                "After that he has saved as many lives as one could possible imagine.",
                "But there was this one time where he couldn’t save everyone from dying. It was during the fight with Thanos for stopping him from wiping out half the universe. It wasn’t Strange’s fault.",
                "He tried to see to possible future outcomes of beating Thanos.",
                "Of many possibilities in the alternate future, he only found one, where they could win.",
                "But he didn’t tell anyone how many possibilities were there. Can you find it out?",
                "9/J, 6/G, 20/U, ?/B, 26/A                                      ? : 1",
                " ?,  10,  28,  82,  244                                        ? : 4",
                "?, 001, 010, 011, 100, 101, 110, 111                           ? : 000",
                "3, ?, 11, 20, 37, 70                                           ? : 6",
                "-8, -4, -2, -1, ?, 1, 2, 4, 8                                  ? : 0",
                "1, ?, 11, 19, 29, 41                                           ? : 5",
            ],
            14: [
                "Great! You know Dr. Strange very closely. Then you also know that it’s TIME. It’s time to end this once and for all.",
                "It’s to collect the last but not the least important infinity stone, SOUL stone. But before that, one last task.",
                "We need to remind everyone who we are, what we stand for and what we can do.",
                "If in Norse language FSWXSR is written as BOSTON. Then in that language the word EZIRKIVW EWWIQFPI can be written as?",
            ],
            15: [
                "Congrats for decoding, CAPTAIN! Now we have to find the code number which is so close to every MCU fan.",
                "For that, you need to find the mean of all the numbers corresponding to the alphabet in the previous answer.",
                "Round off the mean to the nearest integer, then multiply it by 1500 and divide it by 5.",
            ],
        },
        5: {
            1: [
                "All the stones are acquired and Bruce is given the nano gauntlet made by Tony.",
                "As they are putting the stones on Thanos opens a space crack and stops them from putting on the last stone.",
                "Bruce was unable to move his fingers to snap. None of them expected such a blast full entry.",
                "They were terrified, but weren’t ready to give up. Captain lost all his hope at the end, but he was ready to fight till his last breath.",
                "Then suddenly all the Avengers walk out of a portal and everyone is ready to fight Thanos and are waiting for Captain’s final words before the war, “AVENGERS ASSEMBLE”.",
                "A fight breaks apart with Thanos and avengers try their best to defeat him. The biggest obstacle in their way was Thanos’ ship. The ship had caused a huge damage.",
                "Avengers tried their best to destroy the ship but couldn’t. The ship of Thanos causes huge damage and the Avengers lose all the hope. But at that time, Captain Marvel makes a blast full entry and destroys the whole ship with all her powers.",
                "Meanwhile when everyone’s eyes are on Captain Marvel Thanos takes a chance and acquires all the stones from them.",
                "The fight continues, Thanos is currently in battle with the avengers. Thor starts to fight with Thanos and manages to strike off the time stone.",
                "Meanwhile taking the advantage of the situation, Spiderman shoots a web and swings the stone directly to Dr. strange without touching the stone.",
                "Now Dr. Strange decides to destroy thanos completely and thinks of the idea which he used to defeat DORMAMU. He decided to loop Thanos and his army in a time loop in Mirror dimension.",
                "Dr. Strange tries opens the EYE OF AGAMOTTO as it is the only way to make a time loop. But in the mirror dimensions he couldn’t figure out how to open it.",
                "So, he needs your help to figure out the geometry and rotations to open the eye of Agamotto.",
                "Since they entered the mirror dimension, to work with the eye of agamotto, Strange needs to imagine its mirror image. Help Strange and find the mirror image of the Eye of Agamotto. Take the mirror image about the axis located at your right-hand side.",
                "Rotate the thus obtained image clockwise by degrees that the hour hand and the minute hand will make at 3:40.",
            ],
            2: [
                "Angle traced by hour hand in 12 hours = 360°",
                "Angle traced by hour hand in 3hrs 40 mins, i.e., 11/3 hours = {11/3 x 360/12} = 110°",
                "Angle traced by minute hand in 60min = 360°",
                "Angle traced by minute hand in 40 mins ={40 x 360 / 60} = 240°",
                "Difference = (240-110) =130°",
                "Now rotate the thus obtained halfway opened Eye of Agamotto 13 times in the anti-clockwise direction with degree made by minute or hour hand when both are exactly aligned after 4PM.",
                "(Take the approx. values)",
            ],
            3: [
                "13 rotations by 130°",
                "Let the time when both align be 4 hours x minutes.",
                "Angle traced by hour hand in 12 hours = 360°",
                "Angle traced by hour hand in 4hrs x mins, i.e., (240+x)/60 hours =",
                "{(240+x)/60 x 360/12} = 120° + x/2",
                "Angle traced by minute hand in 60min = 360°",
                "Angle traced by minute hand in x mins =",
                "{x x 360 / 60} = 6x",
                "Now 120° + x/2 = 6x",
                "11x = 240°",
                "x = 21.8 mins",
                "x ~= 20 mins",
                "Same as above. Angle b/w hour and minute hand at 4:20.",
            ],
            4:[
                'Bravo!! The Eye of Agamotto is now opened and Dr. Strange makes a time loop to trap Thanos in mirror dimension.', 
                'Thanos is put in the mirror dimension. But Thanos has the power of other stones so he escapes the time loop with the help of their powers.',
'Thor tries to stop Thanos from escaping and tries to get his hammer back. But Thanos in between catches it.', 
'This makes Thor shocked and makes him stand still in front of Thanos. Thanos taking advantage of the situation hits Thor with his hammer.',
'But suddenly Captain America arrives and saves Thor with his shield. Thanos gets surprised that how can a shield absorb such a massive attack.',
'There present Hawkeye and Natasha smirks and tell him that this is because of vibranium!',
'The shield is made of an alloy of steel and vibranium. The steel is to provide strength and rigidity so that when Captain America throws his mighty shield, it will ricochet,', 
'and the vibranium because it absorbs all vibrations, making it the perfect shock absorber, as seen in the scene where it absorbs Thor\'s hammer blow.',
'Energy can\'t be destroyed. It can only be converted to another form. The energy of the hammer strike is converted into sound waves in the hammer, and if the vibranium absorbs it,', 
'it\'s converted into blue light, ultraviolet light, this enormous flash of light that\'s given off. It\'s showing that the vibranium is actually a perfect sonoluminescent material.',
'"Sono" meaning sound, "luminescent" meaning light. You send sound waves in, and you get light out.',
'There is only a very narrow frequency range where sound and light waves overlap around 100 GHz to 10 THz. During this period, the',
'sound waves cause the air to compress and decompress which will affect the ______ of light going through the air perturbed by a sound wave.'

            ],
            5:[
                'Well, it’s great that you have a good knowledge of sound and light!',
'Dr. Strange hints Tony that this is the one possibility that he saw where they could win. Tony sees an opportunity in the confusion and transfers the stones to his nano gauntlet.', 
'So, Tony shows that he is trying to grab the gauntlet off of Thanos, but instead grabs all the stones and place them in his nano-tech gauntlet. “And I… am… Iron Man”. *Snaps* ',
'But nothing happens. Everyone gets confuse and look at each other as if they want to ask each other that \'Why didn\'t it work?!\'. ',
'Thanos on the other hand tries to get out of the mirror dimension. ',
'Dr. Strange knows that Tony Stark would die after he snaps. He still thinks about a way so that he can save Tony’s life.', 
'As every action has an equal opposite reaction, the consequences of using the power of the stones is that something is taken from the one who used them.', 
'Tony being a mortal was ready to use the stones to kill the whole army and face the consequence of losing all his lifespan and dying.', 
'So, Dr. Strange decides to seal Thanos in mirror dimension forever. For this Bruce comes forward and gets ready to bear the consequences of the same.',
'Bruce then snaps his fingers to seal the mirror dimension forever which does not affect the reality much. Hence the consequences he receives is losing the power to ever become Hulk.', 
'Thus, Thanos gets trapped in the mirror dimension forever and without anyone sacrificing their life!',
'With a happy ending Nick Fury summons all the avengers and throws a party where he cheers to their win and tells that,',
'“I still believe in ________. And you guys proved it!”',

            ]
        },
    }
    try:
        return render_template(
                "Part1/P1_Q1.html",
                points=points_dict[level][Number],
                Level=level,
                stone=level - 1,
                question=question_dict[level][Number],
                Number=Number,
                images=image_dict[level][Number]
            )
    except:
        return render_template(
                "Part1/P1_Q1.html",
                points=points_dict[level][Number],
                Level=level,
                stone=level - 1,
                question=question_dict[level][Number],
                Number=Number,
            )


@app.route("/P1_pass-key1", methods=["POST", "GET"])
def p1_passkey():

    if request.method == "POST":
        in1 = request.form["in1"]
        in2 = request.form["in2"]
        in3 = request.form["in3"]
        in4 = request.form["in4"]
        pass_key = str(in1) + "-" + str(in2) + "-" + str(in3) + "-" + str(in4)
        print(pass_key)

        if pass_key == "1234-1234-1234-1234":
            return render_template("Part1/P1_video1.html")

    return render_template("Part1/P1_passkey.html")


if __name__ == "__main__":
    app.run()
