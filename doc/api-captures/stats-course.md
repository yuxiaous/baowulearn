# 课程完成情况查询

> 原始接口名：finishInfo

查询单门课程当前的完成度和得分情况。

POST https://learn.baowugroup.com/learn-gateway/service/tms/ols/onlineClassCourse/finishInfo

## 接口概览

- 接口作用：查询单门课程当前的完成度、得分和各项学习要求完成情况。
- 调用时机：在进入课程详情页、刷新学习进度，或完成视频学习后希望查看课程是否达标时调用。
- 前置条件：已完成登录并携带有效 `token`，已明确当前课程的 `courseNo`、`olClassNo`、`tenantCode` 和 `centerCode`。
- 后续依赖：可根据本接口结果决定是否继续学习、补考试，或刷新课程和专区整体完成度展示。

## 请求示例

这个请求示例展示了课程完成情况查询的最小输入。它通常用于详情页进度刷新，或在完成一段学习后重新拉取最新状态。

### 请求字段说明

- `courseNo`: 目标课程编号。
- `olClassNo`: 当前课程所属班级或专区编号。
- `tenantCode`: 当前租户编号。
- `centerCode`: 学习中心编号。

### 请求体

```json
{
  "centerCode": "C001",
  "courseNo": "1L2BSTA000240",
  "olClassNo": "1997868434762895360",
  "tenantCode": "BSTA"
}
```

## 响应示例

响应中的 `data` 对象会给出课程总体完成情况，以及不同考核项的完成明细。判断是否达标时，通常要同时看总体分值和明细项。

### 响应字段说明

- `data.learnScore`: 当前课程完成进度。
- `data.passScore`: 达标分数或完成门槛。
- `data.learnStatus`: 当前课程状态。
- `data.details[]`: 各项考核指标的完成值和目标值。

### 响应体

```json
{
    "isSuccess": true,
    "statusCode": 200,
    "message": "",
    "jwt": null,
    "data": {
        "totalScore": "100",
        "passScore": "60",
        "learnScore": "0.02",
        "strategyTip": null,
        "strategyDesc": null,
        "learnStatus": "1",
        "details": [
            {
                "attributeCode": "CE001",
                "attributeName": "考试",
                "percentage": "30",
                "finishValue": "0.00000",
                "attributeUnit": "分",
                "predValue": "100"
            },
            {
                "attributeCode": "CE002",
                "attributeName": "学习时长",
                "percentage": "70",
                "finishValue": "0.01667",
                "attributeUnit": "分钟",
                "predValue": "61"
            },
            {
                "attributeCode": "CE009",
                "attributeName": "课程调查",
                "percentage": "0",
                "finishValue": "未参加",
                "attributeUnit": "",
                "predValue": "1"
            }
        ]
    },
    "encrypt": false,
    "encryptType": "1"
}
```
