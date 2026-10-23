cat = Pipeline([
("imputer", SimpleImputer(strategy="most_frequent")),
("encoder", OneHotEncoder(
handle_unknown="ignore", sparse_output=False)),
])
a = cat.fit_transform(X_train[CAT])
b = cat.transform(X_valid[CAT])
print(a.shape, b.shape)
print(cat.named_steps["encoder"].categories_[0].tolist())