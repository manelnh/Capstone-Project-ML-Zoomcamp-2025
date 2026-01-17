
import requests

url = "http://localhost:8888/predict"

data = {
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

response = requests.post(url, json=data)
print(response.json())




