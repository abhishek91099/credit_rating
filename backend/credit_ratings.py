from logger import setup_logger

# Set up logger for this module
logger = setup_logger(__name__)

def loan_to_value(loan_amount, property_value):
    """Calculate risk score based on loan-to-value ratio"""
    try:
        ltv = (loan_amount / property_value) * 100
        logger.info(f"Calculated LTV: {ltv:.2f}%")
        
        if ltv > 90:
            logger.info("LTV > 90%: Adding 2 points to risk score")
            return 2
        elif ltv > 80:
            logger.info("LTV > 80%: Adding 1 point to risk score")
            return 1
        else:
            logger.info("LTV <= 80%: No points added to risk score")
            return 0
    except ZeroDivisionError:
        logger.error("Property value cannot be zero when calculating LTV")
        return 2  # Assign maximum risk if property value is zero

def debt_to_income(debt_amount, annual_income):
    """Calculate risk score based on debt-to-income ratio"""
    try:
        dti = (debt_amount / annual_income) * 100
        logger.info(f"Calculated DTI: {dti:.2f}%")
        
        if dti > 50:
            logger.info("DTI > 50%: Adding 2 points to risk score")
            return 2
        elif dti > 40:
            logger.info("DTI > 40%: Adding 1 point to risk score")
            return 1
        else:
            logger.info("DTI <= 40%: No points added to risk score")
            return 0
    except ZeroDivisionError:
        logger.error("Annual income cannot be zero when calculating DTI")
        return 2  # Assign maximum risk if annual income is zero

def credit_score_check(credit_score):
    """Calculate risk score based on credit score"""
    if credit_score >= 700:
        logger.info("Credit score >= 700: Subtracting 1 point from risk score")
        return -1
    elif credit_score >= 650:
        logger.info("650 <= Credit score < 700: No change to risk score")
        return 0
    else:
        logger.info("Credit score < 650: Adding 1 point to risk score")
        return 1

def loan_type_process(loan_type):
    """Calculate risk score based on loan type"""
    if loan_type == 'fixed':
        logger.info("Fixed-rate loan: Subtracting 1 point from risk score")
        return -1
    else:  # 'adjustable'
        logger.info("Adjustable-rate loan: Adding 1 point to risk score")
        return 1

def property_type_process(property_type):
    """Calculate risk score based on property type"""
    if property_type == 'single_family':
        logger.info("Single-family home: No change to risk score")
        return 0
    else:  # 'condo'
        logger.info("Condo: Adding 1 point to risk score")
        return 1

def average_credit_process(avg_credit_score):
    """Calculate risk score adjustment based on average credit score"""
    if avg_credit_score >= 700:
        logger.info("Average credit score >= 700: Subtracting 1 point from risk score")
        return -1
    elif avg_credit_score < 650:
        logger.info("Average credit score < 650: Adding 1 point to risk score")
        return 1
    else:
        logger.info("650 <= Average credit score < 700: No change to risk score")
        return 0

def calculate_credit_rating(risk_score):
    """Determine credit rating based on risk score"""
    if risk_score <= 2:
        logger.info(f"Risk score {risk_score} <= 2: Assigning AAA rating")
        return "AAA"
    elif risk_score <= 5:
        logger.info(f"Risk score 3 <= {risk_score} <= 5: Assigning BBB rating")
        return "BBB"
    else:
        logger.info(f"Risk score {risk_score} > 5: Assigning C rating")
        return "C"

def calculate_risk_score(data, avg_credit_score=None):
    """Calculate the total risk score for a mortgage"""
    logger.info("Starting risk score calculation")
    
    # Extract data
    loan_amount = float(data.get('loanAmount', 0))
    property_value = float(data.get('propertyValue', 0))
    credit_score = int(data.get('creditScore', 0))
    annual_income = float(data.get('annualIncome', 0))
    debt_amount = float(data.get('debtAmount', 0))
    loan_type = data.get('loanType', 'fixed')
    property_type = data.get('propertyType', 'single_family')
    
    # Use the provided credit score as average if not specified
    if avg_credit_score is None:
        avg_credit_score = credit_score
    
    # Calculate individual risk scores
    ltv_score = loan_to_value(loan_amount, property_value)
    dti_score = debt_to_income(debt_amount, annual_income)
    credit_score_adjustment = credit_score_check(credit_score)
    loan_type_adjustment = loan_type_process(loan_type)
    property_type_adjustment = property_type_process(property_type)
    avg_credit_adjustment = average_credit_process(avg_credit_score)
    
    # Calculate total risk score
    total_score = ltv_score + dti_score + credit_score_adjustment + loan_type_adjustment + property_type_adjustment + avg_credit_adjustment
    
    logger.info(f"Risk score components: LTV={ltv_score}, DTI={dti_score}, Credit={credit_score_adjustment}, "
                f"Loan={loan_type_adjustment}, Property={property_type_adjustment}, AvgCredit={avg_credit_adjustment}")
    logger.info(f"Total risk score: {total_score}")
    
    return total_score