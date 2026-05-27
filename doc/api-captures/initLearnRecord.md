# initLearnRecord

初始化课程学习，在开始一个课程前发送

POST https://learn.baowugroup.com/learn-gateway/service/tms/ols/learnRecord/initLearnRecord

## Request

```json
{
  "courseNo": "1L2BSTA000240",
  "olClassNo": "1997868434762895360",
  "pageId": "b417d84d-2883-4d67-b9da-fdba161f9b94" // 
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
    "guid": null,
    "olClassNo": null,
    "stuCode": null,
    "courseNo": null,
    "learnDate": null,
    "beginTime": null,
    "endTime": null,
    "learnTime": null,
    "learnRealTime": null,
    "deviceId": null,
    "sessionId": null,
    "status": null,
    "createUser": null,
    "createTime": null,
    "updateUser": null,
    "updateTime": null,
    "deleteUser": null,
    "deleteTime": null,
    "deleteFlag": null,
    "tenantCode": null,
    "centerCode": null,
    "cataNo": "2042131390983704576",
    "wareCode": "2042131465256439808",
    "lastPlayTime": "00:07:00"
  },
  "encrypt": false,
  "encryptType": "1"
}
```
