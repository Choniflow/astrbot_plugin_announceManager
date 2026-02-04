'''FileHeader
: @Author: Chroniflow
: @Date: 2/2/2026, 10:29:27 PM
: @LastEditors: Chroniflow
: @LastEditTime: 2/2/2026, 10:29:31 PM
: @Description: 
: @Copyright: Copyright (©)}) 2026 Chroniflow. All rights reserved.
: @Email: code@ylyq.site
'''

from io import TextIOWrapper
from astrbot.core.utils.astrbot_path import get_astrbot_data_path
from astrbot.api import logger
import data.plugins.astrbot_plugin_announceManager.processor.sqlite as sqlite

plugin_data_path: str = get_astrbot_data_path()+"/plugin_data/astrbot_plugin_announceManager"
plugin_path: str = get_astrbot_data_path()+"/plugins/astrbot_plugin_announceManager"
db_file_path: str = plugin_data_path+"/data.db"

async def addUser(QID: int, PermittedGroup: str) -> tuple[int, int, int]:
    """
    addUser 的 Docstring
    
    :param QID: 说明
    :type QID: int
    :param PermittedGroup: 说明
    :type PermittedGroup: str
    :return: 0: exitCode; 1: SUCCESS_TOTAL; 2: FAILED_TOTAL
    :rtype: tuple[int, int, int]
    """

    EXIT_CODE: int = 0
    TOTAL: int = 1
    SUCCESS_TOTAL: int = 0
    FAILED_TOTAL: int = 0

    try:
        sqlTemplate: TextIOWrapper = open(f"{plugin_path}/templates/sql/user/add.sql")
        sqlStatement: list[str] = await sqlite.parse(sqlTemplate)
    except Exception as e:
        logger.error(f"Error when adding user(parse): {e}")
        EXIT_CODE = -1
        FAILED_TOTAL = TOTAL
    finally:
        sqlTemplate.close()
        if EXIT_CODE == -1:
            return EXIT_CODE, SUCCESS_TOTAL, FAILED_TOTAL
    
    try:
        for i in sqlStatement:
            try:
                i = i.replace("%qid%", str(QID)).replace("%permitted_group%", PermittedGroup)
                logger.info("Executing SQL statement: %s", i)
                await sqlite.execute(i)
                SUCCESS_TOTAL += 1
                continue
            except Exception as e:
                FAILED_TOTAL += 1
                logger.warning(f"Error when adding user(execute), ignored:\n{e}")
                continue

    except Exception as e:
        logger.error(f"Error when adding user(execute): {e}")
        EXIT_CODE = -2
        return EXIT_CODE, SUCCESS_TOTAL, FAILED_TOTAL

    return EXIT_CODE, SUCCESS_TOTAL, FAILED_TOTAL

def __init__() -> None:
    pass