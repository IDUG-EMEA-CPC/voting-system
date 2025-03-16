
DROP INDEX "SessionEVAL_IDX";
DROP INDEX "CompanyType_IDX";
DROP INDEX "PresentationPlatform_IDX";
DROP INDEX "PresentationTheme_IDX";
DROP INDEX "SessionModerator_IDX";
DROP INDEX "Session_IDX";


DROP TABLE "vote"."CompanyType" cascade;
DROP TABLE "vote"."PresentationPlatform" cascade;
DROP TABLE "vote"."PresentationTheme" cascade;
DROP TABLE "vote"."SessionEVAL";
DROP TABLE "vote"."SessionModerator";
DROP TABLE "vote"."Session";

-------------------------------------

CREATE TABLE "vote"."CompanyType" (
                "CompanyTypeCode" CHAR(1) NOT NULL,
                "CompanyTypeName" VARCHAR(200),

                primary key ("CompanyTypeCode")
        );

CREATE TABLE "vote"."PresentationPlatform" (
                "PresentationPlatformCode" CHAR(1) NOT NULL,
                "PresentationPlatformName" VARCHAR(200),

                primary key ("PresentationPlatformCode")
        );

CREATE TABLE "vote"."PresentationTheme" (
                "PresentationThemeCode" CHAR(1) NOT NULL,
                "PresentationThemeName" VARCHAR(200),

                primary key ("PresentationThemeCode")
        );

CREATE TABLE "vote"."Session" (
                "SessionCode" VARCHAR(10) NOT NULL,
                "SecondSpeaker" VARCHAR(200),
                "SessionNumber" VARCHAR(200),
                "SessionTitle" VARCHAR(200),
                "SessionType" VARCHAR(200),
                "PrimaryPresenterFullName" VARCHAR(200),
                "PrimaryPresenterCompany" VARCHAR(200),
                "SecondaryPresenterPanelistFullName" VARCHAR(200),
                "SecondaryPresenterPanelistCompany" VARCHAR(200),
                "PresentationCategory" VARCHAR(300),
                "PresentationPlatformCode" CHAR(1) NOT NULL,
                "CompanyTypeCode" CHAR(1) NOT NULL,
                "PresentationThemeCode" CHAR(1) NOT NULL,

                primary key ("SessionCode"),
                foreign key ("CompanyTypeCode") references "vote"."CompanyType"("CompanyTypeCode"),
                foreign key ("PresentationPlatformCode") references "vote"."PresentationPlatform"("PresentationPlatformCode"),
                foreign key ("PresentationThemeCode") references "vote"."PresentationTheme"("PresentationThemeCode")
        );

CREATE TABLE "vote"."SessionEVAL" (
                "SessionCode" VARCHAR(10) NOT NULL,
                "OverallRating" INT,
                "SpeakerRating" INT,
                "MaterialRating" INT,
                "ExpectationRating" INT,
                "AtendeeName" VARCHAR(200),
                "Company" VARCHAR(200),
                "Comments" VARCHAR(200),

                foreign key ("SessionCode") references "vote"."Session"("SessionCode")
        );

CREATE TABLE "vote"."SessionModerator" (
                "SessionCode" VARCHAR(10) NOT NULL,
                "StartCount" INT NOT NULL,
                "MidCount" INT NOT NULL,
                "Comments" VARCHAR(200),

                foreign key ("SessionCode") references "vote"."Session"("SessionCode")
        );

-------------------------------------

CREATE INDEX "SessionEVAL_IDX" ON "vote"."SessionEVAL" ("SessionCode");
CREATE UNIQUE INDEX "CompanyType_IDX" ON "vote"."CompanyType" ("CompanyTypeCode");
CREATE UNIQUE INDEX "PresentationPlatform_IDX" ON "vote"."PresentationPlatform" ("PresentationPlatformCode");
CREATE UNIQUE INDEX "PresentationTheme_IDX" ON "vote"."PresentationTheme" ("PresentationThemeCode");
CREATE UNIQUE INDEX "SessionModerator_IDX" ON "vote"."SessionModerator" ("SessionCode");
CREATE UNIQUE INDEX "Session_IDX" ON "vote"."Session" ("SessionCode");

