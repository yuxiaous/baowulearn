# 专区课程完成明细查询

查询专区内每门课程的完成情况。

POST https://learn.baowugroup.com/learn-gateway/service/tms/ols/onlineClass/itemFinishStatisticsSortPage

## 接口概览

- 接口作用：查询专区内每门课程的完成情况，帮助定位具体哪门课程尚未达标。
- 调用时机：在进入专区统计页、查看专区分项完成情况，或刷新专区课程进度列表时调用。
- 前置条件：已完成登录并携带有效 `token`，已明确专区的 `olClassNo`、`centerCode` 和 `tenantCode`。
- 后续依赖：可根据未完成课程的状态，回到专区课程列表或课程详情继续补学习。

## 请求示例

这个请求示例展示了专区分项统计查询的常见分页方式。它适合用于展示专区内每门课程的学习完成情况列表。

### 请求字段说明

- `current`、`size`: 控制分页范围。
- `data.olClassNo`: 目标专区编号。
- `data.centerCode`: 学习中心编号。
- `data.tenantCode`: 当前租户编号。

### 请求体

```json
{
    "current": 1,
    "size": 100,
    "data": {
        "centerCode": "C001",
        "olClassNo": "2048570976672813056",
        "tenantCode": "BSTA"
    }
}
```

## 响应示例

响应中的 `records` 数组会按课程粒度返回完成情况。它适合用于查找专区中尚未完成或尚未达标的具体课程。

### 响应字段说明

