#app.py
from flask import *
import json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///registration.db'
db = SQLAlchemy(app)
class UserDetails(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    user_email = db.Column(db.String, nullable = False) 
    def __repr__(self):
        return (self.user_id,"logged in using",self.user_email)

def check_none():
    temp_attempt=(request.cookies.get('Attempt'))
    if temp_attempt==None:
        temp_attempt=0
    elif temp_attempt!=None:
        temp_attempt=int(temp_attempt)
    return(temp_attempt)


def question(option,answer,que_page,to_page):
            

            if option==answer:
                attempt=0
                resp = make_response(redirect(to_page))
                
                resp.set_cookie('Attempt', json.dumps(attempt))
                return resp
            else:
                attempt=request.cookies.get('Attempt')
                if attempt!=None:
                    attempt=1+int(attempt)
                    resp = make_response(render_template(que_page))
                
                    resp.set_cookie('Attempt', json.dumps(attempt))
                    return resp
                elif attempt==None:
                    attempt=1
                    resp = make_response(render_template(que_page))
                
                    resp.set_cookie('Attempt', json.dumps(attempt))
                    

               
                    return resp
      
"""
@app.route('/this_question', methods = ['POST', 'GET'])
def px_question_x():
  
    temp_attempt=check_none()

    if temp_attempt<3:
        if request.method == 'POST':
            option = request.form['answer']
            option=option.lower()
            
            
            resp=question(option,"Answer","Question Page","Next Question")

            if resp!=None:
                return resp

        return render_template(' Question Page ')
    else:
        return render_template('out.html')
"""

#Pages

@app.route('/', methods = ['POST', 'GET'])
def main():
    return render_template('main.html')

@app.route('/rules', methods = ['POST', 'GET'])
def rules():
    return render_template('rules.html')

@app.route('/thanks', methods = ['POST', 'GET'])
def thanks():
    return render_template('thanks.html')


@app.route('/P1_Q1', methods = ['POST', 'GET'])
def p1_question_1():
  
    temp_attempt=check_none()

    if temp_attempt<3:
        if request.method == 'POST':
            option = request.form['answer']
            option=option.lower()
            
            resp=question(option,"1","Part1/P1_Q1.html","/P1_Q2")

            if resp!=None:
                return resp
        return render_template('Part1/P1_Q1.html')
    else:
        return render_template('out.html')


@app.route('/P1_Q2', methods = ['POST', 'GET'])
def p1_question_2():
  
    temp_attempt=check_none()

    if temp_attempt<3:
        if request.method == 'POST':
            option = request.form['answer']
            option=option.lower()
            
            
            resp=question(option,"2","Part1/P1_Q2.html","/P1_Q3")

            if resp!=None:
                return resp

        return render_template('Part1/P1_Q2.html')
    else:
        return render_template('out.html')


@app.route('/P1_Q3', methods = ['POST', 'GET'])
def p1_question_3():
  
    temp_attempt=check_none()

    if temp_attempt<3:
        if request.method == 'POST':
            option = request.form['answer']
            option=option.lower()
            
            
            resp=question(option,"3","Part1/P1_Q3.html","/P1_Q4")

            if resp!=None:
                return resp

        return render_template('Part1/P1_Q3.html')
    else:
        return render_template('out.html')

@app.route('/P1_Q4', methods = ['POST', 'GET'])
def p1_question_4():
  
    temp_attempt=check_none()

    if temp_attempt<3:
        if request.method == 'POST':
            option = request.form['answer']
            option=option.lower()
            
            
            resp=question(option,"4","Part1/P1_Q4.html","/P1_Q5")

            if resp!=None:
                return resp

        return render_template('Part1/P1_Q4.html')
    else:
        return render_template('out.html')

@app.route('/P1_Q5', methods = ['POST', 'GET'])
def p1_question_5():
  
    temp_attempt=check_none()

    if temp_attempt<3:
        if request.method == 'POST':
            option = request.form['answer']
            option=option.lower()
            
            
            resp=question(option,"5","Part1/P1_Q5.html","/P1_pass-key1")

            if resp!=None:
                return resp

        return render_template('Part1/P1_Q5.html')
    else:
        return render_template('out.html')

@app.route('/P1_pass-key1', methods = ['POST', 'GET'])
def p1_passkey():
  
        if request.method == 'POST':
            in1 = request.form['in1']
            in2 = request.form['in2']
            in3 = request.form['in3']
            in4 = request.form['in4']
            pass_key=str(in1)+'-'+str(in2)+'-'+str(in3)+'-'+str(in4)
            print(pass_key)
            
            if pass_key=="1234-1234-1234-1234":
                return render_template('Part1/P1_video1.html')

           

           
        return render_template('Part1/P1_passkey.html')
    

if __name__ == "__main__":
    app.run()

