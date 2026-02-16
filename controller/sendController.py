"""FileHeader
: @Author: Chroniflow
: @Date: 2/5/2026, 7:15:33 PM
: @LastEditors: Chroniflow
: @LastEditTime: 2/5/2026, 7:15:35 PM
: @Description:
: @Copyright: Copyright (©)}) 2026 Chroniflow. All rights reserved.
: @Email: code@ylyq.site
"""


from astrbot.core import logger
from astrbot.core.platform import AstrMessageEvent
from astrbot.core.star import Star
# from data.plugins.astrbot_plugin_announceManager.processor import permission
from ..processor.permission import checkPermission
from ..processor.message import textMessage

async def send(self: Star,
               event: AstrMessageEvent,
               target: list[str],
               message: str) -> dict[str, list[str]]:

    success: list[str] = []
    failed: list[str] = []

    permission = checkPermission(event.get_sender_id(), target)

    for target in permission.get("allowed"):
        try:
            await textMessage(self, event.get_session_id(), target, message)
            success.append(target)
        except Exception as e:
            logger.error(e)
            failed.append(target)

    return {"success": success, "denied": permission.get("denied"), "failed": failed}


async def __init__() -> None:
    pass