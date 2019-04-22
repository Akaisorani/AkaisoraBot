# AkaisoraBot
Chat with AkaisoraBot by this Link:\
https://telegram.me/AkaisoraBot

## Description
AkaisoraBot is a useful telegram bot, of course used in *Telegram*, that can send pixiv pictures to you on demands. It can also be added into *Group*.

## Usage
### Simple Way
type `/pixiv` and follow the keyboard response.

### Full Command
`/pixiv <classification> [tag] [>photo(default) | >file]`

Parameter description

`<classification>` :

* normalrank : *normal ranklist*
* tag : *tag for search*
* id : *illust id*
* r18rank : *r18 rankllist (NSFW)*

`tag` :

* Tags you want to search

`[>photo(default) | >file]` :

* use this parameter to control the way AkaisoraBot send you picture, if missed, it will use *>photo* by default.

    * `>photo` : by image, but images will be compressed by telegram anyway
    * `>file` : by file, original large image

## Examples
```
/pixiv normalrank
/pixiv tag fate
/pixiv id 61777818
/pixiv normalrank >file
```
<table><tr>
<td><img src="https://s2.ax1x.com/2019/04/22/EAMO0S.gif" alt="EAMO0S.gif" border="0" /></td>
<td><img src="https://s2.ax1x.com/2019/04/22/EAMXTg.gif" alt="EAMXTg.gif" border="0" /></td>
</tr></table>