# 账号登录

完成账号密码登录并获取访问令牌。

POST https://learn.baowugroup.com/learn-gateway/service/ss/auth/user/login

## 接口概览

- 接口作用：完成账号登录，并返回后续业务接口需要使用的访问令牌。
- 调用时机：在首次进入系统、令牌失效或需要重新建立登录态时调用。
- 前置条件：已准备登录用户名、密码和验证码标识，且登录用户名与密码已经按平台要求完成 SM2 加密。
- 后续依赖：登录成功后，课程、视频、统计相关接口都依赖本接口返回的 `accessToken`。

## 请求示例

这个请求示例展示了密码登录所需的最小请求体。核心输入是加密后的登录凭据和验证码上下文。

### 请求字段说明

- `loginName`: 加密后的登录用户名。
- `password`: 加密后的登录密码。
- `captchaId`: 当前验证码会话标识。
- `type`: 登录方式，示例中为密码登录。
- `clientType`: 客户端类型，示例中为 `PC`。

### 请求体

```json
{
    "mobile": "",
    "loginName": "<SM2加密的登录用户名>",
    "password": "<SM2加密的登录密码>",
    "captchaCode": "0",
    "captchaNum": "",
    "captchaId": "<验证码ID>",
    "type": "byPassword",
    "clientType": "PC"
}
```

## 响应示例

登录成功后，返回值中的 `data` 对象会给出访问令牌、过期时间以及当前租户信息。后续接口最直接依赖的是访问令牌。

### 响应字段说明

- `data.accessToken`: 后续业务接口请求头中的 `token` 值。
- `data.expiresTime`: 令牌过期时间，可用于判断是否需要重新登录。
- `data.tenantCode`: 后续部分接口会直接使用该租户标识。
- `data.userPermissionType`: 当前用户权限类型。

### 响应体

```json
{
    "isSuccess": true,
    "statusCode": 200,
    "message": "",
    "jwt": null,
    "data": {
        "userName": "<用户名称>",
        "loginName": "<登录用户名>",
        "clientType": "PC",
        "tenantCode": "BSTA",
        "accessToken": "<token>",
        "refreshToken": null,
        "expiresTime": 1779984036252000,
        "centerCode": null,
        "userPermissionType": "0",
        "tenantList": [
            {
                "tenantName": "中国宝武集团有限公司",
                "tenantCode": "BSTA"
            }
        ]
    },
    "encrypt": false,
    "encryptType": "1"
}
```
