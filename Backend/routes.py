from app import app, db
from flask import request, jsonify
from models import friend

#Get all friends
@app.route("/api/friends", method=['GET'])
def get_friends():
    friends = friend.query.all()
    result = [friend.to_json() for friend in friends]
    return jsonify(result), 200          #BY DEFAULT, IT IS 200    

#create A Friend
@app.route("/api/friends", method=['POST'])
def create_friend():
    try:
        data = request.jason

        name = data.get("name")
        role = data.get("role")
        description = data.get("description")                  #16618968911760
        gender = data.get("gender")
        name = data.get("name")
       

        #fetch Avater image base on gender 
        if gender == "male":
           img_url = f"https://avatar.iran.liara.run/public/boy?username={name}" 
        elif gender == "female":
            img_url = f"https://avatar.iran.liara.run/public/girl?username={name}"
        else:
            img_url = None
            
        new_friend = friend(name=name, role=role, description=description, gender=gender, img_url=img_url)

        db.session.add(new_friend)
        db.session.commit()
        
        return jsonify({"msg: Friend created successfully!"}), 201   #jsonify(new_friend.to_jason)
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error":str(e)}), 500

                        
         

        

