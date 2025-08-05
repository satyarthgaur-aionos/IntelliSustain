# Machine Learning Implementation Guide for IntelliSustain

## 🎯 Overview for Non-ML Developers

This guide helps you implement real ML features without deep ML knowledge. The system uses **scikit-learn** for most ML tasks, which is beginner-friendly and powerful.

## 📚 What You Need to Know (Minimal ML Knowledge)

### 1. Basic ML Concepts
- **Supervised Learning**: Predict outcomes from historical data
- **Unsupervised Learning**: Find patterns in data without known outcomes
- **Feature Engineering**: Creating useful inputs from raw data
- **Model Training**: Teaching the model to recognize patterns
- **Prediction**: Using trained model to make new predictions

### 2. Key ML Libraries (Already in requirements)
```python
# Core ML library - handles most tasks
import sklearn

# Data manipulation
import pandas as pd
import numpy as np

# Model persistence
import joblib
```

## 🚀 Quick Start: Your First ML Model

### Step 1: Prepare Your Data
```python
# Example: Predicting device failures from telemetry data
def prepare_device_data(telemetry_data):
    """Convert raw telemetry to ML-ready format"""
    df = pd.DataFrame(telemetry_data)
    
    # Extract features
    df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
    df['temperature'] = df['temperature'].apply(lambda x: x.get('value', 0))
    df['humidity'] = df['humidity'].apply(lambda x: x.get('value', 0))
    df['battery'] = df['battery'].apply(lambda x: x.get('value', 100))
    
    # Create target (what we want to predict)
    df['failure_risk'] = calculate_failure_risk(df)
    
    return df

def calculate_failure_risk(df):
    """Simple rule-based failure risk (you can improve this)"""
    risk = np.zeros(len(df))
    
    # High temperature = high risk
    risk += np.where(df['temperature'] > 80, 0.8, 0.1)
    
    # Low battery = high risk
    risk += np.where(df['battery'] < 3.0, 0.9, 0.1)
    
    # High humidity = medium risk
    risk += np.where(df['humidity'] > 70, 0.5, 0.1)
    
    return np.clip(risk, 0, 1)  # Keep between 0 and 1
```

### Step 2: Train Your Model
```python
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def train_predictive_model(device_id, historical_data):
    """Train ML model for device failure prediction"""
    
    # Prepare data
    df = prepare_device_data(historical_data)
    
    # Select features (inputs) and target (output)
    features = ['hour', 'temperature', 'humidity', 'battery']
    X = df[features].values
    y = df['failure_risk'].values
    
    # Split data: 80% for training, 20% for testing
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
    # Scale features (important for ML models)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    # Test model
    predictions = model.predict(X_test_scaled)
    accuracy = model.score(X_test_scaled, y_test)
    
    print(f"Model accuracy: {accuracy:.3f}")
    
    # Save model for later use
    joblib.dump(model, f'models/device_{device_id}_model.pkl')
    joblib.dump(scaler, f'models/device_{device_id}_scaler.pkl')
    
    return model, scaler
```

### Step 3: Make Predictions
```python
def predict_device_failure(device_id, current_data):
    """Predict failure risk for a device"""
    
    # Load trained model
    model = joblib.load(f'models/device_{device_id}_model.pkl')
    scaler = joblib.load(f'models/device_{device_id}_scaler.pkl')
    
    # Prepare current data
    features = prepare_current_features(current_data)
    X = scaler.transform([features])
    
    # Make prediction
    risk_score = model.predict(X)[0]
    
    return {
        'device_id': device_id,
        'risk_score': float(risk_score),
        'urgency': 'HIGH' if risk_score > 0.7 else 'MEDIUM' if risk_score > 0.4 else 'LOW',
        'recommendation': get_recommendation(risk_score)
    }
```

## 🔧 Common ML Tasks for Facility Management

### 1. Anomaly Detection (Find Unusual Patterns)
```python
from sklearn.ensemble import IsolationForest

def detect_anomalies(device_data):
    """Find unusual patterns in device data"""
    
    # Prepare features
    features = ['temperature', 'humidity', 'energy_consumption']
    X = device_data[features].values
    
    # Train anomaly detector
    detector = IsolationForest(contamination=0.1)  # Expect 10% anomalies
    detector.fit(X)
    
    # Detect anomalies
    predictions = detector.predict(X)
    anomaly_scores = detector.decision_function(X)
    
    # Return anomalies
    anomalies = []
    for i, (pred, score) in enumerate(zip(predictions, anomaly_scores)):
        if pred == -1:  # Anomaly detected
            anomalies.append({
                'index': i,
                'score': float(score),
                'severity': 'HIGH' if score < -0.5 else 'MEDIUM'
            })
    
    return anomalies
```

