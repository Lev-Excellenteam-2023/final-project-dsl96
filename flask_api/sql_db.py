from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import joinedload, subqueryload

from tabels import User, Upload, _session, Status


class sqldb:

    def add_Upload(self, upload):
        """
        Adds an Upload object to the database.

        Parameters
        ----------
        upload : Upload
            The Upload object to be added to the database.

        Returns
        -------
        None
        """
        with _session() as s:
            s.add(upload)
            s.commit()
            s.refresh(upload)

    def get_Upload(self, id):
        """
        Retrieves an Upload object from the database based on its ID.

        Parameters
        ----------
        id : int
            The ID of the Upload object to be retrieved.

        Returns
        -------
        Upload or None
            The retrieved Upload object if found, or None if not found.
        """
        query = select(Upload).where(Upload.id == id)
        with _session() as s:
            upload = s.execute(query).scalar()
        return upload

    def add_user(self, user):
        """
        Adds a User object to the database.

        Parameters
        ----------
        user : User
            The User object to be added to the database.

        Returns
        -------
        None
        """
        with _session() as s:
            s.add(user)
            s.commit()
            s.refresh(user)

    def get_user_by_query(self, query):
        """
        Retrieves a User object from the database based on a custom query.

        Parameters
        ----------
        query
            The custom query used to retrieve the User object.

        Returns
        -------
        User or None
            The retrieved User object if found, or None if not found.
        """
        with _session() as s:
            user = s.execute(query).scalar()
        return user

    def get_user_by_email(self, email):
        """
        Retrieves a User object from the database based on the user's email.

        Parameters
        ----------
        email : str
            The email of the User object to be retrieved.

        Returns
        -------
        User or None
            The retrieved User object if found, or None if not found.
        """
        query = select(User).where(User.email == email)
        return self.get_user_by_query(query)

    def get_user_by_id(self, user_id):
        """
        Retrieves a User object from the database based on the user's ID.

        Parameters
        ----------
        user_id : int
            The ID of the User object to be retrieved.

        Returns
        -------
        User or None
            The retrieved User object if found, or None if not found.
        """
        query = select(User).where(User.id == user_id)
        return self.get_user_by_query(query)

    def add_upload_to_user_by_email(self, email, upload):
        """
        Adds an Upload object to the user's uploads based on the user's email.

        Parameters
        ----------
        email : str
            The email of the User object to which the Upload will be added.
        upload : Upload
            The Upload object to be added to the user's uploads.

        Returns
        -------
        Upload
            The added Upload object.
        """
        query = select(User).where(User.email == email)
        with _session() as s:
            user = s.execute(query).scalar()

            if not user:
                raise ValueError("User with this email does not exist.")

            user.uploads.append(upload)
            s.commit()
            s.refresh(upload)
        return upload


if __name__ == '__main__':
    db = sqldb()

    new_upload = Upload(
        filename="example.txt",
        upload_time=datetime .utcnow(),
        status=Status .pending,
    )
    u = db.add_upload_to_user_by_email('206tamar@gmail.com', new_upload)
    print(u)
