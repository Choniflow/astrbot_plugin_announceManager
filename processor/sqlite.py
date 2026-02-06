'''FileHeader
: @Author: Chroniflow
: @Date: 1/24/2026, 8:31:06 PM
: @LastEditors: Chroniflow
: @LastEditTime: 1/24/2026, 10:17:41 PM
: @Description: SQLite处理模块
: @Copyright: Copyright (©)}) 2026 Chroniflow. Open-Source with GPL Licence.
: @Email: code@ylyq.site
'''

from io import TextIOWrapper
import sqlite3 as sql
from astrbot.core.utils.astrbot_path import get_astrbot_data_path
from astrbot.api import logger
import asyncio
import os

plugin_data_path = get_astrbot_data_path()+"/plugin_data/astrbot_plugin_announceManager"
plugin_path = get_astrbot_data_path()+"/plugins/astrbot_plugin_announceManager"
db_file_path: str = plugin_data_path+"/data.db"


##################################################################
# Modules
##################################################################


async def execute(statement: str) -> bool | Exception:
    """
    execute 执行SQL语句
    
    :param statement: 需要执行的语句
    :type statement: str
    :return: True表执行成功,不成功则返回Exception
    :rtype: bool | Exception
    """

    try:
        with sql.connect(db_file_path) as conn: sql.Connection
        cursor = conn.cursor()
        logger.debug("Executing SQL: %s", statement)
        cursor.execute(statement)
        conn.commit()
        conn.close()
        del cursor,conn
        return True
    except Exception as e:
        conn.close()
        del cursor,conn
        return e
    

async def parse(template_file: TextIOWrapper) -> list[str]:
    """
    parse 的 Docstring
    解析一个SQL模版文件
    
    :param template_file: 模版文件读写流
    :type template_file: TextIOWrapper
    :return: 模版List
    :rtype: list[str]
    :throws: Exception | TypeError
    """

    # 初始化结果列表
    statement: list[str] = [""]

    # 尝试读取模版文件并转化为列表
    # :throws Exception
    try:
        template: list[str] = template_file.readlines()
    except Exception as e:
        raise e
    
    # 尝试读取列表行
    # 如果遇到`#EOF`, 则结束
    # 如果遇到`#EOS`, 则切换为下一语句
    # 如果以`#`开头, 则忽略此行
    # :throws TypeError
    # :throws Exception
    # :return List[str]: 返回结果列表
    try:
        HEAD: int = 0
        # logger.info("Now the pointer is pointing at: %s\nAnd its value is: %s", HEAD, statement[HEAD])
        for i in template:
            if i.startswith("#EOF"):
                break
            if i.startswith("#EOS"):
                HEAD += 1
                statement.append("")
                logger.debug("Jumping into next statement...")
                continue
            if i.startswith("#"):
                continue
            statement[HEAD] = statement[HEAD] + i + "\n"
            logger.debug("Added a statement: %s", i)
            continue
    
    except TypeError:
        raise TypeError
    except Exception as e:
        raise e
    
    else:
        return statement

