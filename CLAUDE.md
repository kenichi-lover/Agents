# Agent Party — 多 Agent 实时聚会平台

> **项目定位**：一个支持多 Agent 与人类用户实时互动的虚拟聚会平台。
> **核心体验**：Agent 拥有独立人格、记忆和社交关系，能在聚会中自发对话、回应用户、参与圆桌讨论。

---

## 一、当前进度

> 最后更新：2026-06-25

### ✅ 已完成（Tasks 1-17）

| # | 任务 | 说明 |
|---|------|------|
| 1 | 基础架构 | 依赖、settings、bcrypt、security、DDL、lifespan |
| 2 | 数据模型 | User, Agent, Party, PartyMember, Message（SQLModel table=True） |
| 3 | Pydantic schemas | Create/Read DTOs 全实体 |
| 4 | Auth Service | register, login, get_current_user, WS token 解码 |
| 5 | Auth Router | POST /auth/register, POST /auth/login, GET /auth/me |
| 6 | Party Router | CRUD + join/leave |
| 7 | Messages + WebSocket | GET /parties/{id}/messages, WebSocket 路由修复 |
| 8 | Seed Agents + 登录页 | 3 个默认 Agent, 登录页对接 API, axios interceptor, Next.js rewrites |
| 9 | Party 页 Token | localStorage 读取 token → WebSocket 认证连接 |
| 10 | Bug #1 修复 | WebSocket 消息 `is_user` 标记 + ChatStream 消息分类渲染修复 |
| 11 | Agent CRUD API | GET/POST/PATCH/DELETE /api/agents + 前端 AgentPanel 对接 |
| 12 | 首页/大厅 | 聚会列表 + 创建聚会入口，登录后跳转大厅 |
| 13 | Presence Tracker | 后端 ConnectionManager + GET /api/presence/{party_id}，前端 PresenceBar 实时显示 |
| 14 | Agent Engine + LLM Service | LLM 封装(openai stub) + WebSocket user:prompt 触发推理引擎 |
| 15 | Alembic 迁移 | 自动检测 schema 变更，生成 initial schema migration |
| 16 | 3D 聚会空间 | React Three Fiber 3D 房间 + Agent 胶囊体 + 圆桌场景 + 自由走动 |
| 17 | 测试套件 | 后端 101 pytest + 前端 46 vitest 全部通过 |

**端到端链路已打通**：注册/登录 → 大厅 → 聚会房间 → WebSocket → Agent 自动回复

> 2026-06-25 完成最终审计：Party 列表 API、ChatStream 发消息、AgentPanel 交互均已确认端到端可用。

### ✅ 全部完成（Tasks 1-17）

| # | 任务 | 说明 |
|---|------|------|
| 1 | 基础架构 | 依赖、settings、bcrypt、security、DDL、lifespan |
| 2 | 数据模型 | User, Agent, Party, PartyMember, Message（SQLModel table=True） |
| 3 | Pydantic schemas | Create/Read DTOs 全实体 |
| 4 | Auth Service | register, login, get_current_user, WS token 解码 |
| 5 | Auth Router | POST /auth/register, POST /auth/login, GET /auth/me |
| 6 | Party Router | CRUD + join/leave |
| 7 | Messages + WebSocket | GET /parties/{id}/messages, WebSocket 路由修复 |
| 8 | Seed Agents + 登录页 | 3 个默认 Agent, 登录页对接 API, axios interceptor, Next.js rewrites |
| 9 | Party 页 Token | localStorage 读取 token → WebSocket 认证连接 |
| 10 | Bug #1 修复 | WebSocket 消息 `is_user` 标记 + ChatStream 消息分类渲染修复 |
| 11 | Agent CRUD API | GET/POST/PATCH/DELETE /api/agents + 前端 AgentPanel 对接 |
| 12 | 首页/大厅 | 聚会列表 + 创建聚会入口，登录后跳转大厅 |
| 13 | Presence Tracker | 后端 ConnectionManager + GET /api/presence/{party_id}，前端 PresenceBar 实时显示 |
| 14 | Agent Engine + LLM Service | LLM 封装(openai stub) + WebSocket user:prompt 触发推理引擎 |
| 15 | Alembic 迁移 | 自动检测 schema 变更，生成 initial schema migration |
| 16 | 3D 聚会空间 | React Three Fiber 3D 房间 + Agent 胶囊体 + 圆桌场景 + 自由走动 |
| 17 | 测试套件 | 后端 101 pytest + 前端 46 vitest 全部通过 |

