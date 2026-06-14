# 专区总体完成度查询

查询专区整体完成情况和达标要求。

POST https://learn.baowugroup.com/learn-gateway/service/tms/ols/onlineClass/totalFinishStatistics

## 接口概览

- 接口作用：查询专区整体完成情况，展示当前专区总进度、达标要求和各项统计规则。
- 调用时机：在进入专区统计页、刷新专区整体学习状态，或课程完成后查看专区最新进度时调用。
- 前置条件：已完成登录并携带有效 `token`，已明确专区的 `olClassNo`、`centerCode` 和 `tenantCode`。
- 后续依赖：可结合专区分项统计接口，进一步定位是哪些课程或要求尚未完成。

## 请求示例

这个请求示例展示了专区总体完成度查询的最小输入。它适合用于专区统计页顶部总览数据的刷新。

### 请求字段说明

- `olClassNo`: 目标专区编号。
- `centerCode`: 学习中心编号。
- `tenantCode`: 当前租户编号。

### 请求体

```json
{
    "centerCode": "C001",
    "olClassNo": "2048570976672813056",
    "tenantCode": "BSTA"
}
```

## 响应示例

响应中的 `data` 对象给出专区整体完成度和统计规则。定位问题时，通常会同时关注总体分值和各个统计项的目标值。

### 响应字段说明

- `data.learnScore`: 当前专区总体完成度。
- `data.passScore`: 达标门槛。
- `data.strategyDesc`: 专区统计规则说明。
- `data.details[]`: 各类学习要求的完成值和目标值。

### 响应体

```json
{
    "isSuccess": true,
    "statusCode": 200,
    "message": "",
    "jwt": null,
    "data": {
        "totalScore": "100",
        "passScore": "100",
        "learnScore": "20.83333",
        "strategyTip": null,
        "strategyDesc": "在专区考试栏目里，要求直播课程结束后一周内完成该门课程考试。",
        "learnStatus": "1",
        "details": [
            {
                "attributeCode": "ZE001",
                "attributeName": "选修课程学时",
                "percentage": "50",
                "finishValue": "52.50000",
                "attributeUnit": "课时",
                "predValue": "126"
            },
            {
                "attributeCode": "ZE013",
                "attributeName": "学习要求（考试）",
                "percentage": "50",
                "finishValue": "4.00000",
                "attributeUnit": "门",
                "predValue": "12"
            }
        ]
    },
    "encrypt": false,
    "encryptType": "1"
}
```
