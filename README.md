# 哔哩哔哩DD机

[![VERSION](https://img.shields.io/github/v/release/SK-415/bilibili-dd-bot)](https://github.com/SK-415/bilibili-dd-bot/releases)
[![STARS](https://img.shields.io/github/stars/SK-415/bilibili-dd-bot)](https://github.com/SK-415/bilibili-dd-bot/stargazers)
[![LICENSE](https://img.shields.io/github/license/SK-415/bilibili-dd-bot)](https://github.com/SK-415/bilibili-dd-bot/blob/master/LICENSE)

## 简介

一款基于 [`nonebot`](https://github.com/nonebot/nonebot) 开发的QQ机器人, 支持将指定B站UP主的直播与动态信息推送至指定QQ群聊/私聊.

目前支持的功能有:
* 开播提醒
* 动态转发
* 群聊/私聊自定义推送列表
* 群聊直播提醒设置@全体成员

本项目初衷是为B站VUP们提供一个优质廉价的粉丝群推送方案. 极大的减轻管理员负担, 不会再遇到突击无人推送的尴尬情况. 同时还能将B博动态截图转发至粉丝群, 活跃群话题. 

虽然随着不断升级, DD机推送列表已经支持无上限订阅, 但是订阅过多的UP主, **推送会产生极高的延迟**. 因此除非能忍受极高的延迟, **目前不建议订阅过多UP主作为DD机使用**.

> 受限于B站对API爬取频率限制, 目前DD机会将所有UP主排成一列, 每隔十秒检查一位. 因此DD机订阅了 `x` 位UP主最高延迟就是 `10x` 秒.

既然项目名叫DD机自然能看出作者的野心. 目前 `v1.0` 阶段将持续完善对粉丝群的单推部分, 但是未来将会着手开发 `v2.0` 对DD机提供更加完善的支持, 尤其是解决大量订阅带来的高延迟的问题.

## 使用说明

先写个简单的说明, 之后再完善.

先下载 [`go-cqhttp`](https://github.com/Mrs4s/go-cqhttp/releases) 然后配置首次启动后自动生成的 `config.json` , 以下给出一份参考配置:

```
{
	"uin": 你的QQ号,
	"password": "你的QQ密码",
	"encrypt_password": false,
	"password_encrypted": "",
	"enable_db": true,
	"access_token": "",
	"relogin": {
		"enabled": true,
		"relogin_delay": 3,
		"max_relogin_times": 0
	},
	"ignore_invalid_cqcode": false,
	"force_fragmented": true,
	"heartbeat_interval": 0,
	"http_config": {
		"enabled": false,
		"host": "0.0.0.0",
		"port": 5700,
		"timeout": 0,
		"post_urls": {}
	},
	"ws_config": {
		"enabled": false,
		"host": "0.0.0.0",
		"port": 6700
	},
	"ws_reverse_servers": [
		{
			"enabled": true,
			"reverse_url": "ws://127.0.0.1:8080/ws",
			"reverse_api_url": "",
			"reverse_event_url": "",
			"reverse_reconnect_interval": 3000
		}
	],
	"post_message_format": "string",
	"debug": false,
	"log_level": ""
}
```

然后将本项目克隆或下载到本地, 确认安装了 `Python3.7+` . 之后在项目根目录运行 `cmd` , 依次执行:

```
pip install -r requirements.txt
pyppeteer-install
```

如果运行 `pyppeteer-install` 遇到 SSL 问题, 可以参考[这篇博客](https://www.sk415.com/article/article-detail/7/)最下面

安装完毕后就可以在命令行运行 `python bot.py` 或者直接双击 `bot.py` 文件运行了. 运行时请确保 `go-cqhttp` 也在正常工作.

本人目前学业繁忙, 暂时没有时间维护这个项目, 如果在使用过程中遇到问题, 可以提issue或者加我QQ: 2967923486

## 实装列表

> 目前实装的粉丝群, 感谢各位VUP和管理员们对本项目的支持

- [@白神遥Haruka](https://space.bilibili.com/477332594)
- [@寇蔻_Official](https://space.bilibili.com/493549454)
- [@初霜Shimo](https://space.bilibili.com/743603)
- [@宫本夏凌](https://space.bilibili.com/1319467)
- [@秋凛子Rinco](https://space.bilibili.com/479633069)
- [@月霖_咕咕](https://space.bilibili.com/4322043)
- [@芮音GoryRuin](https://space.bilibili.com/427275473)
- [@凛星RinStar](https://space.bilibili.com/82803440)

## 鸣谢

> 以下项目均直接或间接对本项目提供了帮助

- [`nonebot`](https://github.com/nonebot/nonebot) : DD机的根基, 感谢RC带来了如此强大的框架

- [`nonebot2`](https://github.com/nonebot/nonebot2) : 什么都别说了, RCNB!

- [`go-cqhttp`](https://github.com/Mrs4s/go-cqhttp) : 感谢Mrs4s对mirai与cqhttp协议的移植, 使本项目能无缝移植到mirai上

- [`mirai`](https://github.com/mamoe/mirai) : 感谢mirai社区延续了QQ机器人的火种

- [`bilibili-API-collect`](https://github.com/SocialSisterYi/bilibili-API-collect) : 目前最新最详细的B站api文档, 对本项目提供了极大的帮助

- [`bilibili_api`](https://github.com/Passkou/bilibili_api) : 好用而又强大的一个Python库, 为本项目的爬取逻辑提供了参考
