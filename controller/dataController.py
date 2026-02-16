"""FileHeader
: @Author: Chroniflow
: @Date: 2/2/2026, 10:23:34 PM
: @LastEditors: Chroniflow
: @LastEditTime: 2/2/2026, 10:23:59 PM
: @Description:
: @Copyright: Copyright (©)}) 2026 Chroniflow. All rights reserved.
: @Email: code@ylyq.site
"""

from io import TextIOWrapper
from astrbot.core.utils.astrbot_path import get_astrbot_data_path
from astrbot.api import logger
from processor import sqlite
import os

plugin_data_path = get_astrbot_data_path()+"/plugin_data/astrbot_plugin_announceManager"
plugin_path = get_astrbot_data_path()+"/plugins/astrbot_plugin_announceManager"
db_file_path: str = plugin_data_path+"/data.db"


async def initTable(user: str | None) -> bool:
    """initTable: 初始化数据库结构"""

    if user is not None:
        logger.warning("Admin %s is initialing table!", user)

    logger.info("Initialing dataset to file: %s", db_file_path)

    logger.info("Trying to create directory: %s", plugin_data_path)

    try:
        os.mkdir(plugin_data_path, 755)
    except FileExistsError:
        pass
    except Exception as e:
        raise e

    # 执行SQL
    try:
        sql_template: TextIOWrapper = open(f"{plugin_path}/templates/sql/init.sql") # 打开SQL模版
        sql_statements = await sqlite.parse(sql_template)

        if sql_statements == TypeError:
            raise TypeError
        if sql_template == Exception:
            raise Exception
        
        sql_template.close() # 关闭模版文件
        del sql_template # 释放内存

        logger.debug("We've get SQL Statements: %s", str(sql_statements))

        for i in sql_statements:
            result: bool | Exception = await sqlite.execute(i)
            
            if result == Exception:
                logger.error(result)
                return False
            continue
        
        return True
    
    except Exception as err:
        sql_template.close()
        del sql_template
        # logger.error("Error when initialing table: {0}".format(err))
        # return False
        raise err
    

async def cleanAll(user: str) -> bool:
    """
    cleanAll 的 Docstring
    
    :param user: 说明
    :type user: str
    :return: 说明
    :rtype: bool
    """

    logger.warning("管理员 %s 正在清除数据!", user)
    try:
        sql_template: TextIOWrapper = open(f"{plugin_path}/templates/sql/cleanAll.sql") # 打开SQL模版
        sql_statements = await sqlite.parse(sql_template)

        if sql_statements == TypeError:
            raise TypeError
        if sql_template == Exception:
            raise Exception
        
        sql_template.close() # 关闭模版文件
        del sql_template # 释放内存

        # logger.debug("We've get SQL Statements: %s", str(sql_statements))

        for i in sql_statements:
            result: bool | Exception = await sqlite.execute(i)
            
            if result == Exception:
                logger.error(result)
                return False
            continue
        
        return True
    
    except Exception as err:
        sql_template.close()
        del sql_template
        logger.error("Error when initialing table: {0}".format(err))
        return False
        
def __init__() -> None:
    pass