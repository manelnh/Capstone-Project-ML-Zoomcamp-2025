import warnings
warnings.filterwarnings('ignore')
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import r2_score

# Load data
data = pd.read_csv('sp_500_risk_rating.csv')

# Data cleaning
data.columns = data.columns.str.lower().str.replace(' ', '_')
categorical = list(data.dtypes[data.dtypes == 'object'].index)
for c in categorical:
    data[c] = data[c].str.lower().str.replace(' ', '_')

data.dropna(subset=['total_esg_risk_score', 'environment_risk_score', 'governance_risk_score', 'social_risk_score'], inplace=True)


# Define features and target
categorical_columns = ['sector', 'industry', 'controversy_level', 'esg_risk_level']
numerical_columns = ['environment_risk_score', 'governance_risk_score', 'social_risk_score', 'controversy_score']
features = categorical_columns + numerical_columns
target = 'total_esg_risk_score'

# Convert dataframe rows to list of dicts
data_features = data[features].to_dict(orient='records')

# Initialize DictVectorizer and transform
dv = DictVectorizer(sparse=False)
X = dv.fit_transform(data_features)

y = data[target].values

# Split data
X_full_train, X_test, y_full_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_full_train, y_full_train, test_size=0.25, random_state=42)

# Model training
rf_model = RandomForestRegressor(n_estimators=200,
                                 max_depth=9,
                                 min_samples_leaf=1,
                                 n_jobs=-1, 
                                 random_state=42)
rf_model.fit(X_train, y_train)

# Testing example

new_data = {
      "sector": "energy",
      "industry": "oil_and_gas_exploration",
      "controversy_level": "high_controversy_level",
      "esg_risk_level": "high",
      "environment_risk_score": 15.2,
      "governance_risk_score": 10.5,
      "social_risk_score": 12.0,
      "controversy_score": 4.5,
      "esg_risk_percentile": 85.0
    }

# Transform input data using DictVectorizer
X_input = dv.transform([new_data])

# Predict using your RandomForest model
prediction = rf_model.predict(X_input)
actual_value = 42.2
print(f"Predicted total ESG risk score: {prediction[0]}, Actual total ESG risk score: {actual_value}")

r_squared = r2_score(y_test, rf_model.predict(X_test))
print(f"R^2 score on test set: {r_squared}")


# Save model and DictVectorizer
import pickle
output_file = 'model_rfr.bin'
with open(output_file, 'wb') as f_out:
    pickle.dump((rf_model, dv), f_out)
print(f'Model and vectorizer saved to {output_file}')
