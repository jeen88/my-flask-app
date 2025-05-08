from flask import Flask, render_template, request, redirect, url_for
import math

app = Flask(__name__)

# ---------- Coefficients ----------

districts = [
    "Coimbatore", "Cuddalore", "Dharmapuri", "Dindigul", "Erode", "Kancheepuram", "Kanniyakumari", "Karur", "Krishnagiri", "Madurai",
    "Nagapattinam", "Namakkal", "Perambalur", "Pudukkottai", "Ramanathapuram", "Salem", "Sivagangai", "Thanjavur", "The Nilgiris", "Theni",
    "Thiruvallur", "Thiruvarur", "Thoothukudi", "Tiruchirappalli", "Tirunelveli", "Tiruppur", "Tiruvannamalai", "Vellore", "Villupuram", "Virudhunagar"
]

facility_options = ["primary", "Secondary", "tertiary", "missing"]


# -------------------------------MODEL 1 CALCULATOR- NIKSHAY VARIABLES------------------------------------
# Model1 early death
intercept_model1early = -4.64
age_model1early =  0.03
gender_model1early = {'Female': 0, 'Male': 0.21, 'Transgender': -11.16}
district_model1early = { 'Coimbatore': 0, 'Cuddalore': -0.30, 'Dharmapuri': -0.11, 'Dindigul': -0.83,
    'Erode': 0.15, 'Kancheepuram': -0.77, 'Kanniyakumari': 0.16, 'Karur': -0.28,
    'Krishnagiri': -0.04, 'Madurai': -0.08, 'Nagapattinam': -0.17, 'Namakkal': -0.43,
    'Perambalur': -1.43, 'Pudukkottai': -0.21, 'Ramanathapuram': -0.91, 'Salem': -0.12,
    'Sivagangai': -0.66, 'Thanjavur': 0.08, 'The Nilgiris': -0.50, 'Theni': -0.68,
    'Thiruvallur': -0.28, 'Thiruvarur': 0.33, 'Thoothukudi': 0.00, 'Tiruchirappalli': -0.03,
    'Tirunelveli': 0.02, 'Tiruppur': -0.24, 'Tiruvannamalai': -0.19, 'Vellore': -0.38,
    'Villupuram': -0.30, 'Virudhunagar': -0.15}
bank_model1early = {'Available': 0, 'Not available': 1.28}
microbio_model1early = {'No': 0, 'Yes': -0.02}
site_model1early = {'Pulmonary': 0, 'Extrapulmonary': -0.10, 'Missing': 0.71}
prev_tb_model1early = {'No': 0, 'Yes': 0.15}
hiv_model1early = {'Negative': 0, 'Unknown': 0.45, 'Positive': 0.85}
facility_model1early = {'Primary': 0, 'Secondary': -0.33, 'Tertiary': -0.61, 'Missing': -11.35}
diabetes_model1early = {'Negative': 0, 'Unknown': -0.07, 'Positive': -0.10}

#-----------
# Model1 total death 

intercept_model1total = -4.12
age_model1total = 0.03
gender_model1total = {'Female': 0, 'Male': 0.20, 'Transgender': -11.58}
district_model1total = { 'Coimbatore': 0, 'Cuddalore': -0.36, 'Dharmapuri': -0.25, 'Dindigul': -0.78,
    'Erode': 0.04, 'Kancheepuram': -0.67, 'Kanniyakumari': -0.01, 'Karur': -0.50,
    'Krishnagiri': 0.07, 'Madurai': -0.05, 'Nagapattinam': -0.22, 'Namakkal': -0.41,
    'Perambalur': -1.14, 'Pudukkottai': -0.24, 'Ramanathapuram': -1.05, 'Salem': -0.23,
    'Sivagangai': -0.90, 'Thanjavur': 0.11, 'The Nilgiris': -0.41, 'Theni': -0.70,
    'Thiruvallur': -0.24, 'Thiruvarur': 0.24, 'Thoothukudi': 0.02, 'Tiruchirappalli': -0.05,
    'Tirunelveli': -0.04, 'Tiruppur': -0.23, 'Tiruvannamalai': -0.28, 'Vellore': -0.38,
    'Villupuram': -0.45, 'Virudhunagar': -0.19}
