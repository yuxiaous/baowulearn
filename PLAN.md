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

### 运行方式

```bash
# 安装依赖
pip install -r requirements.txt

# 运行
python main.py
```

---

## 3. 待完成阶段

### 阶段二 — 课程列表（需要新 HAR）

**需要用户抓包的操作：** 登录后进入课程列表页面

**需要找到的 API：**
- 获取课程列表（公开课、必修课等）
- 每门课的字段：ID、名称、状态、总时长、已看时长、成绩

**计划实现：**
- `api/course.py`：`get_courses() → List[Course]`
- `models/course.py`：`Course` dataclass
- `ui/main_window.py`：`ttk.Treeview` 课程列表，显示状态/时长/成绩

### 阶段三 — 挂机引擎（需要新 HAR）

**需要用户抓包的操作：** 开始观看视频，等待约 60 秒看到心跳请求，完成视频

**需要找到的 API：**
- 开始视频（`start` 或 `play`）
- 心跳（`heartbeat`）：每 60 秒，携带当前播放位置
- 完成视频（`complete`）

**计划实现：**

```
core/
├── heartbeat_worker.py    # 后台线程：定时心跳 → 完成信号
└── queue_manager.py       # 队列状态机：一次一门，顺序执行
```

**心跳时序（关键）：**
```
t=0       开始视频
t=60      第一次心跳（position=60）
t=120     第二次心跳（position=120）
…
t=T-ε     最后一次心跳（position=T，精确结束位置）
t=T       发送完成信号 → 触发下一视频/课程
```

**队列逻辑：**
- 用户通过 UI 将课程加入等待队列
- 系统一次处理一门课，每门课内顺序完成所有视频
- 支持随时停止（threading.Event）

### 阶段四 — 打包

```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

生成 `dist/main.exe`，无需 Python 环境即可运行。

---

## 4. 架构约定

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
