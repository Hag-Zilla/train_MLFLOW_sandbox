#############################################################################################################################
#                                                       train_diabetes                                                      #
#############################################################################################################################

# ================================================          Header           ================================================

"""

Title : train_diabetes.py
Init craft date : 30/09/2022
Handcraft with love and sweat by : Damien Mascheix @Hagzilla
Notes :
    MLflow model using ElasticNet (sklearn) and Plots ElasticNet Descent Paths

    Uses the sklearn Diabetes dataset to predict diabetes progression using ElasticNet
        The predicted "progression" column is a quantitative measure of disease progression one year after baseline
        http://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_diabetes.html
    Combines the above with the Lasso Coordinate Descent Path Plot
        http://scikit-learn.org/stable/auto_examples/linear_model/plot_lasso_coordinate_descent_path.html
        Original author: Alexandre Gramfort <alexandre.gramfort@inria.fr>; License: BSD 3 clause

    Usage:
    python train_diabetes.py 0.01 0.01
    python train_diabetes.py 0.01 0.75
    python train_diabetes.py 0.01 1.0

"""
# ================================================       Optimisations        ================================================

""" 
Blablabla

"""

# ================================================    Modules import     =====================================================

# Script timing
import time
start_time = time.time()

# Classics
import warnings
import sys
import pandas as pd
import numpy as np
import logging
from itertools import cycle

# URL management
from urllib.parse import urlparse

# MLFLOW
import mlflow
import mlflow.sklearn


# Modeling
from sklearn.linear_model import lasso_path, enet_path
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from sklearn import datasets

#VIZ
import matplotlib.pyplot as plt

# ================================================          Functions          ================================================

# Evaluate metrics
def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2

# ================================================          Warfield          ================================================

# Logger section
logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)

# Warning configuration
warnings.filterwarnings("ignore")

# Set the seed
np.random.seed(40)


if __name__ == "__main__":

    # Users informations
    print("\n========== Start of run example ==========\n")

    # Storage mode configuration 
    storage_mode = 'file' # 'file' (in mlruns directory) or 'db' (in sqlite db)
    path = "/home/ubuntu/train_DST_MLFLOW/mlruns" 
    if storage_mode == 'file':
        mlflow.set_tracking_uri("file://"+ path)
    elif storage_mode == 'db':
        mlflow.set_tracking_uri("http://localhost:5000")
    # Just for debug
    print("Tracking URI : ",mlflow.get_tracking_uri())

    # Manage the experiment Ids names
    experiment_name = "ElasticNet_diabetes" 

    try:
        experiment_id = mlflow.create_experiment(experiment_name)
    except:
        current_experiment=dict(mlflow.get_experiment_by_name(experiment_name)) 
        experiment_id=current_experiment['experiment_id']

    print("experiment_name :",experiment_name)
    print("experiment_id : ",experiment_id)


    ####======= Data management =======####

    # Load Diabetes datasets
    diabetes = datasets.load_diabetes()
    X = diabetes.data
    y = diabetes.target

    # Create pandas DataFrame for sklearn ElasticNet linear_model
    Y = np.array([y]).transpose()
    d = np.concatenate((X, Y), axis=1)
    cols = diabetes.feature_names + ["progression"]
    data = pd.DataFrame(d, columns=cols)

    # Split the data into training and test sets. (0.75, 0.25) split.
    train, test = train_test_split(data)

    # The predicted column is "progression" which is a quantitative measure of disease progression one year after baseline
    train_x = train.drop(["progression"], axis=1)
    test_x = test.drop(["progression"], axis=1)
    train_y = train[["progression"]]
    test_y = test[["progression"]]

    alpha = float(sys.argv[1]) if len(sys.argv) > 1 else 0.1
    l1_ratio = float(sys.argv[2]) if len(sys.argv) > 2 else 0.8

    ####======= mlflow store =======####
    with mlflow.start_run(experiment_id =experiment_id):
        ####======= Modeling =======####
        lr = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42)
        lr.fit(train_x, train_y)
        predicted_qualities = lr.predict(test_x)
        (rmse, mae, r2) = eval_metrics(test_y, predicted_qualities)

        # Print out ElasticNet model metrics
        print("Elasticnet model (alpha=%f, l1_ratio=%f):" % (alpha, l1_ratio))
        print("  RMSE: %s" % rmse)
        print("  MAE: %s" % mae)
        print("  R2: %s" % r2)

        # Log mlflow attributes for mlflow UI
        mlflow.log_param("alpha", alpha)
        mlflow.log_param("l1_ratio", l1_ratio)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("mae", mae)
        mlflow.sklearn.log_model(lr, "model")

        # Compute paths
        eps = 5e-3  # the smaller it is the longer is the path

        print("Computing regularization path using the elastic net.")
        alphas_enet, coefs_enet, _ = enet_path(X, y, eps=eps, l1_ratio=l1_ratio)

        # Display results
        fig = plt.figure(1)
        ax = plt.gca()

        colors = cycle(["b", "r", "g", "c", "k"])
        neg_log_alphas_enet = -np.log10(alphas_enet)
        for coef_e, c in zip(coefs_enet, colors):
            l2 = plt.plot(neg_log_alphas_enet, coef_e, linestyle="--", c=c)

        plt.xlabel("-Log(alpha)")
        plt.ylabel("coefficients")
        title = "ElasticNet Path by alpha for l1_ratio = " + str(l1_ratio)
        plt.title(title)
        plt.axis("tight")

        # Save figures
        fig.savefig("ElasticNet-paths.png")

        # Close plot
        plt.close(fig)

        # Log artifacts (output files)
        mlflow.log_artifact("ElasticNet-paths.png")
        data.to_csv('/home/ubuntu/train_DST_MLFLOW/diabetes.txt', encoding = 'utf-8', index=False) 
        mlflow.log_artifact('/home/ubuntu/train_DST_MLFLOW/diabetes.txt') 

        print(mlflow.get_tracking_uri() )

        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        # Model registry does not work with file store
        if tracking_url_type_store != "file":

            # Register the model
            # There are other ways to use the Model Registry, which depends on the use case,
            # please refer to the doc for more information:
            # https://mlflow.org/docs/latest/model-registry.html#api-workflow
            mlflow.sklearn.log_model(lr, "model", registered_model_name="ElasticnetWineModel")
        else:
            mlflow.sklearn.log_model(lr, "model")
            # Users informations

    print(f"\nAll the data have been stored there : {mlflow.get_tracking_uri()}")
    print("\n========== End of run ==========")
    print("==========   %s seconds   ==========" % round((time.time() - start_time),2))