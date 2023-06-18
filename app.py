from flask import Flask, jsonify, request, redirect, render_template, url_for, flash, session,wrappers, make_response
from flask_session import Session
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from twilio.twiml.messaging_response import MessagingResponse
from models import *
from decimal import Decimal
from num import countDigit, averaGe
from validate import Validate
from repay import Repay
from balancer import account
#import re
# from functools import wrapspy
import pdfkit
import os
import string
import random
import datetime
import re

 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ProfessorSecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/loan_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
ma.init_app(app)


login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


with app.app_context():
    db.create_all()

ALLOWED_EXTENSIONS = {'jpeg'}

GREETING_INPUTS = ("hi", "hello", "hey", "helloo", "hellooo", "g morning",  "gmorning",  "good morning", "morning", "good day", "good afternoon", "good evening", "greetings", "greeting", "good to see you", "its good seeing you", "how are you", "how're you", "how are you doing", "how ya doin'", "how ya doin", "how is everything", "how is everything going", "how's everything going", "how is you", "how's you", "how are things", "how're things", "how is it going", "how's it going", "how's it goin'", "how's it goin", "how is life been treating you", "how's life been treating you", "how have you been", "how've you been", "what is up", "what's up", "what is cracking", "what's cracking", "what is good", "what's good", "what is happening", "what's happening", "what is new", "what's new", "what is neww", "g'day", "howdy",)
GREETING_RESPONSES = ["I am glad! You are talking to me. Type the word menu to continue", "Great, hope you're good! Type the word *menu* to continue"]
def greeting(sentence):
 
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)
   

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def zesa(amount):
    token = random.randint(1000000000,9999999999)
    zs = Zesa.query.first()
    if(zs == None):
        return 0, 0
    
    watts = (zs.price/zs.kilowatts) * amount 

    return watts, token

@app.route("/wa")
def wa_hello():
    
    return "Hello, World!"
 
