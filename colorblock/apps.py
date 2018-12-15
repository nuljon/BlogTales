from django.apps import AppConfig


class ColorblockConfig(AppConfig):
    name = 'colorblock'
    verbose_name = "ColorBlock"
    verbose_name_plural = "ColorBlocks"

    def ready(self):
        import colorblock.wagtail_hooks