### 🚧 待开发（P3 低优先级，用户可选）

| 模块 | 说明 |
|------|------|
| 记忆系统 | Redis + 向量存储，Agent 持久化记忆 |
| 圆桌讨论逻辑 | 后端调度 (3D 场景已完成) |
| 本地 LLM | Ollama/vLLM 支持 |
| 聚会回放导出 | 消息归档 |

---

## 二、项目结构

```
fastapi/agent/
├── CLAUDE.md                  # 本文档：项目框架与约束
├── backend/                   # FastAPI 后端
│   ├── main.py                # 应用入口
│   ├── pyproject.toml         # uv 依赖管理
│   ├── .env                   # 环境变量
│   ├── .venv/                 # uv 虚拟环境
│   ├── config/
│   │   └── settings.py        # Pydantic Settings
│   ├── models/                # SQLModel 数据模型
│   │   ├── __init__.py
│   │   ├── agent.py           # Agent 人格/配置/记忆/关系
│   │   ├── party.py           # 聚会/房间/圆桌
│   │   ├── message.py         # 消息/事件
│   │   └── user.py            # 用户
│   ├── api/
│   │   ├── __init__.py
│   │   ├── websocket.py       # WebSocket 路由
│   │   ├── agents.py          # Agent CRUD
│   │   ├── parties.py         # 聚会管理
│   │   └── messages.py        # 消息历史
│   ├── core/
│   │   ├── __init__.py
│   │   ├── party_manager.py   # 聚会生命周期
│   │   ├── agent_engine.py    # Agent 推理引擎
│   │   ├── message_router.py  # 消息路由/广播
│   │   ├── memory_store.py    # 记忆管理 (Redis + 向量)
│   │   └── presence_tracker.py # 在线状态
│   └── services/
│       ├── __init__.py
│       ├── llm_service.py     # LLM 调用封装
│       └── embedding_service.py
│
└── frontend/                  # Next.js 15 前端
    ├── next.config.ts
    ├── package.json
    ├── tsconfig.json
    ├── app/
    │   ├── layout.tsx         # 根布局
    │   ├── page.tsx           # 首页/大厅入口
    │   ├── globals.css
    │   ├── party/
    │   │   └── [partyId]/
    │   │       └── page.tsx   # 聚会房间
    │   ├── agents/
    │   │   └── page.tsx       # Agent 管理页
    │   ├── login/
    │   │   └── page.tsx       # 登录/注册页（VANTA 粒子背景）
    │   └── api/               # Next.js API Routes (如需)
    ├── components/
    │   ├── PartyRoom.tsx
    │   ├── ChatStream.tsx
    │   ├── AgentCard.tsx
    │   ├── MessageBubble.tsx
    │   ├── AgentThinking.tsx
    │   ├── PresenceBar.tsx
    │   └── RoundTable.tsx
    ├── hooks/
    │   ├── useWebSocket.ts
    │   ├── useParty.ts
    │   └── useAgent.ts
    ├── lib/
    │   ├── websocket.ts
    │   └── utils.ts
    └── types/
        └── index.ts
```

---

## 三、技术栈

| 层级 | 技术 | 版本约束 |
|------|------|---------|
| 前端框架 | Next.js | ^15.0 (App Router) |
| 前端语言 | TypeScript | ^5.6 |
| 样式 | Tailwind CSS | ^3.4 |
| 状态管理 | Zustand | ^5.0 |
| 动画 | Framer Motion | ^11.0 |
| 后端框架 | FastAPI | ^0.115 |
| 后端语言 | Python | ^3.12 |
| ORM | SQLModel | ^0.0.22 |
| 数据库 | PostgreSQL | 15+ |
| 缓存/状态 | Redis | 7+ |
| 包管理 | uv | latest |
| LLM | OpenAI / Anthropic | API |

---

## 四、编码约束

### 3.1 Python 后端

- **异步优先**：所有 I/O 操作必须使用 `async/await`
- **类型严格**：所有函数必须有类型注解，禁用 `Any` 除非必要
- **SQLModel 规范**：
  - 数据库表模型：`class Model(Base, table=True)`
  - API 请求模型：`class ModelCreate(Base)`
  - API 响应模型：`class ModelPublic(Base)`
  - 运行时状态（Redis）：`class ModelRuntimeState(SQLModel)`
