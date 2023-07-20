from sqlalchemy import select

from tabels import User, Upload, _session


class sqldb:

    def add_Upload(self, upload):
        with _session() as s:
            s.add(upload)
            s.commit()
            s.refresh(upload)

    def get_Upload(self, id):
        query = select(Upload).where(Upload.id == id)
        with _session() as s:
            upload = s.execute(query).scalar()
        return upload

    def add_user(self, user):
        with _session() as s:
            s.add(user)
            s.commit()
            s.refresh(user)


if __name__ == '__main__':
    db = sqldb()
    u = User(email='206tamar@gmail.com')
    db.add_user(u)
    print(u)
