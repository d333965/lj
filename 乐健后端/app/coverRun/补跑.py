from .login import LoginGetInfo,getsemesterId,Oct_SecretKey
from .routeLine import getRouteLine
from .runTask import runTask

def coverRun(账号,密码,day1,day2,day_goals,schoolName,runType,rounds):
    try:
        # 简化日期逻辑
        days = []
        if day1: days.append(1)
        if day2: days.append(2)
        if not days:
            return ",补跑失败,请至少选择一天进行补跑"
            
        # 获取必要信息
        accessToken, schoolId, campusId, userId = LoginGetInfo(账号, 密码)
        OctSecretKey = Oct_SecretKey(userId, schoolId)
        routine_line = getRouteLine(schoolName, rounds)
        semesterId = getsemesterId(accessToken, schoolId)
        
        for n in days:
            runTask(day_goals, accessToken, semesterId, routine_line, runType, OctSecretKey, n)

        return ",补跑成功"
        
    except Exception as e:
        return f",补跑失败: {str(e)}"


