
import numpy as np
from sklearn.linear_model import LinearRegression

# Generate some sample data
x = np.array([[1], [2], [3], [4], [5]])
y = np.array([2, 4, 6, 8, 10])

# Create a linear regression model
reg = LinearRegression().fit(x, y)

# Use the model to make predictions
future_x = np.array([[6], [7], [8], [10]])
future_y = reg.predict(future_x)

print(f"Prediction for x = 6: {future_y[0]}")
print(f"Prediction for x = 7: {future_y[1]}")
print(f"Prediction for x = 8: {future_y[2]}")
print(f"Prediction for x = 8: {future_y[3]}")

print(future_x, future_y)
