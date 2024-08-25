from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)

# GET route for returning operation_code
@app.route('/bfhl', methods=['GET'])
def get_operation_code():
    return jsonify({"operation_code": 1}), 200

# POST route for processing JSON input
@app.route('/bfhl', methods=['POST'])
def handle_bfhl_post():
    # Initialize response values
    user_id = "lavanya_v_16092003"  # Replace with your actual user ID
    email = "lavanyavijayan2017@gmail.com"         # Replace with your actual email
    roll_number = "21BPS1141"         # Replace with your actual roll number

    # Default response data
    response_data = {
        "is_success": False,
        "user_id": user_id,
        "email": email,
        "roll_number": roll_number,
        "numbers": [],
        "alphabets": [],
        "highest_lowercase_alphabet": []
    }
    
    # Get JSON data from the form
    json_data = request.form.get('json_data')
    display_choice = request.form.get('select', 'none')
    
    if json_data:
        try:
            # Enclose the data in curly braces if not already present
            if not json_data.startswith('{'):
                json_data = '{' + json_data + '}'
            
            # Parse JSON data
            data = json.loads(json_data)
            if "data" in data:
                data = data["data"]
                
                # Separate numbers and alphabets
                numbers = [item for item in data if item.isdigit()]
                alphabets = [item for item in data if item.isalpha()]
                
                # Find the highest lowercase alphabet
                highest_lowercase = max([ch for ch in data if ch.islower()], default="")
                
                # Prepare the response data
                response_data = {
                    "is_success": True,
                    "user_id": user_id,
                    "email": email,
                    "roll_number": roll_number,
                    "numbers": numbers,
                    "alphabets": alphabets,
                    "highest_lowercase_alphabet": [highest_lowercase] if highest_lowercase else []
                }
        except json.JSONDecodeError:
            # Handle invalid JSON
            response_data = {
                "is_success": False,
                "user_id": user_id,
                "email": email,
                "roll_number": roll_number,
                "numbers": [],
                "alphabets": [],
                "highest_lowercase_alphabet": []
            }

    # Filter response data based on display_choice
    if display_choice == 'Alphabets':
        filtered_data = {
            "numbers": [],
            "alphabets": response_data["alphabets"],
            "highest_lowercase_alphabet": []
        }
    elif display_choice == 'Numbers':
        filtered_data = {
            "numbers": response_data["numbers"],
            "alphabets": [],
            "highest_lowercase_alphabet": []
        }
    elif display_choice == 'Highest lowercase alphabet':
        filtered_data = {
            "numbers": response_data["numbers"],
            "alphabets": response_data["alphabets"],
            "highest_lowercase_alphabet": response_data["highest_lowercase_alphabet"]
        }
    else:
        filtered_data = response_data

    return render_template('index.html', response_data=filtered_data, json_data=json_data)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
