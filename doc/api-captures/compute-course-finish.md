# 课程完成度重算

> 原始接口名：saveComputeTask4StuCourseDetail

触发课程维度的完成度重新计算。

POST https://learn.baowugroup.com/learn-gateway/service/tms/ols/computeTask/saveComputeTask4StuCourseDetail

## 接口概览

- 接口作用：触发课程维度的完成度重新计算，让课程完成情况和学习分数及时更新。
- 调用时机：在某门课程的视频完成状态发生变化后调用，常见于完成视频播放后刷新课程进度。
- 前置条件：已完成登录并携带有效 `token`，当前课程的学习数据已经完成必要的上报，且已明确 `classNo` 和 `courseNo`。
- 后续依赖：计算任务触发后，可继续调用课程完成情况接口查看最新的 `learnScore` 和 `learnStatus`。

## 请求示例

这个请求示例展示了课程完成度刷新动作。它常用于服务端重新汇总当前课程下所有学习记录。

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

响应中的任务标识表示课程完成度重算请求已经进入服务端处理流程。

### 响应字段说明

- `data`: 服务端返回的课程完成度计算任务标识。

### 响应体

```json
{
    "isSuccess": true,
    "statusCode": 200,
    "message": "",
    "jwt": null,
    "data": "2058382359228715008",
    "encrypt": false,
    "encryptType": "1"
}
```
