# 宝武学习系统挂课工具 — 实现计划

## 1. 项目目标

用 Python + tkinter 模拟宝武学习系统（https://learn.baowugroup.com）的课程视频观看行为，
实现"挂机"功能：自动循环播放队列中的课程视频，定时发送心跳，完成课时。

---

## 2. 已完成阶段：阶段一 — 登录

### 技术发现

| 项目 | 详情 |
|---|---|
| 登录 API | `POST /learn-gateway/service/ss/auth/user/login` |
| 验证码 API | `POST /learn-gateway/service/ss/auth/user/captchaImage` |
| 加密算法 | **SM2**（国密非对称加密，GB/T 32918） |
| 公钥（base64）| `BJeYoHWNsf60Vr2wPJWEWRvjH6m5r/JvK7Pww8SdohnwAkHKVy0tikYYOYmuKhR83BUS+duMyjAbVtyXZTfc+jY=` |
| 密文格式 | C1（128 hex，无04前缀）+ C3（SM3哈希，64 hex）+ C2（密文）|
| Token 头名称 | `token`（不是 `Authorization: Bearer`） |
| Python 库 | `gmssl` |

### 登录请求体

```json
{
  "mobile": "",
  "loginName": "<SM2加密后的工号，hex字符串>",
  "password": "<SM2加密后的密码，hex字符串>",
  "captchaCode": "<用户输入的验证码文本>",
  "captchaNum": "",
  "captchaId": "<captchaImage接口返回的ID>",
  "type": "byPassword",
  "clientType": "PC"
}
```

### 已创建文件

```
baowulearn/
├── main.py                   ✅ 入口（启动登录窗口）
├── requirements.txt          ✅ requests, Pillow, gmssl
├── config.py                 ✅ BASE_URL + SM2公钥 + 默认请求头
├── core/
│   ├── __init__.py           ✅
│   └── crypto.py             ✅ sm2_encrypt() 函数
├── api/
│   ├── __init__.py           ✅
│   ├── client.py             ✅ requests.Session 封装
│   └── auth.py               ✅ get_captcha() + login()
├── ui/
│   ├── __init__.py           ✅
│   └── login_window.py       ✅ tkinter 登录窗口
└── models/
    └── __init__.py           ✅
```

---

## 3. 已完成阶段：阶段二 — 课程列表

### 技术发现

| 项目 | 详情 |
|---|---|
| 课程列表 API | `POST /learn-gateway/service/tms/ols/student/queryPageOpenClass` |
| 分页参数 | `{"current":1,"size":100,"data":{"learnStatus":"","searchInfo":"","searchType":"1","sortClass":"1","sortType":"desc"}}` |
| learnStatus | `""` 全部，`"1"` 学习中，`"2"` 已完成 |

### 课程记录关键字段

| 字段 | 含义 |
|---|---|
| `courseGuid` | 课程 ID |
| `courseNo` | 课程编号（所有视频 API 均用此字段） |
| `courseName` | 课程名称 |
| `olClassName` | 所属班级名称 |
| `guid` / `olClassNo` | 班级课程 ID（视频 API 中用作 olClassNo） |
| `learnStatus` | `"1"` 学习中 / `"2"` 已完成 |
| `courseHours` | 总时长（小时，float） |
| `nearLearnHours` | 已学时长（秒，int） |
| `centerCode` | 学习中心代码（如 `"C001"`） |
| `tenantCode` | 租户代码（如 `"BSTA"`，finishInfo 接口使用） |

### 新增文件

```
models/
├── course.py             ✅ Course dataclass + HangStatus 枚举
api/
└── course.py             ✅ get_courses()
ui/
└── main_window.py        ✅ Treeview 课程列表 + 工具栏按钮
```

---

## 4. 已完成阶段：阶段三 — 挂机引擎

### 技术发现：视频 API

#### 获取视频列表
```
POST /service/tms/rls/courseOutline/queryCourseOutlineContentTreeListSimple
Body: {"centerCode":"C001","courseNo":"<courseNo>","isAppendPre":"1"}
```
响应 `data[].content[]` 中取 `contentType=="1"` 且 `status=="1"` 的条目：

| 字段 | 含义 |
|---|---|
| `cataNo` | 视频 ID（所有视频 API 均用此字段） |
| `wareCode` | 资源 ID（用作 `wareId`） |
| `wareType` | 资源类型（固定 `"1"`） |
| `duration` | 时长（秒，整数） |
| `markeTimePoint` | 进度打卡时间点，逗号分隔的 `HH:MM:SS` 串 |
| `newContentName` | 视频标题 |

#### 初始化学习记录（每门课调用一次）
```
POST /service/tms/ols/learnRecord/initLearnRecord
Body: {"courseNo":"...","olClassNo":"...","pageId":"<uuid4>"}
```
`pageId` 在整个课程会话中保持不变。

#### 视频播放控制
```
POST /service/tms/ols/learnVideoRecord/listenVideoOptRecord
开始: operateType="1", videoStatus="1", videoBeginTime="<续播位置 HH:MM:SS>"
结束: operateType="2", videoStatus="2", videoBeginTime="<结束位置 HH:MM:SS>"
```

