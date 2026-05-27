# 公开课列表查询

> 原始接口名：queryPageOpenClass

获取公开课列表及进入课程学习所需的关键标识。

POST https://learn.baowugroup.com/learn-gateway/service/tms/ols/student/queryPageOpenClass

## 接口概览

- 接口作用：获取公开课列表，并返回进入具体课程学习所需的课程和班级标识。
- 调用时机：在登录成功后进入公开课页面时调用，也可在切换学习状态、搜索条件或分页时再次调用。
- 前置条件：已完成登录并携带有效 `token`，且已经明确公开课列表的筛选条件和排序方式。
- 后续依赖：拿到 `courseGuid`、`courseNo` 和 `olClassNo` 后，可继续调用课程详情、课程目录、初始化学习和进度统计接口。

## 请求示例

这个请求示例展示了公开课列表页的常见查询方式。通过学习状态、关键字和排序条件，可以定位到需要继续学习的课程。

### 请求字段说明

- `current`、`size`: 控制分页范围。
- `data.searchType`: 公开课学习状态筛选条件。
- `data.searchInfo`: 关键字搜索条件。
- `data.sortClass`、`data.sortType`: 控制列表排序方式。

### 请求体

```json
{
  "current":1,
  "size":10, // 分页尺寸
  "data":{
    "learnStatus":"",
    "searchInfo":"", // 搜索过滤字段
    "searchType":"2", // "1" 全部, "2" 学习中, "3" 已完成
    "sortClass":"1",
    "sortType":"desc"
  }
}
```

## 响应示例

响应中的 `records` 数组同时提供了公开课列表展示信息，以及进入课程详情和学习链路所需的业务标识。

### 响应字段说明

