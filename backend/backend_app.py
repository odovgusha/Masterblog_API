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
    posts = POSTS.copy()

    sort_field = request.args.get('sort')       # title or content
    direction = request.args.get('direction')   # asc or desc

    if sort_field and sort_field not in ['title', 'content']:
        return jsonify({"error": "Invalid sort field. Must be 'title' or 'content'."}), 400
    #print(sort_field)
    if direction and direction not in ['asc', 'desc']:
        return jsonify({"error": "Invalid direction. Must be 'asc' or 'desc'."}), 400

    if sort_field:
        reverse = True if direction == 'desc' else False
        posts.sort(key=lambda x: x[sort_field].lower(), reverse=reverse)

    return jsonify(posts), 200

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

    for post in POSTS:
        if post["id"] == id:

            # Update only provided fields
            if data:
                if "title" in data:
                    post["title"] = data["title"]
                if "content" in data:
                    post["content"] = data["content"]
            #print data
            return jsonify({
                "id": post["id"],
                "title": post["title"],
                "content": post["content"]
            }), 200

    # Post not found
    return jsonify({
        "error": f"Post with id {id} was not found."
    }), 404


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title_query = request.args.get('title', '').lower()
    content_query = request.args.get('content', '').lower()

    results = []

    for post in POSTS:
        title_match = title_query in post["title"].lower()
        content_match = content_query in post["content"].lower()
        #print results
        if title_match or content_match:
            results.append(post)

    return jsonify(results), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
