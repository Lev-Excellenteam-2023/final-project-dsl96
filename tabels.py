import os, enum, datetime, uuid
from typing import List, Optional
from sqlalchemy import String, create_engine, ForeignKey, Enum, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker, validates
from email_validate import validate


# get dir to sqlite (create if dont exist)
file_path = os.path.abspath(__file__)
root_dir = os.path.dirname(file_path)
TABLE_DIR = os.path.join(root_dir, 'database')
os.makedirs(TABLE_DIR, exist_ok=True)
print(TABLE_DIR)

engine = create_engine(f'sqlite+pysqlite:///{TABLE_DIR}//sqlite.db', echo=False)

_session = sessionmaker(bind=engine)


class Status(enum.Enum):
    pending = 1
    complete = 2
    sent = 3


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    uploads: Mapped[List["Upload"]] = relationship("Upload", back_populates="user", cascade="all, delete", lazy='joined')

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "uploads": [upload.to_dict() for upload in self.uploads]
        }

    @validates('email')
    def validate_email_format(self, key, email):
        if not validate(
                email_address=email,
                check_format=True,
                check_smtp=False):
            raise ValueError('Invalid email format')

        if not validate(
                 email_address=email,
                 check_smtp=True):
            raise ValueError('email dont exist')

        return email

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, email={self.email!r})"


class Upload(Base):
    __tablename__ = "Upload"
    id: Mapped[int] = mapped_column(primary_key=True)
    uid: Mapped[uuid] = mapped_column(Uuid, default=uuid.uuid4)
    filename: Mapped[str]
    upload_time: Mapped[datetime.datetime]
    finish_time: Mapped[Optional[datetime.datetime]]
    status = mapped_column(Enum(Status), nullable=False)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"))
    user: Mapped[Optional["User"]] = relationship(back_populates="uploads")

    @property
    def upload_path(self):
        return 'uploads\\' + str(self.uid)

    @property
    def downloads_path(self):
        return 'downloads\\' + str(self.uid)

    def to_dict(self):
        return {
            "id": self.id,
            "uid": self.uid,
            "filename": self.filename,
            "upload_time": self.upload_time.strftime("%Y-%m-%d %H:%M:%S"),
            "finish_time": self.finish_time.strftime("%Y-%m-%d %H:%M:%S") if self.finish_time else None,
            "status": self.status.name,
            "user_id": self.user_id
        }

    def __repr__(self) -> str:
        return f"Upload(id={self.id}, user_id={self.user_id} ,uuid={self.uid}, status={self.status} )"


if __name__ == '__main__':
    metadata_obj = Base.metadata
    metadata_obj.create_all(bind=engine)
