# 学习心跳上报

> 原始接口名：saveLearnHertRecord

按固定间隔上报学习心跳并累计学习时长。

POST https://learn.baowugroup.com/learn-gateway/service/tms/ols/learnHertRecord/saveLearnHertRecord

## 接口概览

- 接口作用：按固定间隔上报学习心跳，累计学习时长，是平台计算视频学习进度的核心接口之一。
- 调用时机：在视频持续播放过程中定时调用，通常会周期性发送，直到本次播放结束或暂停。
- 前置条件：已完成登录并携带有效 `token`，已通过学习初始化接口拿到 `pageId`，并已明确当前视频的 `cataNo`、`wareId`、`wareType`。
- 后续依赖：心跳上报通常会持续贯穿整个播放过程，并与动作事件、打点和完成度计算接口配合使用。

## 请求示例

这个请求示例展示了播放器正常播放时的一次心跳上报。它主要用于告诉服务端当前播放到哪里、这段时间累计了多少有效学习时长。

### 请求字段说明

- `curPlayTime`: 当前播放位置。
- `learnTime`: 本次上报对应的累计学习时长。
- `learnRealTime`: 真实学习时长，通常与心跳间隔对应。
- `pageId`: 当前学习页面会话标识。
- `isBlur`: 页面是否失焦。

### 请求体

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

## 响应示例

响应结果通常只需要关注本次心跳是否被接受。若返回成功，播放器可继续按既定周期发送下一次心跳。

### 响应字段说明

- `data.status`: 心跳是否被服务端接受。
- `data.heartDesc`: 服务端返回的处理结果说明。

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
