import requests  # 用于发送HTTP请求
from bs4 import BeautifulSoup  # 用于解析HTML
import csv  # 用于处理CSV文件
import time  # 用于添加延迟和计时
import threading  # 用于多线程处理
import queue  # 用于线程间的安全数据交换
import os  # 用于操作系统相关功能
import multiprocessing  # 用于获取CPU核心数
import random  # 用于生成随机数

def get_headers():
    """
    返回一个包含HTTP请求头信息的字典
    这些头信息模拟了真实浏览器的请求,有助于绕过一些基本的反爬虫措施
    """
    return {
        'authority': 'ukuzy0.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        'cookie': 'cf_clearance=zIF_.5Zk4SeiXtZjwIAHBy9wUvQG_KnDj43xeLcW0Qw-1725442702-1.2.1.1-1f4.jnGV2mSS4FY0ubprTjptnYxDZTINgXA0gJkY2kJ94hchTmxEVM_jOncDraSSwmO3o37doHre_fYimy99QlLcjz2h180YSERPXgNHFHwJqCF1iFzt.FquP09QlbSHZofD3KwYBZ_0cCV_sH6H4h7yGPZkNTbPH8p3QDzT4.ofuCWgyZX1j0dLIolCjzD0hz2YmsjpI2DK3ar.Va9oQDOTFvRc6DLu59J6Gz403ilSkohg.lsjO4dLgD8az.qAA6JgdWlAaoCdj9.nO4sjlAajvVeuqZrI4E0_iS7q21Gmgw0pbxlKfnBOO6N_6XuE80_OK3QLRlWhvqiq45lHWyRvTN2J5T0m725DcE7IW6NpaCgUgUrygdCkM0CpnfDH',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
    }

def get_movie_details(url):
    """
    从给定的URL获取电影详情
    
    参数:
    url (str): 电影详情页的URL
    
    返回:
    dict: 包含电影详情的字典,如果获取失败则返回None
    """
    try:
        # 发送GET请求获取页面内容
        response = requests.get(url, headers=get_headers(), timeout=10)
        # 使用BeautifulSoup解析HTML内容
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 获取电影标题
        title_element = soup.find('h2')
        if title_element is None:
            print(f"无法找到标题元素,URL: {url}")
            return None
        title = title_element.text.strip()
        
        # 获取电影信息
        info_element = soup.find('div', class_='vodinfobox')
        if info_element is None:
            print(f"无法找到信息元素,URL: {url}")
            return None
        info = info_element.text.strip()
        
        # 初始化电影信息变量
        director = ''
        actors = ''
        genre = ''
        region = ''
        language = ''
        release_date = ''
        
        # 解析电影信息
        for line in info.split('\n'):
            if '导演：' in line:
                director = line.split('：')[1].strip()
            elif '主演：' in line:
                actors = line.split('：')[1].strip()
            elif '类型：' in line:
                genre = line.split('：')[1].strip()
            elif '地区：' in line:
                region = line.split('：')[1].strip()
            elif '语言：' in line:
                language = line.split('：')[1].strip()
            elif '上映：' in line:
                release_date = line.split('：')[1].strip()
        
        # 获取播放链接
        play_1_element = soup.find('div', id='play_1')
        play_link = ''
        if play_1_element:
            first_link = play_1_element.find('a')
            if first_link:
                play_link = first_link['href']
        
        # 获取封面图片
        cover_img_element = soup.find('div', class_='vodImg')
        cover_image = cover_img_element.find('img')['src'] if cover_img_element and cover_img_element.find('img') else ''
        
        # 获取剧情简介
        plot_summary_element = soup.find('div', class_='vodplayinfo')
        plot_summary = plot_summary_element.text.strip() if plot_summary_element else ''
        
        # 获取评分
        rating_element = soup.find('div', class_='vodh')
        rating = rating_element.find('label').text.strip() if rating_element and rating_element.find('label') else ''
        
        # 返回包含所有信息的字典
        return {
            '标题': title,
            '导演': director,
            '主演': actors,
            '类型': genre,
            '地区': region,
            '语言': language,
            '上映日期': release_date,
            '播放链接': play_link,
            '封面图片': cover_image,
            '剧情简介': plot_summary,
            '评分': rating
        }
    except Exception as e:
        print(f"获取电影详情时出错: {url}, 错误: {str(e)}")
        return None

