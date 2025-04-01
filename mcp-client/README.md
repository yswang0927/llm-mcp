# 这是一个自己实现的 MCP Client客户端。

### 提供了三个客户端示例程序：

- `simple-mcp-client.py` 最简单的客户端
- `mcp-client.py` 对接了大模型(本地ollama)的客户端
- `mcp-client-server.py` 对接了大模型(本地ollama) 和 MCP-Server(server-demo1.py) 的客户端

### 命令行交互式运行体验：

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
