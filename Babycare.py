#by:哆啦A梦
#TL库
#入口:小程序-Babycare官方旗舰店
#抓包api.bckid.com.cn域名下的authorization，多账号换行分割

import os
import requests
import json

# 从环境变量中获取 token，支持多账号换行分割
tokens = os.environ.get('Babycare', '').split('\n')

# 定义 URL
url = "https://api.bckid.com.cn/operation/front/bonus/userSign/v3/sign"
primary_url = "https://github.com/3288588344/toulu/raw/refs/heads/main/tl.txt"
backup_url = "https://tfapi.cn/TL/tl.json"

# 定义请求头
headers = {
    "Host": "api.bckid.com.cn",
    "content-length": "2",
    "content-type": "application/json",
    "charset": "utf-8",
    "referer": "https://servicewechat.com/wxab5642d7bced2dcc/447/page-frame.html",
    "accept-encoding": "gzip, deflate, br"
}

def print_divider():
    print("\n" + "=" * 35)

def print_account_info(account_num, token):
    print_divider()
    print(f"🤖 正在为账号 {account_num} 签到...")
    print_divider()

def print_sign_success(account_num, result):
    print_divider()
    print(f"🎉 账号 {account_num} 签到成功！")
    print(f"💪 最大连续签到天数: {result.get('maxSignDay', '信息获取失败')}")
    print(f"📅 当前连续签到天数: {result.get('signDaysCount', '信息获取失败')}")
    print(f"🎁 抽奖机会: {result.get('lotteryCount', '信息获取失败')}")
    print_divider()

def print_already_signed(account_num):
  
    print(f"👻 账号 {account_num} 今天已经签到过了，请明天再来！")
    print_divider()

def print_sign_failed(account_num, message):
    
    print(f"❌ 账号 {account_num} 签到失败！错误信息: {message}")
    print_divider()

def print_empty_token(account_num):
    
    print(f"⚠️ 账号 {account_num} 的 token 为空，跳过")
    print_divider()

def print_request_error(account_num, error):
    
    print(f"⚠️ 账号 {account_num} 请求异常: {error}")
    print_divider()


print("🚀 开始执行签到任务")
# 添加账号编号提示
for idx, token in enumerate(tokens, start=1):
    if not token.strip():
        print_empty_token(idx)
        continue

    print_account_info(idx, token)
    headers["authorization"] = token.strip()

    try:
        response = requests.post(url, headers=headers, data=json.dumps({}))
        
        if response.status_code == 200:
            json_response = response.json()
            if json_response.get("code") == "200":
                print_sign_success(idx, json_response.get('body', {}))
            elif json_response.get("code") == "400":
                print_already_signed(idx)
            else:
                print_sign_failed(idx, json_response.get("message", "未知错误"))
        else:
            print_sign_failed(idx, f"HTTP状态码: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print_request_error(idx, e)
    except json.JSONDecodeError:
        print_sign_failed(idx, "响应内容不是有效的 JSON 格式")


print("🏆 所有账号签到任务完成！")
print_divider()
