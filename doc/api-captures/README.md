# api-captures

本目录收集了宝武学习平台核心学习流程的抓包示例，覆盖登录、专区/公开课列表、课程详情、视频播放上报以及完成度统计。

## 通用约定

- Host: `https://learn.baowugroup.com`
- 网关前缀: `/learn-gateway/service`
- 请求方式: `GET` 或 `POST`
- 认证: 除登录接口外，其余接口都需要在请求头中携带 `token`
- 内容类型: `application/json;charset=UTF-8`
- 响应结构通常为:

```json
{
	"isSuccess": true,
	"statusCode": 200,
	"message": "",
	"data": {},
    "jwt": null,
    "encrypt": false,
    "encryptType": "1"
}
```

## 请求头与响应头

### 请求头

| 头字段 | 是否关键 | 说明 |
| --- | --- | --- |
| `token` | 必需（除登录外） | 登录后获得的访问令牌。文档中的令牌统一用 `<accessToken>` 表示。 |
| `Content-Type: application/json;charset=UTF-8` | 必需 | 请求体使用 JSON 编码 |
| `Accept: application/json, text/plain, */*` | 建议保留 | 前端常规声明，服务端返回 JSON |
| `Origin: https://learn.baowugroup.com` | 建议保留 | 浏览器环境下的来源声明，和跨域策略有关 |
| `Referer: https://learn.baowugroup.com/` | 建议保留 | 浏览器页面来源，通常随前端请求一起发送 |
| `User-Agent` / `sec-ch-ua*` / `Sec-Fetch-*` | 可选 | 这些更偏浏览器上下文字段，程序化请求通常不是核心鉴权条件 |

### 响应头

| 头字段 | 说明 |
| --- | --- |
| `Content-Type: application/json` | 响应体是 JSON，可直接按统一响应结构解析 |
| `X-Trace-Id` / `X-Req-Id` | 服务端链路追踪字段，排查请求问题时有用 |
| `Access-Control-Allow-*` | 跨域相关响应头，主要服务于浏览器端调用 |
| `Cache-Control` / `Pragma` / `Expires` | 表明接口响应通常不缓存 |
| `Server` / `x-via` / `x-ws-request-id` | 网关/CDN/接入层信息，通常只在诊断网络链路时使用 |

## 关键字段

| 字段 | 含义 |
| --- | --- |
| `olClassNo` | 学习项目/公开课/专区编号，后续大多数接口都会依赖它 |
| `guid` | 某门课程在专区或公开课中的记录主键，常用于查询课程详情 |
| `courseNo` | 课程编号，查询视频列表、初始化学习、刷新课程完成度时使用 |
| `cataNo` | 视频目录或课件节点编号 |
| `wareId` | 视频资源或课件资源编号 |
| `wareType` | 资源类型，样例中视频均为 `1` |
| `pageId` | 一次学习会话的页面标识，初始化学习后在心跳/打点中复用 |
| `centerCode` | 学习中心编号，样例中常见为 `C001` |
| `tenantCode` | 租户编号，样例中为 `BSTA` |

## 调用链概览

### 公开课学习流程

1. [login.md](./login.md): 登录，换取 `accessToken`
2. [queryPageOpenClass.md](./queryPageOpenClass.md): 获取公开课列表，拿到 `olClassNo`、`courseGuid`、`courseNo`
3. [detailOnlineClassCourse.md](./detailOnlineClassCourse.md): 根据课程 `guid` 查询课程详情
4. [queryCourseOutlineContentTreeListSimple.md](./queryCourseOutlineContentTreeListSimple.md): 根据 `courseNo` 拉取视频列表与每个视频的 `cataNo`、`wareId`、`markeTimePoint`
5. [initLearnRecord.md](./initLearnRecord.md): 开始学习前初始化记录，建立 `pageId` 对应的学习会话
6. [getMaxTimeAndLastTime.md](./getMaxTimeAndLastTime.md): 查询该视频的历史播放进度
7. [listenVideoOptRecord.md](./listenVideoOptRecord.md): 上报开始、暂停、拖动、回到焦点等播放事件
8. [saveLearnHertRecord.md](./saveLearnHertRecord.md): 按固定间隔发送学习心跳，累计学习时长
9. [listenVideoMarkProgress.md](./listenVideoMarkProgress.md): 到达关键打点时间时上报一次打卡
10. [saveComputeTask4AfterVideoPlayed.md](./saveComputeTask4AfterVideoPlayed.md): 视频播放完成后触发视频完成计算
11. [saveComputeTask4StuCourseDetail.md](./saveComputeTask4StuCourseDetail.md): 刷新课程完成度
12. [finishInfo.md](./finishInfo.md): 查询课程完成情况与得分进度

