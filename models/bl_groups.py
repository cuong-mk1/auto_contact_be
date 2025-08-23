from .databaseConfig import db
class BlGroups(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f'<bl_groups {self.name}>'
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    @classmethod
    def create_blacklist_group(cls, data):
        bl_group = cls(name=data['name'], description=data.get('description'))
        db.session.add(bl_group)
        db.session.commit()
        return bl_group
    # get by id
    @classmethod
    def get_blacklist_group(cls, id):
        bl_group = cls.query.get(id)
        return bl_group
    @classmethod
    def get_all_blacklist_groups(cls):
        bl_groups = cls.query.order_by(cls.id.desc()).all()
        return bl_groups
        