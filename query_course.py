from datetime import datetime,timedelta
from lxml import etree
from prettytable import PrettyTable


class oneclass():
    def __init__(self,name,adr,classify):
        self.name=name
        self.adr=adr
        self.classify=classify

def query_course(session,school_data):
    url='http://222.194.15.1:7777/pls/wwwbks/xk.CourseView'
    result=session.get(url)
    selector = etree.HTML(result.text)
    key=selector.xpath('//table/td[@class="td_hz_bj"]/p/text()')
    value=selector.xpath('//table[@class="table_biankuan"][2]//td[@class="td_biaogexian"]/p/text()')#后面的[2]表示第二个符合的table
    lessons=[]
    for i in range(len(value)//9):
        single_lesson={}
        adr=i*9;
        single_lesson[key[0]]=value[adr].replace('\xa0','')
        single_lesson[key[5]]=value[adr+5].replace('\xa0','')
        single_lesson[key[6]]=value[adr+6].replace('\xa0','')
        time=value[adr+7].replace('\xa0','').split('-')
        single_lesson['week']=time[0]
        single_lesson['time']=time[1]
        single_lesson[key[8]]=value[adr+8].replace('\xa0','')
        lessons.append(single_lesson)

    # for line in lessons:
    #     print(line)

    dates=school_data.split('-')
    startdate=datetime(int(dates[0]),int(dates[1]),int(dates[2]))   #这里已经默认开学不会放在周六周日
    start_week=startdate.weekday()          #开学那天是周几
    if start_week==5 or start_week==6:      #若输入的开学日期是周六或周日，则默认往后推至周一
        first_days=7
    else:
        first_days=7-start_week             #第一周有几天
    days=(datetime.today()-startdate).days+1      #两者相距多少天
    now_week=1
    if days>first_days:
        weeks=(days-first_days)//7
        leave_days=(days-first_days)%7
        # print(first_days,"---",weeks,"---",leave_days)
        if leave_days>0:
            now_week=weeks+2    #开学第一周+当前周，所以是2
        else:
            now_week=weeks+1
    else:       #还是在第一周
        now_week=1

    attend_weeks=[]     #用于存每门课上课的周次
    for lesson in lessons:
        weeks = []          #用于存一行的结果
        period = lesson['上课周次'].replace('周上', '')
        span = period.split(',')
        for one_period in span:         #每一个区间
            single = one_period.split('-')      #每一个区间的小区间
            if len(single) == 1:
                weeks.append(int(single[0]))
            else:
                for i in range(int(single[1]) + 1):
                    if i >= int(single[0]):
                        weeks.append(i)
        attend_weeks.append(weeks)      #所有课程的上课周次

    mon = [-1, -1, -1, -1, -1, -1, -1]
    tues = [-1, -1, -1, -1, -1, -1, -1]
    wed = [-1, -1, -1, -1, -1, -1, -1]
    thur = [-1, -1, -1, -1, -1, -1, -1]
    fri = [-1, -1, -1, -1, -1, -1, -1]
    sat = [-1, -1, -1, -1, -1, -1, -1]
    sun = [-1, -1, -1, -1, -1, -1, -1]
    week_course=[mon,tues,wed,thur,fri,sat,sun]
    for i in range(len(lessons)):
        if now_week in attend_weeks[i]:         #该门课在本周有课
            onelesson=oneclass(lessons[i]['课程名称'],lessons[i]['上课地点'],lessons[i]['考试类型'])
            week_course[int(lessons[i]['week'])-1][int(lessons[i]['time'])-1]=onelesson

    # for line in week_course:
    #     print(line)

    table=PrettyTable([" ", "星期一", "星期二", "星期三","星期四","星期五","星期六","星期日"])
    num_lesson=["第一大节","第二大节","第三大节","第四大节","第五大节","第六大节","第七大节"]
    table.align[" "] = "l"
    table.padding_width = 1  #
    for i in range(7):  #7大节课
        onerow=[]
        onerow.append(num_lesson[i])
        for j in range(7):  #7天
            if week_course[j][i]!=-1:
                temp=week_course[j][i]
                onerow.append(temp.name+"/"+temp.adr)
            else:
                onerow.append("无")
        table.add_row(onerow)

    print(table)

    # print(now_week)
        # day = timedelta(days=1)
        # data2=date+day*(-3)
        # print(data2)
