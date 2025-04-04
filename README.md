# llm-mcp
这是一个大模型MCP客户端和服务端开发的示例程序

## mcp uv 创建 mcp-server 过程：

1. 创建目录  `uv init mcp-server`

2. 创建虚拟环境
```shell
cd mcp-server
uv venv 
source .venv/bin/activate  # 激活虚拟环境
```

3. 添加相关依赖库：
```shell
uv add mcp
uv add mcp[cli]  # 后面运行测试 mcp dev xx.py 需要
```

4. 添加一个 server.py：

```python
from mcp.server.fastmcp import FastMCP
import httpx
import json

"""
这是一个简单的MCP-Server示例程序，提供了三个工具方法。
"""

# Create an MCP server
mcp = FastMCP("Demo")

# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """计算两个数相加"""
    return a + b


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """获得个性化的问候"""
    return f"Hello, {name}!"

@mcp.tool()
def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """在给定体重（kg）和身高（米）的情况下计算BMI"""
    return weight_kg / (height_m**2)


@mcp.tool()
async def fetch_weather(city: str) -> str:
    """获取一个城市的当前天气"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://restapi.amap.com/v3/weather/weatherInfo?key=78715e465643f5e2a5aeecdbc3e937d7&city={city}&extensions=all")
        """
        {forecasts:[
            {province:'江苏', city:'南京', casts:[
                { date:'2025-04-01', week:"2", "dayweather": "多云", "nightweather": "多云", 
                    "daytemp": "18", "nighttemp": "8", "daywind": "南",  "nightwind": "南", 
                    "daypower": "1-3", "nightpower": "1-3", 
                    "daytemp_float": "18.0", "nighttemp_float": "8.0" 
                }
            ]
            }
        ]}
        """
        data = json.loads(response.text)
        info = data.get("forecasts")[0]
        province = info.get("province")
        city = info.get("city")
        weathers = info.get('casts')
        # 测试获取今天的天气
        today_weather = weathers[0]

        return (
            f"🌍 {province}-{city} {today_weather.get("date")}(周{today_weather.get("week")}) 天气：\n"
            f"🌡 温度: {today_weather.get("daytemp")}°C\n"
            f"🌬 风速: {today_weather.get("daypower")}级\n"
            f"🌤 天气: {today_weather.get("dayweather")}\n"
        )


if __name__ == "__main__":
    # 以标准 I/O 方式运行 MCP 服务器
    mcp.run(transport='stdio')

```

5. 使用 mcp 内置的界面测试这个 server.py （这个依赖安装 mcp[cli]）

```shell
mcp dev server.py

# 会自动一个http服务，默认地址是：http://localhost:5173/
```

6. 在 cherry-studio 中配置 MCP 服务器：
```
名称：uv-local-demo  # 随意
类型：STDIO
命令：/my-python/uv   # 注意命令这里如果使用 cherry-studio 自己安装的uv命令则无法启动，所以缓存自己python下安装的
参数：
--directory
/<your_path>/mcp-server
run
server.py
```