def worker(q, writer, lock):
    """
    工作线程函数,不断从队列中获取URL并处理
    
    参数:
    q (Queue): 包含待处理URL的队列
    writer (csv.DictWriter): CSV文件写入器
    lock (threading.Lock): 用于同步的锁对象
    """
    while True:
        url = q.get()
        if url is None:
            break
        movie_info = get_movie_details(url)
        if movie_info:
            with lock:
                writer.writerow(movie_info)
        else:
            print(f"无法获取电影信息: {url}")

def get_all_movies(num_threads):
    """
    获取所有电影信息并写入CSV文件
    
    参数:
    num_threads (int): 使用的线程数
    
    返回:
    int: 爬取的电影总数
    """
    base_url = 'https://ukuzy0.com/index.php/vod/type/id/1/page/{}.html'
    page = 1
    movie_count = 0
    
    q = queue.Queue()
    lock = threading.Lock()
    
    with open('movies.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
        fieldnames = ['标题', '导演', '主演', '类型', '地区', '语言', '上映日期', '播放链接', '封面图片', '剧情简介', '评分']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # 创建并启动工作线程
        threads = []
        for _ in range(num_threads):
            t = threading.Thread(target=worker, args=(q, writer, lock))
            t.start()
            threads.append(t)
        
        try:
            while True:
                url = base_url.format(page)
                print(f"\n开始爬取第 {page} 页: {url}")
                response = requests.get(url, headers=get_headers())
                soup = BeautifulSoup(response.text, 'html.parser')
                
                movie_links = soup.select('.xing_vb4 a')
                if not movie_links:
                    print("没有找到更多电影链接,爬取结束")
                    print("页面内容:")
                    print(soup.prettify()[:1000])  # 打印页面前1000个字符以进行调试
                    break
                
                print(f"在第 {page} 页找到 {len(movie_links)} 个电影链接")
                
                for link in movie_links:
                    movie_url = 'https://ukuzy0.com' + link['href']
                    q.put(movie_url)
                    movie_count += 1
                
                page += 1
                print(f"第 {page-1} 页爬取完成,当前共有 {movie_count} 部电影信息")
                
                # 添加随机延迟以避免被封禁
                time.sleep(random.uniform(2, 5))
        
        except KeyboardInterrupt:
            print("用户中断了爬取过程")
        
        except Exception as e:
            print(f"爬取过程中出错: {str(e)}")
        
        finally:
            # 发送结束信号给所有线程
            for _ in range(num_threads):
                q.put(None)
            
            # 等待所有线程结束
            for t in threads:
                t.join()
    
    return movie_count

def suggest_thread_count():
    """
    根据CPU核心数建议线程数量
    
    返回:
    int: 建议的线程数量
    """
    cpu_count = multiprocessing.cpu_count()
    suggested = min(cpu_count * 2, 20)  # 建议线程数不超过20
    return suggested

if __name__ == '__main__':
    # 程序入口点
    suggested_threads = suggest_thread_count()
    print(f"建议的线程数量: {suggested_threads}")
    num_threads = int(input(f"请输入要使用的线程数量 (建议 {suggested_threads}): "))
    
    start_time = time.time()
    print("开始爬取电影信息...")
    total_movies = get_all_movies(num_threads)
    end_time = time.time()
    print(f"爬取完成,共耗时 {end_time - start_time:.2f} 秒")
    print(f"总共爬取了 {total_movies} 部电影信息,并已保存到 movies.csv")