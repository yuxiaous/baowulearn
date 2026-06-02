# 宝武学习系统 (baowulearn)

宝武学习系统桌面挂机工具。项目通过调用学习平台接口、模拟视频播放过程中的开始播放、心跳、进度打卡和结束播放等行为，帮助用户批量完成公开课和学习专区课程。

当前实现是一个基于 PySide6 的 Windows 桌面应用，包含登录界面、课程列表、视频进度面板和串行挂机队列。

## 功能概览

- 工号、密码、验证码登录
- 加载公开课与学习专区课程
- 支持多选课程并加入挂机队列
- 串行处理课程，自动遍历课程内视频
- 每秒刷新当前视频进度，定期发送心跳和进度打卡
- 实时展示课程状态、已学时长和当前视频进度
- 本地记住上次登录凭据
- 提供 PyInstaller 打包脚本

## 适用范围

项目当前面向桌面端使用，主要流程围绕以下场景设计：

1. 启动应用并登录
2. 浏览公开课或学习专区下的课程
3. 选择一门或多门课程加入队列
4. 后台按队列顺序执行挂机任务
5. 观察右侧视频列表和状态栏中的实时进度

## 工作流程

### 登录流程

- 启动入口在 `src/main.py`
- 若 `config.TOKEN` 已配置，则直接写入请求头并跳过登录窗口
- 否则打开 `LoginWindow`，先请求验证码，再提交登录请求
- 登录成功后会将 `username` 和 `password` 保存到根目录 `storage.json`

### 挂机流程

队列由 `QueueManager` 管理，一次只运行一门课程。单门课程由 `HeartbeatWorker` 在后台线程中完成：

1. 获取课程视频列表
2. 读取服务端心跳间隔
3. 初始化课程学习记录
4. 遍历课程内每个视频
5. 查询视频已播放进度，支持续播
6. 发送开始播放信号
7. 每秒推进本地计时
8. 在预设时间点发送进度打卡
9. 按心跳间隔发送学习心跳
10. 视频结束后补发心跳、提交完成状态并结束播放
11. 刷新课程完成情况，进入下一个视频或下一门课程

## 技术架构

### 界面层

- `src/ui/login_window.py`: 登录窗口、验证码加载、登录提交
- `src/ui/main_window.py`: 主窗口、课程展示、视频进度展示、队列操作

### API 层

- `src/api/client.py`: 全局 `requests.Session` 封装，统一管理请求头和 Token
- `src/api/auth.py`: 验证码与登录接口
- `src/api/course.py`: 公开课、专区、课程详情和完成情况相关接口
- `src/api/video.py`: 视频列表、播放开始/结束、心跳、打卡和播放进度相关接口

### 核心逻辑层

- `src/core/crypto.py`: 登录参数使用的 SM2 加密
- `src/core/storage.py`: 本地 TinyDB 存储
- `src/core/queue_manager.py`: 挂机队列状态机与 UI 信号分发
- `src/core/heartbeat_worker.py`: 单门课程的后台挂机执行器

### 数据模型层

- `src/models/course.py`: 课程模型与本地挂机状态枚举
- `src/models/video.py`: 视频模型、时长、打卡点和播放进度
- `src/models/zone.py`: 学习专区模型

## 目录结构

```text
.
├─ src/                    # 主源码目录
│  ├─ api/                 # 平台接口封装
│  ├─ core/                # 队列、存储、心跳线程等核心逻辑
│  ├─ models/              # 数据模型
│  ├─ ui/                  # PySide6 界面
│  ├─ config.py            # 全局配置
│  └─ main.py              # 应用入口
├─ doc/api-captures/       # 接口抓包与字段记录
├─ build.py                # 一键安装 PyInstaller 并打包
├─ pyproject.toml          # 项目元数据与依赖
├─ storage.json            # 本地登录信息存储文件
└─ build/                  # 打包产生的中间产物
```

说明：开发时应以 `src/` 下代码为准；`build/` 目录中的 Python 文件属于打包过程产物，不建议直接修改。

## 运行环境

- Python 3.10 及以上
- Windows 桌面环境
- 可访问 `https://learn.baowugroup.com/learn-gateway`

### 依赖

项目在 `pyproject.toml` 中声明了以下核心依赖：

- `requests`
- `gmssl`
- `tinydb`
- `pyside6`

## 安装与启动

建议先创建虚拟环境，再安装依赖：

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

启动应用：

```bash
python src/main.py
```

## 配置说明

### Token 直登

如果已经拿到有效 Token，可以通过环境变量或 `.env` 文件注入：

```env
TOKEN=your-access-token
```

程序启动时会优先读取该值。只要 `TOKEN` 存在，就会跳过登录窗口。

### `.env` 加载规则

- 开发模式下，从项目根目录读取 `.env`
- 打包为 exe 后，从可执行文件同级目录读取 `.env`
- 仅在环境变量不存在时写入，不覆盖系统已有值

## 打包

根目录提供了 `build.py`：

```bash
python build.py
```

该脚本会：

1. 自动安装 `pyinstaller`
2. 清理旧的 `dist/baowulearn`
3. 以 `--onedir --windowed` 方式打包 `src/main.py`
4. 将 `LICENSE` 和 `third_party_licenses/` 一并打入产物目录
5. 将 `pyproject.toml` 一并打入产物目录，用于读取版本号

默认输出目录：

```text
dist/baowulearn/
```

## 本地存储

### `storage.json`

项目使用 TinyDB 将登录信息保存在应用目录下的 `storage.json` 中，当前会存储：

- `username`
- `password`

开发模式下文件位于项目根目录；打包后位于 exe 同级目录。

## 代码里已经体现出的限制

以下限制并非 README 推测，而是当前代码实现直接决定的行为：

- 只支持串行挂机，一次只能处理一门课程
- 心跳与播放控制基于同步 `requests` 请求，没有统一超时和重试策略
- 停止任务不是即时中断，通常会在当前心跳周期结束后退出
- 登录凭据明文存储在 `storage.json`
- 大量错误以运行时异常形式向上抛出，缺少更细的恢复策略
- 日志主要通过 `print` 输出，没有独立日志文件

## 开发说明

### 关键入口

- 应用入口：`src/main.py`
- 全局配置：`src/config.py`
- 登录 API：`src/api/auth.py`
- 课程 API：`src/api/course.py`
- 视频 API：`src/api/video.py`
- 队列状态机：`src/core/queue_manager.py`
- 挂机线程：`src/core/heartbeat_worker.py`

### 接口资料

`doc/api-captures/` 下保留了多个接口抓包记录，可用于补字段、排查接口变化和理解请求参数来源。

## 后续可改进方向

- 为请求统一增加 `timeout`、重试和更明确的错误分类
- 对本地凭据做加密存储或改为仅记住用户名
- 为挂机过程增加可持久化日志
- 为 API 层补测试和更稳定的返回值校验
- 为停止流程增加更快的取消响应

## License

本项目采用 MIT License 开源，完整条款见根目录 [LICENSE](./LICENSE)。

打包并分发 exe 时，还应同时分发根目录下的 [third_party_licenses/](./third_party_licenses) 目录，用于保留第三方依赖与 PySide6 相关许可文本。
