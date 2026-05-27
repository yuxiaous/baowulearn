# detailOnlineClassCourse

获取课程详情

POST https://learn.baowugroup.com/learn-gateway/service/tms/ols/onlineClassCourse/detailOnlineClassCourse

## Request

```json
{
    "centerCode": "C001",
    "guid": "2047231431331299328", // course guid
    "stuClient": true
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