![getMovie](https://socialify.git.ci/kangvcar/getMovie/image?description=1&descriptionEditable=getMovie%20%E6%98%AF%E4%B8%80%E4%B8%AA%E5%85%88%E8%BF%9B%E7%9A%84%E7%94%B5%E5%BD%B1%E4%BF%A1%E6%81%AF%E9%87%87%E9%9B%86%E5%92%8C%E7%AE%A1%E7%90%86%E7%B3%BB%E7%BB%9F%EF%BC%8C%E4%B8%93%E4%B8%BA%E7%94%B5%E5%BD%B1%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E5%B8%88%E3%80%81%E5%BD%B1%E8%A7%86%E5%BA%94%E7%94%A8%E5%BC%80%E5%8F%91%E8%80%85%E5%92%8C%E7%94%B5%E5%BD%B1%E7%88%B1%E5%A5%BD%E8%80%85%E8%AE%BE%E8%AE%A1%E3%80%82&font=Bitter&forks=1&issues=1&language=1&name=1&owner=1&stargazers=1&theme=Auto)



getMovie 是一个先进的电影信息采集和管理系统，专为电影数据分析师、影视应用开发者和电影爱好者设计。本系统采用 Python 作为核心开发语言，结合了现代爬虫技术和数据处理方法，提供了一个强大而灵活的电影数据采集解决方案。

### 核心功能：

1. **多源数据采集**：支持从多个知名电影网站并发抓取数据，包括但不限于电影标题、导演、演员、类型、地区、语言、上映日期、播放链接、封面图片、剧情简介和评分等关键信息。

2. **智能解析引擎**：采用先进的 HTML 解析技术，能够适应不同网站的页面结构，准确提取所需信息。

3. **高性能并发爬取**：利用多线程技术，显著提高数据采集效率，同时通过智能调度算法避免对目标网站造成过大压力。

4. **数据清洗与结构化**：实时处理采集到的原始数据，进行格式统一、去重、错误修正等操作，确保数据的一致性和可用性。

5. **多样化存储选项**：支持将处理后的数据存入 MySQL 关系型数据库，便于后续的复杂查询和分析；同时提供 CSV 文件导出功能，方便数据共享和备份。

6. **断点续传与增量更新**：内置断点续传机制，支持意外中断后的继续采集；通过增量更新功能，有效避免重复采集，提高系统运行效率。

7. **全面的错误处理**：实现了完善的异常捕获和处理机制，确保系统在面对网络波动、数据异常等情况时能够稳定运行。

8. **详细的日志记录**：系统运行过程中的各项操作和状态变化都会被记录在日志中，方便后续的问题诊断和系统优化。

9. **灵活的配置管理**：通过配置文件可以轻松调整爬虫行为、数据处理规则和存储设置，无需修改代码即可适应不同的采集需求。

10. **中文编码支持**：针对中文网站和内容进行了特别优化，确保中文字符在采集、存储和显示过程中的正确处理。

### 应用场景：

- 电影推荐系统的数据支持
- 影视市场趋势分析
- 个人电影收藏管理
- 电影评分和评论分析
- 电影数据可视化项目
- 影视类移动应用和网站开发

getMovie 不仅仅是一个数据采集工具，它是连接海量电影信息与创新应用之间的桥梁。无论您是数据分析师、软件开发者，还是电影研究者，getMovie 都能为您提供丰富、准确、结构化的电影数据，助力您的项目开发和研究工作。


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


## 贡献

欢迎提交问题和合并请求。对于重大更改,请先开issue讨论您想要改变的内容。

## 联系方式

如有任何问题或建议,请联系 [kangvcar@gmail.com](mailto:kangvcar@gmail.com)。

希望这个README能够全面介绍项目的功能和使用方法。如果还需要补充或修改的地方,请告诉我。

