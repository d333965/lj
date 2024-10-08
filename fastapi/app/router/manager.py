from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.mysql.models import Manager
from fastapi.encoders import jsonable_encoder

router = APIRouter()

@router.post("/register")
async def register(request: Request):
    # 获取请求体数据
    data = await request.json()
    manager = data.get("manager")
    password = data.get("password")
    
    # 检查管理员名是否已存在
    existing_Manager = await Manager.filter(manager=manager).first()
    if existing_Manager:
        return JSONResponse(status_code=400, content={"code": 400, "message": "管理员名已存在"})
    
    # 创建新管理员
    await Manager.create(manager=manager, password=password)
    return JSONResponse(status_code=200, content={"code": 200, "message": "注册成功"})

@router.post("/login")
async def login(request: Request):
    # 获取请求体数据
    data = await request.json()
    manager = data.get("manager")
    password = data.get("password")
    
    # 查找管理员
    existing_Manager = await Manager.filter(manager=manager).first()
    if not existing_Manager:
        return JSONResponse(status_code=400, content={"code": 400, "message": "管理员名不存在"})
    
    # 验证密码
    if existing_Manager.password != password:
        return JSONResponse(status_code=400, content={"code": 400, "message": "密码错误"})
    
    # 登录成功
    return JSONResponse(status_code=200, content={"code": 200, "message": "登录成功"})

# 获取manager信息
@router.post("/getManagerScore")
async def getManagerScore(request: Request):
    # 获取请求体数据
    data = await request.json()
    manager = data.get("manager")
    
    # 查找管理员
    existing_Manager = await Manager.filter(manager=manager).first()

    if not existing_Manager:
        return JSONResponse(status_code=400, content={"code": 400, "message": "管理员名不存在"})
    
    if manager == "风飘儿":
        return JSONResponse(status_code=200, content={"code": 200, "message": "获取成功", "score": existing_Manager.score, "is_admin": True})

    return JSONResponse(status_code=200, content={"code": 200, "message": "获取成功", "score": existing_Manager.score})

# 获取全部manager信息
@router.post("/getAllManager")
async def getAllManager(request: Request):
    # 获取请求体数据
    data = await request.json()
    manager = data.get("manager")
    # 查找管理员
    existing_Manager = await Manager.filter(manager=manager, is_admin=True).first()
    if not existing_Manager:
        return JSONResponse(status_code=400, content={"code": 400, "message": "管理员无权限"})
    # 获取全部manager信息
    all_Manager = jsonable_encoder(await Manager.all().values())
    return JSONResponse(status_code=200, content={"code": 200, "message": "获取成功", "data": all_Manager})

# 修改manager信息
@router.post("/updateManager")
async def updateManager(request: Request):
    # 获取请求体数据
    data = await request.json()
    manager = data.get("manager")
    username = data.get("username")
    score = data.get("score")
    
    # 先检查manager的权限
    existing_Manager = await Manager.filter(manager=manager, is_admin=True).first()
    if not existing_Manager:
        return JSONResponse(status_code=400, content={"code": 400, "message": "管理员无权限"})
    
    # 修改manager信息
    await Manager.filter(manager=username).update(score=score)
    return JSONResponse(status_code=200, content={"code": 200, "message": "修改成功"})

    
