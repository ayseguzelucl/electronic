# The following functions are metrics used to evaluate the performance
def calculate_confusion_matrix_elements(y_true, y_pred):
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    return tn, fp, fn, tp

def calculate_accuracy(tp, tn, fp, fn):
    return (tp + tn) / (tp + tn + fp + fn)

def calculate_precision(tp, fp):
    return tp / (tp + fp) if (tp + fp) != 0 else 0

def calculate_recall(tp, fn):
    return tp / (tp + fn) if (tp + fn) != 0 else 0

def calculate_f1(tp, fp, fn):
    precision = calculate_precision(tp, fp)
    recall = calculate_recall(tp, fn)
    return 2 * (precision * recall) / (precision + recall) if (precision + recall) != 0 else 0

def calculate_f2(tp, fp, fn):
    precision = calculate_precision(tp, fp)
    recall = calculate_recall(tp, fn)
    return 5 * (precision * recall) / (4 * precision + recall) if (4 * precision + recall) != 0 else 0

def calculate_r2(y_true, y_pred):
    
    return r2_score(y_true, y_pred)

def calculate_sensitivity(tp, fn):
    return calculate_recall(tp, fn)

def calculate_positive_predictive_value(tp, fp):
    return calculate_precision(tp, fp)

def calculate_negative_predictive_value(tn, fn):
    return tn / (tn + fn) if (tn + fn) != 0 else 0

def calculate_all_metrics(y_true, y_pred, device, model):
    tn, fp, fn, tp = calculate_confusion_matrix_elements(y_true, y_pred)
    
    accuracy = calculate_accuracy(tp, tn, fp, fn)
    precision = calculate_precision(tp, fp)
    recall = calculate_recall(tp, fn)
    f1 = calculate_f1(tp, fp, fn)
    f2 = calculate_f2(tp, fp, fn)
    r2 = calculate_r2(y_true, y_pred)
    sensitivity = calculate_sensitivity(tp, fn)
    ppv = calculate_positive_predictive_value(tp, fp)
    npv = calculate_negative_predictive_value(tn, fn)
    
    metrics = {
        'Device': [device],
        'Model': [model],
        'Accuracy': [accuracy],
        'Precision': [precision],
        'Recall': [recall],
        'F1 Score': [f1],
        'F2 Score': [f2],
        'R^2 Score': [r2],
        'Sensitivity': [sensitivity],
        'PPV': [ppv],
        'NPV': [npv],
    }
    
    return pd.DataFrame(metrics)
    
    
    
# The following is used to process the data    
def run_experiment(x_data, y_data, device, model):
    
    """
    
       Description:
       
           The following is used to process the data. 
           in case where the testing set is the 1 week timeseries, uncomment the test_data
           and also asjust the final evaluation of the predictor
           
       Input Args:
       
          - x_data, y_data from sequences
          - device, and model used
          
    """  
      
    x_train, x_val, y_train, y_val = train_test_split(x_data, y_data, test_size=0.2, shuffle=True)
    # x_test , y_test = x_week, y_week
    if model == "SVM":
        clf = svm.SVC()

        # Train the classifier
        clf.fit(x_train, y_train)

        # Predict labels for test   data
        y_pred = clf.predict(x_val)



    else:
        model = Sequential([
        Dense(256, activation='relu', input_shape=(len(x_data[0]),)),
        Dropout(0.1),
        Dense(256, activation='relu'),
        Dropout(0.1),
        Dense(256, activation='relu'),
        Dropout(0.1),
        Dense(256, activation='relu'),
        Dropout(0.1),
        Dense(256, activation='relu'),
        Dropout(0.1),
        Dense(256, activation='relu'),
        Dropout(0.1),
        Dense(256, activation='relu'),
        Dropout(0.1),
        Dense(256, activation='relu'),
        Dropout(0.1),
        Dense(256, activation='relu'),
        Dropout(0.1),
        Dense(1, activation='sigmoid'),
        ])

        early_stopping_monitor = EarlyStopping(monitor='val_loss', patience=20, restore_best_weights=True)

        model.compile(optimizer="adam",
                        loss='binary_crossentropy',
                        metrics=['accuracy'])
        history = model.fit(
            x_train, y_train,
            epochs=500,              
            batch_size=1,           
            validation_data=(x_val, y_val),
            callbacks=[early_stopping_monitor],  # Pass the early stopping callback to the fit method
            verbose=False
        )

        # Predict the validation data
        
        y_pred_prob = model.predict(x_val)
        y_pred = (y_pred_prob > 0.5).astype(int)

    return calculate_all_metrics(y_val, y_pred, device, model) 
    
    
    
    
    

def repeat_experiment(x_data, y_data, device,model, num_runs):
    """
       Use the following for several repetitions
    """
    all_metrics = []
    for _ in range(num_runs):
        metrics = run_experiment(x_data, y_data, device,model)
        all_metrics.append(metrics)

    # Convert metrics to numeric types
    all_metrics_numeric = []
    for metric in all_metrics:
        metric_numeric = metric.apply(pd.to_numeric, errors='ignore')
        all_metrics_numeric.append(metric_numeric)

    # Filter out non-numeric columns
    numeric_columns = [col for col in all_metrics_numeric[0] if pd.api.types.is_numeric_dtype(all_metrics_numeric[0][col])]
    all_metrics_numeric_filtered = [metric[numeric_columns] for metric in all_metrics_numeric]
    # Calculate average of each metric
    avg_metrics = pd.concat(all_metrics_numeric_filtered).groupby(level=0).mean()
    return avg_metrics