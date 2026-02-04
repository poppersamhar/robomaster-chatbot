# RoboMaster AI 问答机器人

RoboMaster赛事直播页AI问答机器人，基于RAG + Claude API实现智能问答。

## 功能特性

- 右下角悬浮小粉助手按钮
- 半浮窗聊天界面
- RAG知识库检索 + Claude智能回答
- 敏感词过滤与安全兜底策略

## 项目结构

```
copilot/
├── frontend/          # React前端
├── backend/           # FastAPI后端
│   ├── app/
│   │   ├── api/       # API接口
│   │   ├── llm/       # Claude集成
│   │   └── rag/       # RAG检索
│   └── data/          # 知识库数据
└── docker-compose.yml
```

## 本地开发

### 后端

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入 ANTHROPIC_API_KEY

uvicorn app.main:app --reload
```

### 前端

```bash
cd frontend
npm install
npm start
```

## Docker部署

### 1. 配置环境变量

```bash
cd /path/to/copilot
cp backend/.env.example .env
# 编辑 .env 填入你的 API Key
```

### 2. 启动服务

```bash
docker-compose up -d --build
```

访问 http://localhost 即可使用。

## 阿里云部署指南

### 1. 服务器准备

- 阿里云ECS（建议2核4G以上，首次加载模型需要较多内存）
- 开放安全组端口：80, 443

### 2. 安装Docker

```bash
# 安装Docker
curl -fsSL https://get.docker.com | sh
systemctl start docker
systemctl enable docker

# 安装Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

### 3. 上传代码

```bash
# 本地打包
tar -czvf copilot.tar.gz copilot/

# 上传到服务器
scp copilot.tar.gz root@<服务器IP>:/root/

# 服务器解压
ssh root@<服务器IP>
tar -xzvf copilot.tar.gz
cd copilot
```

### 4. 配置并启动

```bash
# 创建环境变量文件
cat > .env << EOF
ANTHROPIC_API_KEY=your_api_key_here
CLAUDE_MODEL=claude-3-haiku-20240307
EOF

# 启动服务
docker-compose up -d --build

# 查看日志
docker-compose logs -f
```

### 5. 验证部署

```bash
# 检查服务状态
docker-compose ps

# 测试API
curl http://localhost:8000/health
curl -X POST http://localhost/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "你好"}'
```

## API接口

### POST /api/chat

请求：
```json
{"message": "RoboMaster是什么比赛？"}
```

响应：
```json
{"reply": "RoboMaster机甲大师赛是..."}
```

## 技术栈

- 前端：React + TailwindCSS
- 后端：Python FastAPI
- RAG：sentence-transformers + FAISS
- LLM：Claude API (claude-3-haiku)
- 部署：Docker + Nginx

## 问答策略

1. **敏感词检测** → 礼貌拒答 + 官方渠道引导
2. **RAG检索** → 知识库匹配
3. **Claude生成** → 基于RAG上下文智能回答
4. **降级兜底** → LLM失败时返回RAG结果或推荐问题
