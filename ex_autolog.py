import pandas as pd 
from sklearn import svm, datasets 
from sklearn.model_selection import GridSearchCV 
import mlflow
from urllib.parse import urlparse

# Storage mode configuration 
storage_mode = 'db' # 'file' (in mlruns directory) or 'db' (in sqlite db)
path = "/home/ubuntu/train_DST_MLFLOW/mlruns" 
if storage_mode == 'file':
    mlflow.set_tracking_uri("file://"+ path)
elif storage_mode == 'db':
    mlflow.set_tracking_uri("http://localhost:5000")
# Just for debug
print("Tracking URI : ",mlflow.get_tracking_uri())

if __name__ == "__main__":

    # Manage the experiment Ids an names
    experiment_name = "Autolog" 

    # The following code will try to create the experiment and if it exist, it will get the experiment number that will be usefull fo any registration
    try:
        experiment_id = mlflow.create_experiment(experiment_name)
    except:
        current_experiment=dict(mlflow.get_experiment_by_name(experiment_name)) 
        experiment_id=current_experiment['experiment_id']
    # Some prints just for fun
    print("experiment_name :",experiment_name)
    print("experiment_id : ",experiment_id)

    # Run management
    with mlflow.start_run(experiment_id =experiment_id):
        mlflow.sklearn.autolog() 
        iris = datasets.load_iris()
        parameters = {"kernel": ("linear", "rbf"), "C": [1, 10]} 
        svc = svm.SVC() 
        clf = GridSearchCV(svc, parameters) 
        clf.fit(iris.data, iris.target)

        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        # Model registry does not work with file store
        if tracking_url_type_store != "file":

            # Register the model
            # There are other ways to use the Model Registry, which depends on the use case,
            # please refer to the doc for more information:
            # https://mlflow.org/docs/latest/model-registry.html#api-workflow
            mlflow.sklearn.log_model(clf, "model", registered_model_name="AutologSVC")
        else:
            mlflow.sklearn.log_model(clf, "/home/ubuntu/train_DST_MLFLOW/artifacts", registered_model_name="AutologSVC")