#### 心跳（每 60 秒）
```
POST /service/tms/ols/learnHertRecord/saveLearnHertRecord
Body: {cataNo, classCourseCenterCode, courseNo, curPlayTime:"HH:MM:SS",
       isBlur:"0", learnRealTime:<delta秒>, learnTime:<delta秒>,
       olClassNo, pageId, status:"1", videoSpeed:1, wareId, wareType}
```
`learnRealTime` = 距上次心跳的秒数。最后一次心跳在视频结束时发送，值为剩余秒数。

#### 进度打卡（在 markeTimePoint 时刻）
```
POST /service/tms/ols/learnWareProgress/listenVideoMarkProgress
Body: {cataNo, courseNo, curPlayTime, markeTimePoint, olClassNo, pageId, wareId, wareType}
```

#### 完成视频
```
POST /service/tms/ols/computeTask/saveComputeTask4AfterVideoPlayed
Body: {"classNo":"<olClassNo>","courseNo":"<courseNo>"}
```

#### 查询已播放最大时间（续播）
```
POST /service/tms/ols/learnWareProgress/getMaxTimeAndLastTime
Body: {cataNo, courseNo, olClassNo, wareId, wareType}
Response: data.maxPlayTime "HH:MM:SS"
```
返回该视频历史最大播放位置，用于**续播**。若 `maxPlayTime >= duration` 则跳过该视频。

#### 查询课程完成情况
```
POST /service/tms/ols/onlineClassCourse/finishInfo
Body: {"centerCode":"C001","courseNo":"...","olClassNo":"...","tenantCode":"BSTA"}
Response: data.details[].{attributeName, finishValue(分钟), predValue(要求分钟), percentage}
```
每次心跳后调用，结果存入 `Course.finish_info`，实时展示在课程列表的"已学时长"列。

### 每视频挂机流程

```
initLearnRecord (每门课一次)
for each video:
  1. getMaxTimeAndLastTime → start_secs
     if start_secs >= duration → 跳过（已完成）
  2. listenVideoOptRecord (start, videoBeginTime=start_secs)
  3. 循环 (每秒 sleep 1):
       elapsed += 1
       if mark_point <= elapsed → listenVideoMarkProgress
       if elapsed - last_hb >= 60 → saveLearnHertRecord + finishInfo
  4. 最后一次 saveLearnHertRecord (剩余秒)
  5. saveComputeTask4AfterVideoPlayed
  6. listenVideoOptRecord (end)
  7. finishInfo (刷新完成情况)
```

### 新增文件

```
models/
└── video.py              ✅ Video dataclass + _parse_mark_points()
api/
└── video.py              ✅ get_course_videos / init_learn_record /
                               start_video / end_video / send_heartbeat /
                               mark_progress / complete_video /
                               get_play_progress / get_finish_info
core/
├── heartbeat_worker.py   ✅ HeartbeatWorker 后台线程（含续播、进度打卡、容错重试）
└── queue_manager.py      ✅ QueueManager 队列状态机
ui/
└── main_window.py        ✅ 更新：队列按钮接入 QueueManager，
                               状态栏实时显示挂机进度，
                               已学时长列展示 finishInfo 数据
```

---

## 5. 待完成阶段

### 阶段四 — 打包

```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

生成 `dist/main.exe`，无需 Python 环境即可运行。

---

## 6. 当前项目结构

```
baowulearn/
├── main.py                   ✅ 入口（登录 → 主窗口）
├── config.py                 ✅ BASE_URL + SM2公钥 + 请求头
├── requirements.txt          ✅ requests, Pillow, gmssl
├── PLAN.md                   ✅ 本文件
├── .gitignore                ✅
├── core/
│   ├── __init__.py           ✅
│   ├── crypto.py             ✅ sm2_encrypt()
│   ├── heartbeat_worker.py   ✅ HeartbeatWorker
│   └── queue_manager.py      ✅ QueueManager
├── api/
│   ├── __init__.py           ✅
│   ├── client.py             ✅ requests.Session 封装
│   ├── auth.py               ✅ get_captcha() + login()
│   ├── course.py             ✅ get_courses()
│   └── video.py              ✅ 全部视频相关 API
├── ui/
│   ├── __init__.py           ✅
│   ├── login_window.py       ✅ 登录窗口
│   └── main_window.py        ✅ 课程列表 + 挂机控制
└── models/
    ├── __init__.py           ✅
    ├── course.py             ✅ Course dataclass + HangStatus
    └── video.py              ✅ Video dataclass
```

---

## 7. 架构约定

| 约定 | 说明 |
|---|---|
| UI 框架 | tkinter + ttk（内置，零 UI 依赖） |
| HTTP | `requests.Session`（持久连接，自动带 Cookie） |
| 加密 | `gmssl.sm2.CryptSM2` |
| 图片 | `PIL.Image` → `ImageTk.PhotoImage` 显示在 Label 中 |
| 后台线程 | `threading.Thread(daemon=True)` |
| 线程安全 | 后台线程通过 `root.after(0, callback)` 更新 UI |
| 停止信号 | `threading.Event` |
| Token 存储 | `api/client.py` 模块级变量，写入 Session headers |
| 续播 | 每视频开始前查 `getMaxTimeAndLastTime`，从 maxPlayTime 续播 |
| 完成情况 | 每次心跳后查 `finishInfo`，存入 `Course.finish_info`，UI 实时刷新 |
