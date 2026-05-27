# saveLearnHertRecord

保存观看记录心跳

POST https://learn.baowugroup.com/learn-gateway/service/tms/ols/learnHertRecord/saveLearnHertRecord

## Request

```json
{
  "cataNo": "2042131390983704576",
  "classCourseCenterCode": "C001",
  "courseNo": "1L2BSTA000240",
  "curPlayTime": "00:08:00",
  "isBlur": "0",
  "learnRealTime": 60,
  "learnTime": 60,
  "olClassNo": "1997868434762895360",
  "pageId": "b417d84d-2883-4d67-b9da-fdba161f9b94",
  "status": "1",
  "videoSpeed": 1,
  "wareId": "2042131465256439808",
  "wareType": "1"
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
    "status": "success",
    "heartDesc": "成功"
  },
  "encrypt": false,
  "encryptType": "1"
}
```
