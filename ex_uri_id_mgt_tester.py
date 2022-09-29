# URI and experiment Ids management tester

import mlflow

# Storage mode configuration 
storage_mode = 'db' # 'file' (in mlruns directory) or 'db' (in sqlite db)
path = "/home/ubuntu/train_DST_MLFLOW/mlruns" 
if storage_mode == 'file':
    mlflow.set_tracking_uri("file://"+ path)
elif storage_mode == 'db':
    mlflow.set_tracking_uri("http://localhost:5000")
# Just for debug
print("Tracking URI : ",mlflow.get_tracking_uri())

# We set the experiment name
experiment_name = "Experiment_Creation_Test" 

# The following code will try to create the experiment and if it exist, it will get the experiment number that will be usefull fo any registration
try:
    experiment_id = mlflow.create_experiment(experiment_name)
except:
    current_experiment=dict(mlflow.get_experiment_by_name(experiment_name)) 
    experiment_id=current_experiment['experiment_id']

# Some prints just for fun
print("experiment_name :",experiment_name)
print("experiment_id : ",experiment_id)
