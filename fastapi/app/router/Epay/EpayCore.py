import requests
import hashlib
from urllib.parse import urlencode

class EpayCore:
    def __init__(self, config):
        self.pid = config['pid']
        self.key = config['key']
        self.submit_url = config['apiurl'] + 'submit.php'
        self.sign_type = 'MD5'

    def page_pay(self, param_tmp, button='支付'):
        param = self.build_request_param(param_tmp)
        html = f'''
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>正在跳转到支付页面</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    background-color: #f0f0f0;
                }}
                .container {{
                    text-align: center;
                    padding: 20px;
                    background-color: white;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                }}
                h1 {{
                    color: #333;
                }}
                .loader {{
                    border: 5px solid #f3f3f3;
                    border-top: 5px solid #3498db;
                    border-radius: 50%;
                    width: 50px;
                    height: 50px;
                    animation: spin 1s linear infinite;
                    margin: 20px auto;
                }}
                @keyframes spin {{
                    0% {{ transform: rotate(0deg); }}
                    100% {{ transform: rotate(360deg); }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>正在跳转到支付页面</h1>
                <div class="loader"></div>
                <p>请稍候，我们正在为您准备支付页面...</p>
                <form id="dopay" action="{self.submit_url}" method="post">
        '''
        for k, v in param.items():
            html += f'<input type="hidden" name="{k}" value="{v}"/>'
        html += f'''
                </form>
                <script>
                    setTimeout(function() {{
                        document.getElementById("dopay").submit();
                    }}, 1000);
                </script>
            </div>
        </body>
        </html>
        '''
        return html

    def verify_notify(self, params):
        if not params:
            return False
        sign = self.get_sign(params)
        return sign == params.get('sign')

    verify_return = verify_notify

    def build_request_param(self, param):
        param['sign'] = self.get_sign(param)
        param['sign_type'] = self.sign_type
        return param

    def get_sign(self, param):
        sorted_param = sorted([(k, v) for k, v in param.items() if k != "sign" and k != "sign_type" and v])
        param_str = "&".join([f"{k}={v}" for k, v in sorted_param])
        param_str += self.key
        return hashlib.md5(param_str.encode()).hexdigest()
    
    # 乐点验证
    def verify_score(self, score,money):
        if score < 0:
            return False
        elif score >= 200 and score <= 500:
            if score * 0.16 != money:
                return False
        elif score == 1000:
            if score * 0.14 != money:
                return False
        elif score == 2000:
            if score * 0.12 != money:
                return False
        elif score == 5000:
            if score * 0.1 != money:
                return False
        return True


        

        
