from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import TagModel, StoreModel, ItemModel
from schemas import ItemSchema, TagSchema, TagAndItemSchema

bp = Blueprint('Tags', __name__, description= 'Operation on tags')

@bp.route('/store/<string:store_id>/tag')
class TagsInStore(MethodView):

    @bp.response(200, TagSchema(many = True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()

    @bp.arguments(TagSchema)
    @bp.response(201, TagSchema)
    def post(self, data, store_id):
        tag = TagModel(**data, store_id = store_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message = str(e))

        return tag
    
@bp.route('/tag/<string:tag_id>')
class Tag(MethodView):
    @bp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag
    
    @bp.response(200)
    @bp.alt_response(404)
    @bp.alt_response(400)
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag deleted"}
        else:
            abort(404, message='The tag is in use')



@bp.route('/item/<string:item_id>/tag/<string:tag_id>')
class LinkTagsToItem(MethodView):
    @bp.response(201, ItemSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = ItemModel.query.get_or_404(tag_id)

        item.tags.append(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, str(e))
        
        return item

    @bp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)
        
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, str(e))
        
        return {"message":"Item and tag unlinked", "tag": tag, "item": item}