bank_model1total = {'Available': 0, 'Not available': 1.02}
microbio_model1total = {'No': 0, 'Yes': -0.04}
site_model1total = {'Pulmonary': 0, 'Extrapulmonary': -0.10, 'Missing': 0.71}
prev_tb_model1total = {'No': 0, 'Yes': 0.15}
hiv_model1total = {'Negative': 0, 'Unknown': 0.45, 'Positive': 0.85}
facility_model1total = {'Primary': 0, 'Secondary': -0.33, 'Tertiary': -0.61, 'Missing': -11.35}
diabetes_model1total = {'Negative': 0, 'Unknown': -0.07, 'Positive': -0.10}

#-----------
# Model1 early death (with LTFU)
intercept_model1earlyltfu = -4.12
age_model1earlyltfu =  0.03
gender_model1earlyltfu = {'Female': 0, 'Male': 0.16, 'Transgender': -11.36}
district_model1earlyltfu = { 'Coimbatore': 0, 'Cuddalore': -0.36, 'Dharmapuri': -0.01, 'Dindigul': -0.86,
    'Erode': 0.20, 'Kancheepuram': -0.61, 'Kanniyakumari': 0.09, 'Karur': -0.44,
    'Krishnagiri': 0.00, 'Madurai': -0.15, 'Nagapattinam': -0.28, 'Namakkal': -0.41,
    'Perambalur': -0.93, 'Pudukkottai': -0.22, 'Ramanathapuram': -1.05, 'Salem': -0.06,
    'Sivagangai': -0.70, 'Thanjavur': -0.07, 'The Nilgiris': -0.48, 'Theni': -0.60,
    'Thiruvallur': -0.29, 'Thiruvarur': 0.27, 'Thoothukudi': 0.04, 'Tiruchirappalli': -0.02,
    'Tirunelveli': 0.01, 'Tiruppur': -0.12, 'Tiruvannamalai': 0.01, 'Vellore': -0.25,
    'Villupuram': -0.32, 'Virudhunagar': -0.35}
bank_model1earlyltfu = {'Available': 0, 'Not available': 1.56}
microbio_model1earlyltfu = {'No': 0, 'Yes': -0.04}
site_model1earlyltfu = {'Pulmonary': 0, 'Extrapulmonary': -0.04, 'Missing': 1.12}
prev_tb_model1earlyltfu = {'No': 0, 'Yes': 0.07}
hiv_model1earlyltfu = {'Negative': 0, 'Unknown': 0.05, 'Positive': 0.63}
facility_model1earlyltfu = {'Primary': 0, 'Secondary': -0.33, 'Tertiary': -0.42, 'Missing': -11.27}
diabetes_model1earlyltfu = {'Negative': 0, 'Unknown': 0.12, 'Positive': -0.16}

#-----------
# Model1 total death (with LTFU)

intercept_model1totalltfu = -3.40
age_model1totalltfu = 0.02
gender_model1totalltfu = {'Female': 0, 'Male': 0.27, 'Transgender': -11.84}
district_model1totalltfu = { 'Coimbatore': 0, 'Cuddalore': -0.42, 'Dharmapuri': -0.17, 'Dindigul': -0.90,
    'Erode': -0.01, 'Kancheepuram': -0.66, 'Kanniyakumari': -0.14, 'Karur': -0.83,
    'Krishnagiri': -0.06, 'Madurai': -0.14, 'Nagapattinam': -0.52, 'Namakkal': -0.59,
    'Perambalur': -0.60, 'Pudukkottai': -0.42, 'Ramanathapuram': -1.06, 'Salem': -0.21,
    'Sivagangai': -1.02, 'Thanjavur': -0.06, 'The Nilgiris': -0.32, 'Theni': -0.62,
    'Thiruvallur': -0.46, 'Thiruvarur': 0.08, 'Thoothukudi': -0.01, 'Tiruchirappalli': -0.10,
    'Tirunelveli': -0.03, 'Tiruppur': -0.17, 'Tiruvannamalai': -0.11, 'Vellore': -0.19,
    'Villupuram': -0.51, 'Virudhunagar': -0.41}
