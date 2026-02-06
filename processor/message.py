'''FileHeader
: @Author: Chroniflow
: @Date: 2/4/2026, 9:31:54 PM
: @LastEditors: Chroniflow
: @LastEditTime: 2/4/2026, 9:32:00 PM
: @Description: 
: @Copyright: Copyright (©)}) 2026 Chroniflow. All rights reserved.
: @Email: code@ylyq.site
'''


from astrbot.api.event import MessageChain
from astrbot.api.star import Star


async def textMessage(self: Star, source: str | None, target: str, content: str) -> bool:
    """
    textMessage
    发送一条纯文本消息
    
    :param source: 消息来源SID
    :type target: str
    :param target: 消息目标SID
    :type source: str
    :param content: 消息内容
    :type content: str
    :return: 成功则返回True, 失败则返回False
    :rtype: bool
    """


    try:
        messageChain: MessageChain = MessageChain().message(content)
        await self.context.send_message(target, messageChain)
        return True
    except Exception as e:
        messageChain: MessageChain = MessageChain().message(str(e))
        if not source is None:
            await self.context.send_message(source, messageChain)
        return False


async def imageMessage(self: Star, source: str, target: str, content: str) -> bool:
    try:
        messageChain: MessageChain = MessageChain().message(content)
        await self.context.send_message(target, messageChain)
        return True
    except Exception as e:
        messageChain: MessageChain = MessageChain().message(str(e))
        if not source is None:
            await self.context.send_message(source, messageChain)
        return False