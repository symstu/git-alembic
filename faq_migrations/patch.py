from alembic.runtime.migration import HeadMaintainer, MigrationStep

from faq_migrations.models import db_session
from faq_migrations.models.history import VersionHistory


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


class MigrationStepPatched(MigrationStep):

    @classmethod
    def downgrade_from_script(cls, revision_map, script):
        a = super(MigrationStepPatched, cls).downgrade_from_script(
            revision_map, script
        )
        print('RESULT OF MIGRATION : ', a)
        db_session.delete(
            db_session.query(VersionHistory).filter(
                VersionHistory.to_ver == script.revision
            ).first()
        )
        db_session.commit()
        return a