- **WebSocket 消息**：统一使用 `{"type": "...", ...}` 格式
- **错误处理**：使用 FastAPI HTTPException，WebSocket 用 `{"type": "error", ...}`
- **环境变量**：所有配置通过 `pydantic-settings` 读取，禁止硬编码

### 3.2 TypeScript 前端

- **"use client" 显式声明**：只有需要交互的组件才用 `"use client"`
- **Hook 命名**：所有自定义 Hook 必须以 `use` 开头
- **WebSocket 封装**：统一通过 `useWebSocket` hook 管理连接
- **类型导出**：所有类型定义在 `types/index.ts`，禁止内联 `any`
- **组件粒度**：单个组件不超过 200 行，复杂逻辑抽离为 hook
- **样式约束**：全部使用 Tailwind，禁止内联 `style` 和 `css` 文件

### 3.3 通用约束

- **UUID 为主键**：所有实体主键使用 `UUID4`
- **时间戳**：数据库统一使用 `datetime.utcnow()`，API 返回 ISO 8601 字符串
- **命名规范**：
  - Python：`snake_case`
  - TypeScript：`camelCase`（变量/函数）、`PascalCase`（类型/组件）
- **禁止**：
  - 前端直接调用数据库
  - 后端返回完整 SQLModel 对象（必须通过 Public 模型过滤）
  - 在组件中直接管理 WebSocket 连接（必须通过 hook）

---

## 五、核心数据流

```
用户发送消息
    │
    ▼
┌─────────────┐
│  WebSocket  │  ──► 验证身份、解析消息类型
│   Gateway   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Message    │  ──► 存入数据库、广播给房间成员
│   Router    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Agent     │  ──► 判断 Agent 是否响应
│   Engine    │      检索记忆 → 调用 LLM → 生成回复
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Redis     │  ──► 更新 Agent 状态、缓存上下文
│  (Runtime)  │
└─────────────┘
```

---

## 六、Agent 行为约束

1. **响应触发条件**（满足任一即触发）：
   - 被用户 `@提及`
   - 话题匹配其 `expertise`（70% 概率）
   - 随机主动插话（10% 概率，受 `assertiveness` 调节）

2. **思考过程可见**：
   - Agent 生成回复前，发送 `{"type": "chat:thinking", "agent_id": "..."}`
   - 前端显示思考动画
   - 生成完成后替换为正式消息

3. **记忆更新**：
   - 每次交互后自动提取关键信息存入 `agent_memory`
   - 高 `importance` 记忆优先检索
   - 向量相似度检索最近 5 条相关记忆

4. **情绪动态**：
   - `mood` 根据对话内容动态变化
   - 影响 `temperature` 和 `verbosity` 参数
   - 变化事件广播给所有参与者

---

## 七、API 约定

### WebSocket 端点

```
ws://host/ws/party/{party_id}?token={jwt_token}
```

### REST 端点

```
GET    /api/agents              # 列表（分页）
POST   /api/agents              # 创建
GET    /api/agents/{id}         # 详情
PATCH  /api/agents/{id}         # 更新
DELETE /api/agents/{id}         # 删除

GET    /api/parties             # 聚会列表
POST   /api/parties             # 创建聚会
GET    /api/parties/{id}        # 聚会详情
POST   /api/parties/{id}/join   # 加入聚会
POST   /api/parties/{id}/leave  # 离开聚会

GET    /api/parties/{id}/messages  # 消息历史（分页）
```

---

## 八、环境变量模板

```env
# 数据库
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/agent_party

# Redis
REDIS_URL=redis://localhost:6379/0

# LLM
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
DEFAULT_LLM_MODEL=gpt-4o

# 安全
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=60

# 应用
APP_NAME=Agent Party
DEBUG=false
```

---

## 九、开发流程

1. **启动后端**：`cd backend && uv run uvicorn main:app --reload`
2. **启动前端**：`cd frontend && npm run dev`
3. **数据库迁移**：使用 Alembic（后续补充）
4. **Redis**：`redis-server`
5. **代码检查**：
   - Python：`ruff check .`
   - TypeScript：`npx tsc --noEmit`

---

## 十、扩展预留

- [ ] 3D/2D 可视化聚会场景
- [ ] Agent 间私聊（观察者可见/不可见模式）
- [ ] 语音合成（TTS）让 Agent "说话"
- [ ] 本地 LLM 支持（Ollama / vLLM）
- [ ] 聚会回放与导出
- [ ] 多语言 Agent 支持
