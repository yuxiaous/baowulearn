# 学习记录初始化

初始化一次课程学习会话。

POST https://learn.baowugroup.com/learn-gateway/service/tms/ols/learnRecord/initLearnRecord

## 接口概览

- 接口作用：初始化一次课程学习会话，建立后续心跳、打点和播放事件上报所依赖的学习上下文。
- 调用时机：在进入课程页面、准备开始学习前调用，通常每次新的学习页面会话都要调用一次。
- 前置条件：已完成登录并携带有效 `token`，已经获得 `courseNo` 和 `olClassNo`，并已为本次页面会话生成唯一的 `pageId`。
- 后续依赖：初始化成功后，后续心跳、打点和部分播放事件都会复用同一个 `pageId`。

## 请求示例

这个请求示例展示了学习链路真正开始前的会话初始化动作。它负责把当前课程和页面会话绑定起来。

### 请求字段说明

- `courseNo`: 目标课程编号。
- `olClassNo`: 当前课程所属班级或专区编号。
- `pageId`: 本次学习页面会话标识。

### 请求体

```json
{
  "courseNo": "1L2BSTA000240",
  "olClassNo": "1997868434762895360",
  "pageId": "b417d84d-2883-4d67-b9da-fdba161f9b94" // 
}
```

## 响应示例

初始化成功后，响应会给出当前会话默认要继续学习的视频节点和上次停留位置，便于播放器接续学习。

### 响应字段说明

- `data.cataNo`: 当前默认学习的视频目录节点。
- `data.wareCode`: 当前默认学习的视频资源编号。
- `data.lastPlayTime`: 上次学习停留位置，可用于恢复播放。

### 响应体

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
