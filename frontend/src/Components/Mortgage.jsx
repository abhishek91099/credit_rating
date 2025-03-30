
    import React, { useState, useEffect } from 'react';
    import axios from 'axios'; // You'll need to install axios: npm install axios

    const MortgageInputForm = () => {
    const [mortgages, setMortgages] = useState([]);
    const [currentMortgage, setCurrentMortgage] = useState({
        creditScore: '',
        loanAmount: '',
        propertyValue: '',
        annualIncome: '',
        debtAmount: '',
        loanType: 'fixed',
        propertyType: 'single_family',
        creditRating: ''
    });
    const [errors, setErrors] = useState({});
    const [editIndex, setEditIndex] = useState(null);
    const [loading, setLoading] = useState(false);
    const [submitMessage, setSubmitMessage] = useState('');

    // Fetch mortgages from backend on component mount
    useEffect(() => {
        fetchMortgages();
    }, []);

    const fetchMortgages = async () => {
        try {
        setLoading(true);
        const response = await axios.get('http://127.0.0.1:5000/api/mortgages');
        setMortgages(response.data);
        console.log(response.data,'HERE')
        setLoading(false);
        } catch (error) {
        console.error('Error fetching mortgages:', error);
        setLoading(false);
        }
    };

    const validateMortgage = (mortgage) => {
        const newErrors = {};
        
        if (!mortgage.creditScore || mortgage.creditScore < 300 || mortgage.creditScore > 850) {
        newErrors.creditScore = 'Credit score must be between 300 and 850';
        }
        
        if (!mortgage.loanAmount || parseFloat(mortgage.loanAmount) <= 0) {
        newErrors.loanAmount = 'Loan amount must be a positive number';
        }
        
        if (!mortgage.propertyValue || parseFloat(mortgage.propertyValue) <= 0) {
        newErrors.propertyValue = 'Property value must be a positive number';
        }
        
        if (!mortgage.annualIncome || parseFloat(mortgage.annualIncome) <= 0) {
        newErrors.annualIncome = 'Annual income must be a positive number';
        }
        
        if (!mortgage.debtAmount || parseFloat(mortgage.debtAmount) < 0) {
        newErrors.debtAmount = 'Debt amount must be a non-negative number';
        }
        
        return newErrors;
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setCurrentMortgage({
        ...currentMortgage,
        [name]: value
        });
    };

    const handleEdit = (mortgage) => {
        setCurrentMortgage(mortgage);
        setEditIndex(mortgage.id);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setSubmitMessage('');
        
        const newErrors = validateMortgage(currentMortgage);
        
        if (Object.keys(newErrors).length > 0) {
        setErrors(newErrors);
        return;
        }
        
        // Format the mortgage data
        const formattedMortgage = {
        ...currentMortgage,
        creditScore: parseInt(currentMortgage.creditScore),
        loanAmount: parseFloat(currentMortgage.loanAmount),
        propertyValue: parseFloat(currentMortgage.propertyValue),
        annualIncome: parseFloat(currentMortgage.annualIncome),
        debtAmount: parseFloat(currentMortgage.debtAmount)
        };
        
        try {
        setLoading(true);
        
        if (editIndex !== null) {
            // Update existing mortgage
            const response = await axios.put(`http://127.0.0.1:5000/api/mortgages/${editIndex}`, formattedMortgage);
            setSubmitMessage(`Mortgage updated successfully! Credit Rating: ${response.data.creditRating}`);
        } else {
            // Add new mortgage
            const response = await axios.post('http://127.0.0.1:5000/api/mortgages', formattedMortgage);
            setSubmitMessage(`Mortgage added successfully! Credit Rating: ${response.data.creditRating}`);
        }
        
        // Refresh the mortgage list
        fetchMortgages();
        
        // Reset form
        setCurrentMortgage({
            creditScore: '',
            loanAmount: '',
            propertyValue: '',
            annualIncome: '',
            debtAmount: '',
            loanType: 'fixed',
            propertyType: 'single_family',
            creditRating: ''
        });
        setEditIndex(null);
        setErrors({});
        setLoading(false);
        } catch (error) {
        console.error('Error submitting mortgage:', error);
        setSubmitMessage('Error submitting mortgage. Please try again.');
        setLoading(false);
        }
    };

    const handleDelete = async (id) => {
        if (window.confirm('Are you sure you want to delete this mortgage?')) {
        try {
            setLoading(true);
            await axios.delete(`http://127.0.0.1:5000/api/mortgages/${id}`);
            fetchMortgages();
            setLoading(false);
        } catch (error) {
            console.error('Error deleting mortgage:', error);
            setLoading(false);
        }
        }
    };

    const handleCancelEdit = () => {
        setCurrentMortgage({
        creditScore: '',
        loanAmount: '',
        propertyValue: '',
        annualIncome: '',
        debtAmount: '',
        loanType: 'fixed',
        propertyType: 'single_family',
        creditRating: ''
        });
        setEditIndex(null);
        setErrors({});
    };

    return (
        <div style={{ maxWidth: '1000px', margin: '0 auto', padding: '20px' }}>
        {loading && (
            <div style={{ 
            padding: '10px', 
            backgroundColor: '#f3f4f6', 
            textAlign: 'center',
            marginBottom: '20px',
            borderRadius: '4px'
            }}>
            Loading...
            </div>
        )}
        
        {submitMessage && (
            <div style={{ 
            padding: '10px', 
            backgroundColor: '#d1fae5', 
            color: '#065f46',
            marginBottom: '20px',
            borderRadius: '4px'
            }}>
            {submitMessage}
            </div>
        )}
        
        <div style={{ 
            marginBottom: '30px', 
            border: '1px solid #e0e0e0', 
            borderRadius: '8px',
            padding: '20px',
            boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
        }}>
            <h2 style={{ marginBottom: '20px', fontSize: '1.5rem', fontWeight: 'bold' }}>
            {editIndex !== null ? 'Edit Mortgage' : 'Add New Mortgage'}
            </h2>
            <form onSubmit={handleSubmit}>
            <div style={{ 
                display: 'grid', 
                gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', 
                gap: '16px',
                marginBottom: '20px'
            }}>
                <div>
                <label style={{ display: 'block', marginBottom: '6px', fontWeight: '500' }}>
                    Credit Score (300-850)
                </label>
                <input
                    type="number"
                    name="creditScore"
                    value={currentMortgage.creditScore}
                    onChange={handleChange}
                    style={{ 
                    width: '100%', 
                    padding: '8px', 
                    border: errors.creditScore ? '1px solid #e53e3e' : '1px solid #d1d5db',
                    borderRadius: '4px'
                    }}
                    min="300"
                    max="850"
                />
                {errors.creditScore && (
                    <p style={{ color: '#e53e3e', fontSize: '0.875rem', marginTop: '4px' }}>{errors.creditScore}</p>
                )}
                </div>

                <div>
                <label style={{ display: 'block', marginBottom: '6px', fontWeight: '500' }}>
                    Loan Amount 
                </label>
                <input
                    type="number"
                    name="loanAmount"
                    value={currentMortgage.loanAmount}
                    onChange={handleChange}
                    style={{ 
                    width: '100%', 
                    padding: '8px', 
                    border: errors.loanAmount ? '1px solid #e53e3e' : '1px solid #d1d5db',
                    borderRadius: '4px'
                    }}
                    min="0"
                    step="1"
                />
                {errors.loanAmount && (
                    <p style={{ color: '#e53e3e', fontSize: '0.875rem', marginTop: '4px' }}>{errors.loanAmount}</p>
                )}
                </div>

                <div>
                <label style={{ display: 'block', marginBottom: '6px', fontWeight: '500' }}>
                    Property Value 
                </label>
                <input
                    type="number"
                    name="propertyValue"
                    value={currentMortgage.propertyValue}
                    onChange={handleChange}
                    style={{ 
                    width: '100%', 
                    padding: '8px', 
                    border: errors.propertyValue ? '1px solid #e53e3e' : '1px solid #d1d5db',
                    borderRadius: '4px'
                    }}
                    min="0"
                    step="1"
                />
                {errors.propertyValue && (
                    <p style={{ color: '#e53e3e', fontSize: '0.875rem', marginTop: '4px' }}>{errors.propertyValue}</p>
                )}
                </div>

                <div>
                <label style={{ display: 'block', marginBottom: '6px', fontWeight: '500' }}>
                    Annual Income 
                </label>
                <input
                    type="number"
                    name="annualIncome"
                    value={currentMortgage.annualIncome}
                    onChange={handleChange}
                    style={{ 
                    width: '100%', 
                    padding: '8px', 
                    border: errors.annualIncome ? '1px solid #e53e3e' : '1px solid #d1d5db',
                    borderRadius: '4px'
                    }}
                    min="0"
                    step="1"
                />
                {errors.annualIncome && (
                    <p style={{ color: '#e53e3e', fontSize: '0.875rem', marginTop: '4px' }}>{errors.annualIncome}</p>
                )}
                </div>

                <div>
                <label style={{ display: 'block', marginBottom: '6px', fontWeight: '500' }}>
                    Debt Amount 
                </label>
                <input
                    type="number"
                    name="debtAmount"
                    value={currentMortgage.debtAmount}
                    onChange={handleChange}
                    style={{ 
                    width: '100%', 
                    padding: '8px', 
                    border: errors.debtAmount ? '1px solid #e53e3e' : '1px solid #d1d5db',
                    borderRadius: '4px'
                    }}
                    min="0"
                    step="1"
                />
                {errors.debtAmount && (
                    <p style={{ color: '#e53e3e', fontSize: '0.875rem', marginTop: '4px' }}>{errors.debtAmount}</p>
                )}
                </div>

                <div>
                <label style={{ display: 'block', marginBottom: '6px', fontWeight: '500' }}>
                    Loan Type
                </label>
                <select
                    name="loanType"
                    value={currentMortgage.loanType}
                    onChange={handleChange}
                    style={{ 
                    width: '100%', 
                    padding: '8px', 
                    border: '1px solid #d1d5db',
                    borderRadius: '4px'
                    }}
                >
                    <option value="fixed">Fixed</option>
                    <option value="adjustable">Adjustable</option>
                </select>
                </div>

                <div>
                <label style={{ display: 'block', marginBottom: '6px', fontWeight: '500' }}>
                    Property Type
                </label>
                <select
                    name="propertyType"
                    value={currentMortgage.propertyType}
                    onChange={handleChange}
                    style={{ 
                    width: '100%', 
                    padding: '8px', 
                    border: '1px solid #d1d5db',
                    borderRadius: '4px'
                    }}
                >
                    <option value="single_family">Single Family</option>
                    <option value="condo">Condo</option>
                </select>
                </div>
            </div>

            <div style={{ display: 'flex', gap: '10px' }}>
                <button
                type="submit"
                disabled={loading}
                style={{ 
                    padding: '8px 16px', 
                    backgroundColor: '#2563eb', 
                    color: 'white', 
                    border: 'none',
                    borderRadius: '4px',
                    cursor: loading ? 'not-allowed' : 'pointer',
                    opacity: loading ? 0.7 : 1
                }}
                >
                {editIndex !== null ? 'Update Mortgage' : 'Add Mortgage'}
                </button>
                
                {editIndex !== null && (
                <button
                    type="button"
                    onClick={handleCancelEdit}
                    disabled={loading}
                    style={{ 
                    padding: '8px 16px', 
                    backgroundColor: '#6b7280', 
                    color: 'white', 
                    border: 'none',
                    borderRadius: '4px',
                    cursor: loading ? 'not-allowed' : 'pointer',
                    opacity: loading ? 0.7 : 1
                    }}
                >
                    Cancel
                </button>
                )}
            </div>
            </form>
        </div>

        {mortgages.length > 0 && (
            <div style={{ 
            border: '1px solid #e0e0e0', 
            borderRadius: '8px',
            padding: '20px',
            boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
            }}>
            <h2 style={{ marginBottom: '20px', fontSize: '1.5rem', fontWeight: 'bold' }}>
                Mortgage List ({mortgages.length})
            </h2>
            <div style={{ overflowX: 'auto' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead>
                    <tr style={{ backgroundColor: '#f3f4f6' }}>
                    <th style={{ border: '1px solid #e5e7eb', padding: '8px', textAlign: 'left' }}>Credit Score</th>
                    <th style={{ border: '1px solid #e5e7eb', padding: '8px', textAlign: 'left' }}>Loan Amount</th>
                    <th style={{ border: '1px solid #e5e7eb', padding: '8px', textAlign: 'left' }}>Property Value</th>
                    <th style={{ border: '1px solid #e5e7eb', padding: '8px', textAlign: 'left' }}>Annual Income</th>
                    <th style={{ border: '1px solid #e5e7eb', padding: '8px', textAlign: 'left' }}>Debt Amount</th>
                    <th style={{ border: '1px solid #e5e7eb', padding: '8px', textAlign: 'left' }}>Loan Type</th>
                    <th style={{ border: '1px solid #e5e7eb', padding: '8px', textAlign: 'left' }}>Property Type</th>
                    <th style={{ border: '1px solid #e5e7eb', padding: '8px', textAlign: 'left' }}>Credit Rating</th>
                    <th style={{ border: '1px solid #e5e7eb', padding: '8px', textAlign: 'left' }}>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {mortgages.map((mortgage) => (
                    <tr key={mortgage.id} style={{ ':hover': { backgroundColor: '#f9fafb' } }}>
                        <td style={{ border: '1px solid #e5e7eb', padding: '8px' }}>{mortgage.creditScore}</td>
                        <td style={{ border: '1px solid #e5e7eb', padding: '8px' }}>
                        ${mortgage.loanAmount.toLocaleString()}
                        </td>
                        <td style={{ border: '1px solid #e5e7eb', padding: '8px' }}>
                        ${mortgage.propertyValue.toLocaleString()}    
                        </td>
                        <td style={{ border: '1px solid #e5e7eb', padding: '8px' }}>
                        ${mortgage.annualIncome.toLocaleString()}
                        </td>
                        <td style={{ border: '1px solid #e5e7eb', padding: '8px' }}>
                        ${mortgage.debtAmount.toLocaleString()}
                        </td>
                        <td style={{ border: '1px solid #e5e7eb', padding: '8px' }}>
                        {mortgage.loanType === 'fixed' ? 'Fixed' : 'Adjustable'}
                        </td>
                        <td style={{ border: '1px solid #e5e7eb', padding: '8px' }}>
                        {mortgage.propertyType === 'single_family' ? 'Single Family' : 'Condo'}
                        </td>
                        {/* <td style={{ 
                        border: '1px solid #e5e7eb', 
                        padding: '8px',
                        fontWeight: 'bold',
                        color: mortgage.creditRating === 'AAA' ? '#047857' : 
                                mortgage.creditRating === 'BBB' ? '#b45309' : '#dc2626'
                        }}>
                        {mortgage.creditRating}
                        </td> */}
                        <td style={{ 
                        border: '1px solid #e5e7eb', 
                        padding: '8px', 
                        display: 'flex', 
                        gap: '4px' 
                        }}>
                        <button
                            onClick={() => handleEdit(mortgage)}
                            disabled={loading || editIndex !== null}
                            style={{ 
                            padding: '4px 8px', 
                            backgroundColor: '#3b82f6', 
                            color: 'white', 
                            border: 'none',
                            borderRadius: '4px',
                            fontSize: '0.875rem',
                            cursor: (loading || editIndex !== null) ? 'not-allowed' : 'pointer',
                            opacity: (loading || editIndex !== null) ? 0.7 : 1
                            }}
                        >
                            Edit
                        </button>
                        <button
                            onClick={() => handleDelete(mortgage.id)}
                            disabled={loading || editIndex !== null}
                            style={{ 
                            padding: '4px 8px', 
                            backgroundColor: '#dc2626', 
                            color: 'white', 
                            border: 'none',
                            borderRadius: '4px',
                            fontSize: '0.875rem',
                            cursor: (loading || editIndex !== null) ? 'not-allowed' : 'pointer',
                            opacity: (loading || editIndex !== null) ? 0.7 : 1
                            }}
                        >
                            Delete
                        </button>
                        </td>
                    </tr>
                    ))}
                </tbody>
                </table>
            </div>
            </div>
        )}
        </div>
    );
    };

    export default MortgageInputForm;