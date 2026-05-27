# totalFinishStatistics

获取专区完成情况-总体情况

POST https://learn.baowugroup.com/learn-gateway/service/tms/ols/onlineClass/totalFinishStatistics

## Request

```json
{
    "centerCode": "C001",
    "olClassNo": "2048570976672813056",
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
        "passScore": "100",
        "learnScore": "20.83333",
        "strategyTip": null,
        "strategyDesc": "在专区考试栏目里，要求直播课程结束后一周内完成该门课程考试。",
        "learnStatus": "1",
        "details": [
            {
                "attributeCode": "ZE001",
                "attributeName": "选修课程学时",
                "percentage": "50",
                "finishValue": "52.50000",
                "attributeUnit": "课时",
                "predValue": "126"
            },
            {
                "attributeCode": "ZE013",
                "attributeName": "学习要求（考试）",
                "percentage": "50",
                "finishValue": "4.00000",
                "attributeUnit": "门",
                "predValue": "12"
            }
        ]
    },
    "encrypt": false,
    "encryptType": "1"
}
```
