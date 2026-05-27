# finishInfo

查询课程完成情况

POST https://learn.baowugroup.com/learn-gateway/service/tms/ols/onlineClassCourse/finishInfo

## Request

```json
{
  "centerCode": "C001",
  "courseNo": "1L2BSTA000240",
  "olClassNo": "1997868434762895360",
  "tenantCode": "BSTA"
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
        "totalScore": "100",
        "passScore": "60",
        "learnScore": "0.02",
        "strategyTip": null,
        "strategyDesc": null,
        "learnStatus": "1",
        "details": [
            {
                "attributeCode": "CE001",
                "attributeName": "考试",
                "percentage": "30",
                "finishValue": "0.00000",
                "attributeUnit": "分",
                "predValue": "100"
            },
            {
                "attributeCode": "CE002",
                "attributeName": "学习时长",
                "percentage": "70",
                "finishValue": "0.01667",
                "attributeUnit": "分钟",
                "predValue": "61"
            },
            {
                "attributeCode": "CE009",
                "attributeName": "课程调查",
                "percentage": "0",
                "finishValue": "未参加",
                "attributeUnit": "",
                "predValue": "1"
            }
        ]
    },
    "encrypt": false,
    "encryptType": "1"
}
```