@app.route("/wasms", methods=['POST'])
def wa_sms_reply():
    phone = request.form.get('WaId')
    name = request.form.get('ProfileName')
    bot = Bot.query.filter_by(phone=phone).first()

    msg = request.form.get('Body').lower() # Reading the message from the whatsapp
    resp = MessagingResponse()
    reply=resp.message()

    if bot is None:
        # pin = random.randint(1000,9999)
        # new_bot = Bot(name, phone, 'main', 0.00, pin, None)
        # db.session.add(new_bot)
        # db.session.commit()

        # new_cache = LoanCache(new_bot.id, None, None)
        # db.session.add(new_cache)
        # db.session.commit()

        # new_repaycache = RepayCache(new_bot.id, None, None)
        # db.session.add(new_repaycache)
        # db.session.commit()

        # new_feescache = FeesCache(new_bot.id, None, None)
        # db.session.add(new_feescache)
        # db.session.commit()

        reply.body("*SORRY YOUR PHONE NUMBER IS NOT REGISTERED AT BancABC.*\nVisit our offices for assistance.")
        return str(resp)

    
    cache = LoanCache.query.filter_by(botid=bot.id).first()
    repaycache = RepayCache.query.filter_by(botid=bot.id).first()
    feescache = FeesCache.query.filter_by(botid=bot.id).first()
 
    
 
    # Text response
    if msg == "exit":
        bot.menu = 'main'
        db.session.commit()

        cache.option = None
        cache.amount = None
        db.session.commit()

        feescache.schoolid = None
        feescache.amount = None
        db.session.commit()

        repaycache.phone = None
        repaycache.amount = None
        db.session.commit()

        reply.body("The process existed.")

    elif msg == "hi":
        bot.menu = 'main'
        db.session.commit()

        cache.option = None
        cache.amount = None
        db.session.commit()

        repaycache.phone = None
        repaycache.amount = None
        db.session.commit()

        reply.body("Hi, how may i help you?. To know more about the bot type *help* or type *menu*.")

    elif msg == "help":
        reply.body("*HELP*\nInorder to get valid responses please follow the procedural menu options\n _When you feel lost just type *exit* the bot will refresh_")
    
    elif msg == "menu":
        message = "Thank you for contacting BancABC. \n*WELCOME TO BancABC*\n *1)* Request a bank statement.\n *2)* Change your PIN.\n *3)* Transfer money.\n 4) Find the nearest BancAbc branch.\n 5) Report a credit card loss. \n Reply with option number only."
        reply.body(message)

    else:
        if(bot.menu == "main"):
            if(msg == "1"):
                # bot.menu = 'loan'
                db.session.commit()
                message = "BancABC\n First Street Gweru\n Gweru, Midlands\n Date: June 11, 2023\n\n Memory\nmemory@gmail.com\nPhone: 0779400263\n \n Account Number: 52XXXX--7787 \n Account Holder: Memory\n Statement Period: June 1, 2023 - June 30, 2023"
                reply.body(message)

            elif(msg == "2"):
                bot.menu = 'pin'
                db.session.commit()
                message = "Enter old PIN & Please keep this pin safe: "
                # has been automatically generated is *4352*. Please keep this pin safe."
                reply.body(message)

            elif(msg == "3"):
                bot.menu = 'transfer'
                db.session.commit()
                message = "*Please provide an account number to transfer money.*"
                reply.body(message)
            elif(msg == "4"):
                # bot.menu = 'pin'
                db.session.commit()
                message = "*Your nearest branch is Gweru. Click the link for directions: [https://goo.gl/maps/K2sWpVGLbcokrGJ98]"
                reply.body(message)
            elif(msg == "5"):
                # bot.menu = 'loss'
                db.session.commit()
                message = "Thank you for reporting the loss of your credit card. We have temporarily locked your card to prevent any unauthorized transactions. Please visit the nearest branch to obtain a new credit card."
                reply.body(message)
            else:
                message = "Invalid menu option"
                reply.body(message)

        
        elif(bot.menu == "pin"):
            try:
                userpin = int(msg)
            except:
                reply.body("pin must be 4 digits number please try again")
                return str(resp)
            if(userpin == 1212):
                # bot.menu = 'main'
                db.session.commit()
                message = "Your new PIN is is 1212"
                reply.body(message)
            else:
                message = "Invalid Pin please try again or type *exit*"
                reply.body(message)

        elif(bot.menu == "transfer"):
            try:
                acc_num = int(msg)
            except:
                reply.body("Invalid Account Number")
                return str(resp)
            if(acc_num == 1111):
                bot.menu = 'transfer2'
                db.session.commit()
                message = "Please select amount to transfer \n*1)*ZWL 500.\n *2)* ZWL 1000.\n"
                reply.body(message)
            else:
                message = "Invalid Pin please try again or type *exit*"
                reply.body(message)


        #Loan
        elif(bot.menu == "transfer2"):
            if(msg == "1"):
                bot.menu = 'confirm'
                db.session.commit()
                message = "Tranfer money to: John Doe \n Account number: {acc_num} \n Amount: ZWL 500 \n \n Select Answer \n*1)*Confirm.\n *2)* Cancel"
                reply.body(message)

            elif(msg == "2"):
                bot.menu = 'confirm'
                db.session.commit()
                message = "Tranfer money to: John Doe \n Account number: {acc_num} \n Amount: ZWL 1000 \n \n Select Answer \n*1)*Confirm.\n *2)* Cancel"
                # schools = School.query.all()
                # message = "*REQUESTING LOAN FOR SCHOOL FEES*\n *Select school from list below*.\n"
                # count = 0
                # for school in schools:
                #     message = message + "*" + str(school.id) + "*" + " "+ school.name + " $"+str(school.fees)+"\n"
                reply.body(message)
            else:
                message = "Invalid menu option"
                reply.body(message)


        elif(bot.menu == "confirm"):
            if(msg == "1"):
                # bot.menu = 'confirmed'
                db.session.commit()
                message = "*The money transfer you requested has been completed successfully.*"
                reply.body(message)

            elif(msg == "2"):
                # bot.menu = 'cancel'
                db.session.commit()
                message = "*Transfer was Cancelled*"
                reply.body(message)
            else:
                message = "Invalid menu option"
                reply.body(message)

        elif(bot.menu == "personal-account"):
            try:
                amount = Decimal(msg)
            except:
                reply.body("Amount must be a float please try again")
                return str(resp)
            bot.menu = 'personal-account-confirm'
            db.session.commit()
            cache.option = 1
            cache.amount = amount
            db.session.commit()
            message = "Please enter pin to confirm."
            reply.body(message)

        elif(bot.menu == "personal-account-confirm"):
            try:
                userpin = int(msg)
            except:
                reply.body("pin must be 4 digits number please try again")
                return str(resp)

            if (bot.pin == userpin):
                loan = Loan.query.filter_by(botid=bot.id).first()
                if(loan == None):
                    new_loan = Loan(bot.id, cache.amount)
                    db.session.add(new_loan)
                    db.session.commit()

                    #transaction table
                    ct = datetime.datetime.now()
                    new_tran = Transaction(bot.id, 'Personal Loan', 'Bot', cache.amount, 'Personal', ct)
                    db.session.add(new_tran)
                    db.session.commit()

                    bot.balance = bot.balance + cache.amount
                    db.session.commit()

                    bot.menu = 'main'
                    db.session.commit()

                    cache.option = None
                    cache.amount = None
                    db.session.commit()

                    message = "Your loan application was successful."
                    reply.body(message)
                else:
                    if(loan.balance > 0.00):
                        bot.menu = 'main'
                        db.session.commit()

                        cache.option = None
                        cache.amount = None
                        db.session.commit()

                        message = "You have an unsettled loan balance of $"+str(loan.balance)
                        reply.body(message)
                    else:
                        sum_result = Transaction.query.with_entities(
                                db.func.avg(Transaction.amount).label("mySum")
                            ).filter_by(
                                botid=bot.id
                            ).all()
                        sum = round(sum_result[0].mySum, 2)

                        possibility = averaGe(sum, cache.amount)
                        if (possibility < 5):
                            bot.menu = 'main'
                            db.session.commit()

                            cache.option = None
                            cache.amount = None
                            db.session.commit()

                            message = "The amount that we can loan to you is to little. $"+str(possibility)
                            reply.body(message)
                        else:
                            new_loan = Loan(bot.id, possibility)
                            db.session.add(new_loan)
                            db.session.commit()

                            #transaction table
                            ct = datetime.datetime.now()
                            new_tran = Transaction(bot.id, 'Personal Loan', 'Bot', possibility, 'Personal', ct)
                            db.session.add(new_tran)
                            db.session.commit()

                            bot.balance = bot.balance + possibility
                            db.session.commit()

                            bot.menu = 'main'
                            db.session.commit()

                            cache.option = None
                            cache.amount = None
                            db.session.commit()

                            message = "Your loan application was successful."
                            reply.body(message)



            else:
                message = "*Incorrect pin* Please try again or type *exit* to exit process."
                reply.body(message)
            
        elif(bot.menu == "school-fees"):
            try:
                opt = int(msg)
            except:
                reply.body("Option not available please try again.")
                return str(resp)
            
            choice = School.query.filter_by(id=opt).first()
            if(choice == None):
                reply.body("Option not available please try again.")
                return str(resp)
            
            bot.menu = 'school-fees-confirm'
            db.session.commit()

            feescache.school = choice.id
            feescache.amount = choice.fees
            db.session.commit()

            message = "About to pay fees at "+choice.name+" on loan, amount $"+str(choice.fees)+ ". *Enter pin to confirm.*"
            reply.body(message)

        elif(bot.menu == "school-fees-confirm"):
            try:
                userpin = int(msg)
            except:
                reply.body("pin must be 4 digits number please try again")
                return str(resp)

            if (bot.pin == userpin):
                loan = Loan.query.filter_by(botid=bot.id).first()
                if(loan == None):
                    new_loan = Loan(bot.id, cache.amount)
                    db.session.add(new_loan)
                    db.session.commit()

                    #transaction table
                    ct = datetime.datetime.now()
                    new_tran = Transaction(bot.id, 'Fees Loan', 'Bot', feescache.amount, feescache.name, ct)
                    db.session.add(new_tran)
                    db.session.commit()

                    bot.menu = 'main'
                    db.session.commit()

                    feescache.schoolid = None
                    feescache.amount = None
                    db.session.commit()

                    message = "Your school fees loan application was successful."
                    reply.body(message)
                else:
                    if(loan.balance > 0.00):
                        bot.menu = 'main'
                        db.session.commit()

                        cache.option = None
                        cache.amount = None
                        db.session.commit()

                        feescache.schoolid = None
                        feescache.amount = None
                        db.session.commit()

                        message = "You have an unsettled loan balance of $"+str(loan.balance)
                        reply.body(message)
                    else:
                        loan = Loan.query.filter_by(botid=bot.id)
                        loan.amount = loan.amount + feescache.amount
                        db.session.commit()

                        #transaction table
                        ct = datetime.datetime.now()
                        new_tran = Transaction(bot.id, 'School Fees Loan', 'Bot', possibility, feescache.name, ct)
                        db.session.add(new_tran)
                        db.session.commit()

                        bot.menu = 'main'
                        db.session.commit()

                        cache.option = None
                        cache.amount = None
                        db.session.commit()

                        feescache.schoolid = None
                        feescache.amount = None
                        db.session.commit()

                        message = "Your school fees loan application was successful."
                        reply.body(message)


        elif(bot.menu == "zesa-token"):
            try:
                amount = Decimal(msg)
            except:
                reply.body("Amount must be a float please try again")
                return str(resp)
            bot.menu = 'zesa-token-confirm'
            db.session.commit()
            cache.option = 3
            cache.amount = amount
            db.session.commit()
            message = "Please enter pin to confirm."
            reply.body(message)
        
        elif(bot.menu == "zesa-token-confirm"):
            try:
                userpin = int(msg)
            except:
                reply.body("pin must be 4 digits number please try again")
                return str(resp)

            if (bot.pin == userpin):
                loan = Loan.query.filter_by(botid=bot.id).first()
                if(loan == None):
                    zs = zesa(cache.amount)
                    new_loan = Loan(bot.id, cache.amount)
                    db.session.add(new_loan)
                    db.session.commit()

                    #transaction table
                    ct = datetime.datetime.now()
                    new_tran = Transaction(bot.id, 'Zesa Token Loan', 'Bot', cache.amount, 'ZESA', ct)
                    db.session.add(new_tran)
                    db.session.commit()

                    new_token = ZesaToken(bot.id, zs[0], zs[1], cache.amount)
                    db.session.add(new_token)
                    db.session.commit()

                    bot.menu = 'main'
                    db.session.commit()

                    cache.option = None
                    cache.amount = None
                    db.session.commit()

                    message = "Your zesa token loan application was successful. token:"+str(zs[0])+" kilowatts: "+str(zs[1])
                    reply.body(message)
                else:
                    if(loan.balance > 0.00):
                        bot.menu = 'main'
                        db.session.commit()

                        cache.option = None
                        cache.amount = None
                        db.session.commit()

                        message = "You have an unsettled loan balance of $"+str(loan.balance)
                        reply.body(message)
                    else:
                        zs = zesa(cache.amount)
                        loan = Loan.query.filter_by(botid = bot.id).first()
                        loan.balance = loan.balance + cache.amount
                        db.session.commit()

                        #transaction table
                        ct = datetime.datetime.now()
                        new_tran = Transaction(bot.id, 'Zesa Token Loan', 'Bot', cache.amount, 'ZESA', ct)
                        db.session.add(new_tran)
                        db.session.commit()

                        new_token = ZesaToken(bot.id, zs[0], zs[1], cache.amount)
                        db.session.add(new_token)
                        db.session.commit()

                        bot.menu = 'main'
                        db.session.commit()

                        cache.option = None
                        cache.amount = None
                        db.session.commit()

                        message = "Your zesa token loan application was successful. token:"+str(zs[0])+" kilowatts: "+str(zs[1])
                        reply.body(message)



            else:
                message = "*Incorrect pin* Please try again or type *exit* to exit process."
                reply.body(message)
            

        #repay loan
        elif (bot.menu == "repay"):
            try:
                amount = Decimal(msg)
            except:
                reply.body("Amount must be a float please try again")
                return str(resp)
            bot.menu = 'repay-phone'
            db.session.commit()

            repaycache.amount = amount
            db.session.commit()
            message = "*Settling $"+str(amount)+"*\n Now enter ecocash number."
            reply.body(message)

        elif (bot.menu == "repay-phone"):
            if(Validate.econet(msg)):
                paynow = Repay.back(repaycache.amount,msg)
                amnt = repaycache.amount
                if(paynow == 'paid'):
                    loantable = Loan.query.filter_by(botid=bot.id).first()
                    balanced = account(loantable.balance, repaycache.amount)
                    if(balanced == 0):
                        loantable.balance = loantable.balance - repaycache.amount
                        db.session.commit()
                    else:
                        loantable.balance = 0
                        db.session.commit()

                        bot.balance = bot.balance - balanced
                        db.session.commit()
                    

                    #transaction table
                    ct = datetime.datetime.now()
                    new_tran = Transaction(bot.id, 'Loan Settlement', 'Paynow', repaycache.amount, 'African Century', ct)
                    db.session.add(new_tran)
                    db.session.commit()

                    bot.menu = 'main'
                    db.session.commit()

                    cache.option = None
                    cache.amount = None
                    db.session.commit()

                    repaycache.phone = None
                    repaycache.amount = None
                    db.session.commit()

                    message = "*Successfully paid $"+str(amnt)+"*\n loan settlement."
                    reply.body(message)
                else:
                    bot.menu = 'main'
                    db.session.commit()

                    cache.option = None
                    cache.amount = None
                    db.session.commit()

                    repaycache.phone = None
                    repaycache.amount = None
                    db.session.commit()

                    message = "*An error occured try again later.*"
                    reply.body(message)
            else:
                message = "*Please enter a valid econet number and try again*"
                reply.body(message)
            



        #account services
        elif(bot.menu == "services"):
            if(msg == "1"):
                bot.menu = 'account-statement'
                db.session.commit()
                message = "*REQUESTING ACCOUNT STATEMENT*\n Please enter pin."
                reply.body(message)

            elif(msg == "2"):
                bot.menu = 'account-balance'
                db.session.commit()
                message = "*REQUESTING ACCOUNT BALANCE*\n Please enter pin."
                reply.body(message)

            else:
                message = "Invalid menu option"
                reply.body(message)

        elif(bot.menu == "account-statement"):
            try:
                userpin = int(msg)
            except:
                reply.body("pin must be 4 digits number please try again")
                return str(resp)
            if(userpin == bot.pin):
                transactions = Transaction.query.filter_by(botid=bot.id).all()
                loanacc = Loan.query.filter_by(botid=bot.id).first()
                if(transactions == None):
                    bot.menu = 'main'
                    db.session.commit()
                    reply.body("Accounts statement is still empty.")
                    return str(resp)
                print(transactions)
                randomstring = randomword(16)
                docname = str(randomstring) + '.pdf'
                css = 'static/style.css'

                import datetime

                current_dateTime = datetime.datetime.now()
                pdf_content = render_template('statement.html', transactions=transactions, balance=bot.balance, name=name, phone=phone, loan=loanacc, current_dateTime=current_dateTime) 
                configpath = pdfkit.configuration(wkhtmltopdf="C:\\Program Files (x86)\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")

                static_dir = os.path.abspath('static')
                pdf_file = pdfkit.from_string(pdf_content, configuration=configpath, css=css)
                with open(os.path.join(static_dir, docname), 'wb') as f:
                    f.write(pdf_file)

                bot.menu = 'main'
                db.session.commit()
                reply.media("static/"+docname)
            else:
                message = "Invalid Pin please try again or type *exit*"
                reply.body(message)

        elif(bot.menu == "account-balance"):
            try:
                userpin = int(msg)
            except:
                reply.body("pin must be 4 digits number please try again")
                return str(resp)
            if(userpin == bot.pin):
                bot.menu = 'main'
                db.session.commit()
                message = "Your account balance is $"+str(bot.balance)
                reply.body(message)
            else:
                message = "Invalid Pin please try again or type *exit*"
                reply.body(message)
            

        #account pin
        elif(bot.menu == "pin"):
            try:
                userpin = int(msg)
            except:
                reply.body("pin must be 4 digits number please try again")
                return str(resp)

            if (bot.pin == userpin):
                bot.menu = 'new-pin'
                bot.newpin = None
                db.session.commit()
                message = "Please enter new pin."
                reply.body(message)
            else:
                message = "*Incorrect pin* Please try again or type *exit* to exit process."
                reply.body(message)

        elif(bot.menu == "new-pin"):
            try:
                userpin = int(msg)
            except:
                reply.body("pin must be 4 digits number please try again")
                return str(resp)
            if (bot.pin == userpin):
                message = "Enter a different pin."
                reply.body(message)
            else:
                print(len(str(userpin)))
                if(len(str(userpin)) == 4):
                    bot.menu = 'confirm-pin'
                    bot.newpin = userpin
                    db.session.commit()
                    message = "Please Confirm Pin."
                    reply.body(message)
                else:
                    message = "Pin must be four digits try again or type *exit*."
                    reply.body(message)

        elif(bot.menu == "confirm-pin"):
            try:
                userpin = int(msg)
            except:
                reply.body("pin must be 4 digits number please try again")
                return str(resp)
            if (bot.newpin == userpin):
                bot.menu = 'main'
                bot.pin = bot.newpin
                bot.newpin = None
                db.session.commit()
                message = "Pin Changed Successfully."
                reply.body(message)
            else:
                bot.menu = 'main'
                bot.newpin = None
                db.session.commit()
                message = "Process ended could not confirm new pin."
                reply.body(message)

        else:
            message = "Invalid menu option"
            reply.body(message)
            
    #print(msg)
    return str(resp)
 
