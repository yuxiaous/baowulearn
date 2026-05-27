# getMaxTimeAndLastTime

获取课程的播放时间信息

POST https://learn.baowugroup.com/learn-gateway/service/tms/ols/learnWareProgress/getMaxTimeAndLastTime

## Request

```json
{
    "cataNo": "2042131486236348416",
    "courseNo": "1L2BSTA000240",
    "olClassNo": "1997868434762895360",
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
        "guid": null,
        "olClassNo": "1997868434762895360",
        "stuCode": "<学员工号>",
        "courseNo": "1L2BSTA000240",
        "cataNo": "2042131486236348416",
        "wareId": "2042131531195092992",
        "markeTimePoint": null,
        "maxPlayTime": "00:04:49",
        "lastPlayTime": "00:00:06",
        "lastUpateTime": null,
        "createUser": null,
        "createTime": null,
        "updateUser": null,
        "updateTime": null,
        "deleteUser": null,
        "deleteTime": null,
        "deleteFlag": null,
        "tenantCode": null,
        "centerCode": null,
        "learnRealTime": null
    },
    "encrypt": false,
    "encryptType": "1"
}
```
