import os
import markdown
from markdown import extensions
from markdown.treeprocessors import Treeprocessor
import re
from tqdm import tqdm
import logging
import requests

logging.basicConfig(level=logging.INFO)

error_urls = []

def markdown_parser(file_path):
    urls = []
    paper_pattern = '\[\[paper\]\((.*?)\)\]'
    with open(file_path) as f:
        for line in f.readlines():
            match = re.search(paper_pattern, line)
            if match:
                url = match.group(1)
                if url != "":
                    urls.append(url)
    
    # print(urls)
            # print("\n")
    return urls

def papers_url_normalize(urls):
    '''
    下载论文
    '''
    download_urls = []
    for url in tqdm(urls):
        items = str(url).split("/")
        # print(items)
        category = items[3]
        # print(category)
        if category == "abs":
            alter_url = url.replace("abs","pdf")
            alter_url = alter_url + ".pdf"
            # print(alter_url)
        elif category == "pdf":
            alter_url = url
        else:
            alter_url = url

        # print(alter_url)
        download_urls.append(alter_url)
    # print(download_urls)
    return download_urls

def download_pdf(urls,save_dir):

    if len(urls) == 0:
        return
    
    if os.path.isdir(save_dir):
        pass
    else:
        os.mkdir(save_dir)
    for url in tqdm(urls):
        try:
            response = requests.get(url,stream=True,timeout=5)
            response.raise_for_status()
            content = response.content
            pdf_path = os.path.join(save_dir,url.split("/")[-1])
            with open(pdf_path, 'wb') as f:
                f.write(content)
        except requests.exceptions.Timeout:
            print('下载超时，正在处理响应')
            error_urls.append("{}:{}".format(url,"time out"))
            continue
        except requests.exceptions.ConnectionError as e:
            print('下载失败，正在处理响应')
            error_urls.append("{}:{}".format(url,e))
            continue
        except requests.exceptions.HTTPError as e:
            print('HTTP错误:', e)
            error_urls.append("{}:{}".format(url,e))
            continue
        except requests.exceptions.RequestException as e:
            print('请求异常:', e)
            error_urls.append("{}:{}".format(url,e))
            continue
        except Exception as e:
            print('其他异常:', e)
            error_urls.append("{}:{}".format(url,e))
            continue



if __name__ == "__main__":
    file_path = 'README.md'
    urls = markdown_parser(file_path)
    downloads_urls = papers_url_normalize(urls)
    # print(downloads_urls,len(downloads_urls))
    download_pdf(downloads_urls,"./papers")
    print("下载完成")
    logging.info(error_urls)
