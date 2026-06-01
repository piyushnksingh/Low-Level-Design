from abc import ABC, abstractmethod
from typing import final


class ModelTrainer(ABC):
    def __init_subclass__(cls, **kwargs): # Enforcing overriding at runtime
        super().__init_subclass__(**kwargs)
        if "train_pipeline" in cls.__dict__:
            raise TypeError(
                f"{cls.__name__} cannot override final method train_pipeline"
            )

    @staticmethod
    def load_data(path):
        print(f"[Common] Loading dataset from {path}")
        # e.g., read CSV, images, etc.

    @staticmethod
    def preprocess_data():
        print("[Common] Splitting into train/test and normalizing")

    @abstractmethod
    def train_model(self):
        pass

    @abstractmethod
    def evaluate_model(self):
        pass

    # Default implementation (optional to override)
    def save_model(self):
        print("[Common] Saving model to disk as default format")

    @final # prevents overriding in static analysis tools like mypy or PyCharm, but not at runtime.
    def train_pipeline(self, data_path):
        self.load_data(data_path)
        self.preprocess_data()
        self.train_model()
        self.evaluate_model()
        self.save_model()


class NeuralNetworkTrainer(ModelTrainer):
    def train_model(self):
        print("[NeuralNet] Training Neural Network for 100 epochs")
        # pseudo-code: forward/backward passes, gradient descent...

    def evaluate_model(self):
        print("[NeuralNet] Evaluating accuracy and loss on validation set")

    def save_model(self):
        print("[NeuralNet] Serializing network weights to .h5 file")


class DecisionTreeTrainer(ModelTrainer):
    def train_model(self):
        print("[DecisionTree] Building decision tree with max_depth=5")

    def evaluate_model(self):
        print("[DecisionTree] Computing classification report (precision/recall)")

def main():
    print("=== Neural Network Training ===")
    nn_trainer = NeuralNetworkTrainer()
    nn_trainer.train_pipeline("data/images/")

    print("\n=== Decision Tree Training ===")
    dt_trainer = DecisionTreeTrainer()
    dt_trainer.train_pipeline("data/iris.csv")


if __name__ == "__main__":
    main()