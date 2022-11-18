
from flask import Flask, jsonify, render_template,request
from flask_cors import CORS
import pymysql

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
CORS(app, resources={r"./*":{"origins":["http://127.0.0.1:5500"]}})

db = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='',
    database='school',
    charset='utf8mb4'
)

cursor = db.cursor()


menuData = {
            '4號餐': { 'name': '大麥克', 'price': 72 },
            '5號餐': { 'name': '雙層牛肉吉事堡', 'price': 62 },
            '6號餐': { 'name': '嫩煎雞腿堡', 'price': 82 },
            'A': { 'name': '中薯+飲料', 'price': 55 },
            'B': { 'name': '冰旋風+飲料', 'price': 85 },
            'C': { 'name': '麥克雞塊+薯條+飲料', 'price': 100 }
        }

@app.route('/',methods=['GET'])
def home():
    return render_template("index.html")

@app.route('/menu',methods=['GET'])
def menu():
    return jsonify(menuData)

@app.route('/school',methods=['GET'])
def scoolGetAll():
    res = {"success":False, "info":"查詢失敗"}
    try:
        sql = 'SELECT * FROM `students` WHERE `s_id` < 5'
        cursor.execute(sql)

        if cursor.rowcount > 0:
            result = cursor.fetchall()

            res['success'] = True
            res['info'] = '查詢成功'
            res['result'] = result
        else:
            res['info'] = '查無資料'

        db.commit()

    except Exception as e:
        db.rollback()
        res['info']= f'SQL 執行失敗: {e}'

    return jsonify(res)

@app.route('/school/<int:id>',methods=['DELETE'])
def delStudent(id):
    res = {"success":False, "info":"刪除失敗"}
    try:
        sql = 'DELETE FROM `students` WHERE `s_id` = %s'
        cursor.execute(sql, (id))

        if cursor.rowcount > 0:

            res['success'] = True
            res['info'] = '刪除成功'

        else:
            res['info'] = '查無資料'

        db.commit()

    except Exception as e:
        db.rollback()
        res['info']= f'SQL 執行失敗: {e}'

    return jsonify(res)



@app.route('/newStudent',methods=['POST'])
def newStudent():
    res = {"success":False, "info":"註冊失敗"}
    try:
        sql = 'INSERT INTO `students` (`s_name`,`s_gender`,`s_nickname`) VALUES (%s,%s,%s)'
        cursor.execute(sql, (request.json['name'], request.json['gender'],request.json['nickname']))

        if cursor.rowcount > 0:

            res['success'] = True
            res['info'] = '新增成功'

        else:
            res['info'] = '新增失敗'

        db.commit()

    except Exception as e:
        db.rollback()
        res['info']= f'SQL 執行失敗: {e}'

    return jsonify(res)


@app.route('/login',methods=['POST'])
def login():
    res = {"success":False, "info":"登入失敗"}
    print(request.json['name'])
    print(request.json['nickname'])

    try:
        sql = "SELECT * FROM `students` WHERE `s_name` = %s AND `s_nickname`= %s"
        cursor.execute(sql, (request.json['name'],request.json['nickname']))

        if cursor.rowcount > 0:
            result = cursor.fetchall()
            res['success'] = True
            res['info'] = '登入成功'
            res['result'] = result

        else:
            res['info'] = '登入失敗'

        db.commit()

    except Exception as e:
        db.rollback()
        res['info']= f'SQL 執行失敗: {e}'

    return jsonify(res)

@app.route('/update/<int:id>',methods=['PUT'])
def update(id):
    res = {"success":False, "info":"修改失敗"}

    try:
        sql = "UPDATE FROM `students` SET `s_name` = %s ,`s_nickname`= %s WHERE `s_id` = %s"
        cursor.execute(sql, (request.json['name'],request.json['nickname'],id))

        if cursor.rowcount > 0:

            res['success'] = True
            res['info'] = '修改成功'

        else:
            res['info'] = '修改失敗'

        db.commit()

    except Exception as e:
        db.rollback()
        res['info']= f'SQL 執行失敗: {e}'

    return jsonify(res)


app.run()

