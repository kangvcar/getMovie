# 电影信息爬虫系统

## 项目简介

这是一个使用Python开发的电影信息爬虫系统。该系统可以从指定的电影网站抓取电影详情信息,并将数据保存到MySQL数据库和CSV文件中。

## 主要功能

1. 多线程并发爬取电影详情页面
2. 提取电影标题、导演、演员、类型、地区、语言、上映日期、播放链接、封面图片、剧情简介和评分等信息
3. 将抓取的数据保存到MySQL数据库
4. 将抓取的数据导出为CSV文件
5. 支持断点续爬功能
6. 自动处理中文编码问题

## 技术栈

- Python 3.x
- requests: 发送HTTP请求
- BeautifulSoup: 解析HTML
- mysql-connector-python: MySQL数据库操作
- threading: 多线程编程
- csv: CSV文件处理

## 如何运行

1. 克隆项目到本地:

```
git clone https://github.com/your_username/movie-crawler.git
cd movie-crawler
```

2. 安装依赖:

```
pip install -r requirements.txt
```

3. 配置数据库:

编辑 `create_db_and_import.py` 文件中的 `DB_CONFIG` 字典,填入你的MySQL数据库连接信息。

4. 创建数据库和表:

```
python create_db_and_import.py
```

5. 运行爬虫:

```
python main.py
```

## 项目结构

```
movie-crawler/
│
├── main.py                 # 主程序入口
├── create_db_and_import.py # 数据库创建和数据导入脚本
├── movies.csv              # 爬取结果CSV文件
├── requirements.txt        # 项目依赖
└── README.md               # 项目说明文档
```

## 工作原理

1. 程序首先会创建MySQL数据库和表结构。

2. 主程序使用多线程并发抓取电影详情页面。每个线程负责处理一部分URL。

3. 对于每个电影页面,程序会解析HTML提取所需信息。

4. 提取的数据会实时保存到MySQL数据库中。

5. 同时,数据也会被写入CSV文件作为备份。

6. 程序支持断点续爬,会记录已爬取的URL,避免重复爬取。

7. 整个过程中会进行错误处理和异常捕获,确保程序稳定运行。


# 数据库表结构

```sql
CREATE TABLE IF NOT EXISTS movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    director VARCHAR(255),
    actors TEXT,
    genre VARCHAR(100),
    region VARCHAR(100),
    language VARCHAR(100),
    release_date VARCHAR(100),
    play_link VARCHAR(255),
    cover_image VARCHAR(255),
    synopsis TEXT,
    rating DECIMAL(3,1)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
```

数据库表字段说明:

| 字段名 | 数据类型 | 说明 |
|--------|----------|------|
| id | INT | 主键,自动递增,用于唯一标识每条电影记录 |
| title | VARCHAR(255) | 电影标题,不允许为空 |
| director | VARCHAR(255) | 导演姓名 |
| actors | TEXT | 演员列表,可能包含多个演员名字 |
| genre | VARCHAR(100) | 电影类型/风格,如动作、喜剧、爱情等 |
| region | VARCHAR(100) | 电影制作地区或国家 |
| language | VARCHAR(100) | 电影使用的语言 |
| release_date | VARCHAR(100) | 电影上映日期 |
| play_link | VARCHAR(255) | 电影播放链接 |
| cover_image | VARCHAR(255) | 电影封面图片的URL地址 |
| synopsis | TEXT | 电影剧情简介 |
| rating | DECIMAL(3,1) | 电影评分,保留一位小数 |

注意事项:

1. 表使用 `utf8mb4` 字符集和 `utf8mb4_unicode_ci` 排序规则,支持存储包括 emoji 在内的各种特殊字符。

2. `actors` 和 `synopsis` 字段使用 TEXT 类型,因为这些内容可能较长。

3. `rating` 字段使用 DECIMAL 类型,可以精确存储小数评分。

4. 除了 `title` 字段,其他字段都允许为 NULL,因为某些电影可能缺少部分信息。

5. `id` 字段设置为自动递增的主键,可以唯一标识每条记录,便于数据管理和查询。

这个表结构设计考虑了电影信息的多样性和完整性,能够有效地存储从网站爬取的各种电影数据。如果您需要对表结构进行任何修改或有任何疑问,请随时告诉我。

## 注意事项

- 请遵守目标网站的robots.txt规则和使用条款。
- 建议设置适当的爬取间隔,避免对目标网站造成压力。
- 首次运行时需要较长时间完成全量数据爬取,后续运行可以增量更新。

## 许可证

本项目采用 MIT 许可证。详情请参阅 [LICENSE](LICENSE) 文件。

## 贡献

欢迎提交问题和合并请求。对于重大更改,请先开issue讨论您想要改变的内容。

## 联系方式

如有任何问题或建议,请联系 [your-email@example.com](mailto:your-email@example.com)。

希望这个README能够全面介绍项目的功能和使用方法。如果还需要补充或修改的地方,请告诉我。