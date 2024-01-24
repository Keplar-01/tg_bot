from database import Session
from utils.data_sources.IDataSource import IDataSource


class SQLAlchemyDataSource(IDataSource):
    def __init__(self, session):
        self.session = session

    def get_list(self, table_type, *args, **kwargs):
        return self.session.query(table_type).all()

    def get_item(self, item_id, table_type, *args, **kwargs):
        return self.session.query(table_type).filter_by(id=item_id).first()

    def get_item_by_filter(self, table_type, *args, **kwargs):
        return self.session.query(table_type).filter_by(**kwargs).first()

    def get_list_by_filter(self, table_type, *args, **kwargs):
        return self.session.query(table_type).filter_by(**kwargs).all()

    def insert_item(self, item, *args, **kwargs):
        self.session.add(item)
        self.session.commit()

    def update_item(self, item, *args, **kwargs):
        if item:
            for key, value in kwargs.items():
                setattr(item, key, value)

            self.session.commit()

    def commit(self):
        self.session.commit()

    def delete_item(self, item):
        self.session.delete(item)
        self.session.commit()

    def delete_items_by_filter(self, table_type, **kwargs):
        items_to_delete = self.session.query(table_type).filter_by(**kwargs).all()

        for item in items_to_delete:
            self.session.delete(item)

        self.session.commit()

