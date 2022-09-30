# train_DST_MLFLOW
Warning : Do not forget to clone the https://github.com/mlflow/mlflow before use.

Theses scripts are base on MLflow scripts examples.

## Scripts
### ex_uri_id_mgt_tester.py
This script is just here to play with tracking URI and experiment Ids management.

### sklearn_elasticnet_diabetes .py
MLflow application on diabetes use case

### sklearn_elasticnet_wine.py
MLflow application on wine quality use case

### ex_autolog.py
This script is to try the autolog function. You can track either in file or db mode. It can also register the model to make the version follow-up

If you want to track with a db sqlite type, please


## Datastore configuration

Natively, MLflow will store locally models and results in a mlruns directory. This can be an issue when you want to use Model Registry from MLflow. You should configure the server as below :

Mlflow required DB as datastore for Model Registry So you have to run tracking server with DB as backend-store and log model to this tracking server. The easiest way to use DB is to use SQLite.

	mlflow server \
		--backend-store-uri sqlite:///mlflow.db \
		--default-artifact-root ./artifacts \
		--host 0.0.0.0

In one line :) 

	mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./artifacts --host 0.0.0.0

And set MLFLOW_TRACKING_URI environment variable to http://localhost:5000 or directly in you script with :

	mlflow.set_tracking_uri("http://localhost:5000")

After go to http://localhost:5000 and you can register a logged model from UI or from the code.
