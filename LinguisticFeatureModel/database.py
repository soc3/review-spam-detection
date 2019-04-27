from flask import Flask,render_template,request,json,url_for
import sqlite3
from sklearn.externals import joblib
import features
import pandas as pd
app = Flask(__name__)

conn = sqlite3.connect('database.db')
print ("Opened database successfully");

#conn.execute('CREATE TABLE reviews3 (name TEXT)')
print("Table created successfully");

@app.route('/')
def home_page():
   return render_template('index.html')

@app.route('/predict2',methods = ['POST', 'GET'])
def predict2():
      try:
         rv = request.form['raw_text']
         print(rv)
         a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12 = features.majorfunc(rv)
         a13 = -1
         data = [[a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12, a13]]
         X_test = pd.DataFrame(data, index=range(0,1), columns=['A', 'B', 'C', 'D', 'E', 'F', 
            'G', 'H', 'I', 'J', 'K', 'L', 'M'])
         #print(X_test)
         model = joblib.load('model.pkl')

         y_test = model.predict(X_test)
         print(y_test)
         with sqlite3.connect("database.db") as con:
            if y_test == 1:
               print("hello")
               cur = con.cursor()
               print("hello")
               cur.execute("INSERT INTO reviews3 (name) VALUES (?)",(rv,) )
               print("hello")
               con.commit()
               msg = "Record successfully added"
               print(msg)
      except Exception as e:
         print(e)
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return render_template("result.html")
         con.close()

@app.route('/list2')
def list2():
   con = sqlite3.connect("database.db")
   con.row_factory = sqlite3.Row
   
   cur = con.cursor()
   cur.execute("select name from reviews3")
   
   rows = cur.fetchall()
   con.close()
   return render_template("list2.html",rows = rows) 


if __name__ == '__main__':
	app.run(debug=True)
