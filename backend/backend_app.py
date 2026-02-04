from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()

    missing_fields = []
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    if "title" not in data:
        missing_fields.append("title")
    if "content" not in data:
        missing_fields.append("content")

    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "missing": missing_fields
        }), 400

    if POSTS:
        last_post = POSTS[-1]
        new_id = last_post["id"] + 1
    else:
        new_id = 1

    new_post = {
        "id": new_id,
        "title": data["title"],
        "content": data["content"]
    }

    POSTS.append(new_post)

    return jsonify(new_post), 201


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    for post in POSTS:
        if post["id"] == id:
            POSTS.remove(post)
            return jsonify({
                "message": f"Post with id {id} has been deleted successfully."
            }), 200
    #print(post)
    return jsonify({
        "error": f"Post with id {id} was not found."
    }), 404

@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    data = request.get_json()

    # Find the post
    for post in POSTS:
        if post["id"] == id:

            # Update only provided fields
            if data:
                if "title" in data:
                    post["title"] = data["title"]
                if "content" in data:
                    post["content"] = data["content"]

            return jsonify({
                "id": post["id"],
                "title": post["title"],
                "content": post["content"]
            }), 200

    # Post not found
    return jsonify({
        "error": f"Post with id {id} was not found."
    }), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
