# 这是一个python实现的 MCP Client客户端

>
> 代码整理自：https://deepseek.csdn.net/67e28cf28393e26e265938ce.html
> 

### 提供了三个客户端示例程序：

- `simple-mcp-client.py` 最简单的客户端
- `mcp-client.py` 对接了大模型(本地ollama)的客户端
- `mcp-client-server.py` 对接了大模型(本地ollama) 和 MCP-Server(server-demo1.py) 的客户端

### 1. 运行前准备：初始化虚拟环境和安装依赖包

```shell
cd mcp-client

# 在当前目录下创建虚拟环境
uv venv
# 激活虚拟环境
source .venv/bin/activate
# 安装依赖包
uv pip install -r requirements.txt

# 测试：运行如下命令，浏览器访问：http://localhost:5173/
# 使用提供的在线环境，连接到此 mcp-server，可以在 Tools 下查看提供的工具列表和测试
mcp dev server-demo1.py
```

### 2. 命令行交互式运行体验：

> 大模型配置信息在文件 `.env` 中：
> 
> BASE_URL=http://localhost:11434/v1/
> 
> MODEL=qwen2.5-coder:7b 
> 
> OPENAI_API_KEY=ollama
> 

```shell
python simple-mcp-client.py
# 或者
uv run simple-mcp-client.py
```

```shell
python mcp-client.py
# 或者
uv run mcp-client.py
```

```shell
python mcp-client-server.py server-demo1.py
# 或者
uv run mcp-client.py server-demo1.py
```
