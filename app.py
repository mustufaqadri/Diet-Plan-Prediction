# ************** Importing libraries **************
import pandas as pd
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier
import numpy
from flask_cors import CORS, cross_origin
from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.widgets import TextArea
from wtforms.validators import InputRequired, Email, Length
import pymongo

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
Bootstrap(app)
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["login_signup_db"]
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-type'
current_user = "" 

# admin = {
#     'username': 'admin',
#     'password': '1234'
# }
# result = mydb.admin.insert_one(admin)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4,max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8,max=80)])
    remember = BooleanField('Remember me')

class RegistrationForm(FlaskForm):
    name = StringField('Full Name', validators=[InputRequired(), Length(max=50)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4,max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8,max=80)])

class ContactForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    fullname = StringField('Full Name', validators=[InputRequired(), Length(min=3,max=15)])
    phone = StringField('Phone', validators=[InputRequired(), Length(min=7,max=15)])
    message = StringField(u'Messages', widget=TextArea())

class FoodForm(FlaskForm):
    foodname = StringField('Food Name', validators=[InputRequired(), Length(min=1,max=15)])
    Category= StringField('Category', validators=[InputRequired(), Length(min=1,max=15)])
    Calories = StringField('Calories', validators=[InputRequired(), Length(min=1,max=15)])
    TotalFat = StringField('Total Fat', validators=[InputRequired(), Length(min=1,max=15)])
    Sodium = StringField('Sodium', validators=[InputRequired(), Length(min=1,max=15)])
    Potassium = StringField('Potassium', validators=[InputRequired(), Length(min=1,max=15)])
    TotalCarbs = StringField('Carbo-hydrates', validators=[InputRequired(), Length(min=1,max=15)])
    DietFiber = StringField('Dietary Fiber', validators=[InputRequired(), Length(min=1,max=15)])
    Sugar = StringField('Sugar', validators=[InputRequired(), Length(min=1,max=15)])
    Protein = StringField('Protein', validators=[InputRequired(), Length(min=1,max=15)])
    VitA = StringField('Vitamin A', validators=[InputRequired(), Length(min=1,max=15)])
    VitC = StringField('Vitamin B', validators=[InputRequired(), Length(min=1,max=15)])
    Calcium = StringField('Calcium', validators=[InputRequired(), Length(min=1,max=15)])
    Iron = StringField('Iron', validators=[InputRequired(), Length(min=1,max=15)])
    SatFat = StringField('Saturated Fat', validators=[InputRequired(), Length(min=1,max=15)])
    Cholestrol = StringField('Cholestrol', validators=[InputRequired(), Length(min=1,max=15)])

class DelForm(FlaskForm):
    foodname = StringField('Food Name', validators=[InputRequired(), Length(min=1,max=15)])

