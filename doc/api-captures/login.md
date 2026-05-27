# login

登录

POST https://learn.baowugroup.com/learn-gateway/service/ss/auth/user/login

## Request

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

## Response

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
