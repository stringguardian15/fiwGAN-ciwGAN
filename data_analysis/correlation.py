'''
Perform a correlation analysis to find z values the coincide with a feature on the output
In particular, find z values that correspond with sentence-initial consonants
'''
import matplotlib as plt
import numpy as np
import re
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix

class Z_Correlator:
    def __init__(self,text_grid_file, z_file, num_z_vals):
        self.atg = Annotated_TextGrid(text_grid_file)
        self.zt = Z_Trials(z_file,num_z_vals)
        self.rsq_vals = []
        self.linear_regression()
        self.z_to_rsq = []
        for z in range(num_z_vals):
            self.z_to_rsq.append((z,self.rsq_vals[z]))
        self.z_to_rsq = sorted(self.z_to_rsq,key=lambda x:-x[1])

        #Now try logistic regression
        self.logistic_scores = []
        self.z_to_logistic_scores = []
        self.logistic_regression()
        for z in range(num_z_vals):
            self.z_to_logistic_scores.append((z,self.logistic_scores[z]))
        self.z_to_logistic_scores = sorted(self.z_to_logistic_scores,key=lambda x:-x[1])

    def print_highest_scoring_z_vals(self,num_vals,score_type='linear'):
        if score_type == 'linear':
            for i in range(num_vals):
                print(self.z_to_rsq[i])
        elif score_type == 'logistic':
            for i in range(num_vals):
                print(self.z_to_logistic_scores[i])

    def linear_regression(self):
        for i in range(len(self.zt.trial_instance_by_z_val)):
            x = self.zt.trial_instance_by_z_val[i]
            x = np.array(x)
            x = x.reshape((-1,1))
            y = self.atg.consonants
            y = np.array(y)
            model = LinearRegression()
            model.fit(x,y)
            r_sq = model.score(x,y)
            self.rsq_vals.append(r_sq)

    def logistic_regression(self):
        for i in range(len(self.zt.trial_instance_by_z_val)):
            x = self.zt.trial_instance_by_z_val[i]
            x = np.array(x)
            x = x.reshape((-1,1))
            y = self.atg.consonants
            y = np.array(y)
            model = LogisticRegression(solver='liblinear',random_state=0,class_weight='balanced')
            model.fit(x,y)
            score_ = model.score(x,y)
            confusion_matrix_ = confusion_matrix(y,model.predict(x))
            #print(confusion_matrix_)
            self.logistic_scores.append(score_)

class Z_Trials:
    def __init__(self,z_file,num_z_vals):
        '''
        ** Initialize the object and parse the input file **
        :param file: a file consisting of a list of z values for 1 or more trials
        :param num_z_vals: the number of z values in each trial
        '''
        self.z_vals_by_trial = [] #a list of lists.
            #Outer list is of dimension |number of trials|
            #Inner list is of dimension |num_z_vals_by_trial|
        self.trial_instance_by_z_val = [] #another list of lists, but with weird dimensions
            #Outer list is num_z_vals
            #Inner list is num of trials.
            #Want a list organized by z values to make simple linear regression easier
        for i in range(num_z_vals):
            self.trial_instance_by_z_val.append([])
        z_counter = 1
        trial_num = 0
        with open(z_file,'r') as fi:
            for line in fi.readlines():
                z_val = float(line)
                self.trial_instance_by_z_val[z_counter - 1].append(z_val)
                if z_counter == 1:
                    self.z_vals_by_trial.append([])
                self.z_vals_by_trial[trial_num].append(z_val)
                if z_counter == num_z_vals:
                    z_counter = 1
                    trial_num += 1
                else:
                    z_counter += 1

class Annotated_TextGrid:
    def __init__(self,text_grid):
        '''
        ** Initialize the object and parse the input file **
        :param text_grid: Annotated TextGrid file (from praat)
        '''
        self.intervals = []
        self.texts = []
        intervals_re = '.*intervals \[([0-9]+)\].*'
        text_re = '.*text = "(.*)"'
        with open(text_grid,'r') as fi:
            for line in fi.readlines():
                if re.match(intervals_re,line):
                    m = re.match(intervals_re,line)
                    interval = m.group(1)
                    self.intervals.append(interval)
                elif re.match(text_re,line):
                    m = re.match(text_re,line)
                    text = m.group(1)
                    self.texts.append(text)
        self.consonants = self.mark_trials_for_consonants()

    def mark_trials_for_consonants(self):
        '''
        ** Return a list the same size as 'texts' but with only 1s or 0s **
        ** 1 means a consonant was found. 0 means not **
        :return: list of 0s and 1s corresponding to consonants in annotation
        '''
        output = []
        cons_re = '.*_[pkt]$'
        for val in self.texts:
            if re.match(cons_re,val):
                output.append(1)
            else:
                output.append(0)
        return output


def main():
    #atg = Annotated_TextGrid('epenthesis9403seed345_10_final.TextGrid')
    #zt = Z_Trials('epenthesis9403seed345_10.txt',100)
    zc_10 = Z_Correlator(text_grid_file='epenthesis9403seed345_10_final.TextGrid',
                         z_file='epenthesis9403seed345_10.txt',
                         num_z_vals=100)
    zc_01 = Z_Correlator(text_grid_file='epenthesis9403seed345_01chain_final.TextGrid',
                         z_file='epenthesis9403seed345_01.txt',
                         num_z_vals=100)
    print("10 highest scoring z values for 10 file:")
    zc_10.print_highest_scoring_z_vals(10)
    print("10 highest scoring z values for 01 file:")
    zc_01.print_highest_scoring_z_vals(10)
    print("10 highest scoring z values for 10 file (with logistic regression):")
    zc_10.print_highest_scoring_z_vals(10,score_type='logistic')
    print("10 highest scoring z values for 01 file (with logistic regression):")
    zc_01.print_highest_scoring_z_vals(100,score_type='logistic')

    ## Do logistic regression for both files appended
    scores = []
    for i in range(len(zc_01.zt.trial_instance_by_z_val)):
        x = zc_01.zt.trial_instance_by_z_val[i] + zc_10.zt.trial_instance_by_z_val[i]
        x = np.array(x).reshape((-1,1))
        y = zc_01.atg.consonants + zc_10.atg.consonants
        y = np.array(y)
        model = LogisticRegression(solver='liblinear', random_state=0, class_weight='balanced')
        model.fit(x, y)
        score_ = model.score(x, y)
        #confusion_matrix_ = confusion_matrix(y, model.predict(x))
        scores.append(score_)
    z_vals_to_scores = []
    for z in range(len(zc_01.zt.trial_instance_by_z_val)):
        z_vals_to_scores.append((z,scores[z]))
    z_vals_to_scores = sorted(z_vals_to_scores,key=lambda x:-x[1])
    print("z values for combined data:")
    num_z_vals = 100
    for i in range(num_z_vals):
        print(z_vals_to_scores[i])



if __name__ == '__main__':
    main()

