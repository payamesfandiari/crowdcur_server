import pandas as pd
import numpy as np
import itertools
from scipy.optimize import minimize
from sklearn.linear_model.logistic import _logistic_loss_and_grad,_logistic_loss
from sklearn.utils.extmath import softmax
from sklearn.model_selection import train_test_split, KFold
from sklearn import metrics


class Constraints:
    def __init__(self,columns):
        self.all_constraints = []
        self.columns = columns

    def gen_col_ind_map(self):
        out = {}
        for i, c in enumerate(self.columns):
            out[c] = i
        return out

    def gen(self,i, j):
        return {'type': 'ineq', 'fun': eval('lambda x: np.array([x[{0}]-x[{1}]-0.01])'.format(i, j))}

    def add_constraint(self,rankings):
        for a,b in itertools.combinations(rankings,2):
            if (a,b) in self.all_constraints or (b,a) in self.all_constraints:
                continue
            else:
                self.all_constraints.append((a,b))

    def get_constraint(self):
        if self.columns is None:
            return ()
        if len(self.all_constraints) < 1:
            return ()
        constraints = []
        col_to_ind_map = self.gen_col_ind_map()
        for a,b in self.all_constraints :
            if a in col_to_ind_map and b in col_to_ind_map:
                constraints.append(self.gen(col_to_ind_map[a],col_to_ind_map[b]))
        return tuple(constraints)


class Learning:
    def __init__(self,data,y_data,cons=(),alpha=0.1):
        self.data = data.assign(intercept=1)
        self.data = self.data.values
        self.y = y_data
        self.cons = cons
        self.alpha = alpha
        self.dataTdata = np.dot(self.data.T,self.data)
        self.dataTy = 2 * np.dot(self.y,self.data)
        self.I = np.identity(self.data.shape[1])
        self.res = None

    def loss(self,w):
        return np.sum(np.square(np.dot(self.data, w) - self.y)) + self.alpha * np.dot(w, w.T)

    def gradient(self,w):
        return 2 * np.dot(w,(self.dataTdata + (self.alpha * self.I))) - self.dataTy

    def fit(self):
        w0 = np.zeros((self.data.shape[1]))
        self.res = minimize(self.loss,w0,jac=self.gradient,method='SLSQP',constraints=self.cons,options={'disp':False})
        return self

    def loss_x(self,w,x,y):
        d = x.assign(intercept=1)
        return np.sum(np.square(np.dot(d, w) - y)) + self.alpha * np.dot(w, w.T)

    def predict(self,X):
        if self.res is None :
            raise NotImplementedError()

        return np.dot(X,self.res.x[:-1]) + self.res.x[-1]

    def get_coef(self):
        return self.res.x[:-1],self.res.x[-1]

    def set_coef(self,coef,intercept):
        self.res.x[:-1] = coef
        self.res.x[-1] = intercept


class LearningLogLos:
    def __init__(self,data,y_data,cons=(),alpha=0.1):
        self.data = data.assign(intercept=1)
        self.y = y_data
        self.cons = cons
        self.alpha = alpha
        self.res = None
        self.classes_ = np.unique(y_data.values)

    @staticmethod
    def gradient(w, X, y, alpha):
        _, grad = _logistic_loss_and_grad(w,X,y,alpha)
        return grad

    def fit(self):
        w0 = np.zeros((self.data.shape[1]))
        self.res = minimize(_logistic_loss,w0,args=(self.data,self.y,self.alpha),
                            jac=self.gradient,method='SLSQP',
                            constraints=self.cons,options={'disp':False})
        return self

    def predict(self, X):
        if self.res is None :
            raise NotImplementedError()
        scores = np.dot(X,self.res.x[:-1]) + self.res.x[-1]
        indices = (scores > 0).astype(np.int)
        return self.classes_[indices]

    def get_coef(self):
        return self.res.x[:-1],self.res.x[-1]

    def set_coef(self,coef,intercept):
        self.res.x[:-1] = coef
        self.res.x[-1] = intercept

    def predict_proba(self,X):
        prob = np.dot(X, self.res.x[:-1]) + self.res.x[-1]
        prob *= -1
        np.exp(prob, prob)
        prob += 1
        np.reciprocal(prob, prob)
        if prob.ndim == 1:
            return np.vstack([1 - prob, prob]).T
        else:
            # OvR normalization, like LibLinear's predict_probability
            prob /= prob.sum(axis=1).reshape((prob.shape[0], -1))
            return prob


def find_alpha(x, y, m ,scorer=metrics.f1_score, cv=3, cons=()):
    cv_m = KFold(n_splits=cv)
    if not isinstance(y,np.ndarray):
        y = np.array(y)
    alpha = [0.0001, 0.001, 0.01, 0.1, 1, 10, 100,0]
    best_score = best_alpha = np.inf
    for a in alpha:
        score = 0
        for ind_train, ind_test in cv_m.split(x, y):
            mod = m(x.iloc[ind_train], y[ind_train], cons=cons, alpha=a)
            mod.fit()
            score += scorer(y[ind_test], mod.predict(x.iloc[ind_test]))
        score /= cv
        if score < best_score:
            best_score = score
            best_alpha = a
    return best_alpha, best_score