### 专区学习流程

1. [login.md](./login.md): 登录
2. [myClassPage.md](./myClassPage.md): 获取学习专区列表，拿到专区 `olClassNo`
3. [getOnlineClassCourseSortPage.md](./getOnlineClassCourseSortPage.md): 获取专区下课程列表，拿到课程 `guid` 与 `courseNo`
4. 进入课程后的学习流程与公开课相同，仍然会使用课程详情、视频目录、初始化学习、播放上报和完成度刷新接口
5. [totalFinishStatistics.md](./totalFinishStatistics.md): 查询专区整体完成度
6. [itemFinishStatisticsSortPage.md](./itemFinishStatisticsSortPage.md): 查询专区下每门课程的完成情况
7. [saveComputeTask4StuClassDetail.md](./saveComputeTask4StuClassDetail.md): 刷新区整体完成度

## 接口分组整理

### 1. 认证

| 接口 | 路径 | 作用 | 关键输入 | 关键输出 |
| --- | --- | --- | --- | --- |
| [login.md](./login.md) | `/ss/auth/user/login` | 用户登录 | `loginName`、`password` 需要先做 SM2 加密，另含验证码字段 | `data.accessToken`、`expiresTime`、用户信息 |

### 2. 课程与专区列表

| 接口 | 路径 | 作用 | 关键输入 | 关键输出 |
| --- | --- | --- | --- | --- |
| [myClassPage.md](./myClassPage.md) | `/tms/ols/student/myClassPage` | 查询学习专区列表 | `classType`、`status`、分页参数 | 专区 `guid`/`olClassNo`、名称、时间范围、课程数 |
| [getOnlineClassCourseSortPage.md](./getOnlineClassCourseSortPage.md) | `/tms/ols/onlineClassCourse/getOnlineClassCourseSortPage` | 查询专区下课程列表 | `olClassNo`、`olClassType`、分页参数 | 课程 `guid`、`courseNo`、`courseName`、`learnStatus` |
| [queryPageOpenClass.md](./queryPageOpenClass.md) | `/tms/ols/student/queryPageOpenClass` | 查询公开课列表 | `searchType`、`searchInfo`、分页参数 | `olClassNo`、`courseGuid`、`courseNo`、`courseName`、最近学习时间 |

### 3. 课程详情与目录

| 接口 | 路径 | 作用 | 关键输入 | 关键输出 |
| --- | --- | --- | --- | --- |
| [detailOnlineClassCourse.md](./detailOnlineClassCourse.md) | `/tms/ols/onlineClassCourse/detailOnlineClassCourse` | 查询课程详情 | `guid`、`centerCode`、`stuClient` | 课程标题、教师、课时、课程简介、所属 `olClassNo` |
| [queryCourseOutlineContentTreeListSimple.md](./queryCourseOutlineContentTreeListSimple.md) | `/tms/rls/courseOutline/queryCourseOutlineContentTreeListSimple` | 查询课程视频目录 | `courseNo`、`centerCode` | 每个视频的 `cataNo`、`wareCode`/`wareId`、`duration`、`markeTimePoint`、`hashCode` |

### 4. 学习初始化与进度恢复

| 接口 | 路径 | 作用 | 关键输入 | 关键输出 |
| --- | --- | --- | --- | --- |
| [initLearnRecord.md](./initLearnRecord.md) | `/tms/ols/learnRecord/initLearnRecord` | 开始学习前初始化会话 | `courseNo`、`olClassNo`、`pageId` | 当前课件的 `cataNo`、`wareCode`、`lastPlayTime` |
| [getMaxTimeAndLastTime.md](./getMaxTimeAndLastTime.md) | `/tms/ols/learnWareProgress/getMaxTimeAndLastTime` | 获取视频历史播放进度 | `courseNo`、`olClassNo`、`cataNo`、`wareId` | `maxPlayTime`、`lastPlayTime` |

