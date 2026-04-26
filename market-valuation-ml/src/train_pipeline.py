from src.features import create_training_set
from src.train_gbm import train_gbm


def train_pipeline():
    create_training_set()
    train_gbm()


if __name__ == "__main__":
    train_pipeline()
