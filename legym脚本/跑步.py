from login import LoginGetInfo,getsemesterId,Oct_SecretKey
from routeLine import getRouteLine
from runTask import runTask
账号 = '17886920656'
密码 = 'XQYun0822'
n = 2  #补跑前面第几天的
day_goals = 2.4 #每天跑步公里数
runType = '自由跑'

schoolName = '西油成都' #轻化工和中飞院填校区
rounds = 6 #跑步圈数



accessToken, schoolId, campusId, userId = LoginGetInfo(账号, 密码)
OctSecretKey = Oct_SecretKey(userId, schoolId)
routine_line = getRouteLine(schoolName, rounds)
semesterId = getsemesterId(accessToken, schoolId)

max_attempts = 1
attempt_count = 0

while attempt_count < max_attempts:
    message = runTask(day_goals, accessToken, semesterId, routine_line, runType, OctSecretKey,n)
    print(f"尝试 {attempt_count + 1}: {message}")
    
    if message == "success":
        attempt_count += 1
    else:
        break

print(f"总共成功执行 {attempt_count} 次")