### 2. Energy Consumption Forecasting
```python
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

def forecast_energy_consumption(historical_data, days_ahead=7):
    """Predict energy consumption for next N days"""
    
    # Prepare time series data
    df = pd.DataFrame(historical_data)
    df['date'] = pd.to_datetime(df['timestamp'])
    df['day_of_year'] = df['date'].dt.dayofyear
    
    # Create features
    X = df[['day_of_year', 'temperature', 'humidity']].values
    y = df['energy_consumption'].values
    
    # Train model
    model = LinearRegression()
    model.fit(X, y)
    
    # Create future dates for prediction
    future_dates = pd.date_range(
        start=df['date'].max() + pd.Timedelta(days=1),
        periods=days_ahead,
        freq='D'
    )
    
    # Make predictions
    predictions = []
    for date in future_dates:
        features = [date.dayofyear, 25, 50]  # Default temp/humidity
        pred = model.predict([features])[0]
        predictions.append({
            'date': date.strftime('%Y-%m-%d'),
            'predicted_energy': float(pred)
        })
    
    return predictions
```

### 3. Occupancy Prediction
```python
from sklearn.ensemble import RandomForestClassifier

def predict_occupancy(historical_data):
    """Predict room occupancy based on patterns"""
    
    df = pd.DataFrame(historical_data)
    
    # Create features
    df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
    df['day_of_week'] = pd.to_datetime(df['timestamp']).dt.dayofweek
    df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
    
    # Target: occupancy level (0-1)
    df['occupancy_level'] = df['occupancy'].apply(lambda x: x.get('value', 0))
    
    # Train classifier
    features = ['hour', 'day_of_week', 'is_weekend', 'temperature']
    X = df[features].values
    y = (df['occupancy_level'] > 0.5).astype(int)  # Binary: occupied or not
    
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X, y)
    
    return model
```

## 📊 Data Requirements for ML

### Minimum Data Requirements
- **Historical Data**: 3-6 months of device telemetry
- **Data Points**: Temperature, humidity, energy, battery, occupancy
- **Frequency**: At least hourly readings
- **Quality**: Clean data with minimal missing values

### Data Sources
```python
# From your existing APIs
def get_training_data():
    """Collect data for ML training"""
    
    # Get device telemetry
    telemetry_data = make_api_request("plugins/telemetry/DEVICE/{device_id}/values/timeseries")
    
    # Get alarm data
    alarm_data = make_api_request("alarms?deviceId={device_id}")
    
    # Get weather data
    weather_data = fetch_weather_forecast("city")
    
    # Combine all data
    combined_data = combine_data_sources(telemetry_data, alarm_data, weather_data)
    
    return combined_data
```

## 🎯 Real-World Implementation Steps

### Phase 1: Data Collection (Week 1)
```python
# 1. Set up data collection
def collect_training_data():
    """Collect 1 month of data for initial training"""
    
    devices = get_all_devices()
    training_data = {}
    
    for device in devices:
        device_id = device['id']
        
        # Collect telemetry for 30 days
        end_time = datetime.now()
        start_time = end_time - timedelta(days=30)
        
        telemetry = get_device_telemetry(
            device_id, 
            start_time=start_time,
            end_time=end_time
        )
        
        training_data[device_id] = telemetry
    
    return training_data

# 2. Validate data quality
def validate_data_quality(data):
    """Check if data is suitable for ML"""
    
    issues = []
    
    for device_id, device_data in data.items():
        if len(device_data) < 100:  # Need at least 100 data points
            issues.append(f"Device {device_id}: Insufficient data")
        
        # Check for missing values
        missing_pct = calculate_missing_percentage(device_data)
        if missing_pct > 0.2:  # More than 20% missing
            issues.append(f"Device {device_id}: Too many missing values ({missing_pct:.1%})")
    
    return issues
```

### Phase 2: Model Training (Week 2)
```python
# 1. Train models for each device type
def train_device_models():
    """Train ML models for different device types"""
    
    device_types = ['thermostat', 'sensor', 'hvac', 'lighting']
    trained_models = {}
    
    for device_type in device_types:
        devices = get_devices_by_type(device_type)
        
        if len(devices) >= 5:  # Need at least 5 devices for training
            model = train_device_type_model(device_type, devices)
            trained_models[device_type] = model
    
    return trained_models

# 2. Validate model performance
def validate_models(models):
    """Check if models are performing well"""
    
    validation_results = {}
    
    for device_type, model in models.items():
        # Test on recent data
        test_data = get_recent_data(device_type, days=7)
        accuracy = test_model_performance(model, test_data)
        
        validation_results[device_type] = {
            'accuracy': accuracy,
            'status': 'GOOD' if accuracy > 0.7 else 'NEEDS_IMPROVEMENT'
        }
    
    return validation_results
```

