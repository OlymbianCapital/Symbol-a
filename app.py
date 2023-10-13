from flask import *
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
 
UPLOAD_FOLDER = os.path.join('staticFiles', 'uploads')
# Define allowed files
ALLOWED_EXTENSIONS = {'csv'}
app = Flask(__name__)
# Configure upload file path flask
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
uri = 'mongodb+srv://SuperUser:lnxXk6WtK3ODyqq8@cluster0.rkzkni6.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(uri, server_api=ServerApi('1'))
mongo_db = client['RestaurantsDB']
restaurant_collection = mongo_db['restaurants']

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        document = dict()
        document['title'] = request.form.get('title')
        document['cuisine'] = request.form.get('cuisine')
        document['type'] = request.form.getlist('type')
        document['address'] = request.form.get('address')
        document['area'] = request.form.get('area')
        document['description'] = request.form.get('description')
        document['phone'] = request.form.get('phone')
        document['email'] = request.form.get('email')
        document['payment'] = request.form.getlist('payment')
        document['services'] = request.form.getlist('services')
        document['recommended'] = request.form.getlist('recommended')
        document['reviews'] = request.form.get('reviews')
        document['min_price'] = request.form.get('min_price')
        document['max_price'] = request.form.get('max_price')
        restaurant_collection.insert_one(document)
    return render_template('admin.html')

# @app.route('/admin_csv', methods=['GET', 'POST'])
# def uploadFile():
#     if request.method == 'POST':
#       # upload file flask
#         lines = request.files.get('csvFile').stream.readlines()
#         for line in lines:
#             data = str(line, encoding='UTF-8').replace('\'','').replace('b','',1).replace('\\n','').split(',')
#             print(data)
#             record = {}
#             record['title'] = data[0]
#             record['cuisine'] = data[1]
#             record['type'] = data[2]
#             record['area'] = data[3]
#             record['description'] = data[4]
#             record['telephone'] = data[5]
#             record['email'] = data[6]
#             record['payment'] = data[7].split('-')
#             record['services'] = data[8].split('-')
#             record['address'] = data[9]
#             restaurant_collection.insert_one(record)
#     return render_template('admin.html')

@app.route('/', methods=['GET', 'POST'])
def home():
    docs = restaurant_collection.find({}).sort('title').limit(5)
    slider_elements = list()
    for doc in docs:
        title = doc['title']
        if 'picture' not in doc:
          image = 'images/logo.png'
        else:
          image = doc['picture']
        address = doc['address']
        description = doc['description']
        cuisine = doc['cousine']
        area = doc['area']
        rest_type= doc['type']
        slider_elements.append((title, image, address, description, cuisine, area, rest_type))
    return render_template('index.html', slider_elements=slider_elements)


