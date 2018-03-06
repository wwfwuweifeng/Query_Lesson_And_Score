import requests
from lxml import etree
import re
session = requests.Session()
data={'stuid':150410218,'pwd':1314520}
url='http://222.194.15.1:7777/pls/wwwbks/bks_login2.login?jym2005=14587.549670888036'
result=session.post(url,data)
s=result.text
print(s.find('不能登录'))
r=session.get('http://222.194.15.1:7777/pls/wwwbks/bkscjcx.curscopre')
selector=etree.HTML(r.text)
key=selector.xpath('//tr/td[@class="td_hz_bj"]/p/text()')
value=selector.xpath('//td[@class="td_biaogexian"]/p/text()')
judge_code=re.compile('^([A-Z]{2})([0-9]+)')
courses=[]

single_course = {}    #对象在外面定义
for i in range(len(value)):
    if judge_code.search(value[i]):
        single_course[key[2]]=value[i+1]    #课程名
        single_course[key[4]]=value[i+3]    #学分
    elif value[i]=='\xa0':
        if value[i-3]==' ' or len(value[i-3])>3:
            single_course[key[10]] = '暂无'  # 最后成绩
        else:
            single_course[key[10]]=value[i-3]   #最后成绩
        single_course[key[13]]=value[i-1]   #考试类型
        # print(single_course)
        #lesson=single_course    这样也不行，会导致courses里面的数据全部变成最后一项
        lesson={key[2]:single_course[key[2]],key[4]:single_course[key[4]],key[10]:single_course[key[10]],key[13]:single_course[key[13]]}
        courses.append(lesson)
# single_course[key[2]]='22'    #课程名
# single_course[key[4]]='22'    #学分
# single_course[key[10]] = '暂无'
# single_course[key[13]]='22'
print(courses)


