from flask import Response, jsonify, request, Blueprint

from archivy import data
from archivy.models import DataObj

api_bp = Blueprint('api', __name__)


@api_bp.route("/bookmarks/<int:bookmark_id>")
def get_bookmark(bookmark_id):
    bookmark_post = data.get_item(bookmark_id)

    return jsonify(
        bookmark_id=bookmark_id,
        title=bookmark_post["title"],
        content=bookmark_post.content,
        md_path=bookmark_post["fullpath"],
    ) if bookmark_post is not None else Response(status=404)


@api_bp.route("/bookmarks", methods=["POST"])
def create_bookmark():
    json_data = request.get_json()
    bookmark = DataObj(
        url=json_data['url'],
        desc=json_data['desc'],
        tags=json_data['tags'],
        path=json_data['path'],
        type="bookmarks",
    )
    bookmark.process_bookmark_url()
    bookmark_id = bookmark.insert()
    if bookmark_id:
        return jsonify(
            bookmark_id=bookmark_id,
        )
    return Response(status=400)