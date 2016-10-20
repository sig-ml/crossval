#!/usr/bin/env python
import os
import pandas as pd
from sklearn.datasets import make_classification
import sys


def make_dataset(**kwargs):
    x, y = make_classification(**kwargs)
    df = pd.DataFrame(x)
    df.columns = ['Feature'+str(i) for i in df.columns]
    df['target'] = y
    print('Splitting into train test')
    mask = pd.np.random.random(len(df)) < 0.8
    train, test = df[mask], df[~mask]
    ground = test[['target']]
    test = test.drop('target', axis=1)
    return ground, train, test

def upload_dataset(ground, train, test):
    from django.core.files import File
    with open(filepath, 'wb+') as doc_file:
       doc.documen.save(filename, File(doc_file), save=True)

if __name__ == "__main__":
    #os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crossval.settings")
    kwargs = dict(n_samples=10000,
            n_features=10,
            n_informative=8,
            n_redundant=2,
            n_clusters_per_class=5,
            weights=[0.7, 0.3],
            flip_y=0.2
            )

    ground, train, test = make_dataset(**kwargs)
    #upload_dataset(ground, train, test)
    print('Saving')
    ground.to_csv('ground.csv', index=False)
    train.to_csv('train.csv', index=False)
    test.to_csv('test.csv', index=False)
