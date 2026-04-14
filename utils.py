"""
Utility functions for the Mortality Prediction Application
"""

import pickle
import numpy as np
import pandas as pd
from datetime import datetime
import json
from pathlib import Path
from typing import Dict, List, Tuple, Union

class ModelManager:
    """Manage XGBoost model loading and predictions"""
    
    def __init__(self, model_path: str = 'final_model_XGB.pkl'):
        self.model_path = model_path
        self.model_dict = None
        self.xgb_model = None
        self.optimal_threshold = None
        self.load_model()
    
    def load_model(self):
        """Load XGBoost model from pickle file"""
        try:
            with open(self.model_path, 'rb') as f:
                self.model_dict = pickle.load(f)
            self.xgb_model = self.model_dict['model']
            self.optimal_threshold = self.model_dict['optimal_threshold']
            print(f"✓ Model loaded successfully from {self.model_path}")
        except FileNotFoundError:
            raise FileNotFoundError(f"Model file not found: {self.model_path}")
        except Exception as e:
            raise Exception(f"Error loading model: {str(e)}")
    
    def predict(self, group: float, ddplus: float, age: float, pdw: float,
                bun: float, ldh: float, alt: float, pt: float) -> Dict:
        """
        Make a single prediction
        
        Args:
            group: Patient group (1-5)
            ddplus: DDPLUS score (0-100)
            age: Age in years (0-120)
            pdw: Platelet distribution width (0-50%)
            bun: Blood urea nitrogen (0-200 mg/dL)
            ldh: Lactate dehydrogenase (0-2000 U/L)
            alt: Alanine aminotransferase (0-1000 U/L)
            pt: Prothrombin time (0-100 seconds)
        
        Returns:
            Dictionary with mortality risk and classification
        """
        input_data = np.array([[group, ddplus, age, pdw, bun, ldh, alt, pt]])
        pred_proba = self.xgb_model.predict_proba(input_data)[0]
        
        mortality_risk = pred_proba[1]
        survival_prob = pred_proba[0]
        
        # Classify risk
        if mortality_risk >= 0.65:
            risk_category = "HIGH"
        elif mortality_risk >= 0.35:
            risk_category = "MODERATE"
        else:
            risk_category = "LOW"
        
        return {
            'mortality_risk': mortality_risk,
            'survival_prob': survival_prob,
            'risk_category': risk_category,
            'odds_ratio': mortality_risk / (1 - mortality_risk) if mortality_risk < 1 else float('inf')
        }
    
    def batch_predict(self, df: pd.DataFrame, 
                     patient_id_col: str = None,
                     patient_name_col: str = None) -> pd.DataFrame:
        """
        Make batch predictions from DataFrame
        
        Args:
            df: DataFrame with required columns
            patient_id_col: Column name for patient ID
            patient_name_col: Column name for patient name
        
        Returns:
            DataFrame with predictions
        """
        required_cols = ['group', 'DDPLUS', 'age', 'PDW', 'BUN', 'LDH', 'ALT', 'PT']
        
        # Validate columns
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing columns: {missing_cols}")
        
        results = []
        
        for idx, row in df.iterrows():
            try:
                prediction = self.predict(
                    group=row['group'],
                    ddplus=row['DDPLUS'],
                    age=row['age'],
                    pdw=row['PDW'],
                    bun=row['BUN'],
                    ldh=row['LDH'],
                    alt=row['ALT'],
                    pt=row['PT']
                )
                
                result = {
                    'patient_id': row.get(patient_id_col, f'P{idx+1}') if patient_id_col else f'P{idx+1}',
                    'patient_name': row.get(patient_name_col, 'N/A') if patient_name_col else 'N/A',
                    'mortality_risk': prediction['mortality_risk'],
                    'survival_prob': prediction['survival_prob'],
                    'risk_category': prediction['risk_category'],
                    'odds_ratio': prediction['odds_ratio']
                }
                results.append(result)
            except Exception as e:
                print(f"Error processing row {idx}: {str(e)}")
                continue
        
        return pd.DataFrame(results)


