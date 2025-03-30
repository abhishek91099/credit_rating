from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Mortgage
from credit_ratings import *
from logger import setup_logger
import Config as config

# Set up logger for this module
logger = setup_logger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS

# Configure the app
app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS

# Initialize the database
db.init_app(app)

@app.route('/api/mortgages', methods=['POST'])
def create_mortgage():
    """Create a new mortgage entry and calculate its credit rating"""
    try:
        data = request.json
        logger.info(f"Received request to create mortgage: {data}")
        
        # Validate required fields
        required_fields = ['creditScore', 'loanAmount', 'propertyValue', 'annualIncome', 'debtAmount', 'loanType', 'propertyType']
        for field in required_fields:
            if field not in data:
                logger.error(f"Missing required field: {field}")
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Calculate average credit score from all existing mortgages
        all_mortgages = Mortgage.query.all()
        if all_mortgages:
            avg_credit_score = sum(m.credit_score for m in all_mortgages) / len(all_mortgages)
        else:
            avg_credit_score = data.get('creditScore')
        
        logger.info(f"Average credit score for calculation: {avg_credit_score}")
        
        # Calculate risk score and credit rating
        risk_score = calculate_risk_score(data, avg_credit_score)
        credit_rating = calculate_credit_rating(risk_score)
        
        # Create new mortgage record
        new_mortgage = Mortgage(
            credit_score=data.get('creditScore'),
            loan_amount=data.get('loanAmount'),
            property_value=data.get('propertyValue'),
            annual_income=data.get('annualIncome'),
            debt_amount=data.get('debtAmount'),
            loan_type=data.get('loanType'),
            property_type=data.get('propertyType'),
            # credit_rating=credit_rating,
            # risk_score=risk_score
        )
        
        # Save to database
        db.session.add(new_mortgage)
        db.session.commit()
        logger.info(f"Created new mortgage with ID {new_mortgage.id} and credit rating {credit_rating}")
        
        # Return the created mortgage with its credit rating
        return jsonify({
            "message": "Mortgage created successfully",
            "mortgage": new_mortgage.to_dict(),
            "creditRating": credit_rating
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating mortgage: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/mortgages', methods=['GET'])
def get_mortgages():
    """Retrieve all mortgages from the database"""
    try:
        logger.info("Received request to get all mortgages")
        mortgages = Mortgage.query.all()
        logger.info(f"Retrieved {len(mortgages)} mortgages")
        return jsonify([mortgage.to_dict() for mortgage in mortgages]), 200
    except Exception as e:
        logger.error(f"Error retrieving mortgages: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/mortgages/<int:id>', methods=['GET'])
def get_mortgage(id):
    """Retrieve a single mortgage by ID"""
    try:
        logger.info(f"Received request to get mortgage with ID {id}")
        mortgage = Mortgage.query.get(id)
        if not mortgage:
            logger.warning(f"Mortgage with ID {id} not found")
            return jsonify({"error": "Mortgage not found"}), 404
        logger.info(f"Retrieved mortgage with ID {id}")
        return jsonify(mortgage.to_dict()), 200
    except Exception as e:
        logger.error(f"Error retrieving mortgage: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/mortgages/<int:id>', methods=['PUT'])
def update_mortgage(id):
    """Update an existing mortgage"""
    try:
        logger.info(f"Received request to update mortgage with ID {id}")
        mortgage = Mortgage.query.get(id)
        if not mortgage:
            logger.warning(f"Mortgage with ID {id} not found")
            return jsonify({"error": "Mortgage not found"}), 404
        
        data = request.json
        logger.info(f"Update data: {data}")
        
        # Calculate average credit score (excluding this mortgage)
        all_mortgages = Mortgage.query.filter(Mortgage.id != id).all()
        if all_mortgages:
            avg_credit_score = sum(m.credit_score for m in all_mortgages) / len(all_mortgages)
        else:
            avg_credit_score = data.get('creditScore')
        
        logger.info(f"Average credit score for calculation: {avg_credit_score}")
        
        # Calculate new risk score and credit rating
        risk_score = calculate_risk_score(data, avg_credit_score)
        credit_rating = calculate_credit_rating(risk_score)
        
        # Update mortgage fields
        mortgage.credit_score = data.get('creditScore', mortgage.credit_score)
        mortgage.loan_amount = data.get('loanAmount', mortgage.loan_amount)
        mortgage.property_value = data.get('propertyValue', mortgage.property_value)
        mortgage.annual_income = data.get('annualIncome', mortgage.annual_income)
        mortgage.debt_amount = data.get('debtAmount', mortgage.debt_amount)
        mortgage.loan_type = data.get('loanType', mortgage.loan_type)
        mortgage.property_type = data.get('propertyType', mortgage.property_type)
        
        db.session.commit()
        logger.info(f"Updated mortgage with ID {id}")
        
        return jsonify({
            "message": "Mortgage updated successfully",
            "mortgage": mortgage.to_dict(),
            "creditRating": credit_rating
        }), 200
    except Exception as e:
        logger.error(f"Error updating mortgage: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/mortgages/<int:id>', methods=['DELETE'])
def delete_mortgage(id):
    """Delete a mortgage by ID"""
    try:
        logger.info(f"Received request to delete mortgage with ID {id}")
        mortgage = Mortgage.query.get(id)
        if not mortgage:
            logger.warning(f"Mortgage with ID {id} not found")
            return jsonify({"error": "Mortgage not found"}), 404
        
        db.session.delete(mortgage)
        db.session.commit()
        logger.info(f"Deleted mortgage with ID {id}")
        
        return jsonify({"message": "Mortgage deleted successfully"}), 200
    except Exception as e:
        logger.error(f"Error deleting mortgage: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/calculate-rating', methods=['POST'])
def calculate_rating():
    """Calculate credit rating without saving to database"""
    try:
        data = request.json
        logger.info(f"Received request to calculate rating: {data}")
        
        # Calculate average credit score from all existing mortgages
        all_mortgages = Mortgage.query.all()
        if all_mortgages:
            avg_credit_score = sum(m.credit_score for m in all_mortgages) / len(all_mortgages)
        else:
            avg_credit_score = data.get('creditScore')
        
        # Calculate risk score and credit rating
        risk_score = calculate_risk_score(data, avg_credit_score)
        credit_rating = calculate_credit_rating(risk_score)
        
        logger.info(f"Calculated credit rating: {credit_rating} with risk score: {risk_score}")
        
        return jsonify({
            "creditRating": credit_rating,
            "riskScore": risk_score,
            "components": {
                "loanToValue": loan_to_value(float(data.get('loanAmount', 0)), float(data.get('propertyValue', 0))),
                "debtToIncome": debt_to_income(float(data.get('debtAmount', 0)), float(data.get('annualIncome', 0))),
                "creditScore": credit_score_check(int(data.get('creditScore', 0))),
                "loanType": loan_type_process(data.get('loanType', 'fixed')),
                "propertyType": property_type_process(data.get('propertyType', 'single_family')),
                "avgCreditScore": average_credit_process(avg_credit_score)
            }
        }), 200
    except Exception as e:
        logger.error(f"Error calculating rating: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist
        logger.info("Database tables created")
    
    logger.info("Starting Flask application")
    app.run(debug=True)