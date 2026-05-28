# 心跳间隔配置查询

> 原始接口名：queryPropValue

读取学习心跳发送频率配置，为后续心跳上报确定发送间隔。

POST https://learn.baowugroup.com/learn-gateway/service/ss/properties/queryPropValue

## 接口概览

- 接口作用：查询服务端配置的学习心跳发送间隔，通常用于确定 `saveLearnHertRecord` 的调用周期。
- 调用时机：在开始持续播放前、准备启动心跳循环时调用；也可在初始化学习流程时预先读取。
- 前置条件：已完成登录并携带有效 `token`；明确本次要查询的配置键为 `heartFrequency`。
- 后续依赖：返回的 `propertiesValue` 会直接影响后续心跳上报的发送频率，也会影响 `learnTime`、`learnRealTime` 等按周期累计的字段取值。

## 请求示例

这个请求示例展示了播放器在启动心跳循环前读取服务端心跳频率配置的场景。当前抓包里通过 `heartFrequency` 这个配置键获取秒级间隔。

### 请求字段说明

- `propertiesKey`: 要查询的配置项键名，这里固定为 `heartFrequency`，表示学习记录心跳频率。

### 请求体

```json
{
  "propertiesKey": "heartFrequency"
}
```

## 响应示例

响应重点是读取 `data.propertiesValue`，它给出了后续心跳请求应采用的时间间隔。样例中返回 `60`，表示每 60 秒发送一次心跳。

### 响应字段说明

- `data.propertiesKey`: 本次返回的配置项键名，应与请求中的 `propertiesKey` 对应。
- `data.propertiesValue`: 配置项值。对 `heartFrequency` 而言表示心跳发送间隔，单位为秒。
- `data.propertiesDesc`: 配置项说明文字，帮助确认该配置的业务含义。
- `data.propertiesType`: 配置项类型编号，可用于区分不同类别的系统参数。
- `data.tenantCode`: 租户维度配置标识。当前样例为 `null`，表示未体现租户级覆盖。
- `data.centerCode`: 学习中心维度配置标识。当前样例为 `null`，表示未体现中心级覆盖。

### 响应体

```json
{
  "isSuccess": true,
  "statusCode": 200,
  "message": "MSG-SS-0001",
  "jwt": null,
  "data": {
    "propertiesKey": "heartFrequency",
    "propertiesValue": "60",
    "propertiesDesc": "学习记录心跳频率（单位：秒）",
    "propertiesType": "9",
    "tenantCode": null,
    "centerCode": null
  },
  "encrypt": false,
  "encryptType": "1"
}
```
