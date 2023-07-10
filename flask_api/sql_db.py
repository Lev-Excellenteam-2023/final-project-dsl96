from sqlalchemy import select

from tabels import User,Upload,_session


class sqldb:

    def add_Upload(self,upload):
            with  _session()  as s:
                s.add(upload)
                s.commit()
                s.refresh(upload)

    def get_Upload(self,id):
        query = select(Upload).where(Upload.id==id)
        with _session() as s:
            upload = s.execute(query).scalar()
        return upload


if __name__=='__main__':
    print(sqldb().get_Upload(2))