bank_model1totalltfu = {'Available': 0, 'Not available': 1.34}
microbio_model1totalltfu = {'No': 0, 'Yes': 0.00}
site_model1totalltfu = {'Pulmonary': 0, 'Extrapulmonary': -0.14, 'Missing': 0.17}
prev_tb_model1totalltfu = {'No': 0, 'Yes': 0.28}
hiv_model1totalltfu = {'Negative': 0, 'Unknown': 0.28, 'Positive': 0.58}
facility_model1totalltfu = {'Primary': 0, 'Secondary': -0.26, 'Tertiary': -0.41, 'Missing': -11.83}
diabetes_model1totalltfu = {'Negative': 0, 'Unknown': -0.03, 'Positive': -0.17}


# -------------------------------MODEL 2 CALCULATOR-TBSEWA VARIABLES------------------------------------
# Early death
intercept_early = -0.13
district_coeffs_early = {"Coimbatore": 0, "Cuddalore": -0.3, "Dharmapuri": -0.04, "Dindigul": -0.52, "Erode": 0.16,
    "Kancheepuram": -0.54, "Kanniyakumari": 0.06, "Karur": -0.08, "Krishnagiri": -0.06, "Madurai": 0.04, "Nagapattinam": -0.23,
    "Namakkal": -0.25, "Perambalur": -1.34, "Pudukkottai": -0.19, "Ramanathapuram": -0.79, "Salem": -0.19, "Sivagangai": -0.83,
    "Thanjavur": 0.03, "The Nilgiris": -0.35, "Theni": -0.57, "Thiruvallur": -0.28, "Thiruvarur": 0.41, "Thoothukudi": 0.1,
    "Tiruchirappalli": 0.1, "Tirunelveli": 0.01, "Tiruppur": -0.52, "Tiruvannamalai": -0.21, "Vellore": -0.7, "Villupuram": -0.29, "Virudhunagar": -0.15}
facility_coeffs_early = {"tertiary": 0, "Secondary": -0.33, "primary": -0.57, "missing": -11.11}

# Overall death
intercept_overall = 0.04
district_coeffs_overall = {"Coimbatore": 0, "Cuddalore": -0.35, "Dharmapuri": -0.18, "Dindigul": -0.53, "Erode": 0.07,
    "Kancheepuram": -0.53, "Kanniyakumari": -0.05, "Karur": -0.30, "Krishnagiri": 0.06, "Madurai": 0.02, "Nagapattinam": -0.29,
    "Namakkal": -0.20, "Perambalur": -1.05, "Pudukkottai": -0.21, "Ramanathapuram": -0.95, "Salem": -0.25, "Sivagangai": -1.03,
    "Thanjavur": 0.09, "The Nilgiris": -0.34, "Theni": -0.59, "Thiruvallur": -0.25, "Thiruvarur": 0.31, "Thoothukudi": 0.12,
    "Tiruchirappalli": 0.04, "Tirunelveli": -0.04, "Tiruppur": -0.43, "Tiruvannamalai": -0.28, "Vellore": -0.64, "Villupuram": -0.44, "Virudhunagar": -0.19}
facility_coeffs_overall = {"primary": 0, "Secondary": -0.27, "tertiary": -0.55, "missing": -11.51}

# Early death (with LTFU)
intercept_ltfu = -0.42
district_coeffs_ltfu = {"Coimbatore": 0, "Cuddalore": -0.38, "Dharmapuri": 0.00, "Dindigul": -0.58, "Erode": 0.20,
    "Kancheepuram": -0.36, "Kanniyakumari": -0.07, "Karur": -0.33, "Krishnagiri": -0.05, "Madurai": -0.01, "Nagapattinam": -0.38,
    "Namakkal": -0.34, "Perambalur": -0.95, "Pudukkottai": -0.29, "Ramanathapuram": -0.95, "Salem": -0.17, "Sivagangai": -0.92,
    "Thanjavur": -0.14, "The Nilgiris": -0.32, "Theni": -0.55, "Thiruvallur": -0.32, "Thiruvarur": 0.29, "Thoothukudi": -0.02,
    "Tiruchirappalli": 0.05, "Tirunelveli": -0.04, "Tiruppur": -0.37, "Tiruvannamalai": -0.04, "Vellore": -0.51, "Villupuram": -0.33, "Virudhunagar": -0.38}
facility_coeffs_ltfu = {"primary": 0, "Secondary": -0.29, "tertiary": -0.42, "missing": -11.47}

