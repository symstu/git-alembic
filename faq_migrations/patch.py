from alembic.runtime.migration import RevisionStep, HeadMaintainer

from faq_migrations.models.history import VersionHistory


class PatchedMigrationStep:
    @classmethod
    def upgrade(cls, revision_map, script):
        down_revision = script.module.down_revision

        # it may be a list when revision in merge point
        if type(down_revision) in (list, tuple):
            down_revision = str(script.module.down_revision)

        # initial migration
        if down_revision:
            print('PATCH: ', down_revision, script.module.revision)
            db_log = VersionHistory(down_revision, script.module.revision)
            db_log.save()

        return RevisionStep(revision_map, script, True)


class PatchedHeadMaintainer(HeadMaintainer):
    def __init__(self, context, heads):
        super(PatchedHeadMaintainer, self).__init__(context, heads)

    def update_to_step(self, step):
        super(PatchedHeadMaintainer, self).update_to_step(step)

        script = step.revision
        down_revision = script.module.down_revision

        # it may be a list when revision in merge point
        if type(down_revision) in (list, tuple):
            down_revision = str(script.module.down_revision)

        # initial migration. Skip initial migration
        if down_revision:
            # Create log file in current alembic opened session that used
            # in migrations context
            self.context.connection.execute(
                VersionHistory.__table__.insert(),
                from_ver=down_revision,
                to_ver=script.module.revision
            )
