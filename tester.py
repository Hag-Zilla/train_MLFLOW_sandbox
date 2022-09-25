import mlflow


# Set the path of .mlruns
path = "/home/ubuntu/train_DST_MLFLOW/mlruns" 
mlflow.set_tracking_uri("file://"+ path)
print("URI for mlruns : ",mlflow.get_tracking_uri() )


experiment_name = "ElasticNet" 

try:
    experiment_id = mlflow.create_experiment(experiment_name)
except:
    current_experiment=dict(mlflow.get_experiment_by_name(experiment_name)) 
    experiment_id=current_experiment['experiment_id']

print("experiment_name :",experiment_name)
print("experiment_id : ",experiment_id)
