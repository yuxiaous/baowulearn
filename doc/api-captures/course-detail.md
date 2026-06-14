# 课程详情查询

查询单门课程的详细信息。

POST https://learn.baowugroup.com/learn-gateway/service/tms/ols/onlineClassCourse/detailOnlineClassCourse

## 接口概览

- 接口作用：查询课程标题、讲师、课时、课程简介和所属公开课/专区信息。
- 调用时机：在课程列表中选定某门课程后调用，常用于进入课程详情页或开始学习前展示课程信息。
- 前置条件：已完成登录并携带有效 `token`，且已经通过公开课列表或专区课程列表拿到课程 `guid`。
- 后续依赖：拿到 `courseNo` 和 `olClassNo` 后，可继续调用视频目录、学习初始化和课程完成情况接口。

## 请求示例

这个请求示例展示了如何通过课程 `guid` 查询课程详情。请求体只有少量字段，但它们决定了能否准确定位到当前课程。

### 请求字段说明

- `guid`: 课程详情查询的核心标识。
- `centerCode`: 学习中心编号。
- `stuClient`: 指示当前请求来自学员端。

### 请求体

```json
{
    "centerCode": "C001",
    "guid": "2047231431331299328", // course guid
    "stuClient": true
}
```

## 响应示例

响应中的核心内容集中在 `data` 对象。除了课程基础信息，还会返回后续学习链路要继续使用的关键标识。

### 响应字段说明

- `data.courseNo`: 后续查询目录、初始化学习和完成情况时都会用到。
- `data.olClassNo`: 所属公开课或专区编号。
- `data.teacherName`: 课程讲师展示信息。
- `data.courseHours`、`data.courseTime`: 课程课时和时长。
- `data.courseContent`: 课程简介，可用于详情展示。

### 响应体

```json
{
    "isSuccess": true,
    "statusCode": 200,
    "message": "",
    "jwt": null,
    "data": {
        "guid": "2047231431331299328",
        "onlineClassGuid": null,
        "olClassType": "OCE",
        "olClassNo": "1997868434762895360",
        "olClassName": "2026年度公开课（专业化能力）",
        "olClassCode": "03",
        "olClassificationName": null,
        "annual": "2026",
        "status": "1",
        "beginTime": "2026-04-16",
        "endTime": "2026-12-31",
        "courseNo": "1L2BSTA000240",
        "courseName": "“龙虾”来了，AI最新发展及安全影响",
        "isMustTeach": "0",
        "courseTypeCode": null,
        "sort": "00000",
        "createUser": "<创建人工号>",
        "createUserName": null,
        "createTime": "20260423162943607",
        "updateUser": "<更新人工号>",
        "updateTime": "20260423163025446",
        "deleteUser": null,
        "deleteTime": null,
        "deleteFlag": "0",
        "tenantCode": "BSTA",
        "centerCode": "C001",
        "centerName": null,
        "managerEmp": null,
        "managerEmpName": null,
        "teacherNo": "<讲师标识>",
        "teacherName": "<讲师姓名>",
        "courseStrategyCode": null,
        "courseStrategyName": null,
        "courseHours": "3.5",
        "courseTime": "151",
        "courseContent": "<p>课程紧扣前沿科技趋势与企业实战需求，以近期席卷全球的现象级开源智能体“龙虾”（OpenClaw）为破冰切入点，深度剖析AI从“对话思考”迈向“自主执行”的技术范式跃迁。课程聚焦“行动派AI”的底层架构与工业级安全底线，直击高权限智能体带来的“致命三要素”及合规红线，明晰企业办公与生产环境中的安全防范策略，并结合大模型（LLM）的第一性原理，拆解Transformer、RAG、智能体协同等硬核技术栈，展示AI技术赋能千行百业的真实路径。通过本次培训，旨在帮助员工打破认知盲区，实现AI认知从浅层工具了解向深度业务认同的转变，在筑牢网络安全与数据合规底线的同时，切实提升以“数智思维”破解核心业务痛点的实战能力。</p>",
        "imgUrl": null,
        "viewCnt": 0,
        "likeCnt": 0,
        "linkUrl": null,
        "learnNum": null,
        "learnStatus": null,
        "onlineClassCourseStatResp": null,
        "completedPeople": null,
        "registerSum": null,
        "courseTypeName": null,
        "rlsCourseTypeName": null,
        "courseOutlineResp": null,
        "courseInformationResp": null,
        "studentResp": null,
        "courseStuNum": null,
        "courseLikeNum": null,
        "isDataDown": "1",
        "inDataTime": null,
        "imageUrl": null,
        "ocClassCode": "03-08-08",
        "ocClassName": "人工智能",
        "ocClassPathName": null,
        "likeNum": null
    },
    "encrypt": false,
    "encryptType": "1"
}
```