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
from colorblock.models import ColorBlock


class BrickmakerBlock(blocks.StaticBlock):

    class Meta:
        icon = 'user'
        label = 'Message Author Profile'
        admin_text = '{label} : is cofigured by User Profile snippet'.format(
            label=label)
        template = 'thewall/blocks/brickmaker_block.html'
