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

待更新

## 鸣谢

> 以下项目均直接或间接对本项目提供了帮助

https://github.com/nonebot/nonebot

https://github.com/Mrs4s/go-cqhttp

https://github.com/mamoe/mirai

https://github.com/SocialSisterYi/bilibili-API-collect

https://github.com/Passkou/bilibili_api