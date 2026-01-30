"""
Data Generation Module
Generates synthetic health monitoring dataset
"""

import numpy as np
import pandas as pd
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import HEALTH_PARAMS, DATA_PATH, DATASET_SIZE


class DataGenerator:
    """Generate synthetic health monitoring data"""
    
    def __init__(self, size=DATASET_SIZE):
        self.size = size
        np.random.seed(42)
    
    def generate_health_data(self):
        """Generate synthetic health dataset with various health conditions"""
        data = []
        
        for i in range(self.size):
            # Generate base vital signs
            condition = np.random.choice(['healthy', 'at_risk', 'critical'], 
                                        p=[0.7, 0.2, 0.1])
            
            if condition == 'healthy':
                heart_rate = np.random.normal(75, 10)
                bp_systolic = np.random.normal(115, 8)
                bp_diastolic = np.random.normal(75, 6)
                temperature = np.random.normal(36.6, 0.3)
                oxygen = np.random.normal(98, 1)
                respiratory = np.random.normal(16, 2)
                risk_score = np.random.uniform(0, 0.3)
                
            elif condition == 'at_risk':
                heart_rate = np.random.choice([
                    np.random.normal(55, 5),  # Low
                    np.random.normal(110, 10)  # High
                ])
                bp_systolic = np.random.normal(140, 10)
                bp_diastolic = np.random.normal(90, 8)
                temperature = np.random.normal(37.5, 0.5)
                oxygen = np.random.normal(93, 2)
                respiratory = np.random.normal(22, 3)
                risk_score = np.random.uniform(0.4, 0.7)
                
            else:  # critical
                heart_rate = np.random.choice([
                    np.random.normal(45, 5),  # Very low
                    np.random.normal(140, 15)  # Very high
                ])
                bp_systolic = np.random.normal(170, 15)
                bp_diastolic = np.random.normal(105, 10)
                temperature = np.random.normal(38.5, 0.8)
                oxygen = np.random.normal(88, 3)
                respiratory = np.random.normal(28, 4)
                risk_score = np.random.uniform(0.7, 1.0)
            
            # Apply constraints
            heart_rate = np.clip(heart_rate, 40, 200)
            bp_systolic = np.clip(bp_systolic, 70, 200)
            bp_diastolic = np.clip(bp_diastolic, 40, 130)
            temperature = np.clip(temperature, 35.0, 42.0)
            oxygen = np.clip(oxygen, 70, 100)
            respiratory = np.clip(respiratory, 8, 40)
            
            data.append({
                'heart_rate': round(heart_rate, 1),
                'blood_pressure_systolic': round(bp_systolic, 1),
                'blood_pressure_diastolic': round(bp_diastolic, 1),
                'temperature': round(temperature, 1),
                'oxygen_saturation': round(oxygen, 1),
                'respiratory_rate': round(respiratory, 1),
                'risk_score': round(risk_score, 3)
            })
        
        return pd.DataFrame(data)
    
    def save_dataset(self, filepath=DATA_PATH):
        """Generate and save dataset to CSV file"""
        df = self.generate_health_data()
        df.to_csv(filepath, index=False)
        print(f"Dataset saved to {filepath}")
        print(f"Dataset shape: {df.shape}")
        print(f"\nDataset statistics:\n{df.describe()}")
        return df


if __name__ == "__main__":
    generator = DataGenerator()
    df = generator.save_dataset()
