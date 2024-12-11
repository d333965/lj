# main.py
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.router.manager import router as manager_router
from app.router.legymCustomer import router as legymCustomer_router
# tortoise-orm
from tortoise.contrib.fastapi import register_tortoise
from app.mysql.settings import TORTOISE_ORM
from tortoise import Tortoise
from app.router.Epay.index import router as epay_router

app = FastAPI()

async def init():
    db_url = f"mysql://{TORTOISE_ORM['connections']['default']['credentials']['user']}:" \
             f"{TORTOISE_ORM['connections']['default']['credentials']['password']}@" \
             f"{TORTOISE_ORM['connections']['default']['credentials']['host']}:" \
             f"{TORTOISE_ORM['connections']['default']['credentials']['port']}/" \
             f"{TORTOISE_ORM['connections']['default']['credentials']['database']}"
    
    await Tortoise.init(
        db_url=db_url,
        modules={'models': ['app.mysql.models']}
    )
    await Tortoise.generate_schemas()

# 在这里注册Tortoise
register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=False,
    add_exception_handlers=True,
)

# 注册路由
app.include_router(manager_router, prefix="/api/manager")
app.include_router(legymCustomer_router, prefix="/api/legymCustomer")
app.include_router(epay_router, prefix="/api/epay")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法，包括 POST 和 OPTIONS
    allow_headers=["*"],  # 允许所有头部
)

@app.on_event("startup")
async def startup_event():
    await init()

@app.on_event("shutdown")
async def shutdown_event():
    await Tortoise.close_connections()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
