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

## 整体说明

本目录中的接口示例可以按两条主线理解：一条是公开课学习链路，另一条是专区学习链路。两条链路在入口不同，但进入单门课程后，会收敛到同一套课程详情、视频播放、进度上报和完成度统计接口。

从阅读顺序上看，可以先理解入口接口如何拿到 `olClassNo`、`guid`、`courseNo`，再理解这些标识如何在课程详情、目录查询、学习初始化、播放上报和统计接口之间传递。

## 文件命名约定

本目录中的单接口文档不再直接使用接口原始方法名作为文件名，而是改为按业务语义命名。这样做的目的是让文件名本身就能表达“这个接口在学习链路里负责什么”，而不是要求读者先理解接口字段名。

命名上按职责分组：`auth-*` 表示认证接口，`open-*` 和 `zone-*` 表示入口与列表接口，`course-*` 表示课程详情和目录接口，`learn-*` 表示学习过程接口，`compute-*` 表示重算或刷新接口，`stats-*` 表示统计结果接口。

## 按学习链路说明

### 公开课学习链路

公开课链路从登录开始。登录成功后，通过 [auth-login.md](./auth-login.md) 获取 `accessToken`，再用 [open-course-list.md](./open-course-list.md) 获取公开课列表。这个列表接口会返回后续要继续使用的 `olClassNo`、`courseGuid` 和 `courseNo`。

拿到课程标识后，先用 [course-detail.md](./course-detail.md) 查询课程详情，再用 [course-outline.md](./course-outline.md) 获取视频目录。目录接口会返回具体视频的 `cataNo`、`wareId`/`wareCode`、`wareType` 和 `markeTimePoint`，这些字段会直接进入后续播放链路。

真正开始学习前，需要调用 [learn-init-record.md](./learn-init-record.md) 建立学习会话，并生成后续心跳和打点接口要复用的 `pageId`。随后可通过 [learn-playback-progress.md](./learn-playback-progress.md) 恢复历史播放进度，并可通过 [learn-heartbeat-interval.md](./learn-heartbeat-interval.md) 读取服务端配置的心跳发送间隔，再结合 [learn-video-event.md](./learn-video-event.md)、[learn-heartbeat.md](./learn-heartbeat.md) 和 [learn-mark-progress.md](./learn-mark-progress.md) 完成动作上报、心跳累计和关键时间点打卡。

当视频达到完成条件后，通常还要继续调用 [compute-video-finish.md](./compute-video-finish.md) 和 [compute-course-finish.md](./compute-course-finish.md) 触发服务端重算，最后再通过 [stats-course-finish.md](./stats-course-finish.md) 查看课程完成情况和得分进度。

### 专区学习链路

专区链路同样从登录开始。登录成功后，先通过 [zone-list.md](./zone-list.md) 获取专区列表，拿到目标专区的 `olClassNo`。进入专区后，再通过 [zone-course-list.md](./zone-course-list.md) 获取该专区下的课程列表，并拿到课程 `guid` 和 `courseNo`。

当进入某门课程后，后续学习流程与公开课一致，仍然会依次使用课程详情、课程目录、学习初始化、播放事件、心跳、打点和课程完成度刷新接口。

专区链路和公开课链路的主要区别在统计维度。课程学习完成后，除了刷新课程完成度，还可以使用 [compute-zone-finish.md](./compute-zone-finish.md) 触发专区维度的重算，再分别通过 [stats-zone-total.md](./stats-zone-total.md) 查看专区总体完成度，通过 [stats-zone-items.md](./stats-zone-items.md) 查看专区内每门课程的完成情况。

## 按接口分组说明

### 认证接口

这组接口负责建立登录态，为后续所有业务请求准备访问令牌。

| 接口 | 路径 | 主要作用 | 结果关注点 |
| --- | --- | --- | --- |
| [auth-login.md](./auth-login.md) | `/ss/auth/user/login` | 完成账号登录 | `data.accessToken`、`expiresTime`、租户信息 |

### 入口与列表接口

这组接口负责拿到学习入口和课程入口，是整条学习链路的起点。它们的共同特点是返回后续接口需要复用的 `olClassNo`、`guid` 或 `courseNo`。

| 接口 | 路径 | 主要作用 | 结果关注点 |
| --- | --- | --- | --- |
| [zone-list.md](./zone-list.md) | `/tms/ols/student/myClassPage` | 获取学习专区列表 | 专区 `olClassNo`、名称、课程数 |
| [zone-course-list.md](./zone-course-list.md) | `/tms/ols/onlineClassCourse/getOnlineClassCourseSortPage` | 获取专区课程列表 | 课程 `guid`、`courseNo`、`learnStatus` |
| [open-course-list.md](./open-course-list.md) | `/tms/ols/student/queryPageOpenClass` | 获取公开课列表 | `olClassNo`、`courseGuid`、`courseNo`、`learnStatus` |

### 课程详情与目录接口

这组接口负责把“课程入口标识”转成“可学习内容”。前者补齐课程详情信息，后者给出具体的视频目录和播放标识。

