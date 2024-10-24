import pandas as pd

def get_data_hr_report():
    data = pd.read_excel('src/assets/data_sources/hr_report.xlsx', usecols=["employee_id", "department", "recruitment_channel",  "no_of_trainings",  "previous_year_rating",  "length_of_service", "KPIs_met >80%", "awards_won?",  "avg_training_score"])
    
    new_columns = ["employee_id", "department", "recruitment_channel",  "no_of_trainings",  "previous_year_rating",  "length_of_service", "kpis_met", "awards_won", "avg_training_score"]
    
    data.columns = new_columns
    
    data["previous_year_rating"] = data["previous_year_rating"].replace("", 0).fillna(0)
    
    return data.to_json()