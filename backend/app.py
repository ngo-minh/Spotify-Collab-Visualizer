from flask import Flask, request, jsonify
from flask_cors import CORS
from spotify_client import get_artist_id, get_all_collaborations
import logging

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
CORS(app)

@app.route('/search', methods=['POST'])
def search_artist():
    artist_name = request.json['artistName']
    artist_id = get_artist_id(artist_name)
    if artist_id:
        nodes, edges, top_collaborators = get_all_collaborations(artist_id)
        return jsonify({
            "artistId": artist_id,
            "collaborations": nodes,
            "vertex_count": len(nodes),
            "edge_count": len(edges),
            "top_collaborators": top_collaborators
        })
    else:
        return jsonify({"error": "Artist not found"}), 404



if __name__ == '__main__':
    app.run(debug=True)

