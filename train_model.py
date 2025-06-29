import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

# Sample Dataset
data = pd.DataFrame({
    'distance_km': [10, 50, 100, 150],
    'traffic_level': [1, 3, 2, 5],
    'holiday_flag': [0, 1, 0, 1],
    'weather_condition': [1, 3, 2, 4],
    'delay_minutes': [10, 60, 45, 120]
})

X = data[['distance_km', 'traffic_level', 'holiday_flag', 'weather_condition']]
y = data['delay_minutes']

# Train Model
model = LinearRegression()
model.fit(X, y)

# Save Model
with open('delay_model.pkl', 'wb') as file:
    pickle.dump(model, file)

print('✅ Model trained and delay_model.pkl saved successfully!')
