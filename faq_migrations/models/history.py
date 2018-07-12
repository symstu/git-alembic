from sqlalchemy import Column, Integer, String
from . import Base, db_session, engine, MetaData


class VersionHistory(Base):
    __tablename__ = 'alembic_version_history'

    id = Column(Integer, primary_key=True)
    from_ver = Column(String, nullable=False)
    to_ver = Column(String, nullable=False)

    def __init__(self, previous_revision, forward_revision):
        self.from_ver = previous_revision
        self.to_ver = forward_revision

    def check_for_copy(self):
        result = db_session.query(VersionHistory)\
            .filter(VersionHistory.to_ver == self.to_ver)\
            .filter(VersionHistory.from_ver == self.from_ver)\
            .first()

        return True if not result else False

    @staticmethod
    def list(offset=0, limit=0):
        return db_session.query(VersionHistory)\
            .filter()\
            .order_by(VersionHistory.id.desc()) \
            .offset(offset) \
            .limit(limit)

    def save(self):

        if not engine.dialect.has_table(engine, self.__tablename__):
            metadata = MetaData(engine)
            metadata.create_all()

        if self.check_for_copy():
            db_session.add(self)
            db_session.commit()

            return True

        return False

    def __repr__(self):
        return f"<Version({self.id}) {self.from_ver} -> " \
               f"{self.to_ver}>"