@app.route('/', methods=['GET', 'POST'])
def index():
    form = ContactForm()

    if form.validate_on_submit():
        mycol = mydb["msgs"]
        input_data = {"fullname":form.fullname.data, "phone":form.phone.data, "email":form.email.data, "message":form.message.data}
        x = mycol.insert_one(input_data)
        return 'Success! message sent successfully.'

    return render_template('index.html', form = form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        mycol = mydb["user"]
        x = mycol.find({"username":form.username.data, "password":form.password.data})
        
        for value in x:
            if value:
                session['loggedin'] = True
                # session['id'] = value["_id"]
                session['username'] = value['username']
                global current_user
                # current_user = value['_id']
                current_user = value['username']
                print(current_user)
                # current_user = value['name']
                return redirect(url_for('dashboard'))  
            
        flash("Error signing in! Wrong username/password.")
        # return "Error signing in!"
        # return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form = form)

@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    form = LoginForm()

    if form.validate_on_submit():
        mycol = mydb["admin"]
        x = mycol.find({"username":form.username.data, "password":form.password.data})
        
        for value in x:
            if value:
                session['loggedin'] = True
                # session['id'] = value["_id"]
                session['username'] = value['username']
                # current_user = value['_id']
                current_user = value['username']
                # current_user = value['name']
                return redirect(url_for('adminpanel'))
            
        flash("Error signing in! Wrong username/password.")
        # return "Error signing in!"
        # return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'
    return render_template('adminlogin.html', form = form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()

    if form.validate_on_submit():
        mycol = mydb["user"]
        input_data = {"username":form.username.data, "password":form.password.data, "name":form.name.data}
        x = mycol.insert_one(input_data)
        return redirect(url_for('dashboard'))

    return render_template('signup.html', form = form)

@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('username', None)
   return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/searchhistory')
def searchhistory():
    return render_template('history.html')

@app.route('/delfood', methods=['GET', 'POST'])
def delfood():
    # for i in allfood:
    #     print(i)
    form = FoodForm()
    form1 = DelForm()
    # fetch all food
    allfood = mydb["food"].find({})

    # Del food
    if form1.validate_on_submit():
        mycol = mydb["food"]
        input_data = {
            "Food":form1.foodname.data, 
        }
        x = mycol.delete_many(input_data)
        allfood = mydb["food"].find({})
        return render_template('adminpanel.html', food = allfood, addform = form, delform = form1)
    
    return render_template('adminpanel.html', food = allfood, addform = form, delform = form1) 

@app.route('/allmsgs')
def allmsgs():
    allmsgs = mydb["msgs"].find({})
    return render_template('allmsgs.html', msgs = allmsgs)

@app.route('/adminpanel', methods=['GET', 'POST'])
def adminpanel():
    # for i in allfood:
    #     print(i)
    form = FoodForm()
    form1 = DelForm()
    # fetch all food
    allfood = mydb["food"].find({})
    
    # Add food
    if form.validate_on_submit():
        mycol = mydb["food"]
        input_data = {
            "Food":form.foodname.data, 
            "Category":form.Category.data, 
            "Calories":form.Calories.data, 
            "Total Fat":form.TotalFat.data,
            "Sodium":form.Sodium.data,
            "Potassium":form.Potassium.data,
            "Total Carbo-hydrate":form.TotalCarbs.data,
            "Dietary Fiber":form.DietFiber.data,
            "Sugars":form.Sugar.data,
            "Protein":form.Protein.data,
            "Vitamin A":form.VitA.data,
            "Vitamin C":form.VitC.data,
            "Calcium":form.Calcium.data,
            "Iron":form.Iron.data,
            "Saturated Fat":form.SatFat.data,
            "Chole-sterol":form.Cholestrol.data
        }
        x = mycol.insert_one(input_data)
        allfood = mydb["food"].find({})
        return render_template('adminpanel.html', food = allfood, addform = form, delform = form1)
        
    return render_template('adminpanel.html', food = allfood, addform = form, delform = form1)

@cross_origin
# @cross_origin(origin='localhost',headers=['Content- Type','Authorization'],supports_credentials = True)
@app.route('/test', methods=['POST'])
def model():
    global current_user
    count = dict(request.form)
    count = count['count']
    nutrient = request.form.getlist("nutrient[]")
    print(nutrient)
    diet_request = {
        'user_id': current_user,
        'requirement': nutrient
    }
    print(current_user)
    drequest = mydb.diet_request.insert_one(diet_request)

    # ************** Input data **************
    nutritions = pd.read_csv("diet_nutritions.csv")
    nutritions.head()

    # ************** Feature Scaling / Normalization **************
    for column in nutritions:
        if column != 'Food' and column != 'Category':
            x = nutritions[column].values # get numpy array 
            x = x.reshape(-1,1) # 1D array to 2D array
            min_max_scaler = preprocessing.MinMaxScaler() # Normalization type: Min Max Scaler [0,1]
            # print(x)
            x_scaled = min_max_scaler.fit_transform(x) # Normalizational transform applied here
            # print(x_scaled)
            nutritions[column] = pd.DataFrame(x_scaled) # Updating our nutritions dataframe
            pass
        pass

    # # ************** Taking input of the required nutrients **************
    # nutrient = list()
    # count = int(input("How many nutrients do you require? "))
    # for i in range(0,count):
    #     one = input("Please enter the nutrient: ")    
    #     nutrient = nutrient + [one]
    #     pass

    # nutrient = ['Sugars', 'Calories', 'Protein']

    # ************** Breaking dataframe into required features and label **************
    features = nutritions.loc[:, nutrient].values
    label = nutritions.iloc[:, :1].values

    # Possible breaking food into categories first, as required by user
    # Taking input of the number of foods that the user requires for the mentioned nutrients, then handling number of outputs accordingly.

    # ************** Training the KNN Model ***************
    classifier = KNeighborsClassifier(n_neighbors=1)
    classifier.fit(features,label)

    # ************** Producing our [1] list and then Applying the KNN model to make output close to [1] list i.e. maximum nutrients *****************
    req_n = list() 
    # defined a list

    # We fill the list with 1(s) as much as the nutrients that the user asked.
    # For loop runs as much as is the length of the array nutrient
    for i in range(0, len(nutrient)):
        req_n = req_n + [1]
        pass

    req_n_num = numpy.asarray(req_n)
    req_n_num.reshape(1,-1)
    outputPredict = classifier.predict(req_n_num)
    print("The best food recommendation for the required nutrients is: ", outputPredict)
    
    food_details = mydb.food.find_one({"Food": outputPredict[0]})
    fname = outputPredict[0].split(',')[0]
    fquantity = outputPredict[0].split(',')[1]
    fcategory = food_details["Category"]
    
    diet_recommendation = {
        'request_id': drequest.inserted_id,
        'food': food_details["_id"]
    }
    recommendation = mydb.diet_recommendation.insert_one(diet_recommendation)

    user_history = {
        'user_id': current_user,
        'diet_recommendation': {
            'name': fname,
            'quantity': fquantity,
            'category': fcategory
        }
    }
    history = mydb.user_history.insert_one(user_history)

    # return jsonify({'fname': "asd", 'fquantity':"asdf", 'fcategory': "asff"})
    return jsonify({'fname': fname, 'fquantity':fquantity, 'fcategory': fcategory})

@cross_origin
# @cross_origin(origin='localhost',headers=['Content- Type','Authorization'],supports_credentials = True)
@app.route('/history', methods=['POST'])
def history():
    global current_user
    # current_user = "bilal"
    x = mydb["user_history"].find({"user_id":current_user})
    count = x.count()
    food = []

    for value in x:
        if value:
            food.append(value["diet_recommendation"])

    return jsonify({'count': count, 'food':food})

if __name__ == '__main__':
    app.run(debug=True)