from flask import Flask, request, jsonify
from flask_mail import Mail
from config import Config
from utils import generate_otp, send_otp
from models.user import User
from models.otp import OTP

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Flask-Mail
mail = Mail(app)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify if the server is running."""
    return jsonify({"status": "UP", "message": "Server is running"}), 200

@app.route('/send_otp', methods=['POST'])
def send_otp_to_user():
    data = request.json
    email = data.get('email')
    if not email:
        return jsonify({"error": "Email is required"}), 400

    user = User.get_by_email(email)

    if not user:
        user_id = User.create(email)
    else:
        user_id = user["id"]

    # Generate OTP
    otp = generate_otp()

    # Store OTP in the database
    OTP.create(user_id=user_id, otp=otp)

    # Send OTP via email
    try:
        send_otp(email, otp, mail)
    except Exception as e:
        return jsonify({"error": f"Failed to send OTP: {e}"}), 500

    return jsonify({
        "message": "OTP sent successfully",
        "user_id": user_id
    })

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    data = request.json
    email = data.get('email')
    otp = data.get('otp')

    user = User.get_by_email(email)
    if not user:
        return jsonify({"error": "User not found"}), 404

    latest_otp = OTP.get_latest_by_user_id(user_id=user["id"])
    if not latest_otp or latest_otp["otp"] != otp:
        return jsonify({"error": "Invalid or expired OTP"}), 400
    
    OTP.delete(latest_otp["id"])

    return jsonify({"message": "OTP verified successfully"})

if __name__ == '__main__':
    app.run(debug=True)
