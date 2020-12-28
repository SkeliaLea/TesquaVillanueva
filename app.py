import json
from flask import Flask,render_template,request
from flaskext.mysql import MySQL


app=Flask(__name__)

mysql=MySQL()

app.config['MYSQL_DATABASE_HOST']="127.0.0.1"
app.config['MYSQL_DATABASE_USER']="root"
app.config['MYSQL_DATABASE_PASSWORD']=""
app.config['MYSQL_DATABASE_DB']="student_database"
mysql.init_app(app)
conn=mysql.connect
@app.route('/getall')
def get_all():
    conn=mysql.connect()
    cursor=conn.cursor()
    try:
        sql="SELECT * FROM `student` ORDER BY `lastname`";
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql)
        rows=cursor.fetchall()
        return json.dumps({"list":rows})
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()   
		
@app.route("/login",methods=['POST'])
def login():
	
	
	if request.form['username'] =='admin' and request.form['password'] =='admin':
		return render_template("/admin.html")
	else:
		msg = 'Incorrect username / password !'
		return render_template('index.html', msg=msg)



@app.route('/')
def main():
    return render_template('index.html')


@app.route('/logout')
def logout():
    
    return render_template('index.html')

@app.route('/register',methods=['POST'])
def add_student():

    idno=request.form['idno']
    lastname=request.form['lastname']
    firstname=request.form['firstname']
    course=request.form['course']
    level=request.form['level']
    msg = 'You have successfully registered !'
    conn=mysql.connect()
    cursor=conn.cursor()
    conn = conn.cursor()
    cursor.execute('SELECT * FROM student WHERE idno = % s', (idno,))
    student = cursor.fetchone()
		
    if student:
        msg = 'Student already exists !'
    else:
        try:
             
            sql="INSERT INTO `student`(idno,lastname,firstname,course,level) VALUES(%s,%s,%s,%s,%s)"
            conn=mysql.connect()
            cursor=conn.cursor()
            cursor.execute(sql,(idno,lastname,firstname,course,level))
            conn.commit()
                    
        except Exception as e:
            msg = 'Error! Please try again.'
        finally:
            cursor.close()
            conn.close()
	
	
    return render_template('admin.html',msg=msg)



@app.route('/deletestudent', methods=['POST'])
def delete_student():
    idno = request.form['myText']    
    conn=None
    cursor=None
    try:
        sql="DELETE FROM `student` WHERE `idno`=%s"
        conn=mysql.connect()
        cursor=conn.cursor()
        fld=(idno)
        cursor.execute(sql,fld)
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    return render_template('admin.html')


@app.route('/editstudent', methods=['POST'])
def edit_student():
    idno = request.form['myText0']
    lastname = request.form['myText01']
    firstname = request.form['myText02']
    course = request.form['myText03']
    level = request.form['myText04']

    conn=None
    cursor=None
    try:
        sql="UPDATE `student` SET lastname=%s,firstname=%s,course=%s,level=%s WHERE `idno`=%s"
        val1 = (lastname,firstname,course,level,idno)
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql,val1)
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    return render_template('admin.html')


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

if __name__ == '__main__':
    app.debug = True
    app.run()
