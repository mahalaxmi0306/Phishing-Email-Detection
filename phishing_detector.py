import pandas as pd
import re

# Load dataset
data = pd.read_csv("emails.csv")

# Features and labels
X = data["text"]
y = data["label"]

# Convert text into numerical form
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer()

X_vectorized = vectorizer.fit_transform(X)

# Split dataset
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X_vectorized,
    y,
    test_size=0.2,
    random_state=42
)

# Train model
from sklearn.linear_model import LogisticRegression

model = LogisticRegression()

model.fit(X_train, y_train)

# Accuracy
accuracy = model.score(X_test, y_test)

# Predictions for confusion matrix
from sklearn.metrics import confusion_matrix

y_pred = model.predict(X_test)

cm = confusion_matrix(y_test, y_pred)

# Heading
print("===================================")
print(" PHISHING EMAIL DETECTION SYSTEM ")
print("===================================")

# Accuracy
print("\nModel Accuracy:", round(accuracy * 100, 2), "%")

# Confusion Matrix
print("\nConfusion Matrix:")
print(cm)

# Suspicious words
suspicious_words = [

    # Urgency words
    "urgent",
    "immediately",
    "now",
    "quick",
    "hurry",
    "action required",

    # Banking/security words
    "verify",
    "password",
    "bank",
    "login",
    "account",
    "otp",

    # Scam words
    "click",
    "reward",
    "offer",
    "free",
    "winner",
    "claim"
]

# Continuous checking
while True:

    print("\nEnter Email Text:")
    user_email = input()

    # Convert input
    user_vector = vectorizer.transform([user_email])

    # ML prediction
    prediction = model.predict(user_vector)[0]

    # Suspicious score
    score = 0

    # Keyword checking
    for word in suspicious_words:
        if word in user_email.lower():
            score += 1

    # URL detection
    urls = re.findall(r'https?://\S+|www\.\S+', user_email)

    if len(urls) > 0:
        score += 2

    # Final decision
    if score >= 3:
        final_prediction = "phishing"
    else:
        final_prediction = prediction

    # Output
    print("\nPrediction:", final_prediction)

    # Show detected URL
    if len(urls) > 0:
        print("Suspicious URL Detected!")

    # Continue?
    again = input("\nCheck another email? (yes/no): ")

    if again.lower() != "yes":
        print("\nSystem Closed.")
        break