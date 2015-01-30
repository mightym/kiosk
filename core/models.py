from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel

from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailimages.models import Image

from modelcluster.fields import ParentalKey

from omnibus import api
from wagtail.wagtailcore.signals import page_published, page_unpublished

def send_message(sender, instance, **kwargs):
    print('SAVESAVESAVESAVESAVESAVE')
    api.publish(
        'slide_update',  # the name of the channel
        'published',   # the `type` of the message/event, clients use this name
                        # to register event handlers
        {
            'id': instance.id,

        },  # payload of the event, needs to be
            # a dict which is JSON dumpable.
    )



class HomePage(Page):
    body = RichTextField(blank=True)
    subpage_types = ['SectionPage', 'ImprintPage', 'ContactPage']
    indexed_fields = ('body', )


    @property
    def sections(self):
        # Get list of live slide pages that are descendants of this page
        sections = SectionPage.objects.live().descendant_of(self)
        return sections

    @property
    def imprint(self):
        # Get list of live slide pages that are descendants of this page
        imprint = ImprintPage.objects.live().descendant_of(self)
        return imprint

    @property
    def contact(self):
        # Get list of live slide pages that are descendants of this page
        contact = ContactPage.objects.live().descendant_of(self)
        return contact

    class Meta:
        verbose_name = "Homepage"

HomePage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('body', classname="full"),
]

HomePage.promote_panels = [
    MultiFieldPanel(Page.promote_panels, "Common page configuration"),
]

class SectionPage(Page):
    body = RichTextField()
    search_name = "Section"

    indexed_fields = ('body', )
    subpage_types = ['SlidePage']

    @property
    def slides(self):
        # Get list of live slide pages that are descendants of this page
        slides = SlidePage.objects.live().descendant_of(self)
        return slides

SectionPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('body', classname="full"),
]


class ImprintPage(Page):
    body = RichTextField()
    search_name = "Legal"

    indexed_fields = ('body', )
    subpage_types = ['SlidePage']

    @property
    def slides(self):
        # Get list of live slide pages that are descendants of this page
        slides = SlidePage.objects.live().descendant_of(self)
        return slides

ImprintPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('body', classname="full"),
]

class ContactPage(Page):
    body = RichTextField()
    search_name = "Imprint"

    indexed_fields = ('body', )
    subpage_types = ['SlidePage']

    @property
    def slides(self):
    # Get list of live slide pages that are descendants of this page
        slides = SlidePage.objects.live().descendant_of(self)
        return slides


ContactPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('body', classname="full"),
]



class SlidePage(Page):
    body = RichTextField()
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    bg_color = models.CharField(_('Background Color'), max_length=200, default='#0a70a6')
    is_blurred = models.BooleanField(_('Blurr Image'), default=False)
    has_overlay = models.BooleanField(_('Show Color Overlay'), default=False)
    overlay_color = models.CharField(_('Background Color'), max_length=200, default='#0a70a6')
    extra_class = models.CharField(_('Special Class Name'), max_length=200, null=True, blank=True)
    search_name = "Slide"
    indexed_fields = ('body', )

    @property
    def ratio(self):
        ratio = float(self.image.width) / float(self.image.height)
        return ratio

page_published.connect(send_message, sender=SlidePage)


SLIDE_FIELD_COLLECTION = [
    FieldPanel('bg_color', classname="bg_color"),
    FieldPanel('is_blurred', classname="is_blurred"),
    FieldPanel('has_overlay', classname="has_overlay"),
    FieldPanel('overlay_color', classname="overlay_color"),
    FieldPanel('extra_class', classname="extra_class"),
]

SlidePage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('body', classname="full"),
    ImageChooserPanel('image'),
    MultiFieldPanel(
        SLIDE_FIELD_COLLECTION,
            heading="Slide Meta Settings",
            classname="collapsible collapsed"
    ),

]