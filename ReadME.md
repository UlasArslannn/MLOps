
## Project Structure for MLOps Project for bash 

mkdir -p \
data/raw data/processed data/external \
notebooks \
src/data,features,models,utils \
app \
configs \
scripts \
tests \
.github/workflows \
docker \
great_expectations \
mlruns \
artifacts



## Project Structure for MLOps Project for powershell

New-Item -ItemType Directory -Force -Path @(
    "data/raw",
    "data/processed", 
    "data/external",
    "notebooks",
    "src/data",
    "src/features",
    "src/models",
    "src/utils",
    "app",
    "configs",
    "scripts",
    "tests",
    ".github/workflows",
    "docker",
    "great_expectations",
    "mlruns",
    "artifacts"
)


## For downloading the requirements.txt file and installing the dependencies

python -m venv .venv
source .venv/Scripts/activate
pip install --upgrade pip
uv pip install -r requirements.txt




## Optuna Example for cnn 

import optuna
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split

# Örnek veri (sizin veri setiniz olacak)
# X_train, X_test, y_train, y_test = ...

def create_cnn_model(trial):
    """Optuna ile optimize edilecek CNN modeli"""
    
    # 1. Hyperparameter'ları Optuna'dan al
    n_conv_layers = trial.suggest_int("n_conv_layers", 2, 5)
    n_filters_base = trial.suggest_categorical("n_filters_base", [32, 64, 128])
    kernel_size = trial.suggest_categorical("kernel_size", [3, 5])
    dropout_rate = trial.suggest_float("dropout_rate", 0.2, 0.5)
    learning_rate = trial.suggest_float("learning_rate", 1e-5, 1e-2, log=True)
    n_dense_units = trial.suggest_int("n_dense_units", 64, 512)
    use_batch_norm = trial.suggest_categorical("use_batch_norm", [True, False])
    
    # 2. Modeli oluştur
    model = keras.Sequential()
    
    # Input layer
    model.add(layers.Input(shape=(28, 28, 1)))  # Örnek: MNIST
    
    # Convolutional layers (sayısı dinamik)
    for i in range(n_conv_layers):
        n_filters = n_filters_base * (2 ** i)  # 32, 64, 128, 256...
        
        model.add(layers.Conv2D(
            filters=n_filters,
            kernel_size=kernel_size,
            activation='relu',
            padding='same'
        ))
        
        if use_batch_norm:
            model.add(layers.BatchNormalization())
        
        model.add(layers.MaxPooling2D(pool_size=2))
        model.add(layers.Dropout(dropout_rate))
    
    # Flatten
    model.add(layers.Flatten())
    
    # Dense layers
    model.add(layers.Dense(n_dense_units, activation='relu'))
    model.add(layers.Dropout(dropout_rate))
    
    # Output layer
    model.add(layers.Dense(10, activation='softmax'))  # 10 sınıf için
    
    # 3. Compile
    optimizer = keras.optimizers.Adam(learning_rate=learning_rate)
    model.compile(
        optimizer=optimizer,
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model


def objective(trial):
    """Optuna objective fonksiyonu"""
    
    # Model oluştur
    model = create_cnn_model(trial)
    
    # Batch size'ı da optimize edebilirsiniz
    batch_size = trial.suggest_categorical("batch_size", [32, 64, 128])
    epochs = 10  # Hızlı test için az epoch
    
    # Early stopping (zaman kazanmak için)
    early_stopping = keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=3,
        restore_best_weights=True
    )
    
    # Train
    history = model.fit(
        X_train, y_train,
        batch_size=batch_size,
        epochs=epochs,
        validation_split=0.2,
        callbacks=[early_stopping],
        verbose=0  # Sessiz mod
    )
    
    # Validation accuracy'yi döndür (Optuna bunu maksimize edecek)
    val_accuracy = max(history.history['val_accuracy'])
    
    return val_accuracy


# Optuna study oluştur
study = optuna.create_study(direction='maximize')

# Optimize et
study.optimize(objective, n_trials=50)

# En iyi parametreleri al
print("En iyi parametreler:")
print(study.best_params)
print(f"En iyi validation accuracy: {study.best_value:.4f}")

# En iyi modeli tekrar oluştur
best_trial = study.best_trial
best_model = create_cnn_model(best_trial)