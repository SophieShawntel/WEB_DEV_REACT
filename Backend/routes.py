from app import app, db
from flask import request, jsonify
from models import friend

#Get all friends
@app.route("/api/friends", methods=['GET'])
def get_friends():
    friends = friend.query.all()
    result = [friend.to_json() for friend in friends]
    return jsonify(result), 200          #BY DEFAULT, IT IS 200    

#create A Friend
@app.route("/api/friends", methods=['POST'])
def create_friend():
    try:
        data = request.get_json()

                                    #HOW TO CHECK AND HANDLE REQUIRED FIELDS
        required_fields = ["name", "role", "description", "gender"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"missing required field: {field}. Please aaaadd"}), 400



        name = data.get("name")
        role = data.get("role")
        description = data.get("description")                  #16618968911760
        gender = data.get("gender")
       

        #fetch Avater image base on gender 
        if gender == "male":
           img_url = f"https://avatar.iran.liara.run/public/boy?username={name}" 
        elif gender == "female":
            img_url = f"https://avatar.iran.liara.run/public/girl?username={name}"
        else:
            img_url = None   #can ignore else
            
        new_friend = friend(name=name, role=role, description=description, gender=gender, img_url=img_url)

        db.session.add(new_friend)
        db.session.commit()
        
        return jsonify({"msg": "Friend created successfully!"}), 201   #jsonify(new_friend.to_jason)
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error":str(e)}), 500

                                    #DELETE A FRIEND  QST:  is this method applicable to a web app that has many user.


@app.route("/api/friends/<int:id>", methods=['DELETE']) 
def delete_friend(id):
    try:
        friends = friend.query.get(id)                  ## used 'FRIENDS' as variable here becuase 'FRIEND' was having issues. Maybe because of confusing in flask or python have same Class/Model name as variable
        if friends is None:
            return jsonify({"error":"Friend Not Found"}), 404

        db.session.delete(friends)
        db.session.commit()
        return jsonify({"msg":"Friend Deleted"}), 200
    except Exception as e:
        db.session.rollback() 
        return jsonify({"error":str(e)}), 500     


                                         #UPDATE A FRIEND
                                                          
@app.route("/api/friends/<int:id>", methods=['PATCH'])
def update_friend(id):
    try:
        friend = friend.query.get(id)                   # Varaible name 'FRIEND' did not disturb here 
        if friend is None:
            return jsonify({"error":"Friends Not Found"}), 404
        
        data = request.get_json()                           
                                                            #Now remember In the approach below, you're using data.get("field", default_value), which simplifies the logic by allowing you to update only the fields that are provided, while keeping the existing values if a field is not included in the request.
        friend.name = data.get("name", friend.name)          
        friend.role = data.get("role", friend.role)
        friend.description = data.get("description", friend.description)
        friend.gender = data.get("gender", friend.gender)

        db.session.commit()
        
        return jsonify(friend.to_json()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error":str(e)}), 500
                        
         

        

