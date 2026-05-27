# myClassPage

获取学习专区列表

POST https://learn.baowugroup.com/learn-gateway/service/tms/ols/student/myClassPage

## Request

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

## Response

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
