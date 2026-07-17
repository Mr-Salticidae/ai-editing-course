# -*- coding: utf-8 -*-
"""把本地 Markdown 推送到钉钉知识库。

用法:
  python scripts/dingtalk_push.py check                 # 验证凭证是否可用
  python scripts/dingtalk_push.py spaces                # 列出可见的知识库(找 spaceId)
  python scripts/dingtalk_push.py nodes <spaceId>       # 列出知识库根目录节点
  python scripts/dingtalk_push.py push <spaceId> <md文件> [parentNodeId]

凭证放在 scripts/.dingtalk.env (不入库), 格式:
  DINGTALK_APP_KEY=xxx
  DINGTALK_APP_SECRET=xxx
  DINGTALK_OPERATOR_UNIONID=xxx   # 或者提供 DINGTALK_MOBILE 由脚本解析
  DINGTALK_MOBILE=138xxxxxxxx     # 可选, 用于换取 unionId
"""
import json
import sys
import urllib.request
from pathlib import Path

ENV_PATH = Path(__file__).parent / ".dingtalk.env"
API = "https://api.dingtalk.com"
OAPI = "https://oapi.dingtalk.com"


def load_env():
    if not ENV_PATH.exists():
        sys.exit(f"缺少凭证文件: {ENV_PATH}")
    env = {}
    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env


def http(method, url, headers=None, body=None):
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        sys.exit(f"HTTP {e.code} {url}\n{detail}")


def get_token(env):
    r = http("POST", f"{API}/v1.0/oauth2/accessToken",
             body={"appKey": env["DINGTALK_APP_KEY"],
                   "appSecret": env["DINGTALK_APP_SECRET"]})
    return r["accessToken"]


def get_union_id(env, token):
    if env.get("DINGTALK_OPERATOR_UNIONID"):
        return env["DINGTALK_OPERATOR_UNIONID"]
    mobile = env.get("DINGTALK_MOBILE")
    if not mobile:
        sys.exit("请在 .dingtalk.env 里提供 DINGTALK_OPERATOR_UNIONID 或 DINGTALK_MOBILE")
    # 旧版 oapi 需要单独的 access_token
    r = http("GET", f"{OAPI}/gettoken?appkey={env['DINGTALK_APP_KEY']}"
                    f"&appsecret={env['DINGTALK_APP_SECRET']}")
    old_token = r["access_token"]
    r = http("POST", f"{OAPI}/topapi/v2/user/getbymobile?access_token={old_token}",
             body={"mobile": mobile})
    userid = r["result"]["userid"]
    r = http("POST", f"{OAPI}/topapi/v2/user/get?access_token={old_token}",
             body={"userid": userid})
    union_id = r["result"]["unionid"]
    print(f"unionId = {union_id}  (可写入 .dingtalk.env 的 DINGTALK_OPERATOR_UNIONID 免重复解析)")
    return union_id


def auth_headers(token):
    return {"x-acs-dingtalk-access-token": token}


def cmd_check(env):
    token = get_token(env)
    print("accessToken OK")
    uid = get_union_id(env, token)
    print(f"operator unionId OK: {uid}")


def cmd_spaces(env):
    token = get_token(env)
    uid = get_union_id(env, token)
    r = http("GET", f"{API}/v1.0/wiki/spaces?operatorId={uid}&maxResults=50",
             headers=auth_headers(token))
    print(json.dumps(r, ensure_ascii=False, indent=2))


def cmd_nodes(env, space_id):
    token = get_token(env)
    uid = get_union_id(env, token)
    r = http("GET", f"{API}/v1.0/wiki/spaces/{space_id}/nodes"
                    f"?operatorId={uid}&maxResults=50",
             headers=auth_headers(token))
    print(json.dumps(r, ensure_ascii=False, indent=2))


def cmd_push(env, space_id, md_path, parent_node_id=None):
    md = Path(md_path)
    if not md.exists():
        sys.exit(f"文件不存在: {md}")
    token = get_token(env)
    uid = get_union_id(env, token)
    body = {
        "operatorId": uid,
        "name": md.stem,
        "type": "FILE",
        "documentType": "adoc",
    }
    if parent_node_id:
        body["parentNodeId"] = parent_node_id
    r = http("POST", f"{API}/v1.0/wiki/spaces/{space_id}/nodes",
             headers=auth_headers(token), body=body)
    print("创建文档节点:", json.dumps(r, ensure_ascii=False, indent=2))
    # 内容写入在拿到真实返回结构后再对接具体接口(见 push 之后的迭代)


def main():
    env = load_env()
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    cmd = args[0]
    if cmd == "check":
        cmd_check(env)
    elif cmd == "spaces":
        cmd_spaces(env)
    elif cmd == "nodes" and len(args) >= 2:
        cmd_nodes(env, args[1])
    elif cmd == "push" and len(args) >= 3:
        cmd_push(env, args[1], args[2], args[3] if len(args) > 3 else None)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
