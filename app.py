from flask import request, jsonify, make_response
from flask_restx import Resource

from config import api, db, app, DEBUG, User
from manpower_data import manpowerlist


# Create user database
with app.app_context():
    db.create_all(bind_key=None)


@api.route('/')
class IndexRoute(Resource):
    def get():
        return make_response(jsonify({"message": "index route"}), 200)


@api.route('/users')
class UserRoute(Resource):

    @api.response(500, 'Internal error')
    @api.response(200, 'user created')
    def post(self):
        try:
            data = request.get_json()
            new_user = User(username=data.get('username'), email=data.get('email'))
            db.session.add(new_user)
            db.session.commit()
            return make_response(jsonify({"message": "user created"}), 200)
        except Exception as e:
            return make_response(jsonify({"message": str(e)}), 500)

    @api.response(500, 'Internal error')
    @api.response(200, 'Success')
    def get(self):
        try:
            users = User.query.all()
            return make_response(jsonify({"users": [user.json() for user in users]}), 200)
        except Exception as e:
            print(e)
            return make_response(jsonify({"message": "error getting users"}), 500)


@api.route('/users/<int:id>')
@api.doc(params={'id': 'User ID'})
class UserDetailRoute(Resource):

    def get(self, id):
        try:
            user = User.query.filter(id=id).first()
            if user:
                return make_response(jsonify({"user": user.json()}), 200)
            return make_response(jsonify({"message": "user not found"}), 404)
        except Exception:
            return make_response(jsonify({"message": "error getting user"}), 500)

    # update user
    def put(self, id):
        try:
            data = request.get_json()
            user = User.query.filter_by(id=id).first()
            if user:
                user.username = data['username']
                user.email = data['email']
                db.session.commit()
                return make_response(jsonify({"message": "user updated"}), 200)
            return make_response(jsonify({"message": "user not found"}), 404)
        except Exception:
            return make_response(jsonify({"message": "error updating user"}), 500)

    def delete(self, id):
        try:
            user = User.query.filter_by(id=id).first()
            if user:
                db.session.delete()
                db.session.commit()
                return make_response(jsonify({"message": "user deleted"}), 200)
            return make_response(jsonify({"message": "user not found"}), 404)
        except Exception:
            return make_response(jsonify({"message": "error deleting user"}), 500)


@api.route('/manpower/')
@api.doc(params={})
class ManPowerListRoute(Resource):

    def get(self):
        try:
            data = manpowerlist()
            return make_response(jsonify({"data": data}))
        except Exception:
            return make_response(jsonify({"message": "Cannot retrieve manpowerlist data"}), 500)


if __name__ == "__main__":
    app.run(debug=DEBUG)
