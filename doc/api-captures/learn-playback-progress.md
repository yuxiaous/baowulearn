# 历史播放进度查询

查询某个视频当前已经学习到的播放位置。

POST https://learn.baowugroup.com/learn-gateway/service/tms/ols/learnWareProgress/getMaxTimeAndLastTime

## 接口概览

- 接口作用：查询某个视频当前已经学习到的位置，便于进入播放器时恢复播放进度。
- 调用时机：在课程目录中选定具体视频后、真正开始播放前调用。
- 前置条件：已完成登录并携带有效 `token`，已通过课程目录接口拿到 `cataNo`、`wareId`、`wareType`，并已明确 `courseNo` 和 `olClassNo`。
- 后续依赖：拿到播放进度后，可据此恢复播放器位置，并继续发送播放事件、心跳和打点请求。

## 请求示例

这个请求示例用于查询单个视频的历史播放位置。它通常发生在播放器真正开始播放之前。

### 请求字段说明

- `cataNo`: 当前视频所在目录节点编号。
- `courseNo`: 课程编号。
- `olClassNo`: 公开课或专区班级编号。
- `wareId`: 视频资源编号。
- `wareType`: 资源类型，示例中视频为 `1`。

### 请求体

```json
{
    "cataNo": "2042131486236348416",
    "courseNo": "1L2BSTA000240",
    "olClassNo": "1997868434762895360",
    "wareId": "2042131531195092992",
    "wareType": "1"
}
```

## 响应示例

响应中的时间字段决定播放器应该从哪里恢复播放。通常会同时关注最大播放位置和最近一次播放位置。

### 响应字段说明

- `data.maxPlayTime`: 历史上已播放到的最大时间点。
- `data.lastPlayTime`: 最近一次播放停留的位置。
- `data.cataNo`、`data.wareId`: 可用于核对当前查询的视频对象。

### 响应体

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
