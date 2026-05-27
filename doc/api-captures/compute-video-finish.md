# 视频完成度重算

> 原始接口名：saveComputeTask4AfterVideoPlayed

在单个视频播放完成后触发一次服务端计算。

POST https://learn.baowugroup.com/learn-gateway/service/tms/ols/computeTask/saveComputeTask4AfterVideoPlayed

## 接口概览

- 接口作用：在单个视频播放完成后触发一次服务端计算任务，推动视频完成状态落库。
- 调用时机：在视频达到完成条件后调用，通常发生在播放结束或达到平台认可的完成阈值时。
- 前置条件：已完成登录并携带有效 `token`，当前视频对应的课程学习已完成必要的心跳和动作上报，且已明确 `classNo` 和 `courseNo`。
- 后续依赖：触发成功后，通常还会继续调用课程完成度刷新接口，再查询课程完成情况。

## 请求示例

这个请求示例展示了视频完成后的计算触发动作。它本身不直接返回完成度，而是启动一次服务端计算流程。

### 请求字段说明

- `classNo`: 当前课程所属班级或专区编号。
- `courseNo`: 当前课程编号。

### 请求体

```json
{
    "classNo": "1997868434762895360",
    "courseNo": "1L2BSTA000240"
}
```

## 响应示例

返回值中的 `data` 是本次计算请求的任务标识。通常只要任务成功创建，就可以继续刷新课程完成度。

### 响应字段说明

- `data`: 服务端返回的计算任务标识，可理解为本次异步计算请求的任务号。

### 响应体

```json
{
    "isSuccess": true,
    "statusCode": 200,
    "message": "",
    "jwt": null,
    "data": "2058381395381850112",
    "encrypt": false,
    "encryptType": "1"
}
```
