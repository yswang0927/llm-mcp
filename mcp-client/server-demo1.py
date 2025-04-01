from mcp.server.fastmcp import FastMCP
import httpx
import json

"""
这是一个简单的MCP-Server示例程序，提供了三个工具方法。
可以通过 `python mcp-client-server.py server-demo1.py` 来运行测试。
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
    """
    以标准 I/O 方式运行 MCP 服务器
    当指定 transport='stdio' 运行 MCP 服务器时，客户端必须在启动时同时启动当前这个脚本，否则无法顺利通信。
    这是因为 stdio 模式是一种本地进程间通信（IPC，Inter-Process Communication）方式，
    它需要服务器作为子进程运行，并通过标准输入输出（stdin/stdout）进行数据交换。
    """
    mcp.run(transport='stdio')

