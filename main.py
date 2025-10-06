#imports
import requests
from mcp.server.fastmcp import FastMCP
import logging
import uvicorn

#logging
logging.basicConfig(level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

mcp=FastMCP("Weather")

logger=logging.getLogger("mcp_server" )
def main():
    try:
        logger.info("Starting MCP server...")
        #mcp.run()
        logger.info("Server started successfully.")
    except Exception as e:
        logger.error(f"Failed to start MCP server: {e}")
        raise

#openwethermap
api_key = ""


#openwethermap tool

@mcp.resource("weather://{city}")
def get_weather(city: str) -> str:
    logger.info(f"Requested weather for {city}")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        description = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        return f"Weather in {city}: {description}, temperature {temp}°C"
    else:
         return f"cant recive weather data for {city}."


#Weather request prompt

@mcp.prompt()
def weather_prompt(city: str) -> str:
    """Generates a request for weather data output for the specified city."""
    return f"Show the current weather in the city of {city}, including a description of the conditions and the temperature"

app = mcp.sse_app()

if __name__ == "__main__":
    #main()
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
    logger.info("Starting MCP SSE server with uvicorn...")
