# 获取学习专区列表

> 原始接口名：queryMainOnlineClassPage

获取集团站点学习专区列表。

POST https://learn.baowugroup.com/learn-gateway/service/tms/ols/onlineClass/queryMainOnlineClassPage

## 接口概览

- 接口作用：查询学习专区列表，是进入专区学习链路的入口接口。
- 调用时机：在登录成功后进入专区页面时调用，也可在切换筛选条件或分页时再次调用。
- 前置条件：已完成登录并携带有效 `token`，且已经明确专区类型和筛选条件。
- 后续依赖：拿到 `olClassNo` 后，可继续调用专区课程列表、专区总体统计和专区分项统计接口。

## 请求示例

这个请求示例展示了专区列表页常见的分页和筛选条件。请求体中的 `data` 对象决定了返回的专区范围和排序方式。

### 请求字段说明

- `current`、`size`: 控制分页范围。
- `data.olClassType`: 专区类型，示例中为 `ZE0`。
- `data.centerCode`: 专区代码，实例中为 `C001`。

### 请求体

```json
{
  "current": 1,
  "size": 96,
  "data": {
    "olClassCode": "",
    "olClassType": "ZE0",
    "searchInfo": "",
    "userSource": "1",
    "centerCode": "C001", // C001集团站点，C002人才开发院
    "isMine": "1",
    "sortFlag": 5
  }
}
```

## 响应示例

响应中的 `records` 数组给出当前页的专区列表。每条记录同时包含展示信息和后续查询所需的业务标识。

### 响应字段说明

- `data.records[].olClassNo`: 专区编号，后续查询专区课程和专区统计时要用到。
- `data.records[].olClassName`: 专区名称，用于列表展示。
- `data.records[].courseNum`: 专区内课程数量。
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
        "olClassNo": "2048570976672813056",
        "olCourseNo": null,
        "olClassType": "ZE0",
        "olClassCode": "1950475953671114752",
        "firstClassCode": "1950475953671114752",
        "olClassificationName": null,
        "olClassPathName": null,
        "classNo": "N2026SabBSTA031093",
        "olClassName": "2026年申报冶金专业中、高级职称继续教育在线学习",
        "implementOrgName": null,
        "annual": "2026",
        "beginTime": "2026-05-01",
        "endTime": "2026-08-31",
        "managerEmp": "212779",
        "managerEmpName": null,
        "businessForm": null,
        "universityType": null,
        "isCentreCharge": "0",
        "classHours": "152",
        "introduction": "<p>根据《专业技术人员继续教育规定》（人社部令第25号）、《关于完善本市专业技术人员继续教育公需科目培训工作的通知》（沪人社专2017［256］号）要求，完成一定的继续教育课程是申报中、高级专业技术任职资格评审的基本条件之一。</p><p>本专区包括77门、152.5学时网络课程和12门直播课程考试，学员可在专区中自主选择网络课程学习，专业科目培训一般按照三年为一个考核周期计算学时，三年内专业科目累计需完成180学时，其中网络课程126学时、直播课程54学时；要求直播课程结束一周内完成该课程在专区内的考试，考试合格即获得该直播课程学时；网络课程学时达到规定学时且直播课程考试成绩合格者，可在<strong>个人中心——学习档案——学习专区——课程记录里</strong>导出课程及考试成绩清单作为申报冶金专业中、高级任职资格的相关材料。</p><p><br></p>",
        "status": "1",
        "createUser": "212779",
        "createUserName": null,
        "createTime": "20260427091236107",
        "updateUser": "212779",
        "updateTime": "20260501094005802",
        "deleteUser": null,
        "deleteTime": null,
        "deleteFlag": "0",
        "tenantCode": "BSTA",
        "centerCode": "C001",
        "centerName": null,
        "imageSource": "2",
        "imageCode": "",
        "imageUrl": "/service/ss/file/previewFile/2048577484437458944/专区封面.png",
        "isOrderLearn": "0",
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
        "viewCnt": "40190",
        "classInformationRespPage": null,
        "classCourseRespPage": null,
        "qrCode": null,
        "linkUrl": null,
        "learnStatus": null,
        "stuName": null,
        "stuCode": null,
        "nearLearnTime": null,
        "nearLearnHours": null,
        "courseGuid": null,
        "courseNo": null,
        "courseName": null,
        "courseBeginTime": null,
        "courseEndTime": null,
        "crouseCount": null,
        "onlineClassCourseScoreStatResp": null,
        "onlineClassCourseNumStatResp": null,
        "onlineClassCourseResp": null,
        "settlementPrice": null,
        "onlineClassStyleCompResp": null,
        "onlineClassStyleResp": null,
        "imgAnnex": null,
        "learnSource": null,
        "courseSum": 0,
        "registerSum": 0,
        "leaningSum": 0,
        "leanCompleteSum": 0,
        "ocClassCode": null,
        "ocClassName": null,
        "courseHours": null,
        "teacherNo": null,
        "teacherName": null,
        "likeNum": null
      }
    ],
    "total": 1,
    "size": 96,
    "current": 1,
    "pages": 1
  },
  "encrypt": false,
  "encryptType": "1"
}
```
