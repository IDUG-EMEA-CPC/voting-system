

from django_tables2 import tables, TemplateColumn

from ..score.models import Score, Moderators



class ScoreTable(tables.Table):
    score_id = tables.Column(verbose_name="")
    overall_score = tables.Column(verbose_name="Overall", orderable=False)
    speaker_score = tables.Column(verbose_name="Speaker", orderable=False)
    material_score = tables.Column(verbose_name="Material", orderable=False)
    level_score = tables.Column(verbose_name="Expectation", orderable=False)
    notes = tables.Column(verbose_name="Comments", orderable=False)

    def render_score_id(self, value):
        return ""


    class Meta:
        model = Score
        template_name = "django_tables2/bootstrap4.html"
        fields = (
            "score_id",
            "overall_score",
            "speaker_score",
            "material_score",
            "level_score",
            "notes"
        )

    Edit = TemplateColumn(template_name='tables/value_update.html', verbose_name="")
    Delete = TemplateColumn(template_name='tables/value_delete.html', verbose_name="")


class SessionTable(tables.Table):
    session_code = TemplateColumn(template_name='tables/value_session.html', verbose_name="Session Code", orderable=False)
    date = tables.Column(verbose_name="", orderable=False)
    session_date = tables.Column(verbose_name="Day", orderable=False)
    session_time = tables.Column(verbose_name="Time", orderable=False)
    session_title = tables.Column(verbose_name="Title", orderable=False)
    speaker = tables.Column(verbose_name="Speaker(s)", orderable=False)
    subject_desc = tables.Column(verbose_name="Platform", orderable=False)
    moderator_name = tables.Column(verbose_name="Moderator", orderable=False)

    def render_date(self, value):
        return ""

    class Meta:
        model = Moderators
        template_name = "django_tables2/bootstrap4.html"
        fields = (
            "session_code",
            "session_date",
            "session_time",
            "session_title",
            "speaker",
            "subject_desc",
            "moderator_name"
        )
