# 学习专区课程列表查询

获取某个学习专区的课程列表。

POST https://learn.baowugroup.com/learn-gateway/service/tms/ols/onlineClassCourse/getOnlineClassCourseSortPage

## 接口概览

- 接口作用：查询某个学习专区下的课程列表，是专区进入单门课程学习前的关键查询接口。
- 调用时机：在用户选定专区后调用，也可在专区课程页切换分页、课程名称或分类筛选条件时再次调用。
- 前置条件：已完成登录并携带有效 `token`，且已经通过专区列表接口拿到目标专区的 `olClassNo`。
- 后续依赖：拿到 `guid`、`courseNo` 和 `olClassNo` 后，可继续调用课程详情、课程完成情况和视频学习链路接口。

## 请求示例

这个请求示例展示了专区课程页常见的分页和筛选条件。专区编号决定课程范围，分页参数决定返回的记录数量。

### 请求字段说明

- `current`、`size`: 控制分页范围。
- `data.olClassNo`: 目标专区编号。
- `data.olClassType`: 专区类型，决定查询范围。
- `data.centerCode`: 学习中心编号。

### 请求体

```json
{
  "current": 1,
  "size": 4,
  "data": {
    "centerCode": "C001",
    "courseName": "",
    "courseTypeCode": "",
    "isMine": "1",
    "isRecursiveCourse": "1",
    "olClassNo": "2048570976672813056",
    "olClassType": "ZE0"
  }
}
```

## 响应示例

响应中的 `records` 数组给出专区课程列表。每条记录同时携带课程展示信息和进入下一步接口所需的标识。

### 响应字段说明

