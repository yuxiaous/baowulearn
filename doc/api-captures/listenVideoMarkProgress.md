# listenVideoMarkProgress

根据mark时间打卡

POST https://learn.baowugroup.com/learn-gateway/service/tms/ols/learnWareProgress/listenVideoMarkProgress

## Request

```json
{
    "cataNo": "2042131486236348416",
    "courseNo": "1L2BSTA000240",
    "curPlayTime": "00:00:35",
    "markeTimePoint": "00:00:35",
    "olClassNo": "1997868434762895360",
    "pageId": "bb914acf-2fac-4530-a034-0fd8bfc5ea95",
    "wareId": "2042131531195092992",
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
