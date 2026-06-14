# 学习专区课程列表查询

获取课程下的视频或课件目录。

POST https://learn.baowugroup.com/learn-gateway/service/tms/rls/courseOutline/queryCourseOutlineContentTreeListSimple

## 接口概览

- 接口作用：获取课程下的视频或课件目录，是进入具体播放环节前最重要的目录查询接口。
- 调用时机：在进入课程后、开始播放前调用，也可在刷新课程目录或切换课程时再次调用。
- 前置条件：已完成登录并携带有效 `token`，且已经通过课程详情接口拿到 `courseNo`。
- 后续依赖：拿到 `cataNo`、`wareCode`、`wareType` 和 `markeTimePoint` 后，可继续调用播放进度查询、学习初始化、心跳上报和打点接口。

## 请求示例

这个请求示例展示了课程目录查询的最小输入。目录返回结果通常是后续整个播放链路的起点。

### 请求字段说明

- `centerCode`: 学习中心编号, "C001" 集团站点，"C002" 人才开发院。
- `courseNo`: 目标课程编号。
- `isAppendPre`: 是否附加前置内容，示例中为 `1`。

### 请求体

```json
{
    "centerCode": "C001",
    "courseNo": "1L2BSTA000240",
    "isAppendPre": "1"
}
```

## 响应示例

响应结构按目录节点组织，真正要用于播放链路的关键信息集中在每个 `content` 条目里。

### 响应字段说明

- `data[].content[].cataNo`: 目录编号。
- `data[].content[].cataType`: 目录类型。
- `data[].content[].wareCode`: 仓库编号，后续播放链路会继续使用。
- `data[].content[].wareType`: 仓库类型，"1" 视频，"2" pdf文档（待确定）。
- `data[].content[].courseNo`: 课程编号。
- `data[].content[].contentName`: 视频名称，例如：视频名称。
- `data[].content[].newContentName`: 视频名称（带编号），例如：1-1 视频名称。
- `data[].content[].contentType`: 内容类型，"1" 视频
- `data[].content[].duration`: 视频时长（秒）。
- `data[].content[].markeTimePoint`: 视频打卡时间。
- `data[].content[].learnedStatus`: 当前视频学习状态，null 未学习，"0" 学习中，"1" 已完成。
- `data[].content[].status`: 内容状态，"1" 有效

### 响应体