| 接口 | 路径 | 主要作用 | 结果关注点 |
| --- | --- | --- | --- |
| [course-detail.md](./course-detail.md) | `/tms/ols/onlineClassCourse/detailOnlineClassCourse` | 查询课程详情 | `courseNo`、`olClassNo`、讲师、课时、课程简介 |
| [course-outline.md](./course-outline.md) | `/tms/rls/courseOutline/queryCourseOutlineContentTreeListSimple` | 查询课程目录 | `cataNo`、`wareCode`/`wareId`、`duration`、`markeTimePoint` |

### 学习初始化与进度恢复接口

这组接口负责在真正播放前建立学习会话、恢复历史进度，并读取播放前需要确定的关键配置。它们的输出会直接影响播放器从哪里开始、后续请求携带哪个会话标识，以及心跳按什么频率发送。

| 接口 | 路径 | 主要作用 | 结果关注点 |
| --- | --- | --- | --- |
| [learn-init-record.md](./learn-init-record.md) | `/tms/ols/learnRecord/initLearnRecord` | 初始化学习会话 | `pageId` 对应的默认节点、`lastPlayTime` |
| [learn-playback-progress.md](./learn-playback-progress.md) | `/tms/ols/learnWareProgress/getMaxTimeAndLastTime` | 查询历史播放进度 | `maxPlayTime`、`lastPlayTime` |
| [learn-heartbeat-interval.md](./learn-heartbeat-interval.md) | `/ss/properties/queryPropValue` | 查询学习心跳发送间隔 | `propertiesValue`、`propertiesDesc` |

### 播放过程上报接口

这组接口共同组成视频学习过程中的核心上报链路。动作事件负责记录播放器行为，心跳负责累计时长，打点负责确认关键时间点已经被观看。

| 接口 | 路径 | 主要作用 | 结果关注点 |
| --- | --- | --- | --- |
| [learn-video-event.md](./learn-video-event.md) | `/tms/ols/learnVideoRecord/listenVideoOptRecord` | 上报播放动作事件 | `operateType` 对应的动作语义、`data: "true"` |
| [learn-heartbeat.md](./learn-heartbeat.md) | `/tms/ols/learnHertRecord/saveLearnHertRecord` | 周期性发送学习心跳 | `status`、`heartDesc` |
| [learn-mark-progress.md](./learn-mark-progress.md) | `/tms/ols/learnWareProgress/listenVideoMarkProgress` | 在关键打点时间上报进度 | `status`、`heartDesc` |

### 完成度计算与统计接口

这组接口负责把播放过程中的学习记录转成课程或专区层面的最终结果。它们通常在学习动作完成后触发，用于刷新服务端统计值。

| 接口 | 路径 | 主要作用 | 结果关注点 |
| --- | --- | --- | --- |
| [compute-video-finish.md](./compute-video-finish.md) | `/tms/ols/computeTask/saveComputeTask4AfterVideoPlayed` | 触发单个视频完成计算 | 计算任务 ID |
| [compute-course-finish.md](./compute-course-finish.md) | `/tms/ols/computeTask/saveComputeTask4StuCourseDetail` | 刷新课程完成度 | 计算任务 ID |
| [compute-zone-finish.md](./compute-zone-finish.md) | `/tms/ols/computeTask/saveComputeTask4StuClassDetail` | 刷新区完成度 | 计算任务 ID |
| [stats-course-finish.md](./stats-course-finish.md) | `/tms/ols/onlineClassCourse/finishInfo` | 查询课程完成情况 | `learnScore`、`learnStatus`、课程明细 |
| [stats-zone-total.md](./stats-zone-total.md) | `/tms/ols/onlineClass/totalFinishStatistics` | 查询专区总体完成度 | 总体 `learnScore`、`passScore`、统计规则 |
| [stats-zone-items.md](./stats-zone-items.md) | `/tms/ols/onlineClass/itemFinishStatisticsSortPage` | 查询专区课程分项情况 | 课程 `name`、`learnScore`、`learnStatus` |

## 阅读要点

1. 课程播放不是只靠一个接口完成，而是“初始化 + 动作事件 + 心跳 + 打点 + 完成度刷新”的组合。
2. `pageId` 是一次学习会话的重要关联键，`initLearnRecord`、`saveLearnHertRecord`、`listenVideoMarkProgress` 都会用到。
3. `queryCourseOutlineContentTreeListSimple` 返回的 `markeTimePoint` 是打卡依据，`listenVideoMarkProgress` 需要在这些时间点附近发送。
4. 平台区分“视频动作事件”和“学习时长心跳”：前者由 `listenVideoOptRecord` 记录行为，后者由 `saveLearnHertRecord` 累积时长。
5. 完成播放后还需要显式调用计算类接口，否则课程或专区完成度不一定会立即刷新。
6. 公开课和专区最终都收敛到同一套课程播放与统计接口，区别主要在入口列表和统计维度。

## 新增接口文档规范

