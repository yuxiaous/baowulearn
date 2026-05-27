# 专区列表查询

> 原始接口名：myClassPage

获取当前用户可访问的学习专区列表。

POST https://learn.baowugroup.com/learn-gateway/service/tms/ols/student/myClassPage

## 接口概览

- 接口作用：查询学习专区列表，是进入专区学习链路的入口接口。
- 调用时机：在登录成功后进入专区页面时调用，也可在切换筛选条件或分页时再次调用。
- 前置条件：已完成登录并携带有效 `token`，且已经明确专区类型和筛选条件。
- 后续依赖：拿到 `olClassNo` 后，可继续调用专区课程列表、专区总体统计和专区分项统计接口。

## 请求示例

这个请求示例展示了专区列表页常见的分页和筛选条件。请求体中的 `data` 对象决定了返回的专区范围和排序方式。

### 请求字段说明

- `current`、`size`: 控制分页范围。
- `data.classType`: 专区类型，示例中为 `ZE0`。
- `data.status`: 专区状态筛选，空值表示全部。
- `data.keyWord`: 按专区名称或关键字检索。

### 请求体

```json
{
  "current": 1,
  "size": 10,
  "data": {
    "classType": "ZE0", // 专区类型ZE0
    "isLearnNum": "1",
    "keyWord": "", // 搜索过滤字段
    "lastLearnTime": "1",
    "learnStatus": "",
    "sortClass": "1",
    "sortType": "desc",
    "status": "" // 空：全部，1：进行中，2：已结束
  }
}
```

## 响应示例

响应中的 `records` 数组给出当前页的专区列表。每条记录同时包含展示信息和后续查询所需的业务标识。

### 响应字段说明

- `data.records[].olClassNo`: 专区编号，后续查询专区课程和专区统计时要用到。
- `data.records[].olClassName`: 专区名称，用于列表展示。
- `data.records[].courseNum`: 专区内课程数量。
- `data.records[].learnNum`: 当前已学习课程数量。
- `data.total`、`data.pages`: 分页统计信息。

### 响应体

```json
{
  "isSuccess": true,
  "statusCode": 200,
  "message": "",
  "jwt": null,
  "data": {
    "records": [
      {
        "guid": "2048570976672813056",
        "olClassType": "ZE0",
        "olClassNo": "2048570976672813056",
        "olClassName": "2026年申报冶金专业中、高级职称继续教育在线学习",
        "beginTime": "2026-05-01",
        "endTime": "2026-08-31",
        "classHours": "152",
        "imageUrl": "/service/ss/file/previewFile/2048577484437458944/专区封面.png",
        "tenantCode": "BSTA",
        "centerCode": "C001",
        "courseNum": "77",
        "maxTime": "20260524004531633",
        "learnNum": "5"
      },
      {
        "guid": "2018875932768604160",
        "olClassType": "ZE0",
        "olClassNo": "2018875932768604160",
        "olClassName": "DeepSeek助力办公效能提升学习专区",
        "beginTime": "2026-02-10",
        "endTime": "2026-04-10",
        "classHours": "16.5",
        "imageUrl": "/service/ss/file/previewFile/2018964576116281344/专区图片800-450.png",
        "tenantCode": "BSTA",
        "centerCode": "C001",
        "courseNum": "8",
        "maxTime": "20260302133626663",
        "learnNum": "2"
      }
    ],
    "total": 2,
    "size": 10,
    "current": 1,
    "pages": 1
  },
  "encrypt": false,
  "encryptType": "1"
}
```
