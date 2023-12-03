from flask import Flask, render_template, url_for
import pymysql

app = Flask(__name__)

# 配置数据库连接信息
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '000',
    'database': 'movie',
}
# tuple = (1, 'The Shawshank Redemption', '2h 22m', '14-Oct-94', 'drama')

# 连接到数据库
conn = pymysql.connect(**db_config)

@app.route('/')
def movies():
    # 查询数据库中的电影信息
    with conn.cursor() as cursor:
        sql = "SELECT * FROM movies"
        cursor.execute(sql)
        result = cursor.fetchall()
    
    # 渲染模板并显示电影信息
    return render_template('test.html', movies=result, background_image=url_for('static', filename='horror.jpg'),home_image=url_for('static', filename='home-icon.png'))

if __name__ == '__main__':
    app.run(debug=True)