### 5. 播放过程上报

| 接口 | 路径 | 作用 | 关键输入 | 关键输出 |
| --- | --- | --- | --- | --- |
| [listenVideoOptRecord.md](./listenVideoOptRecord.md) | `/tms/ols/learnVideoRecord/listenVideoOptRecord` | 上报播放动作事件 | `operateType` 区分开始(`1`)、停止(`2`)、拖动(`4`)、重新聚焦(`5`) | `data: "true"` |
| [saveLearnHertRecord.md](./saveLearnHertRecord.md) | `/tms/ols/learnHertRecord/saveLearnHertRecord` | 定时心跳，累计学习时长 | `curPlayTime`、`learnTime`、`learnRealTime`、`pageId`、`isBlur` | `status: success` |
| [listenVideoMarkProgress.md](./listenVideoMarkProgress.md) | `/tms/ols/learnWareProgress/listenVideoMarkProgress` | 在关键打点时间上报进度 | `curPlayTime`、`markeTimePoint`、`pageId` | `heartDesc: 成功` |

### 6. 完成度计算与统计

| 接口 | 路径 | 作用 | 关键输入 | 关键输出 |
| --- | --- | --- | --- | --- |
| [saveComputeTask4AfterVideoPlayed.md](./saveComputeTask4AfterVideoPlayed.md) | `/tms/ols/computeTask/saveComputeTask4AfterVideoPlayed` | 单个视频播放结束后触发计算 | `classNo`、`courseNo` | 计算任务 ID |
| [saveComputeTask4StuCourseDetail.md](./saveComputeTask4StuCourseDetail.md) | `/tms/ols/computeTask/saveComputeTask4StuCourseDetail` | 刷新课程完成度 | `classNo`、`courseNo` | 计算任务 ID |
| [saveComputeTask4StuClassDetail.md](./saveComputeTask4StuClassDetail.md) | `/tms/ols/computeTask/saveComputeTask4StuClassDetail` | 刷新区完成度 | `classNo` | 计算任务 ID |
| [finishInfo.md](./finishInfo.md) | `/tms/ols/onlineClassCourse/finishInfo` | 查询课程完成情况 | `courseNo`、`olClassNo`、`tenantCode` | `learnScore`、`learnStatus`、考试/学时/调查等明细 |
| [totalFinishStatistics.md](./totalFinishStatistics.md) | `/tms/ols/onlineClass/totalFinishStatistics` | 查询专区总体完成度 | `olClassNo`、`centerCode`、`tenantCode` | 总体 `learnScore`、`passScore`、统计规则说明 |
| [itemFinishStatisticsSortPage.md](./itemFinishStatisticsSortPage.md) | `/tms/ols/onlineClass/itemFinishStatisticsSortPage` | 查询专区分课程完成情况 | `olClassNo`、分页参数 | 每门课程的 `code`、`name`、`learnScore`、`learnStatus` |

## 从抓包可以看出的实现要点

1. 课程播放不是只靠一个接口完成，而是“初始化 + 事件上报 + 心跳 + 打点 + 完成度刷新”的组合。
2. `pageId` 是一次学习会话的重要关联键，`initLearnRecord`、`saveLearnHertRecord`、`listenVideoMarkProgress` 都会用到。
3. `queryCourseOutlineContentTreeListSimple` 返回的 `markeTimePoint` 是打卡依据，`listenVideoMarkProgress` 需要在这些时间点附近发送。
4. 平台区分“视频动作事件”和“学习时长心跳”：前者由 `listenVideoOptRecord` 记录行为，后者由 `saveLearnHertRecord` 累积时长。
5. 完成播放后还需要显式调用计算类接口，否则课程或专区完成度不一定会立即刷新。
6. 公开课和专区最终都收敛到同一套课程播放与统计接口，区别主要在入口列表和统计维度。
