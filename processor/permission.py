"""FileHeader
: @Author: Chroniflow
: @Date: 2/4/2026, 10:23:34 PM
: @LastEditors: Chroniflow
: @LastEditTime: 2/16/2026, 11:05:44 AM
: @Description: 检查用户权限
: @Copyright: Copyright (©)}) 2026 Chroniflow. All rights reserved.
: @Email: code@ylyq.site
"""

import sqlite3 as sql

from astrbot.core import logger

from astrbot.core.utils.astrbot_path import get_astrbot_data_path

plugin_data_path = get_astrbot_data_path()+"/plugin_data/astrbot_plugin_announceManager"
plugin_path = get_astrbot_data_path()+"/plugins/astrbot_plugin_announceManager"
db_file_path: str = plugin_data_path+"/data.db"

# Testing Environment
# plugin_data_path: str = "/Users/chroniflow/demos/AstrBot/data/plugin_data/astrbot_plugin_announceManager"
# plugin_path: str = "/Users/chroniflow/demos/AstrBot/data/plugins/astrbot_plugin_announceManager/"
# db_file_path: str = plugin_data_path+"/data.db"

print(db_file_path)

def checkPermission(qid: str, request_groups: list[str]) -> dict[str, list[str]]:
    """
    checkPermission: 检查用户是否拥有某群发送权限

    :param qid: 要检查的用户的QID
    :type qid: str
    :param request_groups: 要检查用户是否拥有此群权限
    :type request_groups: list[str]
    :return: {"allowed": list[str], "denied": list[str]}
    :rtype: dict

    """

    # 初始化连接
    try:
        conn: sql.Connection = sql.connect(db_file_path)
        cursor: sql.Cursor = conn.cursor()
    except Exception as e:
        logger.error(e)
        return {"allowed": [], "denied": []}

    # 初始化结果dict
    allowed_groups: list[str] = []
    denied_groups: list[str] = []

    # 遍历列表查询
    for i in request_groups:
        print(i)
        cursor.execute(open(plugin_path + "/templates/sql/user/checkPermission.sql").read(), [qid, i])
        result = cursor.fetchone()
        if result is None:
            denied_groups.append(i)
            continue
        if result[0] == i:
            allowed_groups.append(i)
            continue
        else:
            raise TypeError("Database Data Illegal")

    conn.close()
    del conn


    return {"allowed": allowed_groups, "denied": denied_groups}
