import mlflow 

# prédéfinit le chemin où vous souhaitez stocker vos sauvegardes des runs 
path = "/home/ubuntu/mlruns" 

mlflow.set_tracking_uri("file://"+ path)

print(mlflow.get_tracking_uri() )
