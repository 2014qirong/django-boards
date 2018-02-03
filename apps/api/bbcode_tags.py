from precise_bbcode.bbcode.tag import BBCodeTag
from precise_bbcode.tag_pool import tag_pool


class SpoilerTag(BBCodeTag):
    name = 'spoiler'
    definition_string = '[spoiler={TEXT1}]{TEXT2}[/spoiler]'
    format_string = '<div class="spoiler"><button class="button spoiler__open" type="button" name="button">Spoiler: {TEXT1}</button><div class="spoiler__content">{TEXT2}</div></div>'


class SizeTag(BBCodeTag):
    name = 'size'
    definition_string = '[size={RANGE=1,7}]{TEXT}[/size]'
    format_string = '<font size="+{RANGE=1,7}">{TEXT}</font>'


class UserTag(BBCodeTag):
    name = 'user'
    definition_string = '[user]{TEXT}[/user]'
    format_string = '<a href="/board/profile/{TEXT}/"><i class="fa fa-user" aria-hidden="true"></i> {TEXT}</a>'


class CodeTag(BBCodeTag):
    name = 'code'
    definition_string = '[code]{TEXT}[/code]'
    format_string = '<pre class="prettyprint"><code>{TEXT}</code></pre>'


class FontTag(BBCodeTag):
    name = 'font'
    definition_string = '[font={TEXT1}]{TEXT2}[/font]'
    format_string = '<span style="font-family:{TEXT1}">{TEXT2}</span>'


class UlTag(BBCodeTag):
    name = 'ul'
    definition_string = '[ul]{TEXT}[/ul]'
    format_string = '<ul>{TEXT}</ul>'


class OlTag(BBCodeTag):
    name = 'ol'
    definition_string = '[ol]{TEXT}[/ol]'
    format_string = '<ol>{TEXT}</ol>'


class LiTag(BBCodeTag):
    name = 'li'
    definition_string = '[li]{TEXT}[/li]'
    format_string = '<li>{TEXT}</li>'


class HrTag(BBCodeTag):
    name = 'hr'
    definition_string = '[hr]'
    format_string = '<hr/>'

    class Options:
        standalone = True


class ShadowTag(BBCodeTag):
    name = 'shadow'
    definition_string = '[shadow={TEXT1}]{TEXT2}[/shadow]'
    format_string = '<span style="text-shadow: 0px 0px 1em {TEXT1}">{TEXT2}</span>'


class AnchorTag(BBCodeTag):
    name = 'anchor'
    definition_string = '[anchor]{TEXT}[/anchor]'
    format_string = '<a name="{TEXT}"></a><i class="fa fa-anchor fa-fw"></i> <span style="font-style: italic">#{TEXT}</span>'


class QuoteTag(BBCodeTag):
    name = 'quote'
    definition_string = '[quote={TEXT1}]{TEXT2}[/quote]'
    format_string = '<blockquote><cite><a href="/board/profile/{TEXT1}"><span style="color:green;">{TEXT1}</span></a> said:</cite>{TEXT2}</blockquote>'


tag_pool.register_tag(SpoilerTag)
tag_pool.register_tag(SizeTag)
tag_pool.register_tag(UserTag)
tag_pool.register_tag(CodeTag)
tag_pool.register_tag(FontTag)
tag_pool.register_tag(UlTag)
tag_pool.register_tag(OlTag)
tag_pool.register_tag(LiTag)
tag_pool.register_tag(HrTag)
tag_pool.register_tag(ShadowTag)
tag_pool.register_tag(AnchorTag)
tag_pool.register_tag(QuoteTag)
