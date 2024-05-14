import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Load the data
file_path = r'C:\Users\Renato Ribas\Desktop\Engenharia de Software\Semestre 4\ML\Repositorio\I4.0-Artesian-AI-Monitor\Library-ML\data\raw\Steel_industry_data.csv'
df = pd.read_csv(file_path, index_col=False, encoding='utf-8', delimiter=',')

# Data preprocessing
hi_filter = 50
lo_filter = df['Usage_kWh'].quantile(0.01)
df = df[(df['Usage_kWh'] > lo_filter) & (df['Usage_kWh'] < hi_filter)]

# Select independent and dependent variables
X = df[['Lagging_Current_Reactive.Power_kVarh','Leading_Current_Reactive_Power_kVarh','CO2(tCO2)','Lagging_Current_Power_Factor']]
y = df['Usage_kWh']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize models
model = LinearRegression()
knn_model = KNeighborsRegressor(n_neighbors=5)
regr = RandomForestRegressor()

# Train the models
model.fit(X_train, y_train)
knn_model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)
y_pred_knn = knn_model.predict(X_test)

# Model evaluation
mse_test = mean_squared_error(y_test, y_pred)
mae_test = mean_absolute_error(y_test, y_pred)
r2_test = r2_score(y_test, y_pred)

mse_knn = mean_squared_error(y_test, y_pred_knn)
mae_knn = mean_absolute_error(y_test, y_pred_knn)
r2_knn = r2_score(y_test, y_pred_knn)

# Parameter grid for grid search
param_grid = {'fit_intercept': [True, False]}

# Perform grid search for Linear Regression
grid_search_Reg_Linear = GridSearchCV(model, param_grid, scoring='neg_mean_squared_error', cv=5)
grid_search_Reg_Linear.fit(X, y)

# Evaluate best Linear Regression model
y_pred_grid = grid_search_Reg_Linear.predict(X_test)

mse_grid = mean_squared_error(y_test, y_pred_grid)
r2_grid = r2_score(y_test, y_pred_grid)

# Perform grid search for Random Forest
param_grid_forest = {'n_estimators': [10, 20]}
grid_search_forest_Reg = GridSearchCV(regr, param_grid_forest, scoring='neg_mean_squared_error', cv=5)
grid_search_forest_Reg.fit(X, y)

# Evaluate best Random Forest model
y_pred_grid_forest = grid_search_forest_Reg.predict(X_test)

mse_grid_forest = mean_squared_error(y_test, y_pred_grid_forest)
r2_grid_forest = r2_score(y_test, y_pred_grid_forest)

# Perform grid search for KNN
param_grid_knn = {'n_neighbors': [3, 5, 7, 10], 'weights': ['uniform', 'distance'], 'metric': ['euclidean', 'manhattan']}
grid_search_knn = GridSearchCV(knn_model, param_grid_knn, scoring='neg_mean_squared_error', cv=5)
grid_search_knn.fit(X, y)

# Evaluate best KNN model
y_pred_grid_knn = grid_search_knn.predict(X_test)

mse_grid_knn = mean_squared_error(y_test, y_pred_grid_knn)
r2_grid_knn = r2_score(y_test, y_pred_grid_knn)

# New data for prediction
new_data = pd.DataFrame({'Lagging_Current_Reactive.Power_kVarh': [13.035384],
                         'Leading_Current_Reactive_Power_kVarh': [3.870949],
                         'CO2(tCO2)': [0.011524],
                         'Lagging_Current_Power_Factor': [80.578056]})

# Predict using the best Random Forest model
best_rf_model = grid_search_forest_Reg.best_estimator_
predictions = best_rf_model.predict(new_data)

print(f'A previsão para kWh é de aproximadamente: {predictions[0]:.2f} kWh')

ultima_previsao = predictions[0]

import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func


# Connect to the database
engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/DW_Server')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

#Entidades
class previsaom3h(Base):
    __tablename__ = 'previsaom3h'

    id_previsao = Column(Integer, primary_key=True)
    previsaoregistrada = Column(Float)
    offsettolerancia = Column(Float)
    timestamp = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<previsaoM3h(previsaoregistrada={self.previsaoregistrada}, offsettolerancia={self.offsettolerancia}, timestamp={self.timestamp})>"


# SQL

#INSERT
data_insert = previsaom3h(previsaoregistrada=ultima_previsao, offsettolerancia=21.901, timestamp= func.now())
session.add(data_insert)
session.commit()


#SELECT
data = session.query(previsaom3h).all()
print(data)


session.close()

