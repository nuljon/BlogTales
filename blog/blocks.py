import email
from builtins import object


from wagtail.admin.edit_handlers import FieldPanel, FieldRowPanel, \
    InlinePanel, MultiFieldPanel, PageChooserPanel, StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.blocks import CharBlock, FieldBlock, PageChooserBlock, \
    StructBlock, StructValue, TextBlock, URLBlock
from wagtail.core.blocks.field_block import RichTextBlock
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.core.rich_text import RichText
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.users.models import UserProfile
from wagtail.utils.widgets import WidgetWithScript
from wagtailcodeblock.blocks import CodeBlock
from colorblock.models import ColorBlock

class AuthorBlock(blocks.StaticBlock):

    class Meta:
        icon = 'user'
        label = 'Author Profile'
        admin_text = '{label} : is cofigured by User Profile snippet'.format(label=label)
        template = 'blog/blocks/author_block.html'


class PageHeadingBlock(blocks.StructBlock):
    text = CharBlock(label='Page Heading Text', required=True)
    color = ColorBlock(
        required=False, help_text="Select text color that contrasts background", label="Text Color")
    shadow_offsets = CharBlock(label='Shadow Offsets and Blur Radius', default='1px 1px 2px', required=False, help_text='h-offset v-offset blur-radius')
    shadow_opacity = blocks.FloatBlock(required=False, label='Shadow Opacity', default='0.0',\
        help_text='Opacity of shadow from zero to one')

    class Meta:
        template = 'blog/blocks/page_heading_block.html'
        icon = 'title'
        label = 'Page Heading'
        help_text = 'For best SEO result, match all the titles.'
        max_num = 1


class JumbotronBlock(StructBlock):
    page_heading = PageHeadingBlock(required=False)
    description = blocks.CharBlock(
        required=False, icon='text-full', label='sub-title')
    background_image = ImageChooserBlock(required=True, icon='image', label='Jumbotron Image', help_text='image will be displayed 100% width scaled down to viewport size')

    class Meta:
        template = 'blog/blocks/jumbotron_block.html'
        icon = 'image'
        label = 'Jumbotron Header'
        max_num = 1

class PageHeaderBlock(blocks.StreamBlock):
    page_header = PageHeadingBlock()
    jumbotron_header = JumbotronBlock()

    class Meta:
        max_num = 1
        icon = 'title'
        label = 'Page Header',
        help_text = 'Page Heading = prominent title centered on page top. Jumbotron = prominent title and a sub-title centered at page top over a full width background image.'

class HeadingBlock(blocks.StructBlock):

    text = CharBlock(label='Heading Text', required=True)

    H2 = 'h2'
    H3 = 'h3'
    H4 = 'h4'
    H5 = 'h5'
    H6 = 'h6'

    heading_level = blocks.ChoiceBlock(choices=[

        (H2, 'Heading level 2'),
        (H3, 'Heading level 3'),
        (H4, 'Heading level 4'),
        (H5, 'Heading level 5'),
        (H6, 'Heading level 6'),
    ], required=True, icon='code')

    class Meta:
        template = 'blog/blocks/heading_block.html'
        label = 'Heading'
        icon = 'title'

class SearchBlock(blocks.StaticBlock):

    class Meta:
        template = 'blog/blocks/search_block.html'
        icon = 'search'
        label = 'Search Card'
        admin_text = '{label}: configured elsewhere'.format(label=label)


class ColumnBlock(blocks.StreamBlock):
    heading = HeadingBlock()
    paragraph = blocks.RichTextBlock(icon='pilcrow')
    image = ImageChooserBlock(icon='image')
    video = EmbedBlock(icon='media')
    author = AuthorBlock(icon='user')

    class Meta:
        template = 'blog/blocks/column.html'


class LinkStructValue(StructValue):
    def url(self):
        external_url = self.get('external_url')
        page = self.get('page')
        if external_url:
            return external_url
        elif page:
            return page.url


class QuickLinkBlock(StructBlock):
    text = CharBlock(label='link text', required=True)
    page = PageChooserBlock(label='page', required=False)
    external_url = URLBlock(label='external URL', required=False)

    class Meta:
        template = 'blog/blocks/quick_link_block.html'
        icon = 'site'
        value_class = LinkStructValue


