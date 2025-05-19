from django.db import models


class Companytype(models.Model):
    companytypecode = models.CharField(db_column='CompanyTypeCode', primary_key=True,
                                       max_length=1)  # Field name made lowercase.
    companytypename = models.CharField(db_column='CompanyTypeName', max_length=200, blank=True,
                                       null=True)  # Field name made lowercase.

    class Meta:
      managed = False
      db_table = 'CompanyType'


class Presentationplatform(models.Model):
  presentationplatformcode = models.CharField(db_column='PresentationPlatformCode', primary_key=True,
                                              max_length=1)  # Field name made lowercase.
  presentationplatformname = models.CharField(db_column='PresentationPlatformName', max_length=200, blank=True,
                                              null=True)  # Field name made lowercase.

  class Meta:
    managed = False
    db_table = 'PresentationPlatform'


class Presentationtheme(models.Model):
  presentationthemecode = models.CharField(db_column='PresentationThemeCode', primary_key=True,
                                           max_length=1)  # Field name made lowercase.
  presentationthemename = models.CharField(db_column='PresentationThemeName', max_length=200, blank=True,
                                           null=True)  # Field name made lowercase.

  class Meta:
    managed = False
    db_table = 'PresentationTheme'


class Session(models.Model):
  sessioncode = models.CharField(db_column='SessionCode', primary_key=True, max_length=10)  # Field name made lowercase.
  secondspeaker = models.CharField(db_column='SecondSpeaker', max_length=200, blank=True,
                                   null=True)  # Field name made lowercase.
  sessionnumber = models.CharField(db_column='SessionNumber', max_length=200, blank=True,
                                   null=True)  # Field name made lowercase.
  sessiontitle = models.CharField(db_column='SessionTitle', max_length=200, blank=True,
                                  null=True)  # Field name made lowercase.
  sessiontype = models.CharField(db_column='SessionType', max_length=200, blank=True,
                                 null=True)  # Field name made lowercase.
  primarypresenterfullname = models.CharField(db_column='PrimaryPresenterFullName', max_length=200, blank=True,
                                              null=True)  # Field name made lowercase.
  primarypresentercompany = models.CharField(db_column='PrimaryPresenterCompany', max_length=200, blank=True,
                                             null=True)  # Field name made lowercase.
  secondarypresenterpanelistfullname = models.CharField(db_column='SecondaryPresenterPanelistFullName', max_length=200,
                                                        blank=True, null=True)  # Field name made lowercase.
  secondarypresenterpanelistcompany = models.CharField(db_column='SecondaryPresenterPanelistCompany', max_length=200,
                                                       blank=True, null=True)  # Field name made lowercase.
  presentationcategory = models.CharField(db_column='PresentationCategory', max_length=300, blank=True,
                                          null=True)  # Field name made lowercase.
  presentationplatformcode = models.ForeignKey(Presentationplatform, models.DO_NOTHING,
                                               db_column='PresentationPlatformCode')  # Field name made lowercase.
  companytypecode = models.ForeignKey(Companytype, models.DO_NOTHING,
                                      db_column='CompanyTypeCode')  # Field name made lowercase.
  presentationthemecode = models.ForeignKey(Presentationtheme, models.DO_NOTHING,
                                            db_column='PresentationThemeCode')  # Field name made lowercase.

  class Meta:
    managed = False
    db_table = 'Session'


class Sessioneval(models.Model):
    #id = models.IntegerField(primary_key=True)
    sessioncode = models.ForeignKey(Session, models.DO_NOTHING, db_column='SessionCode')  # Field name made lowercase.
    overallrating = models.IntegerField(db_column='OverallRating', blank=True, null=True)  # Field name made lowercase.
    speakerrating = models.IntegerField(db_column='SpeakerRating', blank=True, null=True)  # Field name made lowercase.
    materialrating = models.IntegerField(db_column='MaterialRating', blank=True, null=True)  # Field name made lowercase.
    expectationrating = models.IntegerField(db_column='ExpectationRating', blank=True, null=True)  # Field name made lowercase.
    atendeename = models.CharField(db_column='AtendeeName', max_length=200, blank=True, null=True)  # Field name made lowercase.
    company = models.CharField(db_column='Company', max_length=200, blank=True, null=True)  # Field name made lowercase.
    comments = models.CharField(db_column='Comments', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SessionEVAL'


class Sessionmoderator(models.Model):
  sessioncode = models.OneToOneField(Session, models.DO_NOTHING, db_column='SessionCode')  # Field name made lowercase.
  startcount = models.IntegerField(db_column='StartCount')  # Field name made lowercase.
  midcount = models.IntegerField(db_column='MidCount')  # Field name made lowercase.
  comments = models.CharField(db_column='Comments', max_length=200, blank=True, null=True)  # Field name made lowercase.

  class Meta:
    managed = False
    db_table = 'SessionModerator'



class Best_Session(models.Model):
    sessioncode = models.CharField(db_column='sessioncode', primary_key=True, max_length=10)
    primarypresenterfullname = models.CharField(db_column='primarypresenterfullname', max_length=200, blank=True, null=True)
    primarypresentercompany = models.CharField(db_column='primarypresentercompany', max_length=200, blank=True, null=True)
    secondarypresenterpanelistfullname = models.CharField(db_column='secondarypresenterpanelistfullname', max_length=200, blank=True, null=True)
    secondarypresenterpanelistcompany = models.CharField(db_column='secondarypresenterpanelistcompany', max_length=200, blank=True, null=True)
    companytypecode = models.CharField(db_column='companytypecode', max_length=1)
    rating = models.FloatField(db_column='rating', blank=True, null=True)
    rank = models.IntegerField(db_column='rank', blank=True, null=True)

    class Meta:
        managed = False
        db_table = "best_session"


class Tracks(models.Model):
    sessioncode = models.CharField(db_column='sessioncode', primary_key=True, max_length=10)
    speaker = models.CharField(db_column='speaker', max_length=200, blank=True, null=True)
    nb_eval = models.IntegerField(db_column='nb_eval', blank=True, null=True)
    rating = models.FloatField(db_column='rating', blank=True, null=True)
    rank = models.IntegerField(db_column='rank', blank=True, null=True)

    class Meta:
        managed = False
        db_table = "tracks"


