# listenVideoOptRecord

发送视频播放事件

POST https://learn.baowugroup.com/learn-gateway/service/tms/ols/learnVideoRecord/listenVideoOptRecord

## Request

### 视频开始 - 开启或恢复时调用

```json
{
    "cataNo": "2042131486236348416",
    "classCourseCenterCode": "C001",
    "courseNo": "1L2BSTA000240",
    "olClassNo": "1997868434762895360",
    "operateType": "1",
    "videoBeginTime": "00:00:00",
    "videoSpeed": 1,
    "videoStatus": "1",
    "wareId": "2042131531195092992",
    "wareType": "1"
}
```

### 视频停止 - 暂停或结束时调用

```json
{
    "cataNo": "2042131486236348416",
    "classCourseCenterCode": "C001",
    "courseNo": "1L2BSTA000240",
    "olClassNo": "1997868434762895360",
    "operateType": "2",
    "videoBeginTime": "00:04:40",
    "videoSpeed": 1,
    "videoStatus": "2",
    "wareId": "2042131531195092992",
    "wareType": "1"
}
```


### 拖动进度条 - 拖动进度条时调用

```json
{
    "cataNo": "2042131486236348416",
    "classCourseCenterCode": "C001",
    "courseNo": "1L2BSTA000240",
    "olClassNo": "1997868434762895360",
    "operateType": "4",
    "videoBeginTime": "00:04:31",
    "videoSpeed": 1,
    "videoStatus": "1",
    "wareId": "2042131531195092992",
    "wareType": "1",
    "dragBeginTime": "00:04:03",
    "dragEndTime": "00:04:31"
}
```

### 成为焦点 - 从非焦点成为焦点时调用

```json
{
    "cataNo": "2042131486236348416",
    "classCourseCenterCode": "C001",
    "courseNo": "1L2BSTA000240",
    "olClassNo": "1997868434762895360",
    "operateType": "5",
    "videoBeginTime": "00:04:40",
    "videoSpeed": 1,
    "videoStatus": "1",
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
    "data": "true",
    "encrypt": false,
    "encryptType": "1"
}
```