```json
{
    "isSuccess": true,
    "statusCode": 200,
    "message": "",
    "jwt": null,
    "data": [
        {
            "guid": null,
            "courseNo": null,
            "cataType": null,
            "cataNo": null,
            "cataName": null,
            "parentCataNo": null,
            "sort": null,
            "status": null,
            "createUser": null,
            "createTime": null,
            "tenantCode": null,
            "centerCode": null,
            "children": null,
            "content": [
                {
                    "guid": "2042131343135084544",
                    "courseNo": "1L2BSTA000240",
                    "cataType": "2",
                    "cataNo": "2042131254945648640",
                    "teStatus": null,
                    "contentName": "技术范式转移",
                    "newContentName": "1-1 技术范式转移",
                    "newContentNameV2": null,
                    "contentType": "1",
                    "wareSource": "1",
                    "wareCode": "2042131342854066176",
                    "wareUrl": "/service/ss/file/previewFile/2042131342422052864",
                    "status": "1",
                    "createUser": "<创建人工号>",
                    "createTime": "20260409144347864",
                    "updateUser": "<更新人工号>",
                    "updateTime": "20260409144921121",
                    "deleteUser": null,
                    "deleteTime": null,
                    "deleteFlag": "0",
                    "tenantCode": "BSTA",
                    "centerCode": "C001",
                    "wareName": null,
                    "wareType": "1",
                    "uploadEmp": null,
                    "uploadTime": null,
                    "duration": "1640",
                    "markeTimePoint": "00:08:38,00:10:07,00:13:20,00:20:35,00:27:19",
                    "piecesTimePoint": null,
                    "hashCode": "99b3613f7f61573fb8b10ed306d4c08f5479e606d64ed9aecec249593851efa6",
                    "learnedStatus": "1"
                },
                {
                    "guid": "2042131465516486656",
                    "courseNo": "1L2BSTA000240",
                    "cataType": "2",
                    "cataNo": "2042131390983704576",
                    "teStatus": null,
                    "contentName": "案例学习与场景探讨",
                    "newContentName": "2-1 案例学习与场景探讨",
                    "newContentNameV2": null,
                    "contentType": "1",
                    "wareSource": "1",
                    "wareCode": "2042131465256439808",
                    "wareUrl": "/service/ss/file/previewFile/2042131464996392960",
                    "status": "1",
                    "createUser": "<创建人工号>",
                    "createTime": "20260409144417047",
                    "updateUser": "<更新人工号>",
                    "updateTime": "20260409144921122",
                    "deleteUser": null,
                    "deleteTime": null,
                    "deleteFlag": "0",
                    "tenantCode": "BSTA",
                    "centerCode": "C001",
                    "wareName": null,
                    "wareType": "1",
                    "uploadEmp": null,
                    "uploadTime": null,
                    "duration": "1258",
                    "markeTimePoint": "00:08:56,00:08:59,00:10:04,00:13:46,00:13:48",
                    "piecesTimePoint": null,
                    "hashCode": "e01afbce501ff1046448255650601900093c60cb96a41db2599e9a7f907cb19c",
                    "learnedStatus": "0"
                },
                {
                    "guid": "2042131531442556928",
                    "courseNo": "1L2BSTA000240",
                    "cataType": "2",
                    "cataNo": "2042131486236348416",
                    "teStatus": null,
                    "contentName": "产业生态与政策红利",
                    "newContentName": "3-1 产业生态与政策红利",
                    "newContentNameV2": null,
                    "contentType": "1",
                    "wareSource": "1",
                    "wareCode": "2042131531195092992",
                    "wareUrl": "/service/ss/file/previewFile/2042131530989572096",
                    "status": "1",
                    "createUser": "<创建人工号>",
                    "createTime": "20260409144432762",
                    "updateUser": "<更新人工号>",
                    "updateTime": "20260409144921123",
                    "deleteUser": null,
                    "deleteTime": null,
                    "deleteFlag": "0",
                    "tenantCode": "BSTA",
                    "centerCode": "C001",
                    "wareName": null,
                    "wareType": "1",
                    "uploadEmp": null,
                    "uploadTime": null,
                    "duration": "289",
                    "markeTimePoint": "00:00:35,00:00:53,00:02:02,00:02:36,00:04:12",
                    "piecesTimePoint": null,
                    "hashCode": "4ce441f9894ee97336111c650a3a8027c8ea28fc77dd45d0a1f425b4a5e92572",
                    "learnedStatus": "0"
                },
                {
                    "guid": "2042131618600194048",
                    "courseNo": "1L2BSTA000240",
                    "cataType": "2",
                    "cataNo": "2042131563747086336",
                    "teStatus": null,
                    "contentName": "安全合规与未来挑战",
                    "newContentName": "4-1 安全合规与未来挑战",
                    "newContentNameV2": null,
                    "contentType": "1",
                    "wareSource": "1",
                    "wareCode": "2042131618306592768",
                    "wareUrl": "/service/ss/file/previewFile/2042131618176569344",
                    "status": "1",
                    "createUser": "<创建人工号>",
                    "createTime": "20260409144453542",
                    "updateUser": "<更新人工号>",
                    "updateTime": "20260409144921123",
                    "deleteUser": null,
                    "deleteTime": null,
                    "deleteFlag": "0",
                    "tenantCode": "BSTA",
                    "centerCode": "C001",
                    "wareName": null,
                    "wareType": "1",
                    "uploadEmp": null,
                    "uploadTime": null,
                    "duration": "688",
                    "markeTimePoint": "00:03:34,00:04:49,00:05:34,00:06:11,00:06:21",
                    "piecesTimePoint": null,
                    "hashCode": "282fe90bf9a755c4dc6ba7cde2f5eeb932e4671ff162c3383a382d60095ac55c",
                    "learnedStatus": null
                },
                {
                    "guid": "2042131698061283328",
                    "courseNo": "1L2BSTA000240",
                    "cataType": "2",
                    "cataNo": "2042131651894579200",
                    "teStatus": null,
                    "contentName": "“龙虾”本地化安装部署",
                    "newContentName": "5-1 “龙虾”本地化安装部署",
                    "newContentNameV2": null,
                    "contentType": "1",
                    "wareSource": "1",
                    "wareCode": "2042131697851568128",
                    "wareUrl": "/service/ss/file/previewFile/2042131697763487744",
                    "status": "1",
                    "createUser": "<创建人工号>",
                    "createTime": "20260409144512487",
                    "updateUser": "<更新人工号>",
                    "updateTime": "20260409144921123",
                    "deleteUser": null,
                    "deleteTime": null,
                    "deleteFlag": "0",
                    "tenantCode": "BSTA",
                    "centerCode": "C001",
                    "wareName": null,
                    "wareType": "1",
                    "uploadEmp": null,
                    "uploadTime": null,
                    "duration": "78",
                    "markeTimePoint": "00:00:01,00:00:09,00:00:11,00:00:14,00:01:05",
                    "piecesTimePoint": null,
                    "hashCode": "6c8fc801135309155c4930d8e7167714ef2245d678e7c7ed44346142cceed7e2",
                    "learnedStatus": "1"
                },
                {
                    "guid": "2042131828806127616",
                    "courseNo": "1L2BSTA000240",
                    "cataType": "2",
                    "cataNo": "2042131737022173184",
                    "teStatus": null,
                    "contentName": "“龙虾”云端部署（以阿里云为例）（上）",
                    "newContentName": "6-1 “龙虾”云端部署（以阿里云为例）（上）",
                    "newContentNameV2": null,
                    "contentType": "1",
                    "wareSource": "1",
                    "wareCode": "2042131828608995328",
                    "wareUrl": "/service/ss/file/previewFile/2042131828428640256",
                    "status": "1",
                    "createUser": "<创建人工号>",
                    "createTime": "20260409144543658",
                    "updateUser": "<更新人工号>",
                    "updateTime": "20260409144921125",
                    "deleteUser": null,
                    "deleteTime": null,
                    "deleteFlag": "0",
                    "tenantCode": "BSTA",
                    "centerCode": "C001",
                    "wareName": null,
                    "wareType": "1",
                    "uploadEmp": null,
                    "uploadTime": null,
                    "duration": "2527",
                    "markeTimePoint": "00:06:51,00:15:15,00:24:28,00:27:58,00:38:37",
                    "piecesTimePoint": null,
                    "hashCode": "346962c661870587ddece65ced30dfe67f59c74e7081454b655595217c468a96",
                    "learnedStatus": null
                },
                {
                    "guid": "2042131938378125312",
                    "courseNo": "1L2BSTA000240",
                    "cataType": "2",
                    "cataNo": "2042131846208294912",
                    "teStatus": null,
                    "contentName": "“龙虾”云端部署（以阿里云为例）（下）",
                    "newContentName": "7-1 “龙虾”云端部署（以阿里云为例）（下）",
                    "newContentNameV2": null,
                    "contentType": "1",
                    "wareSource": "1",
                    "wareCode": "2042131938172604416",
                    "wareUrl": "/service/ss/file/previewFile/2042131937988055040",
                    "status": "1",
                    "createUser": "<创建人工号>",
                    "createTime": "20260409144609786",
                    "updateUser": "<更新人工号>",
                    "updateTime": "20260409144921125",
                    "deleteUser": null,
                    "deleteTime": null,
                    "deleteFlag": "0",
                    "tenantCode": "BSTA",
                    "centerCode": "C001",
                    "wareName": null,
                    "wareType": "1",
                    "uploadEmp": null,
                    "uploadTime": null,
                    "duration": "2602",
                    "markeTimePoint": "00:16:33,00:16:39,00:30:34,00:34:07,00:37:01",
                    "piecesTimePoint": null,
                    "hashCode": "83a4b00efe9f0f77c4bc3916b01b45cbdcf5e8b0dc585c366bf2e26314bf8dc7",
                    "learnedStatus": null
                }
            ]
        }
    ],
    "encrypt": false,
    "encryptType": "1"
}
```