#### train_DST_MLFLOW ####
Warning : Don't forget to clone the https://github.com/mlflow/mlflow before use.


# ex_uri_id_mgt_tester.py
This script is just here to play with tracking URI and experiment Ids management.


# ex_autolog.py
This script is to try the autolog function. You can track either in file or db mode. It can also register the model to make the version follow-up

If you want to track with a db sqlite type, please



====== In progress

Mlflow required DB as datastore for Model Registry So you have to run tracking server with DB as backend-store and log model to this tracking server. The easiest way to use DB is to use SQLite.

mlflow server \
    --backend-store-uri sqlite:///mlflow.db \
    --default-artifact-root ./artifacts \
    --host 0.0.0.0
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./artifacts --host 0.0.0.0

And set MLFLOW_TRACKING_URI environment variable to http://localhost:5000 or

mlflow.set_tracking_uri("http://localhost:5000")

After got to http://localhost:5000 and you can register a logged model from UI or from the code.