class DataProcessor:
    """Process and validate patient data"""
    
    PARAMETER_RANGES = {
        'group': (1, 5),
        'DDPLUS': (0, 100),
        'age': (0, 120),
        'PDW': (0, 50),
        'BUN': (0, 200),
        'LDH': (0, 2000),
        'ALT': (0, 1000),
        'PT': (0, 100)
    }
    
    @staticmethod
    def validate_input(group: float, ddplus: float, age: float, pdw: float,
                      bun: float, ldh: float, alt: float, pt: float) -> Tuple[bool, str]:
        """
        Validate input parameters
        
        Returns:
            (is_valid, error_message)
        """
        params = {
            'group': group,
            'DDPLUS': ddplus,
            'age': age,
            'PDW': pdw,
            'BUN': bun,
            'LDH': ldh,
            'ALT': alt,
            'PT': pt
        }
        
        for param_name, value in params.items():
            min_val, max_val = DataProcessor.PARAMETER_RANGES[param_name]
            if not (min_val <= value <= max_val):
                return False, f"{param_name} must be between {min_val} and {max_val}, got {value}"
        
        return True, ""
    
    @staticmethod
    def load_csv(filepath: str) -> Tuple[bool, Union[pd.DataFrame, str]]:
        """
        Load and validate CSV file
        
        Returns:
            (success, DataFrame or error message)
        """
        try:
            df = pd.read_csv(filepath)
            return True, df
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
        """Normalize column names to expected format"""
        df.columns = df.columns.str.strip().str.lower()
        return df


