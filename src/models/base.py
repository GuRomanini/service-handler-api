from sqlalchemy.ext.declarative import declarative_base


class _Base:
    __allow_unmapped__ = True


Base = declarative_base(cls=_Base)
