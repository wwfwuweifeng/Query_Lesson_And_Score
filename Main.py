import requests
from query_score import query_score
from query_course import query_course

if __name__=='__main__':
    code=input("请输入学号：")
    pwd=input("请输入密码：")
    session = requests.Session()
    data = {'stuid':code, 'pwd': pwd}
    url = 'http://222.194.15.1:7777/pls/wwwbks/bks_login2.login?jym2005=14587.549670888036'
    result = session.post(url, data)
    s= result.text
    if s.find('不能登录')>0:    #登录失败
        print('密码或学号错误')
    else:
        print("1、成绩查询")
        print("2、课表查询")
        select=input("请输入你的选择(1 or 2)：")
        if select=='1':
            scores=query_score(session)
            for line in scores:
                print(line)
        elif select=='2':
            startdate=input("请输入开学日期(2017-01-01)：")
            query_course(session,startdate)
        else:
            print("输入错误")