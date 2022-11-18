
from flask import Flask, jsonify, render_template,request
from flask_cors import CORS
import pymysql

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
CORS(app, resources={r"./*":{"origins":["*"]}})

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


''' CRUD 開始 '''

# 新增學員 API
@app.route('/newStudent',methods=['POST'])
def newStudent():
    res = {"success":False, "info":"註冊失敗"}
    try:
        sql = 'INSERT INTO `students` (`s_name`,`s_gender`,`s_nickname`) VALUES (%s,%s,%s)'
        cursor.execute(sql, (request.
        json['s_name'], request.json['s_gender'],request.json['s_nickname']))

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


# 讀取 API
@app.route('/school/read',methods=['GET'])
def scoolRead():
    res = {"success":False, "info":"查詢失敗"}
    whereSqlString = ' WHERE ';

    for key, value in list(request.args.lists()):
        if value[0] :
            whereSqlString += f'`{key}`="{value[0]}" OR '

    finalSQL = whereSqlString[:-3]

    try:
        sql = f'SELECT * FROM `students` {finalSQL}'
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


# 更新學員資料 API
@app.route('/school/update/<int:id>',methods=['PUT'])
def update(id):
    res = {"success":False, "info":"修改失敗"}
    print(id)
    setSqlString = ' SET ';
    print(request.json)

    for key, value in list(request.json.items()):
        if key != 's_id' and value :
            setSqlString += f'`{key}`="{value}" ,'

    finalSQL = setSqlString[:-1]
    print(finalSQL)

    try:
        sql = f'UPDATE `students` {finalSQL} WHERE `s_id`={id}'
        print('sql',sql)
        cursor.execute(sql)

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

# 刪除學員資料 API
@app.route('/school/delete/<int:id>',methods=['DELETE'])
def delete(id):
    res = {"success":False, "info":"修改失敗"}
    setSqlString = ''
    print(request.json)

    if (id):
        setSqlString += f' WHERE `s_id`={id}'
        if len(list(request.json.items())) > 0:
            setSqlString += ' OR '

    if len(list(request.json.items())) > 0 and id == False:
        setSqlString += ' WHERE '

    for key, value in list(request.json.items()):
        if key != 's_id' and value :
            setSqlString += f'`{key}`="{value}" OR '
    

    finalSQL = setSqlString[:-3]
    print(finalSQL)

    try:
        sql = f'DELETE FROM `students` {finalSQL}'
        print('sql',sql)
        cursor.execute(sql)

        if cursor.rowcount > 0:
            result = cursor.fetchall()
            res['success'] = True
            res['info'] = '刪除成功'
            res['result'] = result
        else:
            res['info'] = '無人可刪除'

        db.commit()

    except Exception as e:
        db.rollback()
        res['info']= f'SQL 執行失敗: {e}'

    return jsonify(res)


# 登入簡易示範
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



app.run()

