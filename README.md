# 公告推送管理器

## 命令一览

|命令|权限|说明|
|:--:|:--:|:--:|
|`anadmin`|su|管理系列命令|
|`anpl`|a|纯文本公告|
|`admd`|a|Markdown公告|
|`anaimd`|a|AI辅助生成公告(暂缓开发)|
|`andel`|a|删除公告|
|`anview`|u|查看公告|

### 发布公告系列命令 参数

|参数|长参数|接受值|描述|默认值|
|--|:--:|:--:|:--:|:--|
|`-g`|`--group`|UMO|发送群聊(all表示所有)|`all`|
|`-a`|`--at`|QID|@的人(all表示全体成员)|None|
|`-r`|`--renderer`|String|渲染器模版名|`default`|
|`-t`|`--template`|String|公告模版名|`default`|
|`-s`|`--set-as-qq-announcement`|Boolen|设置为QQ群公告|`false`|
|`-m`|`--send-to-minecraft`|Boolen|同步发送至Minecraft|`false`|
|`-S`|`--save-time`|Integar|公告存储时间, `-1`表示永久, `0`表示不存储|`-1`|



## 公告模版

### default

```
=====公告======
发布人: %sender%
发布时间: %time%
公告内容:
%content%
==============
```

### plain

```
%content%
```