- `data.records[].code`: 课程编号。
- `data.records[].name`: 课程名称。
- `data.records[].learnScore`: 当前课程完成分值。
- `data.records[].learnStatus`: 当前课程状态。
- `data.records[].isExam`: 是否涉及考试要求。

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
                "code": "1L2BSTA000178",
                "name": "AI提升效率效益——公文写作、智慧办公",
                "passScore": "60",
                "learnScore": "100.00",
                "learnStatus": "2",
                "isExam": "0"
            },
            {
                "code": "1L2BSTA000179",
                "name": "连铸全流程AI模型体系",
                "passScore": "60",
                "learnScore": "100.00",
                "learnStatus": "2",
                "isExam": "0"
            },
            {
                "code": "1L2BSTA000180",
                "name": "镁合金熔铸智能配料AI智能体的开发与应用",
                "passScore": "60",
                "learnScore": "100.00",
                "learnStatus": "2",
                "isExam": "0"
            },
            {
                "code": "1L2BSTA000105",
                "name": "熟用AI，速出好课——借助AI工具开发企业内训课程",
                "passScore": "60",
                "learnScore": "100.00",
                "learnStatus": "2",
                "isExam": "0"
            },
            {
                "code": "1L2BSTA000075",
                "name": "AI赋能 建造未来",
                "passScore": "60",
                "learnScore": "100.00",
                "learnStatus": "2",
                "isExam": "0"
            },
            {
                "code": "1L2BSTA000077",
                "name": "AI赋能日常办公效率提升",
                "passScore": "60",
                "learnScore": "100.00",
                "learnStatus": "2",
                "isExam": "0"
            },
            {
                "code": "1L2BSTA000071",
                "name": "岗位技术创新的认知与思考",
                "passScore": "60",
                "learnScore": "100.00",
                "learnStatus": "2",
                "isExam": "0"
            },
            {
                "code": "97765",
                "name": "智能体设计方法论",
                "passScore": "60",
                "learnScore": "100.00",
                "learnStatus": "2",
                "isExam": "0"
            },
            {
                "code": "97695",
                "name": "加快经济社会发展全面绿色转型 建设美丽中国",
                "passScore": "60",
                "learnScore": "100.00",
                "learnStatus": "2",
                "isExam": "0"
            },
            {
                "code": "96749",
                "name": "新钢特钢事业部高速线材轧制技术集成及应用",
                "passScore": "60",
                "learnScore": "100.00",
                "learnStatus": "2",
                "isExam": "0"
            },
            {
                "code": "96685",
                "name": "加快高水平科技自立自强 引领发展新质生产力",
                "passScore": "60",
                "learnScore": "94.00",
                "learnStatus": "2",
                "isExam": "0"
            },
            {
                "code": "96065",
                "name": "“十五五”宏观经济形势分析与展望",
                "passScore": "60",
                "learnScore": "100.00",
                "learnStatus": "2",
                "isExam": "0"
            },
            {
                "code": "96077",
                "name": "我国能源发展成就与“十五五”展望",
                "passScore": "60",
                "learnScore": "96.00",
                "learnStatus": "2",
                "isExam": "0"
            },
            {
                "code": "95824",
                "name": "高炉煤气喷雾冷却系统设计应用",
                "passScore": "60",
                "learnScore": "100.00",
                "learnStatus": "2",
                "isExam": "0"
            },
            {
                "code": "95830",
                "name": "筑牢钢铁行业业务连续性：信息系统关键技术实践策略与案例分析",
                "passScore": "60",
                "learnScore": "100.00",
                "learnStatus": "2",
                "isExam": "0"
            },
            {
                "code": "95811",
                "name": "钢渣的资源化利用",
                "passScore": "60",
                "learnScore": "100.00",
                "learnStatus": "2",
                "isExam": "0"
            },
            {
                "code": "95738",
                "name": "AI场景自主实施的探索与实践",
                "passScore": "60",
                "learnScore": "100.00",
                "learnStatus": "2",
                "isExam": "0"
            },
            {
                "code": "95720",
                "name": "AI赋能：人人都是程序员",
                "passScore": "60",
                "learnScore": "100.00",
                "learnStatus": "2",
                "isExam": "0"
            },
            {
                "code": "95718",
                "name": "匠心独运 炉炼精算",
                "passScore": "60",
                "learnScore": "100.00",
                "learnStatus": "2",
                "isExam": "0"
            },
            {
                "code": "95716",
                "name": "浅谈工作中精益管理与岗位创新的关系",
                "passScore": "60",
                "learnScore": "100.00",
                "learnStatus": "2",
                "isExam": "0"
            },
            {
                "code": "95724",
                "name": "青年创新者的AI工具包：aPM通用预测模型介绍及应用实践",
                "passScore": "60",
                "learnScore": "100.00",
                "learnStatus": "2",
                "isExam": "0"
            },
            {
                "code": "95135",
                "name": "废水深度回用与零排放研究与实践",
                "passScore": "60",
                "learnScore": "100.00",
                "learnStatus": "2",
                "isExam": "0"
            },
            {
                "code": "94630",
                "name": "DeepSeek引发的AI革命和对各产业的影响（二）",
                "passScore": "60",
                "learnScore": "100.00",
                "learnStatus": "2",
                "isExam": "0"
            },
            {
                "code": "94627",
                "name": "DeepSeek引发的AI革命和对各产业的影响（一）",
                "passScore": "60",
                "learnScore": "100.00",
                "learnStatus": "2",
                "isExam": "0"
            },
            {
                "code": "94457",
                "name": "设备故障知识图谱管理系统培训",
                "passScore": "100",
                "learnScore": "100.00",
                "learnStatus": "2",
                "isExam": "0"
            },
            {
                "code": "94038",
                "name": "如何让AI大模型成为工作利器",
                "passScore": "60",
                "learnScore": "100.00",
                "learnStatus": "2",
                "isExam": "0"
            },
            {
                "code": "92985",
                "name": "向设备要效益，用数据算大账",
                "passScore": "60",
                "learnScore": "100.00",
                "learnStatus": "2",
                "isExam": "0"
            },
            {
                "code": "92944",
                "name": "AI基础课程-Python编程实操",
                "passScore": "60",
                "learnScore": "97.00",
                "learnStatus": "2",
                "isExam": "0"
            },
            {
                "code": "92935",
                "name": "AI基础课程-机器学习算法",
                "passScore": "60",
                "learnScore": "97.00",
                "learnStatus": "2",
                "isExam": "0"
            },
            {
                "code": "92912",
                "name": "从零起步打造个人办公智能体（二）",
                "passScore": "60",
                "learnScore": "100.00",
                "learnStatus": "2",
                "isExam": "0"
            },
            {
                "code": "92910",
                "name": "从零起步打造个人办公智能体（一）",
                "passScore": "60",
                "learnScore": "100.00",
                "learnStatus": "2",
                "isExam": "0"
            },
            {
                "code": "92903",
                "name": "人工智能赋能公文处理 全面提升写作效率（二）",
                "passScore": "60",
                "learnScore": "96.00",
                "learnStatus": "2",
                "isExam": "0"
            },
            {
                "code": "92900",
                "name": "人工智能赋能公文处理 全面提升写作效率（一）",
                "passScore": "60",
                "learnScore": "100.00",
                "learnStatus": "2",
                "isExam": "0"
            },
            {
                "code": "92908",
                "name": "人工智能助力智能决策 从数据洞察到可视化呈现（二）",
                "passScore": "60",
                "learnScore": "100.00",
                "learnStatus": "2",
                "isExam": "0"
            },
            {
                "code": "92906",
                "name": "人工智能助力智能决策 从数据洞察到可视化呈现（一）",
                "passScore": "60",
                "learnScore": "100.00",
                "learnStatus": "2",
                "isExam": "0"
            },
            {
                "code": "92897",
                "name": "智能时代与人工智能协作的沟通法则——高效提示词撰写实战（二）",
                "passScore": "60",
                "learnScore": "96.00",
                "learnStatus": "2",
                "isExam": "0"
            },
            {
                "code": "92894",
                "name": "智能时代与人工智能协作的沟通法则——高效提示词撰写实战（一）",
                "passScore": "60",
                "learnScore": "96.00",
                "learnStatus": "2",
                "isExam": "0"
            },
            {
                "code": "92880",
                "name": "利用AI发现提炼创新成果",
                "passScore": "60",
                "learnScore": "100.00",
                "learnStatus": "2",
                "isExam": "0"
            },
            {
                "code": "92838",
                "name": "镍基耐蚀合金的发展与产品的典型应用",
                "passScore": "60",
                "learnScore": "45.79",
                "learnStatus": "1",
                "isExam": "0"
            },
            {
                "code": "92092",
                "name": "宝钢汽车板先进成形工艺研发及产业化",
                "passScore": "60",
                "learnScore": "0",
                "learnStatus": "0",
                "isExam": "0"
            },
            {
                "code": "92089",
                "name": "热成形钢产品发展与技术创新",
                "passScore": "60",
                "learnScore": "0",
                "learnStatus": "0",
                "isExam": "0"
            },
            {
                "code": "91802",
                "name": "企业高质量数据管理与治理",
                "passScore": "60",
                "learnScore": "0",
                "learnStatus": "0",
                "isExam": "0"
            },
            {
                "code": "91787",
                "name": "数据分析思维在岗位创新中的应用",
                "passScore": "60",
                "learnScore": "0",
                "learnStatus": "0",
                "isExam": "0"
            },
            {
                "code": "91737",
                "name": "SOP标准化作业及生产效率改善",
                "passScore": "60",
                "learnScore": "0",
                "learnStatus": "0",
                "isExam": "0"
            },
            {
                "code": "91734",
                "name": "TQM全面质量管理与品质零缺陷",
                "passScore": "60",
                "learnScore": "0",
                "learnStatus": "0",
                "isExam": "0"
            },
            {
                "code": "91648",
                "name": "Deeepseek+4大AI王炸组合实操攻略",
                "passScore": "60",
                "learnScore": "0",
                "learnStatus": "0",
                "isExam": "0"
            },
            {
                "code": "91278",
                "name": "推动“2526”工程 宝武企业级智能体构建及应用",
                "passScore": "60",
                "learnScore": "0",
                "learnStatus": "0",
                "isExam": "0"
            },
            {
                "code": "90930",
                "name": "DeepSeek技术解读与应用实践",
                "passScore": "60",
                "learnScore": "0",
                "learnStatus": "0",
                "isExam": "0"
            },
            {
                "code": "90846",
                "name": "AI赋能，成就“效率王者”——职场人士AI工具应用",
                "passScore": "60",
                "learnScore": "0",
                "learnStatus": "0",
                "isExam": "0"
            },
            {
                "code": "90508",
                "name": "AI场景赋能：DeepSeek业务应用实操及智能体初探",
                "passScore": "60",
                "learnScore": "0",
                "learnStatus": "0",
                "isExam": "0"
            },
            {
                "code": "90506",
                "name": "Manus风暴：AI的过去、现在和未来",
                "passScore": "60",
                "learnScore": "0",
                "learnStatus": "0",
                "isExam": "0"
            },
            {
                "code": "89665",
                "name": "人工智能大模型DeepSeek引发的技术创新、产业变革和竞争格局变化",
                "passScore": "60",
                "learnScore": "0",
                "learnStatus": "0",
                "isExam": "0"
            },
            {
                "code": "89655",
                "name": "协同推进降碳减污扩绿增长 加快经济社会发展全面绿色转型",
                "passScore": "60",
                "learnScore": "0",
                "learnStatus": "0",
                "isExam": "0"
            },
            {
                "code": "89266",
                "name": "构建科技成果转化生态体系的探索与实践",
                "passScore": "60",
                "learnScore": "0",
                "learnStatus": "0",
                "isExam": "0"
            },
            {
                "code": "89269",
                "name": "央国企科技成果转化实战指南",
                "passScore": "60",
                "learnScore": "0",
                "learnStatus": "0",
                "isExam": "0"
            },
            {
                "code": "89253",
                "name": "AI办公革命：DeepSeek助力工作效能提升",
                "passScore": "60",
                "learnScore": "0",
                "learnStatus": "0",
                "isExam": "0"
            },
            {
                "code": "89130",
                "name": "提升冷连轧生产线全流程算账经营能力的实践",
                "passScore": "60",
                "learnScore": "0",
                "learnStatus": "0",
                "isExam": "0"
            },
            {
                "code": "87992",
                "name": "探索冷弯型钢最高效的工艺流程",
                "passScore": "60",
                "learnScore": "0",
                "learnStatus": "0",
                "isExam": "0"
            },
            {
                "code": "87972",
                "name": "中国宝武绿色低碳发展战略与行动",
                "passScore": "60",
                "learnScore": "0",
                "learnStatus": "0",
                "isExam": "0"
            },
            {
                "code": "87974",
                "name": "转底炉技术与产业化应用",
                "passScore": "60",
                "learnScore": "0",
                "learnStatus": "0",
                "isExam": "0"
            },
            {
                "code": "85068",
                "name": "宝武固废不出厂实践与思考",
                "passScore": "60",
                "learnScore": "0",
                "learnStatus": "0",
                "isExam": "0"
            },
            {
                "code": "84811",
                "name": "大数据+AI与钢铁深度融合示范应用案例",
                "passScore": "60",
                "learnScore": "0",
                "learnStatus": "0",
                "isExam": "0"
            },
            {
                "code": "84833",
                "name": "冶金固废协同城市弃土应用于流态填筑材料的开发及工程应用实践",
                "passScore": "60",
                "learnScore": "0",
                "learnStatus": "0",
                "isExam": "0"
            },
            {
                "code": "84078",
                "name": "图灵机器人产品中的自主创新及应用",
                "passScore": "60",
                "learnScore": "0",
                "learnStatus": "0",
                "isExam": "0"
            },
            {
                "code": "82934",
                "name": "AI与钢铁深度融合示范应用",
                "passScore": "60",
                "learnScore": "0",
                "learnStatus": "0",
                "isExam": "0"
            },
            {
                "code": "82932",
                "name": "人工智能技术与钢铁应用探索",
                "passScore": "60",
                "learnScore": "0",
                "learnStatus": "0",
                "isExam": "0"
            },
            {
                "code": "82663",
                "name": "全面质量管理应用实践",
                "passScore": "60",
                "learnScore": "0",
                "learnStatus": "0",
                "isExam": "0"
            },
            {
                "code": "81957",
                "name": "巧用AIGC，助推企业数字化转型",
                "passScore": "60",
                "learnScore": "0",
                "learnStatus": "0",
                "isExam": "0"
            },
            {
                "code": "80446",
                "name": "企业精益管理思维与方法",
                "passScore": "60",
                "learnScore": "0",
                "learnStatus": "0",
                "isExam": "0"
            },
            {
                "code": "74491",
                "name": "机器人技术",
                "passScore": "60",
                "learnScore": "0",
                "learnStatus": "0",
                "isExam": "0"
            },
            {
                "code": "74465",
                "name": "设备在线监测管理技术规范和标准",
                "passScore": "60",
                "learnScore": "0",
                "learnStatus": "0",
                "isExam": "0"
            },
            {
                "code": "74467",
                "name": "设备智能管理和监测诊断技术应用",
                "passScore": "60",
                "learnScore": "0",
                "learnStatus": "0",
                "isExam": "0"
            },
            {
                "code": "74469",
                "name": "设备状态监测系统的集成与维护",
                "passScore": "60",
                "learnScore": "0",
                "learnStatus": "0",
                "isExam": "0"
            },
            {
                "code": "74231",
                "name": "储能技术发展及应用",
                "passScore": "60",
                "learnScore": "0",
                "learnStatus": "0",
                "isExam": "0"
            },
            {
                "code": "74080",
                "name": "企业数字化转型的新方向",
                "passScore": "60",
                "learnScore": "0",
                "learnStatus": "0",
                "isExam": "0"
            },
            {
                "code": "73983",
                "name": "我国“双碳”战略实施及企业转型路径展望",
                "passScore": "60",
                "learnScore": "0",
                "learnStatus": "0",
                "isExam": "0"
            },
            {
                "code": "71978",
                "name": "情报研究与专利文献获取",
                "passScore": "60",
                "learnScore": "0",
                "learnStatus": "0",
                "isExam": "0"
            },
            {
                "code": "2056636871253037056",
                "name": "TPM 管理在现场的应用考试",
                "passScore": "60",
                "learnScore": "100.0",
                "learnStatus": "3",
                "isExam": "1"
            },
            {
                "code": "2055106849820250112",
                "name": "AI 大模型赋能制造业场景考试",
                "passScore": "60",
                "learnScore": "90.0",
                "learnStatus": "3",
                "isExam": "1"
            },
            {
                "code": "2055106211724005376",
                "name": "变形高温合金应用及发展趋势考试",
                "passScore": "60",
                "learnScore": "80.0",
                "learnStatus": "3",
                "isExam": "1"
            },
            {
                "code": "2052220077289377792",
                "name": "制造业数字化基础知识与实践考试",
                "passScore": "60",
                "learnScore": null,
                "learnStatus": "1",
                "isExam": "1"
            },
            {
                "code": "2052220393518927872",
                "name": "新形势下产品技术创新与知识产权考试",
                "passScore": "60",
                "learnScore": "100.0",
                "learnStatus": "3",
                "isExam": "1"
            },
            {
                "code": "2051926714006769664",
                "name": "技术人员的体系化思维考试",
                "passScore": "60",
                "learnScore": null,
                "learnStatus": "1",
                "isExam": "1"
            },
            {
                "code": "2051925863469027328",
                "name": "数据质量管理与实战案例分析考试",
                "passScore": "60",
                "learnScore": null,
                "learnStatus": "1",
                "isExam": "1"
            }
        ],
        "total": 84,
        "size": 100,
        "current": 1,
        "pages": 1
    },
    "encrypt": false,
    "encryptType": "1"
}
```