- `data.records[].guid`: 查询课程详情时使用的课程记录标识。
- `data.records[].courseNo`: 后续查询视频目录和初始化学习时会使用。
- `data.records[].courseName`: 课程名称，用于列表展示。
- `data.records[].learnStatus`: 当前课程完成状态。
- `data.records[].courseTypeName`: 课程分类展示信息。

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
        "guid": "2048589636808499200",
        "onlineClassGuid": null,
        "olClassType": "ZE0",
        "olClassNo": "2048570976672813056",
        "olClassName": null,
        "olClassCode": "1950475953671114752",
        "olClassificationName": null,
        "annual": null,
        "status": null,
        "beginTime": "2026-05-01",
        "endTime": "2026-08-31",
        "courseNo": "1L2BSTA000178",
        "courseName": "AI提升效率效益——公文写作、智慧办公",
        "isMustTeach": "0",
        "courseTypeCode": "2048570976840585216",
        "sort": null,
        "createUser": null,
        "createUserName": null,
        "createTime": null,
        "updateUser": null,
        "updateTime": null,
        "deleteUser": null,
        "deleteTime": null,
        "deleteFlag": null,
        "tenantCode": null,
        "centerCode": "C001",
        "centerName": null,
        "managerEmp": null,
        "managerEmpName": null,
        "teacherNo": null,
        "teacherName": null,
        "courseStrategyCode": null,
        "courseStrategyName": null,
        "courseHours": null,
        "courseTime": null,
        "courseContent": null,
        "imgUrl": "/service/ss/file/previewFile/2028359260794130432/fm.png",
        "viewCnt": 0,
        "likeCnt": 0,
        "linkUrl": null,
        "learnNum": "1050",
        "learnStatus": "2",
        "onlineClassCourseStatResp": null,
        "completedPeople": null,
        "registerSum": null,
        "courseTypeName": "课程分类",
        "rlsCourseTypeName": null,
        "courseOutlineResp": null,
        "courseInformationResp": null,
        "studentResp": null,
        "courseStuNum": null,
        "courseLikeNum": "3",
        "isDataDown": null,
        "inDataTime": "1",
        "imageUrl": null,
        "ocClassCode": null,
        "ocClassName": null,
        "ocClassPathName": null,
        "likeNum": "3"
      },
      {
        "guid": "2048589636829470720",
        "onlineClassGuid": null,
        "olClassType": "ZE0",
        "olClassNo": "2048570976672813056",
        "olClassName": null,
        "olClassCode": "1950475953671114752",
        "olClassificationName": null,
        "annual": null,
        "status": null,
        "beginTime": "2026-05-01",
        "endTime": "2026-08-31",
        "courseNo": "1L2BSTA000179",
        "courseName": "连铸全流程AI模型体系",
        "isMustTeach": "0",
        "courseTypeCode": "2048570976840585216",
        "sort": null,
        "createUser": null,
        "createUserName": null,
        "createTime": null,
        "updateUser": null,
        "updateTime": null,
        "deleteUser": null,
        "deleteTime": null,
        "deleteFlag": null,
        "tenantCode": null,
        "centerCode": "C001",
        "centerName": null,
        "managerEmp": null,
        "managerEmpName": null,
        "teacherNo": null,
        "teacherName": null,
        "courseStrategyCode": null,
        "courseStrategyName": null,
        "courseHours": null,
        "courseTime": null,
        "courseContent": null,
        "imgUrl": "/service/ss/file/previewFile/2028360068289925120/fm.png",
        "viewCnt": 0,
        "likeCnt": 0,
        "linkUrl": null,
        "learnNum": "796",
        "learnStatus": "2",
        "onlineClassCourseStatResp": null,
        "completedPeople": null,
        "registerSum": null,
        "courseTypeName": "课程分类",
        "rlsCourseTypeName": null,
        "courseOutlineResp": null,
        "courseInformationResp": null,
        "studentResp": null,
        "courseStuNum": null,
        "courseLikeNum": "8",
        "isDataDown": null,
        "inDataTime": "1",
        "imageUrl": null,
        "ocClassCode": null,
        "ocClassName": null,
        "ocClassPathName": null,
        "likeNum": "8"
      },
      {
        "guid": "2048589636829470721",
        "onlineClassGuid": null,
        "olClassType": "ZE0",
        "olClassNo": "2048570976672813056",
        "olClassName": null,
        "olClassCode": "1950475953671114752",
        "olClassificationName": null,
        "annual": null,
        "status": null,
        "beginTime": "2026-05-01",
        "endTime": "2026-08-31",
        "courseNo": "1L2BSTA000180",
        "courseName": "镁合金熔铸智能配料AI智能体的开发与应用",
        "isMustTeach": "0",
        "courseTypeCode": "2048570976840585216",
        "sort": null,
        "createUser": null,
        "createUserName": null,
        "createTime": null,
        "updateUser": null,
        "updateTime": null,
        "deleteUser": null,
        "deleteTime": null,
        "deleteFlag": null,
        "tenantCode": null,
        "centerCode": "C001",
        "centerName": null,
        "managerEmp": null,
        "managerEmpName": null,
        "teacherNo": null,
        "teacherName": null,
        "courseStrategyCode": null,
        "courseStrategyName": null,
        "courseHours": null,
        "courseTime": null,
        "courseContent": null,
        "imgUrl": "/service/ss/file/previewFile/2028362257875996672/fm.png",
        "viewCnt": 0,
        "likeCnt": 0,
        "linkUrl": null,
        "learnNum": "781",
        "learnStatus": "1",
        "onlineClassCourseStatResp": null,
        "completedPeople": null,
        "registerSum": null,
        "courseTypeName": "课程分类",
        "rlsCourseTypeName": null,
        "courseOutlineResp": null,
        "courseInformationResp": null,
        "studentResp": null,
        "courseStuNum": null,
        "courseLikeNum": "0",
        "isDataDown": null,
        "inDataTime": "1",
        "imageUrl": null,
        "ocClassCode": null,
        "ocClassName": null,
        "ocClassPathName": null,
        "likeNum": "0"
      },
      {
        "guid": "2048589636829470722",
        "onlineClassGuid": null,
        "olClassType": "ZE0",
        "olClassNo": "2048570976672813056",
        "olClassName": null,
        "olClassCode": "1950475953671114752",
        "olClassificationName": null,
        "annual": null,
        "status": null,
        "beginTime": "2026-05-01",
        "endTime": "2026-08-31",
        "courseNo": "1L2BSTA000105",
        "courseName": "熟用AI，速出好课——借助AI工具开发企业内训课程",
        "isMustTeach": "0",
        "courseTypeCode": "2048570976840585216",
        "sort": null,
        "createUser": null,
        "createUserName": null,
        "createTime": null,
        "updateUser": null,
        "updateTime": null,
        "deleteUser": null,
        "deleteTime": null,
        "deleteFlag": null,
        "tenantCode": null,
        "centerCode": "C001",
        "centerName": null,
        "managerEmp": null,
        "managerEmpName": null,
        "teacherNo": null,
        "teacherName": null,
        "courseStrategyCode": null,
        "courseStrategyName": null,
        "courseHours": null,
        "courseTime": null,
        "courseContent": null,
        "imgUrl": "/service/ss/file/previewFile/2011316571603079168/封面.png",
        "viewCnt": 0,
        "likeCnt": 0,
        "linkUrl": null,
        "learnNum": "959",
        "learnStatus": "2",
        "onlineClassCourseStatResp": null,
        "completedPeople": null,
        "registerSum": null,
        "courseTypeName": "课程分类",
        "rlsCourseTypeName": null,
        "courseOutlineResp": null,
        "courseInformationResp": null,
        "studentResp": null,
        "courseStuNum": null,
        "courseLikeNum": "0",
        "isDataDown": null,
        "inDataTime": "1",
        "imageUrl": null,
        "ocClassCode": null,
        "ocClassName": null,
        "ocClassPathName": null,
        "likeNum": "0"
      }
    ],
    "total": 77,
    "size": 4,
    "current": 1,
    "pages": 20
  },
  "encrypt": false,
  "encryptType": "1"
}
```
