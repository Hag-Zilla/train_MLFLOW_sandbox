import pandas as pd 
from sklearn import svm, datasets 
from sklearn.model_selection import GridSearchCV 
import mlflow

# prédéfinit le chemin où vous souhaitez stocker vos sauvegardes des runs 
path = "/home/ubuntu/train_DST_MLFLOW/mlruns" 
mlflow.set_tracking_uri("file://"+ path)
print(mlflow.get_tracking_uri() )

if __name__ == "__main__":

    # Manage the experiment Ids an names
    experiment_name = "Autolog" 

    try:
        experiment_id = mlflow.create_experiment(experiment_name)
    except:
        current_experiment=dict(mlflow.get_experiment_by_name(experiment_name)) 
        experiment_id=current_experiment['experiment_id']
    with mlflow.start_run(experiment_id =experiment_id):
        mlflow.sklearn.autolog() 
        iris = datasets.load_iris()
        parameters = {"kernel": ("linear", "rbf"), "C": [1, 10]} 
        svc = svm.SVC() 
        clf = GridSearchCV(svc, parameters) 
        clf.fit(iris.data, iris.target) 