@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def index():
    
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email == '' or password == '':
            flash('some fields are empty.')
            return redirect(url_for('login'))

        user = User.query.filter_by(email=email).first()
        
        if not user:
            flash('Invalid login details.')
            return redirect(url_for('login'))
        if check_password_hash(user.password, password):
            login_user(user)
            session['userid'] = user.id
            return redirect(url_for('dashboard'))

        flash('Invalid login details.')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password_confirmation')

        if password != password2:
            flash('Password confirmation should match!')
            return redirect(url_for('register'))

        if len(password) <= 7:
            flash('Password should be 8 characters or greater!')
            return redirect(url_for('register'))

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists!')
            return redirect(url_for('register'))
        new_user = User(email=email, password=generate_password_hash(password, method='sha256'), name=name, role=1)
        db.session.add(new_user)
        db.session.commit()

        flash('Successfully register new user!')
        return redirect(url_for('login'))
    return render_template('register.html')


def validate_zimbabwe_mobile_number(number):
    pattern = r'^\+263\d{9}$'
    match = re.match(pattern, number)
    if match:
        return True
    else:
        return False
    

def validate_four_digits(number):
    if isinstance(number, int):
        number = str(number)
    if len(number) == 4 and number.isdigit():
        return True
    else:
        return False

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == "POST":
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        phone = request.form.get('phone')
        pin = request.form.get('pin')

        if not validate_zimbabwe_mobile_number(phone):
            flash('error Insert valid Zim numbers that starts with +263!')
            return redirect(url_for('dashboard'))
        
        if not validate_four_digits(pin):
            flash('error Pin must be four digits!')
            return redirect(url_for('dashboard'))

        bot = Bot.query.filter_by(phone=phone[1:]).first()
        if bot:
            flash('error Phone number already exists!')
            return redirect(url_for('dashboard'))
        
        accnum = random.randint(10000000,99999999)
        new_bot = Bot(name=lname+" "+fname, fname=fname, lname=lname, accnum=accnum, phone=phone[1:], menu="main", balance=0.00, pin=pin, newpin=None)
        db.session.add(new_bot)
        db.session.commit()

        new_cache = LoanCache(new_bot.id, None, None)
        db.session.add(new_cache)
        db.session.commit()

        new_repaycache = RepayCache(new_bot.id, None, None)
        db.session.add(new_repaycache)
        db.session.commit()

        new_feescache = FeesCache(new_bot.id, None, None)
        db.session.add(new_feescache)
        db.session.commit()

        flash('Successfully register new account!')
        return redirect(url_for('dashboard'))

    accounts = Bot.query.all()
    return render_template('dashboard.html', accounts=accounts)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    g=None
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)