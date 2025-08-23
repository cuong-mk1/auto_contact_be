from .databaseConfig import db
class BlackLists(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)
    reason = db.Column(db.String, nullable=True)
    bl_group_id = db.Column(db.Integer, db.ForeignKey('bl_groups.id'), nullable=False)

    def __repr__(self):
        return f'<black_lists {self.url}>'
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    @classmethod
    def bulk_create_data_black_lists(cls, data,bl_group_id):
        # skip data if exists
        list_urls_exists = cls.query.filter(cls.url.in_(data), cls.bl_group_id == bl_group_id).all()
        list_urls_exists = [d.url for d in list_urls_exists]
        data = list(set(data) - set(list_urls_exists))
        black_lists = [cls(url=d, bl_group_id=bl_group_id) for d in data]
        db.session.bulk_save_objects(black_lists)
        db.session.commit()
        data = cls.query.order_by(cls.id.desc()).limit(len(black_lists)).all()
        return data
    # delete all
    @classmethod
    def delete_all(cls):
        cls.query.delete()
        db.session.commit()
        return True
    @classmethod
    def create_data_black_lists(cls, data):
        black_list = cls(url=data['url'], reason=data.get('reason'))
        db.session.add(black_list)
    
        # add index  = max index + 1