import csv
import mysql.connector
from mysql.connector import Error
import time

# 数据库连接配置
# 这个字典包含了连接到MySQL数据库所需的所有信息
DB_CONFIG = {
    'host': 'localhost',  # 数据库服务器地址,本地服务器使用localhost
    'user': 'root',  # 数据库用户名
    'password': '123123',  # 数据库密码
    'database': 'movies_db',  # 要使用的数据库名称
    'charset': 'utf8mb4',  # 字符集,utf8mb4支持存储emoji等特殊字符
    'use_unicode': True,  # 使用Unicode编码
}

def print_db_info():
    """
    打印数据库连接信息
    这个函数用于显示数据库连接的详细信息,但会隐藏密码
    """
    print("\n数据库连接信息:")
    print(f"服务器: {DB_CONFIG['host']}")
    print(f"数据库: {DB_CONFIG['database']}")
    print(f"用户名: {DB_CONFIG['user']}")
    print(f"密码: {'*' * len(DB_CONFIG['password'])}")  # 用星号代替实际密码,保护隐私

def create_database():
    """
    创建数据库
    这个函数会连接到MySQL服务器并创建一个新的数据库(如果它不存在的话)
    """
    try:
        # 创建到MySQL服务器的连接
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        if conn.is_connected():
            cursor = conn.cursor()
            # 执行创建数据库的SQL命令,使用utf8mb4字符集和utf8mb4_unicode_ci校对规则
            cursor.execute("CREATE DATABASE IF NOT EXISTS {} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci".format(DB_CONFIG['database']))
            print(f"数据库 '{DB_CONFIG['database']}' 创建成功")
    except Error as e:
        print("创建数据库时出错:", e)  # 如果发生错误,打印错误信息
    finally:
        if conn.is_connected():
            cursor.close()  # 关闭游标
            conn.close()  # 关闭数据库连接

def create_table():
    """
    创建表
    这个函数会在之前创建的数据库中创建一个名为'movies'的表
    """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)  # 使用配置信息连接到数据库
        if conn.is_connected():
            cursor = conn.cursor()
            # 执行创建表的SQL命令
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                director VARCHAR(255),
                actors TEXT,
                genre VARCHAR(100),
                region VARCHAR(100),
                language VARCHAR(100),
                release_date VARCHAR(50),
                play_link TEXT,
                cover_image TEXT,
                plot_summary TEXT,
                rating FLOAT
            ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
            """)
            print("表 'movies' 创建成功")
    except Error as e:
        print("创建表时出错:", e)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def import_data(file_path):
    """
    导入数据
    这个函数从指定的CSV文件中读取数据,并将其导入到数据库表中
    
    参数:
    file_path (str): CSV文件的路径
    """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            cursor = conn.cursor()
            with open(file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  # 跳过CSV文件的标题行
                row_count = 0
                start_time = time.time()  # 记录开始时间
                for row in csv_reader:
                    # 插入数据的SQL命令
                    sql = """INSERT INTO movies 
                    (title, director, actors, genre, region, language, release_date, play_link, cover_image, plot_summary, rating) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                    cursor.execute(sql, row)
                    row_count += 1
                    if row_count % 100 == 0:  # 每导入100条记录打印一次进度
                        print(f"已导入 {row_count} 条记录...")
                conn.commit()  # 提交事务,确保所有数据都被保存
                end_time = time.time()  # 记录结束时间
                print(f"\n数据导入成功")
                print(f"总共导入 {row_count} 条记录")
                print(f"耗时: {end_time - start_time:.2f} 秒")
                
                # 获取表的总记录数
                cursor.execute("SELECT COUNT(*) FROM movies")
                total_records = cursor.fetchone()[0]
                print(f"movies 表中的总记录数: {total_records}")
    except Error as e:
        print("导入数据时出错:", e)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def check_data():
    """
    检查数据
    这个函数从数据库中检索前5条记录并打印出来,用于验证数据是否正确导入
    """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("SELECT title, director FROM movies LIMIT 5")
            results = cursor.fetchall()
            print("\n数据检查:")
            for row in results:
                print(f"标题: {row[0]}, 导演: {row[1]}")
    except Error as e:
        print("检查数据时出错:", e)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def drop_database():
    """
    删除数据库
    这个函数会删除之前创建的整个数据库。请谨慎使用!
    """
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("DROP DATABASE IF EXISTS {}".format(DB_CONFIG['database']))
            print(f"数据库 '{DB_CONFIG['database']}' 已成功删除")
    except Error as e:
        print("删除数据库时出错:", e)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# 程序的主入口
if __name__ == "__main__":
    print_db_info()  # 打印数据库连接信息
    create_database()  # 创建数据库
    create_table()  # 创建表
    import_data('movies.csv')  # 导入数据,确保'movies.csv'文件在正确的路径
    check_data()  # 检查导入的数据
    # drop_database()  # 如果需要删除数据库,取消这行的注释
