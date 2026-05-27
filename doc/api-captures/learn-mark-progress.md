# 关键时间点打卡

> 原始接口名：listenVideoMarkProgress

在关键打点时间上报一次学习进度。

POST https://learn.baowugroup.com/learn-gateway/service/tms/ols/learnWareProgress/listenVideoMarkProgress

## 接口概览

- 接口作用：在视频播放到关键打点时间时上报一次学习进度，帮助平台确认该时间点已经被有效观看。
- 调用时机：在播放过程中，当播放时间到达课程目录接口返回的 `markeTimePoint` 时调用。
- 前置条件：已完成登录并携带有效 `token`，已拿到 `pageId`，且已经通过课程目录接口拿到当前视频的 `markeTimePoint`。
- 后续依赖：该接口通常与心跳接口并行使用，成功后继续正常播放并等待下一个打点时间。

## 请求示例

这个请求示例展示了视频在某个关键打点时间触发的进度上报。打点时间本身来自课程目录接口返回值。

### 请求字段说明

- `curPlayTime`: 当前实际播放时间。
- `markeTimePoint`: 需要打卡的时间点。
- `pageId`: 当前学习页面会话标识。
- `cataNo`、`wareId`、`wareType`: 当前视频标识。

### 请求体

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

## 响应示例

响应结果通常很简单，重点是判断这次打点是否被服务端接受。

### 响应字段说明

- `data.status`: 打点上报是否成功。
- `data.heartDesc`: 服务端返回的结果说明。

### 响应体

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