- `data.records[].olClassNo`: 公开课所属班级编号。
- `data.records[].courseGuid`: 课程详情接口需要的课程记录标识。
- `data.records[].courseNo`: 查询视频目录、初始化学习和统计进度时会继续使用。
- `data.records[].courseName`: 课程名称。
- `data.records[].learnStatus`: 当前课程学习状态，可用于界面展示。

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
        "guid": "1997868434762895360",
        "olClassNo": "1997868434762895360", // class号
        "olCourseNo": null,
        "olClassType": "OCE", // 公开课类型OCE
        "olClassCode": "03",
        "firstClassCode": null,
        "olClassificationName": null,
        "olClassPathName": null,
        "classNo": "",
        "olClassName": "2026年度公开课（专业化能力）",
        "implementOrgName": null,
        "annual": "2026",
        "beginTime": "2025-12-01",
        "endTime": "2026-12-31",
        "managerEmp": "<管理员工号>",
        "managerEmpName": null,
        "businessForm": null,
        "universityType": null,
        "isCentreCharge": null,
        "classHours": null,
        "introduction": null,
        "status": null,
        "createUser": null,
        "createUserName": null,
        "createTime": null,
        "updateUser": null,
        "updateTime": null,
        "deleteUser": null,
        "deleteTime": null,
        "deleteFlag": null,
        "tenantCode": "BSTA",
        "centerCode": "C001", // 
        "centerName": null,
        "imageSource": null,
        "imageCode": null,
        "imageUrl": null,
        "isOrderLearn": null,
        "courseNum": null,
        "registerNum": null,
        "managerOrg": null,
        "managerOrgName": null,
        "headTeacher": null,
        "headTeacherName": null,
        "learnNum": null,
        "tagRespList": null,
        "courseTotalHours": null,
        "courseTotalTime": null,
        "courseTotalTimeMin1d5": null,
        "recentLearnTime": null,
        "viewCnt": null,
        "classInformationRespPage": null,
        "classCourseRespPage": null,
        "qrCode": null,
        "linkUrl": null,
        "learnStatus": "1",
        "stuName": null,
        "stuCode": null,
        "nearLearnTime": "20260523042228187",
        "nearLearnHours": "18",
        "courseGuid": "2047231431331299328", // 课程guid
        "courseNo": "1L2BSTA000240", // 课程号
        "courseName": "“龙虾”来了，AI最新发展及安全影响", // 课程名称
        "courseBeginTime": "2026-04-16",
        "courseEndTime": "2026-12-31",
        "crouseCount": "12949",
        "onlineClassCourseScoreStatResp": null,
        "onlineClassCourseNumStatResp": null,
        "onlineClassCourseResp": null,
        "settlementPrice": null,
        "onlineClassStyleCompResp": null,
        "onlineClassStyleResp": null,
        "imgAnnex": {
          "guid": "2042130947117289472",
          "businessType": "rls-courseOnlineLib",
          "businessNo": "2042131197827616768",
          "annexType": "png",
          "annexSuffix": ".png",
          "annexName": "fm.png",
          "fileSize": "56345",
          "downloadUrl": "/DEFTP/upload/2026/04/09/beb2ca11-16ec-43dc-aca9-ce05fafdc512.png",
          "hashCode": "723e6852968a60f49e15366781fee05d40f888aef0d1551ce60adb18c62f7ae1",
          "filePath": "/DEFTP/upload/2026/04/09/beb2ca11-16ec-43dc-aca9-ce05fafdc512.png",
          "createUser": "<创建人工号>"
        },
        "learnSource": "2",
        "courseSum": 0,
        "registerSum": 0,
        "leaningSum": 0,
        "leanCompleteSum": 0,
        "ocClassCode": null,
        "ocClassName": null,
        "courseHours": "3.5",
        "teacherNo": null,
        "teacherName": null,
        "likeNum": null
      },
      {
        "guid": "1997868434762895360",
        "olClassNo": "1997868434762895360",
        "olCourseNo": null,
        "olClassType": "OCE",
        "olClassCode": "03",
        "firstClassCode": null,
        "olClassificationName": null,
        "olClassPathName": null,
        "classNo": "",
        "olClassName": "2026年度公开课（专业化能力）",
        "implementOrgName": null,
        "annual": "2026",
        "beginTime": "2025-12-01",
        "endTime": "2026-12-31",
        "managerEmp": "<管理员工号>",
        "managerEmpName": null,
        "businessForm": null,
        "universityType": null,
        "isCentreCharge": null,
        "classHours": null,
        "introduction": null,
        "status": null,
        "createUser": null,
        "createUserName": null,
        "createTime": null,
        "updateUser": null,
        "updateTime": null,
        "deleteUser": null,
        "deleteTime": null,
        "deleteFlag": null,
        "tenantCode": "BSTA",
        "centerCode": "C001",
        "centerName": null,
        "imageSource": null,
        "imageCode": null,
        "imageUrl": null,
        "isOrderLearn": null,
        "courseNum": null,
        "registerNum": null,
        "managerOrg": null,
        "managerOrgName": null,
        "headTeacher": null,
        "headTeacherName": null,
        "learnNum": null,
        "tagRespList": null,
        "courseTotalHours": null,
        "courseTotalTime": null,
        "courseTotalTimeMin1d5": null,
        "recentLearnTime": null,
        "viewCnt": null,
        "classInformationRespPage": null,
        "classCourseRespPage": null,
        "qrCode": null,
        "linkUrl": null,
        "learnStatus": "1",
        "stuName": null,
        "stuCode": null,
        "nearLearnTime": "20260523033017383",
        "nearLearnHours": "19",
        "courseGuid": "2056973952475254784",
        "courseNo": "GbeL2BSTA000256",
        "courseName": "国际化视角解读——合规管理体系建设的可持续价值",
        "courseBeginTime": "2026-05-20",
        "courseEndTime": "2026-12-31",
        "crouseCount": "1316",
        "onlineClassCourseScoreStatResp": null,
        "onlineClassCourseNumStatResp": null,
        "onlineClassCourseResp": null,
        "settlementPrice": null,
        "onlineClassStyleCompResp": null,
        "onlineClassStyleResp": null,
        "imgAnnex": {
          "guid": "2046049623528837120",
          "businessType": "rls-courseOnlineLib",
          "businessNo": "2046049633314148352",
          "annexType": "png",
          "annexSuffix": ".png",
          "annexName": "fm.png",
          "fileSize": "83939",
          "downloadUrl": "/DEFTP/upload/2026/04/20/2b41efaa-9ce6-4184-b5e0-ac629afe609e.png",
          "hashCode": "1c2448160eeefc781ac963400e9770918996b11fe89270c8214d3783aa17ea30",
          "filePath": "/DEFTP/upload/2026/04/20/2b41efaa-9ce6-4184-b5e0-ac629afe609e.png",
          "createUser": "<创建人工号>"
        },
        "learnSource": "2",
        "courseSum": 0,
        "registerSum": 0,
        "leaningSum": 0,
        "leanCompleteSum": 0,
        "ocClassCode": null,
        "ocClassName": null,
        "courseHours": "3",
        "teacherNo": null,
        "teacherName": null,
        "likeNum": null
      },
      {
        "guid": "1997868434762895360",
        "olClassNo": "1997868434762895360",
        "olCourseNo": null,
        "olClassType": "OCE",
        "olClassCode": "03",
        "firstClassCode": null,
        "olClassificationName": null,
        "olClassPathName": null,
        "classNo": "",
        "olClassName": "2026年度公开课（专业化能力）",
        "implementOrgName": null,
        "annual": "2026",
        "beginTime": "2025-12-01",
        "endTime": "2026-12-31",
        "managerEmp": "<管理员工号>",
        "managerEmpName": null,
        "businessForm": null,
        "universityType": null,
        "isCentreCharge": null,
        "classHours": null,
        "introduction": null,
        "status": null,
        "createUser": null,
        "createUserName": null,
        "createTime": null,
        "updateUser": null,
        "updateTime": null,
        "deleteUser": null,
        "deleteTime": null,
        "deleteFlag": null,
        "tenantCode": "BSTA",
        "centerCode": "C001",
        "centerName": null,
        "imageSource": null,
        "imageCode": null,
        "imageUrl": null,
        "isOrderLearn": null,
        "courseNum": null,
        "registerNum": null,
        "managerOrg": null,
        "managerOrgName": null,
        "headTeacher": null,
        "headTeacherName": null,
        "learnNum": null,
        "tagRespList": null,
        "courseTotalHours": null,
        "courseTotalTime": null,
        "courseTotalTimeMin1d5": null,
        "recentLearnTime": null,
        "viewCnt": null,
        "classInformationRespPage": null,
        "classCourseRespPage": null,
        "qrCode": null,
        "linkUrl": null,
        "learnStatus": "1",
        "stuName": null,
        "stuCode": null,
        "nearLearnTime": "20260523033006191",
        "nearLearnHours": "19",
        "courseGuid": "2056973952487837696",
        "courseNo": "GbeL2BSTA000255",
        "courseName": "董事、高管履职规范及风险防范",
        "courseBeginTime": "2026-05-20",
        "courseEndTime": "2026-12-31",
        "crouseCount": "1402",
        "onlineClassCourseScoreStatResp": null,
        "onlineClassCourseNumStatResp": null,
        "onlineClassCourseResp": null,
        "settlementPrice": null,
        "onlineClassStyleCompResp": null,
        "onlineClassStyleResp": null,
        "imgAnnex": {
          "guid": "2046045561735483392",
          "businessType": "rls-courseOnlineLib",
          "businessNo": "2046045200530411520",
          "annexType": "png",
          "annexSuffix": ".png",
          "annexName": "封面.png",
          "fileSize": "245503",
          "downloadUrl": "/DEFTP/upload/2026/04/20/ac3bfbfe-5fa7-439e-b48f-652eb7de8c06.png",
          "hashCode": "3a748a8cac4a0af884520ab96e6db589b188b6826c085cdf09e5060afd3e65a7",
          "filePath": "/DEFTP/upload/2026/04/20/ac3bfbfe-5fa7-439e-b48f-652eb7de8c06.png",
          "createUser": "<创建人工号>"
        },
        "learnSource": "2",
        "courseSum": 0,
        "registerSum": 0,
        "leaningSum": 0,
        "leanCompleteSum": 0,
        "ocClassCode": null,
        "ocClassName": null,
        "courseHours": "3",
        "teacherNo": null,
        "teacherName": null,
        "likeNum": null
      }
    ],
    "total": 3,
    "size": 10,
    "current": 1,
    "pages": 1
  },
  "encrypt": false,
  "encryptType": "1"
}
```