class ReportGenerator:
    """Generate reports and export predictions"""
    
    @staticmethod
    def generate_summary_report(predictions: pd.DataFrame) -> Dict:
        """Generate summary statistics from predictions"""
        
        if len(predictions) == 0:
            return {}
        
        risk_counts = predictions['risk_category'].value_counts()
        
        return {
            'total_predictions': len(predictions),
            'avg_mortality_risk': predictions['mortality_risk'].mean(),
            'max_mortality_risk': predictions['mortality_risk'].max(),
            'min_mortality_risk': predictions['mortality_risk'].min(),
            'std_mortality_risk': predictions['mortality_risk'].std(),
            'high_risk_count': risk_counts.get('HIGH', 0),
            'moderate_risk_count': risk_counts.get('MODERATE', 0),
            'low_risk_count': risk_counts.get('LOW', 0),
            'high_risk_percentage': (risk_counts.get('HIGH', 0) / len(predictions) * 100) if len(predictions) > 0 else 0
        }
    
    @staticmethod
    def export_to_csv(df: pd.DataFrame, filepath: str) -> bool:
        """Export predictions to CSV"""
        try:
            df.to_csv(filepath, index=False)
            return True
        except Exception as e:
            print(f"Error exporting to CSV: {str(e)}")
            return False
    
    @staticmethod
    def export_to_json(df: pd.DataFrame, filepath: str) -> bool:
        """Export predictions to JSON"""
        try:
            df.to_json(filepath, orient='records', indent=2)
            return True
        except Exception as e:
            print(f"Error exporting to JSON: {str(e)}")
            return False
    
    @staticmethod
    def generate_html_report(predictions: pd.DataFrame, output_path: str) -> bool:
        """Generate HTML report with summary and table"""
        try:
            summary = ReportGenerator.generate_summary_report(predictions)
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Mortality Risk Assessment Report</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    .header {{ background: linear-gradient(135deg, #1e3a8a 0%, #0369a1 100%);
                               color: white; padding: 20px; border-radius: 8px; }}
                    .summary {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin: 20px 0; }}
                    .metric {{ background: white; padding: 15px; border-radius: 8px; 
                               box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                    .metric-value {{ font-size: 24px; font-weight: bold; color: #1e3a8a; }}
                    .metric-label {{ font-size: 12px; color: #666; margin-top: 5px; }}
                    table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                    th {{ background: #f0f0f0; padding: 10px; text-align: left; border-bottom: 2px solid #1e3a8a; }}
                    td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
                    tr:hover {{ background: #f9f9f9; }}
                    .risk-high {{ color: #dc2626; font-weight: bold; }}
                    .risk-moderate {{ color: #f59e0b; font-weight: bold; }}
                    .risk-low {{ color: #059669; font-weight: bold; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>🏥 Mortality Risk Assessment Report</h1>
                    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
                
                <div class="summary">
                    <div class="metric">
                        <div class="metric-value">{summary.get('total_predictions', 0)}</div>
                        <div class="metric-label">Total Predictions</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{summary.get('avg_mortality_risk', 0)*100:.1f}%</div>
                        <div class="metric-label">Average Mortality Risk</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{summary.get('high_risk_count', 0)}</div>
                        <div class="metric-label">High Risk Patients</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{summary.get('high_risk_percentage', 0):.1f}%</div>
                        <div class="metric-label">High Risk Rate</div>
                    </div>
                </div>
                
                <h2>Patient Results</h2>
                <table>
                    <tr>
                        <th>Patient ID</th>
                        <th>Mortality Risk</th>
                        <th>Risk Category</th>
                        <th>Survival Probability</th>
                    </tr>
            """
            
            for idx, row in predictions.iterrows():
                risk_class = f"risk-{row['risk_category'].lower()}"
                html_content += f"""
                    <tr>
                        <td>{row.get('patient_id', f'P{idx+1}')}</td>
                        <td>{row['mortality_risk']*100:.1f}%</td>
                        <td class="{risk_class}">{row['risk_category']}</td>
                        <td>{row.get('survival_prob', 0)*100:.1f}%</td>
                    </tr>
                """
            
            html_content += """
                </table>
            </body>
            </html>
            """
            
            with open(output_path, 'w') as f:
                f.write(html_content)
            return True
        except Exception as e:
            print(f"Error generating HTML report: {str(e)}")
            return False


class ConfigManager:
    """Manage application configuration"""
    
    DEFAULT_CONFIG = {
        'app_name': 'ICU Mortality Risk Assessment',
        'version': '1.1',
        'model_path': 'final_model_XGB.pkl',
        'risk_thresholds': {
            'low_max': 0.35,
            'moderate_max': 0.65
        },
        'export_formats': ['csv', 'json', 'html']
    }
    
    def __init__(self, config_path: str = 'config.json'):
        self.config_path = config_path
        self.config = self.load_config()
    
    def load_config(self) -> Dict:
        """Load configuration from file or use defaults"""
        if Path(self.config_path).exists():
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}, using defaults")
                return self.DEFAULT_CONFIG.copy()
        return self.DEFAULT_CONFIG.copy()
    
    def save_config(self, config: Dict) -> bool:
        """Save configuration to file"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get(self, key: str, default=None):
        """Get configuration value"""
        return self.config.get(key, default)


# Example usage and testing
if __name__ == "__main__":
    # Test ModelManager
    print("Testing ModelManager...")
    try:
        manager = ModelManager('final_model_XGB.pkl')
        
        # Single prediction
        result = manager.predict(
            group=2, ddplus=45, age=58, pdw=15,
            bun=28, ldh=320, alt=65, pt=13
        )
        print(f"Single prediction result: {result}")
        
        # Batch prediction
        test_data = pd.DataFrame({
            'group': [1, 2, 3, 4, 5],
            'DDPLUS': [20, 45, 60, 75, 95],
            'age': [35, 58, 65, 78, 85],
            'PDW': [12.5, 15, 15.8, 18, 20],
            'BUN': [15, 28, 45, 65, 120],
            'LDH': [200, 320, 450, 580, 900],
            'ALT': [25, 65, 85, 150, 280],
            'PT': [11, 13, 13.8, 16, 22]
        })
        
        batch_results = manager.batch_predict(test_data)
        print(f"\nBatch prediction results:\n{batch_results}")
        
        # Generate report
        print("\nGenerating reports...")
        summary = ReportGenerator.generate_summary_report(batch_results)
        print(f"Summary: {summary}")
        
        ReportGenerator.export_to_csv(batch_results, 'test_results.csv')
        ReportGenerator.export_to_json(batch_results, 'test_results.json')
        ReportGenerator.generate_html_report(batch_results, 'test_report.html')
        print("✓ Reports generated successfully")
        
    except Exception as e:
        print(f"Error: {e}")
