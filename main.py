'''FileHeader
: @Author: Chroniflow
: @Date: 1/24/2026, 8:14:34 PM
: @LastEditors: Chroniflow
: @LastEditTime: 1/25/2026, 12:05:02 PM
: @Description: 公告推送管理器主程序
: @Copyright: Copyright (©)}) 2026 Chroniflow. Open-Source with GPL Licence.
: @Email: code@ylyq.site
'''
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from data.plugins.astrbot_plugin_announceManager.controller import dataController, userController
from astrbot.core.utils.astrbot_path import get_astrbot_data_path

@register("公告推送管理器", "Chroniflow", "公告推送&管理插件", "nightly", "https://github.com/Choniflow/astrbot_plugin_announceManager")
class AnnounceManager(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """初始化进程"""

        logger.info("Welcome to announceManager!")
        logger.info("Getted AstrBot path: %s", get_astrbot_data_path())
        logger.info("Database file: %s", get_astrbot_data_path()+"/plugin_data/"+self.name+"/data.db")

        # 调用sqlite_init初始化SQL结构
        await dataController._init_table(None)

    @filter.command_group("anadmin")
    async def admin_commands(self):
        """
        admin_commands
        Admin指令主类
        
        :param self
        :param event
        :type event: AstrMessageEvent
        """

        pass
    
    @admin_commands.command("hello")
    async def admin_hello(self, event: AstrMessageEvent):
        """
        admin_hello 的 Docstring
        
        :param self: 说明
        :param event: 说明
        :type event: AstrMessageEvent
        """

        user_name = event.get_sender_name()
        yield event.plain_result(open(get_astrbot_data_path()+f"/plugins/astrbot_plugin_announceManager/templates/message/admin/hello.txt","r").read().replace("%user_name%",user_name)) # 发送一条纯文本消息
    
    @filter.permission_type(filter.PermissionType.ADMIN)
    @admin_commands.command("rm-rf/*", alias={"rm -rf /*"})
    async def cleanAll(self, event: AstrMessageEvent):
        """
        cleanAll 的 Docstring
        
        :param self: 说明
        :param event: 说明
        :type event: AstrMessageEvent
        """

        user_name: str = event.get_sender_name()

        yield event.plain_result(str(await dataController._clean_all(user_name)))
    
    @filter.permission_type(filter.PermissionType.ADMIN)
    @admin_commands.command("init")
    async def initTable(self, event: AstrMessageEvent):
        """
        initTable 的 Docstring
        
        :param self: 说明
        :param event: 说明
        :type event: AstrMessageEvent
        """

        user_name: str = event.get_sender_name()

        yield event.plain_result(str(await dataController._init_table(user_name)))

    @filter.permission_type(filter.PermissionType.ADMIN)
    @admin_commands.command("user add")
    async def addUser(self, event: AstrMessageEvent, user: int, permitted_group: str):
        """
        addUser 的 Docstring
        
        :param self: 说明
        :param event: 说明
        :type event: AstrMessageEvent
        """

        userName: str = event.get_sender_name()
        logger.info(f"Admin {userName} is adding a user with permitted group {permitted_group}.")
        try:
            yield event.plain_result(str(await userController.addUser(user, permitted_group)))
        except Exception as e:
            logger.error(e)
            yield event.plain_result(str(e))

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
