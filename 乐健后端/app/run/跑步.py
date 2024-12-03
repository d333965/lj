import asyncio
from tortoise import Tortoise
from login import LoginGetInfo, getsemesterId, Oct_SecretKey
from routeLine import getRouteLine
from runTask import runTask
import sys
import os
from datetime import datetime
import schedule
import time

# 获取当前文件所在目录的上一级目录
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '../../'))

# 将项目根目录添加到 sys.path
sys.path.append(root_dir)

from app.mysql.models import LegymCustomer
from app.mysql.settings import get_tortoise_config

# 初始化数据库连接
async def init_db():
    config = get_tortoise_config()
    await Tortoise.init(config=config)
    await Tortoise.generate_schemas()

# 开始跑步
async def start_run(customer):
    # 检查是否完成总目标
    if customer.complete_goals >= customer.total_goals:
        await customer.delete()
        message = "完成目标"
        return message

    # 检查本周任务是否完成day_in_week
    if customer.complete_day_in_week >= customer.day_in_week:
        customer.is_run = True
        await customer.save()
        message = "完成目标"
        return message
    
    # 检查是否完成跑步
    if customer.is_run:
        message = "完成目标"
        return message

    # 检查是否暂停
    if customer.begin_state == False:
        message = "完成目标"
        return message
    

    # 检查当前时间是否在跑步时间内
    current_hour = datetime.now().hour
    run_times = customer.runTime.split(',')
    is_run_time = any(start <= current_hour < end for time_range in run_times for start, end in [map(int, time_range.split('~'))])

    if not is_run_time:
        message = "不在跑步时间"
        return message
    

    账号 = customer.username
    密码 = customer.password
    n = 0  # 补跑前面第几天的
    day_goals = customer.day_goals  # 每天跑步公里数
    runType = customer.runType

    schoolName = customer.schoolName  
    rounds = customer.rounds  # 跑步圈数

    accessToken, schoolId, userId = LoginGetInfo(账号, 密码)
    if accessToken == 404:
        message = "登录失败"
        return message
    OctSecretKey = Oct_SecretKey(userId, schoolId)
    try:
        routine_line = getRouteLine(schoolName, rounds)
    except Exception as e:
        message = "路线失败"
        return message

    semesterId = getsemesterId(accessToken, schoolId)

    message = runTask(day_goals, accessToken, semesterId, routine_line, runType, OctSecretKey, n)
    return message

# 主程序
async def main():
    await init_db()

    customers = await LegymCustomer.all().order_by('-id')
    # 如果现在时间在01:00~06:00之间，则重置is_run=False
    if datetime.now().hour >= 1 and datetime.now().hour < 6:
        for customer in customers:
            customer.is_run = False
            await customer.save()
        # 检查今天是否为周一
        if datetime.now().weekday() == 0:
            for customer in customers:
                customer.complete_day_in_week = 0
                await customer.save()

    # 不在01:00~06:00之间，则开始跑步
    else:
        for customer in customers:
            try:
                message = await start_run(customer)
            except:
                continue
            # 完成目标或者不在跑步时间
            if message == "完成目标" or message == "不在跑步时间" or message == "登录失败" or message == "路线失败":
                continue
        
            # 跑步成功
            if message == None:
                customer.complete_goals += customer.day_goals
                customer.complete_day_in_week += 1
                customer.is_run = True
                print(customer.username, customer.password, "跑步成功")
                await customer.save()

    # 关闭数据库连接
    await Tortoise.close_connections()

# 新增一个包装函数来运行异步的 main 函数
def run_main():
    asyncio.run(main())

# 修改运行部分
if __name__ == "__main__":
    # 设置每10分钟运行一次主程序
    schedule.every(10).minutes.do(run_main)

    # 持续运行调度器
    while True:
        schedule.run_pending()
        time.sleep(1)
