# 专区完成度重算

触发专区维度的完成度重新计算。

POST https://learn.baowugroup.com/learn-gateway/service/tms/ols/computeTask/saveComputeTask4StuClassDetail

## 接口概览

- 接口作用：触发专区维度的完成度重新计算，让专区总体和分项统计结果更新到最新状态。
- 调用时机：在专区中的课程完成情况发生变化后调用，常见于完成某门课程后刷新专区进度。
- 前置条件：已完成登录并携带有效 `token`，且已明确目标专区的 `classNo`。
- 后续依赖：触发成功后，可继续调用专区总体统计和专区分项统计接口查看最新进度。

## 请求示例

这个请求示例展示了专区完成度刷新动作。它适合在一门课程学习状态变化后统一刷新专区视图。

### 请求字段说明

- `classNo`: 需要刷新统计的专区编号。

### 请求体

```json
{
    "classNo": "2048570976672813056"
}
```

## 响应示例

响应中的任务标识表示专区完成度刷新请求已被服务端接受。

### 响应字段说明

- `data`: 服务端返回的专区完成度计算任务标识。

### 响应体

```json
{
    "isSuccess": true,
    "statusCode": 200,
    "message": "",
    "jwt": null,
    "data": "2059648525913952256",
    "encrypt": false,
    "encryptType": "1"
}
```
