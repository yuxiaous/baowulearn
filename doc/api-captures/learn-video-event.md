# 视频播放事件上报

> 原始接口名：listenVideoOptRecord

记录播放器中的关键动作事件。

POST https://learn.baowugroup.com/learn-gateway/service/tms/ols/learnVideoRecord/listenVideoOptRecord

## 接口概览

- 接口作用：记录播放器中的关键动作事件，帮助平台识别学习开始、暂停、拖动和焦点切换等行为。
- 调用时机：在播放器状态发生变化时调用，例如开始播放、暂停播放、拖动进度条或页面重新回到焦点时。
- 前置条件：已完成登录并携带有效 `token`，已明确当前播放视频的 `cataNo`、`wareId`、`wareType`，且 `courseNo`、`olClassNo` 已可用。
- 后续依赖：该接口与学习心跳、打点接口配合使用，共同构成完整的视频学习上报链路。

## 请求示例

这个接口会在不同播放器动作下重复调用，因此这里保留了多种典型请求体。核心差异主要体现在 `operateType` 和少数字段组合上。

### 请求字段说明

- `operateType`: 播放动作类型，区分开始、停止、拖动和焦点切换。
- `videoBeginTime`: 当前动作发生时的播放时间。
- `videoStatus`: 当前播放器状态。
- `videoSpeed`: 当前播放倍速。
- `dragBeginTime`、`dragEndTime`: 仅在拖动场景下使用。

### 场景说明

- `operateType: "1"`: 视频开始播放或恢复播放。
- `operateType: "2"`: 视频暂停播放或结束播放。
- `operateType: "3"`: 用户离开视频播放页面。
- `operateType: "4"`: 用户拖动进度条。
- `operateType: "5"`: 页面从失焦恢复到前台。

### 请求体

### operateType="1", videoStatus="1" - 视频开始播放或恢复播放

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

### operateType="2", videoStatus="2" - 视频暂停播放或结束播放

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

### operateType="3", videoStatus="0" - 用户离开视频播放页面

```json
{
    "cataNo": "2042131486236348416",
    "classCourseCenterCode": "C001",
    "courseNo": "1L2BSTA000240",
    "olClassNo": "1997868434762895360",
    "operateType": "3",
    "videoBeginTime": "00:04:31",
    "videoSpeed": 1,
    "videoStatus": "0",
    "wareId": "2042131531195092992",
    "wareType": "1"
}
```

### operateType="4", videoStatus="1" - 用户拖动进度条

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

### operateType="5", videoStatus="1" - 页面从失焦恢复到前台

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

## 响应示例

响应结果通常很简单，重点是确认服务端已经接收这次动作记录。

### 响应字段说明

- `data`: 返回 `"true"` 表示服务端已接收该次动作记录。

### 响应体

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
