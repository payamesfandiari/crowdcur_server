
from sklearn.base import RegressorMixin,BaseEstimator
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np
from . import learner
from operator import itemgetter
from sklearn.preprocessing import scale,normalize


class WorkerModel(BaseEstimator,RegressorMixin):
    """
    A very simple Worker Model
    """
    def __init__(self,k_questions=3,preferences=None,columns=None):
        self.k_questions = k_questions
        self.preferences = preferences
        self.columns = columns
        self.obj_cols = None
        self.mod = None
        self.coef_ = None
        self.intercept_ = None

    def clean_x(self,X):
        _x = self._clean_X(X)
        _x = self._transform_X(_x)
        _x = self._std(_x)
        return _x

    def _clean_X(self,X):
        if isinstance(X,pd.DataFrame):
            return X
        if self.columns is None:
            raise NotImplementedError()
        cols = [c for c,i in sorted(self.columns.items(),key=itemgetter(1))]
        return pd.DataFrame(X,columns=cols)

    def _transform_X(self,X):
        object_cols = []
        for t,c in X.dtypes.iteritems():
            if not np.issubdtype(c, np.number):
                object_cols.append(t)
        self.obj_cols = object_cols
        _x = pd.get_dummies(X)
        self.columns = {c:i for i,c in enumerate(_x.columns)}
        return _x

    def _std(self,X):
        return pd.DataFrame(scale(X),columns=X.columns)

    def fit(self,X,y=None):
        x = self.clean_x(X)
        con = learner.Constraints(columns=self.columns)

        if self.preferences is not None:
            for k in self.obj_cols:
                if k in self.preferences:
                    self.preferences.pop(k)
            con.add_constraint(self.preferences)

        alpha, f1_s = learner.find_alpha(x, y, m=learner.Learning, scorer=mean_squared_error,
                                         cons=con.get_constraint())

        mod = learner.Learning(x, y, alpha=alpha, cons=con.get_constraint())
        mod.fit()
        self.mod = mod
        self.coef_,self.intercept_ = mod.get_coef()
        return self

    def get_raw_factor_scores(self):
        return {u: self.coef_[i] for i, u in enumerate(self.columns)}

    def get_factor_scores(self):
        raw_factor_scores = self.get_raw_factor_scores()
        out_factor_scores = {}
        sc = {}
        for obj in self.obj_cols:
            sc[obj] = []
            for factor in raw_factor_scores:
                if obj in factor:
                    sc[obj].append(factor)
        for k in sc:
            temp = 0
            for v in sc[k]:
                temp += raw_factor_scores[v]
                raw_factor_scores.pop(v)
            out_factor_scores[k] = temp

        for k in raw_factor_scores:
            out_factor_scores[k] = raw_factor_scores[k]
        return out_factor_scores

    def get_loss(self,X,y):
        x = self.clean_x(X)
        return mean_squared_error(y,self.mod.predict(x))

