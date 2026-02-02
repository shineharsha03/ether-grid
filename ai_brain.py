import numpy as np
from sklearn.linear_model import LinearRegression

class SolarBrain:
    def __init__(self):
        # Train a simple model: 
        # Time (0-24) -> Energy Output (0-100 Wh)
        self.model = LinearRegression()
        
        # Training Data: Night=0, Noon=100
        X_train = np.array([[0], [6], [8], [12], [16], [18], [24]])
        y_train = np.array([0, 10, 40, 100, 80, 10, 0])
        
        self.model.fit(X_train, y_train)
    
    def predict_generation(self, hour):
        # Predict energy for a specific hour
        prediction = self.model.predict([[hour]])
        return max(0, round(prediction[0], 2)) # No negative energy

if __name__ == "__main__":
    # Test
    brain = SolarBrain()
    print(f"Solar output at 12 PM: {brain.predict_generation(12)} Wh")