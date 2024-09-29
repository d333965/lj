from fastapi import APIRouter, Request
from app.router.Epay.epay_config import epay_config
from app.router.Epay.EpayCore import EpayCore
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.mysql.models import Manager

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post("/epay_order")
async def epay_order(request: Request):
    data = await request.json()
    notify_url = request.url_for('notify_url')
    return_url = request.url_for('return_url')

    manager = data.get('manager')
    score = int(data.get('score'))
    name = str(score) + "乐点 == " + str(manager)
    money = float(data.get('price'))
    out_trade_no = str(data.get('out_trade_no'))

    parameter = {
        "pid": epay_config['pid'],  # 商户ID
        "type": "alipay",  # 支付类型
        "notify_url": notify_url,  # 通知URL
        "return_url": return_url,  # 返回URL
        "out_trade_no": out_trade_no,  # 商户订单号
        "name": name,  # 商品名称
        "money": money,  # 订单金额
    }
    epay = EpayCore(epay_config)
    if not epay.verify_score(score, money):
        return {"error": "验证失败"}
    
    html_text = epay.page_pay(parameter)
    
    return HTMLResponse(content=html_text)

@router.get("/notify_url")
async def notify_url(request: Request):
    epay = EpayCore(epay_config)
    if epay.verify_notify(dict(request.query_params)):
        trade_status = request.query_params.get('trade_status')
        if trade_status == 'TRADE_SUCCESS':
            # 在这里处理订单逻辑
            pass

        return "success"
    else:
        return "fail"

@router.get("/return_url")
async def return_url(request: Request):
    epay = EpayCore(epay_config)
    if epay.verify_return(dict(request.query_params)):
        trade_status = request.query_params.get('trade_status')
        name = request.query_params.get('name')

        if trade_status == 'TRADE_SUCCESS':
            # 提取name中的数字
            score = int(name.split("乐点 == ")[0])
            manager = name.split("乐点 == ")[1]
            # 更新manager的score
            manager = await Manager.get(manager=manager)
            manager.score += score
            await manager.save()
            pass

        return templates.TemplateResponse("return.html", {"request": request, "verify_result": "验证成功"})
    else:
        return templates.TemplateResponse("return.html", {"request": request, "verify_result": "验证失败"})
