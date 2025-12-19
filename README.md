# 《浮生十梦》 - Docker

> 本项目原仓库：[CassiopeiaCode/TenCyclesofFate](https://github.com/CassiopeiaCode/TenCyclesofFate/tree/master)

**《浮生十梦》** 是一款基于 Web 的沉浸式文字冒险游戏。玩家在游戏中扮演一个与命运博弈的角色，每天有十次机会进入不同的“梦境”（即生命轮回），体验由 AI 动态生成的、独一无二的人生故事。游戏的核心在于“知足”与“贪欲”之间的抉择：是见好就收，还是追求更高的回报但可能失去一切？

## ✨ 功能特性

- **动态 AI 生成内容**: 每一次游戏体验都由大型语言模型（如 GPT）实时生成，确保了故事的独特性和不可预测性。
- **实时交互**: 通过 WebSocket 实现前端与后端的实时通信，提供流畅的游戏体验。
- **OAuth2 认证**: 集成 Linux.do OAuth2 服务，实现安全便捷的用户登录。
- **精美的前端界面**: 采用具有“江南园林”风格的 UI 设计，提供沉浸式的视觉体验。
- **互动式判定系统**: 游戏中的关键行动可能触发“天命判定”。AI 会根据情境请求一次 D100 投骰，其“成功”、“失败”、“大成功”或“大失败”的结果将实时影响叙事走向，增加了游戏的随机性和戏剧性。
- **智能反作弊机制**: 内置一套基于 AI 的反作弊系统。它会分析玩家的输入行为，以识别并惩罚那些试图使用“奇巧咒语”（如 Prompt 注入）来破坏游戏平衡或牟取不当利益的玩家，确保了游戏的公平性。
- **数据持久化**: 游戏状态会定期保存，并在应用重启时加载，保证玩家进度不丢失。

## 🛠️ 技术栈

- **后端**: FastAPI, Uvicorn, WebSockets, Python-JOSE, Authlib, SQLite, OpenAI API
- **前端**: HTML, CSS, JavaScript (ESM), marked.js, pako.js

## 🚀 快速开始 (Docker 部署)

推荐使用 Docker 方式快速启动项目。

### 1. 配置环境变量

在项目根目录下创建 `.env` 文件，并参考.env.example进行配置：


### 2. 使用 Docker Compose 启动
下载docker-compose.yml，然后
```bash
docker-compose up -d
```

启动后，访问 `http://localhost:8000` 即可开始游戏。

> **注意**：
> - **Linux.do 登录** 默认关闭 (`ENABLE_LINUXDO_LOGIN=False`)，开启后需配置相关 Client ID 和 Secret。
> - **兑换码系统** 默认关闭 (`ENABLE_REDEMPTION=False`)。

---

## 🛠️ 本地开发部署

如果你希望在本地环境直接运行，请遵循以下步骤。

### 1. 环境准备

- **Python 3.8+**
- **Git**
- **uv** (推荐, `pip install uv`)

### 2. 安装依赖

```bash
uv pip install -r backend/requirements.txt
```

### 3. 配置环境变量

参考上述 Docker 部署部分的环境变量配置，在 `backend/` 目录下创建 `.env` 文件。

### 4. 运行应用

```bash
chmod +x run.sh
./run.sh
```

## 📁 项目结构

- `backend/`: 后端核心代码（FastAPI）
- `frontend/`: 前端静态文件（HTML/CSS/JS）
- `scripts/`: 工具脚本
- `data/`: 存放持久化数据（如数据库文件）
- `Dockerfile`: 镜像构建文件
- `docker-compose.yml`: Docker 服务编排文件
