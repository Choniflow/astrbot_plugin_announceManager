'''FileHeader
: @Author: Chroniflow
: @Date: 2/5/2026, 11:15:29 PM
: @LastEditors: Chroniflow
: @LastEditTime: 2/5/2026, 11:15:31 PM
: @Description: 
: @Copyright: Copyright (©)}) 2026 Chroniflow. All rights reserved.
: @Email: code@ylyq.site
'''


from astrbot.core.utils.astrbot_path import get_astrbot_data_path
from astrbot.api import logger
from playwright.async_api import async_playwright
import os
from asyncio import sleep
# import logging as logger


templatePath = get_astrbot_data_path()+"/plugins/astrbot_plugin_announceManager/templates/html/markdownAnnounce.html"
# templatePath = "/root/AstrBot/data"+"/plugins/astrbot_plugin_announceManager/templates/html/markdownAnnounce.html"
templateFile = open(templatePath)
TMPL: str = templateFile.read()
templateFile.close()


async def render(content) -> str:
    """
    使用playwright渲染HTML代码并截图
    
    Args:
        content: 要插入到模板中的内容
        
    Returns:
        str: 截图文件的路径
    """
    HTMLCode: str = TMPL.replace("%item%", content.replace("`","\\`"), 1)
    screenshot_path = "/tmp/announceManager/screenshot.png"
    
    # 确保目录存在
    os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
    
    async with async_playwright() as p:
        # 启动浏览器
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            # 设置HTML内容
            await page.set_content(HTMLCode)
            
            # 等待页面加载完成
            await page.wait_for_load_state('networkidle')
            # await sleep(5.0)
            
            # 截图
            await page.screenshot(path=screenshot_path, full_page=True)
            
            logger.info(f"截图已保存到: {screenshot_path}")
            
        except Exception as e:
            logger.error(f"渲染HTML时发生错误: {e}")
            raise
        finally:
            # 关闭浏览器
            await browser.close()
    
    return screenshot_path