本节面向维护者和 AI 会话使用，不参与本目录的正常阅读顺序。无论是新的 AI 会话，还是人工补文档，只要要在本目录新增单接口文档，都应先阅读本节，再执行新增和 README 更新。

### 输入约定

新增接口文档时，至少应提供以下信息：

- 接口 URL
- 请求方式
- 请求体示例
- 响应体示例

如果已知，建议一并提供以下补充信息，AI 可直接复用；如果未提供，则由 AI 基于接口路径、字段和现有文档风格自行判断：

- 原始接口名
- 接口作用
- 调用时机
- 前置条件
- 后续依赖

推荐输入格式如下。字段名称可以保持中文，只要语义明确即可：

````markdown
原始接口名: listenVideoStart
接口 URL: /tms/ols/learnVideoRecord/listenVideoStart
请求方式: POST

接口作用:
开始播放视频时通知服务端建立一次播放动作。

请求体:
```json
{
	"pageId": "<pageId>",
	"cataNo": "<cataNo>",
	"wareId": "<wareId>",
	"wareType": "1"
}
```

响应体:
```json
{
	"isSuccess": true,
	"statusCode": 200,
	"data": true
}
```
````

### AI 执行规则

当用户提供上述基本信息后，AI 应按以下顺序完成新增：

1. 先通读本 README，并以本文件为唯一风格和结构来源。
2. 判断该接口所属分组，并生成业务语义化文件名。
3. 新建单接口文档，结构必须与本节中的标准骨架一致。
4. 在文档中保留“业务标题 + 原始接口名副标题”，确保业务可读和接口可追溯同时成立。
5. 对请求体、响应体、请求头、响应头和字段说明中的敏感信息做脱敏处理。
6. 更新本 README 中对应分组的索引表，补入新文档链接、接口路径、主要作用和结果关注点。
7. 如果该接口改变了阅读顺序或学习链路，应同步调整“按学习链路说明”中的相关描述；如果不影响链路，则只更新接口分组表即可。

### 分组与命名规则

- 认证与登录接口：使用 `auth-*`
- 公开课入口或公开课列表接口：使用 `open-*`
- 专区入口、专区列表、专区课程列表接口：使用 `zone-*`
- 课程详情、课程目录、课程基础查询接口：使用 `course-*`
- 学习初始化、播放恢复、播放事件、心跳、打点等学习过程接口：使用 `learn-*`
- 完成度刷新、重算、补计算接口：使用 `compute-*`
- 课程统计、专区统计、分项统计接口：使用 `stats-*`

业务文件名应优先表达“用途”而不是照抄接口名，例如：

- `finishInfo` -> `stats-course-finish.md`
- `queryCourseOutlineContentTreeListSimple` -> `course-outline.md`
- `saveLearnHertRecord` -> `learn-heartbeat.md`

如果无法精确判断业务语义，优先选择最接近的职责分组，并在文档顶部保留原始接口名，不得退回到直接以原始接口名命名文件。

### 标准文档骨架

新增单接口文档时，必须使用以下结构。可以根据接口复杂度补充 `### 场景说明` 等小节，但不得删减主结构。

````markdown
# <业务标题>

> 原始接口名：<rawApiName>

<用一句话说明这个接口解决什么问题。>

<请求方式> https://learn.baowugroup.com/learn-gateway/service<接口 URL>

## 接口概览

- 接口作用：<说明接口在业务流程中的职责>
- 调用时机：<说明通常在什么时候调用>
- 前置条件：<说明调用前需要先拿到哪些标识或令牌>
- 后续依赖：<说明该接口结果会被哪些后续接口继续使用>

## 请求示例

<用一小段话说明这个请求体在什么场景下发送。>

### 请求字段说明

- `<字段名>`: <说明字段含义和作用>

### 请求体

```json
{}
```

## 响应示例

<用一小段话说明这个响应的阅读重点。>

### 响应字段说明

- `<字段路径>`: <说明字段含义和后续用途>

### 响应体

```json
{}
```
````

### 脱敏规则

新增或修改文档时，不得写入真实敏感信息。以下内容必须替换为占位符：

- `token`、`accessToken`、验证码 ID、会话 ID
- 用户名、工号、姓名、手机号、密码、邮箱
- 可直接定位个人或内部人员身份的编号
- 明显属于真实环境的追踪 ID、请求链路 ID

推荐占位符包括：`<accessToken>`、`<验证码ID>`、`<工号>`、`<讲师姓名>`、`<创建人工号>`、`<traceId>`。

### README 更新规则

新增单接口文档后，必须同步更新本 README：

- 在对应分组表格中新增一行，包含文档链接、接口路径、主要作用、结果关注点。
- 如果新接口属于现有链路中的一环，且会影响读者理解调用顺序，应补写到“按学习链路说明”中。
- 如果新接口只是现有分组的补充，不改变阅读顺序，则只更新分组表格，不改动链路说明。
- 新增条目时，优先保持同组接口放在相近职责位置，不按数字排序，不要求全表重排。
