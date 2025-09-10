

from django_tables2 import tables, TemplateColumn

from ..selection.models import Moderators


class ModeratorsTable(tables.Table):
    sessioncode = tables.Column(verbose_name="Session Code", orderable=False)
    sessiontitle = tables.Column(verbose_name="Title", orderable=False)
    speaker = tables.Column(verbose_name="Speaker(s)", orderable=False)
    moderator_name = ""

    search = tables.Column(verbose_name="")

    def render_sessiontitle(self, value):
        return value[:70]

    def render_search(self, value):
        return ""

    Edit = TemplateColumn(template_name='tables/value_update.html', verbose_name="")


    class Meta:
        model = Moderators
        template_name = "django_tables2/bootstrap4.html"
        fields = (
            "sessioncode",
            "sessiontitle",
            "speaker",
            "moderator_name"
            "search"
        )
