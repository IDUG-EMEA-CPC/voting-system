

from django_tables2 import tables, TemplateColumn

from ..score.models import Sessioneval, Session



class SessionEvalTable(tables.Table):
    id = tables.Column(verbose_name="")
    overallrating = tables.Column(verbose_name="Overall", orderable=False)
    speakerrating = tables.Column(verbose_name="Speaker", orderable=False)
    materialrating = tables.Column(verbose_name="Material", orderable=False)
    expectationrating = tables.Column(verbose_name="Expectation", orderable=False)
    atendeename = tables.Column(verbose_name="Attendee", orderable=False)
    company = tables.Column(verbose_name="Company", orderable=False)
    comments = tables.Column(verbose_name="Comments", orderable=False)

    def render_id(self, value):
        return ""


    class Meta:
        model = Sessioneval
        template_name = "django_tables2/bootstrap4.html"
        fields = (
            "id",
            "overallrating",
            "speakerrating",
            "materialrating",
            "expectationrating",
            "atendeename",
            "company",
            "comments"
        )

    Edit = TemplateColumn(template_name='tables/value_update.html', verbose_name="")
    Delete = TemplateColumn(template_name='tables/value_delete.html', verbose_name="")


class SessionTable(tables.Table):
    sessioncode = TemplateColumn(template_name='tables/value_session.html', verbose_name="Session Code", orderable=False)
    sessiontitle = tables.Column(verbose_name="Title", orderable=False)
    primarypresenterfullname = tables.Column(verbose_name="First Speaker", orderable=False)
    primarypresentercompany = tables.Column(verbose_name="Company", orderable=False)
    secondarypresenterpanelistfullname = tables.Column(verbose_name="Second Speaker", orderable=False)
    secondarypresenterpanelistcompany = tables.Column(verbose_name="Company", orderable=False)

    def render_sessiontitle(self, value):
        return value[:70]


    class Meta:
        model = Session
        template_name = "django_tables2/bootstrap4.html"
        fields = (
            "sessioncode",
            "sessiontitle",
            "primarypresenterfullname",
            "primarypresentercompany",
            "secondarypresenterpanelistfullname",
            "secondarypresenterpanelistcompany"
        )