### Phase 3: Integration (Week 3)
```python
# 1. Integrate ML predictions into your agent
def enhance_agent_with_ml():
    """Add ML capabilities to your existing agent"""
    
    # Add new functions to your agent
    new_functions = [
        {
            "name": "predict_maintenance_needs",
            "description": "Predict maintenance needs using ML models",
            "parameters": {"device_id": "string"}
        },
        {
            "name": "detect_anomalies",
            "description": "Detect anomalies in device data",
            "parameters": {"device_id": "string"}
        },
        {
            "name": "forecast_energy",
            "description": "Forecast energy consumption",
            "parameters": {"days": "integer"}
        }
    ]
    
    return new_functions

# 2. Update your agent's function calling logic
def call_ml_function(function_name, arguments):
    """Route ML function calls to appropriate models"""
    
    if function_name == "predict_maintenance_needs":
        device_id = arguments.get('device_id')
        return predict_device_failure(device_id, get_current_data(device_id))
    
    elif function_name == "detect_anomalies":
        device_id = arguments.get('device_id')
        return detect_anomalies(get_device_data(device_id))
    
    elif function_name == "forecast_energy":
        days = arguments.get('days', 7)
        return forecast_energy_consumption(get_historical_data(), days)
```

## 🔍 Monitoring and Improvement

### Model Performance Monitoring
```python
def monitor_model_performance():
    """Track how well your ML models are performing"""
    
    performance_metrics = {}
    
    for model_name, model in trained_models.items():
        # Get recent predictions
        recent_predictions = get_recent_predictions(model_name)
        
        # Calculate accuracy
        actual_outcomes = get_actual_outcomes(model_name)
        accuracy = calculate_accuracy(recent_predictions, actual_outcomes)
        
        performance_metrics[model_name] = {
            'accuracy': accuracy,
            'last_updated': datetime.now(),
            'status': 'HEALTHY' if accuracy > 0.7 else 'NEEDS_RETRAINING'
        }
    
    return performance_metrics

def retrain_models_if_needed():
    """Automatically retrain models if performance drops"""
    
    performance = monitor_model_performance()
    
    for model_name, metrics in performance.items():
        if metrics['accuracy'] < 0.6:  # Performance threshold
            print(f"Retraining model: {model_name}")
            
            # Get new training data
            new_data = get_recent_training_data(model_name, days=90)
            
            # Retrain model
            new_model = train_model(model_name, new_data)
            
            # Replace old model
            trained_models[model_name] = new_model
```

## 🎯 Best Practices for Non-ML Developers

### 1. Start Simple
- Begin with basic models (Random Forest, Linear Regression)
- Focus on one prediction task at a time
- Use rule-based approaches as fallbacks

### 2. Data Quality First
- Clean your data before training
- Handle missing values appropriately
- Validate data quality regularly

### 3. Monitor Everything
- Track model performance over time
- Set up alerts for performance drops
- Log all predictions for analysis

### 4. Iterate Gradually
- Start with small datasets
- Validate results before scaling
- Get feedback from users

### 5. Use Pre-built Solutions
- Leverage scikit-learn's built-in models
- Use established evaluation metrics
- Follow proven data preprocessing steps

## 🚀 Quick Implementation Checklist

- [ ] Install required packages: `pip install scikit-learn pandas numpy joblib`
- [ ] Collect 1 month of historical data
- [ ] Create data preprocessing functions
- [ ] Train your first model (start with Random Forest)
- [ ] Test model on recent data
- [ ] Integrate predictions into your agent
- [ ] Set up monitoring and alerts
- [ ] Deploy and monitor performance

## 📞 Getting Help

### When You're Stuck
1. **Check the data**: 90% of ML issues are data problems
2. **Start simple**: Use basic models before complex ones
3. **Validate assumptions**: Test your data and model assumptions
4. **Document everything**: Keep track of what you tried

### Resources
- **Scikit-learn documentation**: Excellent tutorials and examples
- **Pandas documentation**: Essential for data manipulation
- **Stack Overflow**: Great for specific technical questions
- **Kaggle**: Practice with real datasets

---

**Remember**: You don't need to be an ML expert to implement powerful ML features. Start simple, focus on data quality, and iterate based on results. 
