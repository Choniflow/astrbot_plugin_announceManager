"""FileHeader
: @Author: Chroniflow
: @Date: 1/24/2026, 8:14:34 PM
: @LastEditors: Chroniflow
: @LastEditTime: 1/25/2026, 12:05:02 PM
: @Description: 公告推送管理器主程序
: @Copyright: Copyright (©)}) 2026 Chroniflow. Open-Source with GPL Licence.
: @Email: code@ylyq.site
"""
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from controller import sendController
from .controller import dataController, userController
from .processor import message, markdownRenderer, argumentsParser
from astrbot.core.utils.astrbot_path import get_astrbot_data_path
from astrbot.core.utils.session_waiter import ( session_waiter, SessionController )

@register("公告推送管理器", "Chroniflow", "公告推送&管理插件", "nightly-v0.1.0", "https://github.com/Choniflow/astrbot_plugin_announceManager")
class AnnounceManager(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """初始化进程"""

        logger.info("Welcome to announceManager!")
        logger.info("Got AstrBot path: %s", get_astrbot_data_path())
        logger.info("Database file: %s", get_astrbot_data_path()+"/plugin_data/"+self.name+"/data.db")

        # 调用sqlite_init初始化SQL结构
        await dataController.initTable(None)

    @filter.command_group("anadmin")
    async def admin_commands(self):
        pass
    
    @admin_commands.command("hello")
    async def admin_hello(self, event: AstrMessageEvent):
        """管理员欢迎信息"""

        user_name = event.get_sender_name()
        yield event.plain_result(open(get_astrbot_data_path()+f"/plugins/astrbot_plugin_announceManager/templates/message/admin/hello.txt","r").read().replace("%user_name%",user_name)) # 发送一条纯文本消息
    
    @filter.permission_type(filter.PermissionType.ADMIN)
    @admin_commands.command("rm-rf/*", alias={"rm -rf /*"})
    async def cleanAll(self, event: AstrMessageEvent):
        """清除所有数据"""
        user_name: str = event.get_sender_name()

        yield event.plain_result(str(await dataController.cleanAll(user_name)))
    
    @filter.permission_type(filter.PermissionType.ADMIN)
    @admin_commands.command("init")
    async def initTable(self, event: AstrMessageEvent):
        """初始化表"""

        user_name: str = event.get_sender_name()

        yield event.plain_result(str(await dataController.initTable(user_name)))

    @filter.permission_type(filter.PermissionType.ADMIN)
    @admin_commands.command("user add")
    async def addUser(self, event: AstrMessageEvent, user: int, permitted_group: str):
        """添加用户"""

        userName: str = event.get_sender_name()
        logger.info(f"Admin {userName} is adding a user with permitted group {permitted_group}.")
        try:
            yield event.plain_result(str(await userController.addUser(user, permitted_group)))
        except Exception as e:
            logger.error(e)
            yield event.plain_result(str(e))

    @filter.permission_type(filter.PermissionType.ADMIN)
    @admin_commands.command("message send")
    async def debugSendMessage(self, event: AstrMessageEvent):
        """[测试指令] 发送消息"""

        target: list[str] = argumentsParser.parse_args_advanced(event.message_str,
                                                                {
                                                                    "--target": {
                                                                        "type": str,
                                                                        "short": "-t",
                                                                        "list": True
                                                                    }
                                                                }
                                                                ).get("--target")

        try:
            yield event.plain_result("请发送消息内容")
            issuer: str = event.get_sender_id()

            @session_waiter(timeout=180, record_history_chains=False)
            async def messageSendSession(controller: SessionController, event: AstrMessageEvent):
                content: str = event.message_str

                if event.get_sender_id() != issuer:
                    return

                if content == "Q":
                    await event.send(event.plain_result("取消发送"))
                    controller.stop()

                if content == "":
                    return

                await event.send(event.plain_result("正在发送……"))
                controller.stop()
                result: dict[str, list[str]] = await sendController.send(self, event, target, content)


                # 组织结果语言
                template: list[str] = open("templates/message/admin/sendResult.txt","r").readlines()
                message: str = (template[0]+
                                template[1]+
                                template[2].replace("%total%", str(len(target)))+
                                template[3].replace("%success%", len(result.get("success")).__str__())+
                                template[4].replace("%failed%",
                                                    str( len( result.get("failed") )+len( result.get("denied") ) ))
                                )

                if result.get("denied") is [] and result.get("failed") is []:
                    await event.send(event.plain_result(message))
                    return

                for i in result.get("denied"):
                    message = message + template[5].replace("%group%", i).replace("%detail%", "权限不足")

                for i in result.get("failed"):
                    message = message + template[5].replace("%group%", i).replace("%detail%", "未捕捉的错误, 请联系管理员")

                await event.send(event.plain_result(message))
                return

            try:
                await messageSendSession(event)

            except TimeoutError as _:
                yield event.plain_result("超时了!")

            except Exception as e:
                yield event.plain_result("Error! See Logs!")
                logger.error(e)

            finally:
                event.stop_event()
        except Exception as e:
            logger.error(e)





    @filter.permission_type(filter.PermissionType.ADMIN)
    @admin_commands.command("markdown render")
    async def debugRenderMarkdownImage(self, event: AstrMessageEvent):
        """[测试指令] 渲染Markdown页面"""
        try:
            yield event.plain_result("请发送Markdown内容")
            issuer: str = event.get_sender_id()

            @session_waiter(timeout=180, record_history_chains=False)
            async def renderSession(controller: SessionController, event: AstrMessageEvent):
                content: str = event.message_str

                if event.get_sender_id() != issuer:
                    return
                
                if content == "Q":
                    await event.send(event.plain_result("取消渲染"))
                    controller.stop()
                    return

                if content == "":
                    return
                
                await event.send(event.plain_result("请求已接受, 正在渲染…"))
                # controller.stop()
                

                url = await markdownRenderer.render(content)
                await event.send(event.image_result(url))
                controller.stop()
            
            try:
                await renderSession(event)
            
            except TimeoutError as _:
                yield event.plain_result("Timeout!")
        
            except Exception as e:
                yield event.plain_result("Error! See Logs!")
                logger.error(e)

            finally:
                event.stop_event()

        except Exception as e:
            yield event.plain_result("Error! See Logs!")
            logger.error(e)


    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