# Overall death (with LTFU)
intercept_overall_ltfu = -0.41
district_coeffs_overall_ltfu = {"Coimbatore": 0, "Cuddalore": -0.44, "Dharmapuri": -0.14, "Dindigul": -0.73, "Erode": 0.01,
    "Kancheepuram": -0.63, "Kanniyakumari": -0.23, "Karur": -0.71, "Krishnagiri": -0.11, "Madurai": -0.13, "Nagapattinam": -0.62,
    "Namakkal": -0.49, "Perambalur": -0.60, "Pudukkottai": -0.48, "Ramanathapuram": -1.01, "Salem": -0.25, "Sivagangai": -1.19,
    "Thanjavur": -0.10, "The Nilgiris": -0.33, "Theni": -0.59, "Thiruvallur": -0.51, "Thiruvarur": 0.08, "Thoothukudi": 0.02,
    "Tiruchirappalli": -0.08, "Tirunelveli": -0.05, "Tiruppur": -0.32, "Tiruvannamalai": -0.15, "Vellore": -0.43, "Villupuram": -0.54, "Virudhunagar": -0.47}
facility_coeffs_overall_ltfu = {"primary": 0, "Secondary": -0.21, "tertiary": -0.36, "missing": -11.01}



# ---------- Routes ----------
@app.route('/')
def home():
    return redirect(url_for('model1'))

def calculate_model1_probability(
    intercept, age_coeff, gender_coeffs, district_coeffs, bank_coeffs, microbio_coeffs,
    site_coeffs, prev_tb_coeffs, hiv_coeffs, facility_coeffs, diabetes_coeffs,
    age, gender, district, bank, microbio, site, prev_tb, hiv, facility, diabetes
):
    eta = (
        intercept
        + age_coeff * age
        + gender_coeffs.get(gender, 0)
        + district_coeffs.get(district, 0)
        + bank_coeffs.get(bank, 0)
        + microbio_coeffs.get(microbio, 0)
        + site_coeffs.get(site, 0)
        + prev_tb_coeffs.get(prev_tb, 0)
        + hiv_coeffs.get(hiv, 0)
        + facility_coeffs.get(facility, 0)
        + diabetes_coeffs.get(diabetes, 0)
    )
    prob = math.exp(eta) / (1 + math.exp(eta))
    return round(prob * 100, 2)

@app.route('/model1', methods=['GET', 'POST'])
def model1():
    # Set defaults first
    age = 45
    gender = 'Female'
    district = 'Coimbatore'
    bank = 'Available'
    microbio = 'No'
    site = 'Pulmonary'
    prev_tb = 'No'
    hiv = 'Negative'
    facility = 'Primary'
    diabetes = 'Negative'

    result_early = result_overall = result_ltfu = result_overall_ltfu = None
    if request.method == 'POST':
        age = float(request.form.get('age', age)) 
        gender = request.form.get('gender', 'gender')
        district = request.form.get('district', 'district')
        bank = request.form.get('bank', 'bank')
        microbio = request.form.get('microbio', 'microbio')
        site = request.form.get('site', 'site')
        prev_tb = request.form.get('prev_tb', 'prev_tb')
        hiv = request.form.get('hiv', 'hiv')
        facility = request.form.get('facility', 'facility')
        diabetes = request.form.get('diabetes', 'diabetes')

    result_early = calculate_model1_probability(
            intercept_model1early, age_model1early, gender_model1early, district_model1early,
            bank_model1early, microbio_model1early, site_model1early, prev_tb_model1early,
            hiv_model1early, facility_model1early, diabetes_model1early,
            age, gender, district, bank, microbio, site, prev_tb, hiv, facility, diabetes
        )

    result_overall = calculate_model1_probability(
            intercept_model1total, age_model1total, gender_model1total, district_model1total,
            bank_model1total, microbio_model1total, site_model1total, prev_tb_model1total,
            hiv_model1total, facility_model1total, diabetes_model1total,
            age, gender, district, bank, microbio, site, prev_tb, hiv, facility, diabetes
        )

    result_ltfu = calculate_model1_probability(
            intercept_model1earlyltfu, age_model1earlyltfu, gender_model1earlyltfu, district_model1earlyltfu,
            bank_model1earlyltfu, microbio_model1earlyltfu, site_model1earlyltfu, prev_tb_model1earlyltfu,
            hiv_model1earlyltfu, facility_model1earlyltfu, diabetes_model1earlyltfu,
            age, gender, district, bank, microbio, site, prev_tb, hiv, facility, diabetes
        )

    result_overall_ltfu = calculate_model1_probability(
            intercept_model1totalltfu, age_model1totalltfu, gender_model1totalltfu, district_model1totalltfu,
            bank_model1totalltfu, microbio_model1totalltfu, site_model1totalltfu, prev_tb_model1totalltfu,
            hiv_model1totalltfu, facility_model1totalltfu, diabetes_model1totalltfu,
            age, gender, district, bank, microbio, site, prev_tb, hiv, facility, diabetes
        )

    return render_template(
        'model1.html',
        result_early=result_early,
        result_overall=result_overall,
        result_ltfu=result_ltfu,
        result_overall_ltfu=result_overall_ltfu,
        age=age,
        gender=gender,
        district=district,
        bank=bank,
        microbio=microbio,
        site=site,
        prev_tb=prev_tb,
        hiv=hiv,
        facility=facility,
        diabetes=diabetes,
        districts=districts
    )

