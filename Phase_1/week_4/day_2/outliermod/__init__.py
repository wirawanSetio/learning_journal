import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams

from feature_engine.outliers import Winsorizer

# must be numerical
def outlier_graph(df,size=(15,20),title='Outliers Graphic'):
    
    length = len(df.columns)
    list_val = list(df.columns)
 
    fig,ax = plt.subplots(int(length),2,figsize=size)

    
    fig.suptitle(title,fontsize=24, y=.94)
    fig.subplots_adjust(top=.9)
    fig.subplots_adjust(hspace=.6)

    row = 0
 
    for col in list_val:

        sns.boxplot(x=df[col], ax=ax[row,0])
        ax[row,0].set_title(col + " Box Plot",fontsize= 16)
         
        sns.histplot(x=df[col], kde=True,ax=ax[row,1])
        ax[row,1].set_title(col + " Distribution",fontsize= 16)

        row +=1



# regroup columns by skewness
def skewness(df):
    # list for output, each column will be put inside according to its distribution
    normal = []
    left_skew = []
    right_skew = []
    left_skew_ext = []
    right_skew_ext = []
    
    # all column features
    cols = list(df.columns)
    
    # Define every distribution by its skewness 
    for col in cols:
        skew = df[col].skew()
        if skew > 1 or skew < -1: # Define skew extreme if skewness > 1 or skewness < -1
            if skew < -1:
                left_skew_ext.append(col)
            else:
                right_skew_ext.append(col)
        elif (skew >= -0.5 and skew <= 0.5): # Define normal if skewness < 0.5 and skewness > -0.5
            normal.append(col)
        else: # Define normal if skewness < 0.5 or skewness > -0.5
            if skew < -0.5:
                left_skew.append(col)
            else:
                right_skew.append(col)
    
    #return the list
    return {'normal':normal,'left_skew':left_skew,'left_skew_ext':left_skew_ext,'right_skew':right_skew,'right_skew_ext':right_skew_ext}

# define boundaries on skew distribution feature
def find_skewed_boundaries(df, variable,skewed):
    extreme = ['left_skew_ext','right_skew_ext']
    distance = 3 if skewed in  extreme else 1.5
    quantile = (0.05 if skewed in  extreme else 0.25, 0.95 if skewed in  extreme else 0.75)
    IQR = df[variable].quantile(0.75) - df[variable].quantile(0.25)

    lower_boundary = df[variable].quantile(quantile[0]) - (IQR * distance)
    upper_boundary = df[variable].quantile(quantile[1]) + (IQR * distance)

    return upper_boundary, lower_boundary
# define boundaries on normal distribution feature
def find_normal_boundaries(df, variable):
    upper_boundary = df[variable].mean() + 2 * df[variable].std()
    lower_boundary = df[variable].mean() - 2 * df[variable].std()

    return upper_boundary, lower_boundary

# Check outliers based on the feature distribution using output of skewness function
def outliersCheck(df,obj_skew):
    data_outliers ={}
    for k,v in obj_skew.items():
        # if distribution normal, use find_normal_boundaries
        if k == 'normal':
            if len(v) <= 0: # if there is no feature with normal distribution next loop
                continue
            else:
                for val in v:# if there are some feature, loop the features and check 1 by 1 
                    up_p,low_p = find_normal_boundaries(df,val)
                    l_data = len(df[(df[val]> up_p)  | (df[val] < low_p)])
                    print("feature name : ",val)
                    print("outliers percentage : "+'{:.1%}'.format(l_data/len(df)))
                    print('distribution',k)
                    print('upper :',up_p,'lower :',low_p)
                    print("****************************************************")
                    data_outliers[val] = {'distribution':k,'outliers':l_data/len(df)}
        # if distribution not normal, use find_skewed_boundaries
        else: 
            if len(v) <= 0: # if there is no feature in this distribution next distribution
                continue
            else: # if there are some feature, loop the features and check 1 by 1 
                for val in v:
                    up_p,low_p = find_skewed_boundaries(df,val,k)
                    l_data = len(df[(df[val] > up_p) | (df[val] < low_p)])
                    print('feature name : ',val)
                    print("outliers percentage : "+'{:.1%}'.format(l_data/len(df)))
                    print('distribution',k)
                    print('upper :',up_p,'lower :',low_p)
                    print("****************************************************")
                    data_outliers[val] = {'distribution':k,'outliers':l_data/len(df)}
        if not data_outliers:
            print ("No Outliers Detected")
    return data_outliers

# cesoring outlier using cap method, with Winsorizer
def censoring_outliers(df,outliers,extreme_measure = 0):
    x_train_clean = None
    idx = 0
    fold_num = 0

        
    for key,val in outliers.items():
        
        if val['outliers'] > 0 :
            if val['distribution'] != 'normal':
                distribute =  val['distribution'].split('_')
                
                if extreme_measure == 0:
                    if len(distribute) < 3:
                        fold_num=1.5
                    else:
                        fold_num = 3
                else:
                    fold_num = extreme_measure
                
                capper = Winsorizer(capping_method='iqr' if len(distribute) < 3 else 'quantiles', # choose iqr for IQR rule boundaries or gaussian for mean and std
                                    tail=distribute[0], # cap left, right or both tails 
                                    fold=fold_num,
                                    variables=key)
            else :
                capper = Winsorizer(capping_method='gaussian', # choose iqr for IQR rule boundaries or gaussian for mean and std
                                    tail='both', # cap left, right or both tails 
                                    fold=2,
                                    variables=key) # variable columns
            
            if idx == 0:
                capper.fit(df)
                x_train_clean = capper.transform(df)
            else:
                capper.fit(x_train_clean)
                x_train_clean = capper.transform(x_train_clean)
            idx +=1

    return df if x_train_clean is None else x_train_clean


    
    