class ConstructionBlock(blocks.StreamBlock):
    heading = HeadingBlock(required=False, icon='title')
    richtext = blocks.RichTextBlock(icon='pilcrow', label='Rich Text')
    paragraph = blocks.TextBlock(icon='pilcrow',template='blog/blocks/text_block.html', label='Simple Text')
    blockquote = blocks.BlockQuoteBlock(icon='openquote')
    image = ImageChooserBlock(icon='image')
    video = EmbedBlock(icon='media')
    code = CodeBlock(icon='code')
    search = SearchBlock(icon='search')
    author = AuthorBlock(icon='user')
    document = DocumentChooserBlock(icon='doc-full')
    email = blocks.EmailBlock(icon='mail')
    linklist = blocks.ListBlock(
        QuickLinkBlock(), template='blog/blocks/linklist_block.html', icon='link')
    documentlist = blocks.ListBlock(DocumentChooserBlock(icon='doc-full'))

    class Meta:
        template = 'blog/blocks/construction_block.html'
        icon = 'placeholder'
        label = 'Construction Block'


class SidebarBlock(blocks.StreamBlock):
    heading = HeadingBlock(required=False, icon='bold')
    richtext = blocks.RichTextBlock(icon='pilcrow', label='Rich Text')
    paragraph = blocks.TextBlock(
        icon='pilcrow', template='blog/blocks/text_block.html', label='Simple Text')
    blockquote = blocks.BlockQuoteBlock(icon='openquote')
    image = ImageChooserBlock(icon='image')
    video = EmbedBlock(icon='media')
    search = SearchBlock(icon='search')
    author = AuthorBlock(icon='user')
    document = DocumentChooserBlock(icon='doc-full')
    email = blocks.EmailBlock(icon='mail')
    linklist = blocks.ListBlock(
        QuickLinkBlock(), template='blog/blocks/linklist_block.html', icon='link')
    documentlist = blocks.ListBlock(DocumentChooserBlock(icon='doc-full'))


    class Meta:
        template = 'blog/blocks/sidebar_block.html'
        icon = 'logout'
        label = 'Sidebar block'


class LeftColumnWithSidebarBlock(blocks.StructBlock):

    left_column = ConstructionBlock(
        icon='arrow-left', label='Left column content')
    sidebar_column = SidebarBlock(
        icon='arrow-right', label='Sidebar column content')

    class Meta:
        template = 'blog/blocks/left_column_w_sidebar_block.html'
        icon = 'placeholder'
        label = 'Left column with sidebar'


class TwoColumnBlock(blocks.StructBlock):

    left_column = ConstructionBlock(
        icon='arrow-left', label='Left column content')
    right_column = ConstructionBlock(
        icon='arrow-right', label='Right column content')

    class Meta:
        template = 'blog/blocks/two_column_block.html'
        icon = 'placeholder'
        label = 'Two Columns'


class ThreeColumnBlock(blocks.StructBlock):

    left_column = ConstructionBlock(
        icon='arrow-left', label='Left column content')
    center_column = ConstructionBlock(
        icon='arrow-down', label='Center column content')
    right_column = ConstructionBlock(
        icon='arrow-right', label='Right column content')

    class Meta:
        template = 'blog/blocks/three_column_block.html'
        icon = 'title'
        label = 'Three Columns'


class InlinedItemsBlock(blocks.StreamBlock):
    text = RichTextBlock(icon='edit')
    image = ImageChooserBlock(icon='image')
    blockquote = blocks.BlockQuoteBlock(icon='openquote')
    document = DocumentChooserBlock(icon='doc-full')
    email = blocks.EmailBlock(icon='mail')
    link = QuickLinkBlock(icon='link', template='blog/blocks/quick_link_block.html')

    class Meta:
        template = 'blog/blocks/inlined_items_block.html'
        icon = 'arrow-right'
        label = 'Block-Inline Items'
        help_text = 'A row of flex items justified to full page width with equal spacing between, only wrapping to new row when necessary.'