# ---------- Calculation Function for Model2----------
def calculate_probability(intercept, district, facility, rr, bmi, spo2, unable_stand, leg_swelling,
                          district_coeffs, facility_coeffs, stand_coeff, leg_coeff,
                          rr_coeff, bmi_coeff, spo2_coeff):
    eta = (
        intercept
        + district_coeffs.get(district, 0)
        + facility_coeffs.get(facility, 0)
        + (rr_coeff * rr)
        + (bmi_coeff * bmi)
        + (spo2_coeff * spo2)
        + (stand_coeff if unable_stand == 'yes' else 0)
        + (leg_coeff if leg_swelling == 'yes' else 0)
    )
    prob = math.exp(eta) / (1 + math.exp(eta))
    return round(prob * 100, 2)

@app.route('/model2', methods=['GET', 'POST'])
def model2():
    # Set defaults
    district = 'Coimbatore'
    facility = 'primary'
    rr = 20
    bmi = 22
    spo2 = 95
    unable_stand = 'no'
    leg_swelling = 'no'
    nikshay_id = '12345678'

    result_early = result_overall = result_ltfu = result_overall_ltfu = None

    if request.method == 'POST':
        district = request.form.get('district', district)
        facility = request.form.get('facility', facility)
        rr = float(request.form.get('respiratory_rate' , rr))
        bmi = float(request.form.get('bmi', bmi))
        spo2 = float(request.form.get('oxygen_saturation', spo2))
        unable_stand = request.form.get('unable_to_stand', unable_stand)
        leg_swelling = request.form.get('leg_swelling', leg_swelling)
        nikshay_id = request.form.get('nikshay_id', nikshay_id)

 
    
    result_early = calculate_probability(intercept_early, district, facility, rr, bmi, spo2, unable_stand, leg_swelling,
                                             district_coeffs_early, facility_coeffs_early, 0.46, 1.55, 0.02, -0.09, -0.01)
    result_overall = calculate_probability(intercept_overall, district, facility, rr, bmi, spo2, unable_stand, leg_swelling,
                                               district_coeffs_overall, facility_coeffs_overall, 1.34, 0.43, 0.02, -0.09, -0.01)
    result_ltfu = calculate_probability(intercept_ltfu, district, facility, rr, bmi, spo2, unable_stand, leg_swelling,
                                            district_coeffs_ltfu, facility_coeffs_ltfu, 1.38, 0.42, 0.02, -0.07, -0.01)
    result_overall_ltfu = calculate_probability(intercept_overall_ltfu, district, facility, rr, bmi, spo2, unable_stand, leg_swelling,
                                                    district_coeffs_overall_ltfu, facility_coeffs_overall_ltfu, 1.11, 0.32, 0.02, -0.07, -0.01)
    
    return render_template('model2.html', districts=districts, facilities=facility_options,
     district=district,
     facility=facility,
     respiratory_rate=rr,
     bmi=bmi,
     oxygen_saturation=spo2,
     unable_stand=unable_stand,
     leg_swelling=leg_swelling,
     nikshay_id=nikshay_id,
     result_early=result_early, result_overall=result_overall,
     result_ltfu=result_ltfu, result_overall_ltfu=result_overall_ltfu)



if __name__ == '__main__':
    app.run(debug=True)
