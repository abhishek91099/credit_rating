from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Mortgage(db.Model):
    __tablename__ = "mortgages"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    credit_score = db.Column(db.Integer, nullable=False)
    loan_amount = db.Column(db.Float, nullable=False)
    property_value = db.Column(db.Float, nullable=False)
    annual_income = db.Column(db.Float, nullable=False)
    debt_amount = db.Column(db.Float, nullable=False)
    loan_type = db.Column(db.String(10), nullable=False)  # 'fixed' or 'adjustable'
    property_type = db.Column(db.String(20), nullable=False)  # 'single_family' or 'condo'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert Mortgage object to dictionary"""
        return {
            'id': self.id,
            'creditScore': self.credit_score,
            'loanAmount': self.loan_amount,
            'propertyValue': self.property_value,
            'annualIncome': self.annual_income,
            'debtAmount': self.debt_amount,
            'loanType': self.loan_type,
            'propertyType': self.property_type,
            'createdAt': self.created_at.isoformat()
        }