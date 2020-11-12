# -*- coding: utf-8 -*-
"""
Created on  Nov.2020

@author: JM
"""

class PD(object):

    def __init__(self, df,discrete_variable,loan_status):
        self.df = df
        self.discrete_variable = discrete_variable
        self.loan_status = loan_status

    def WOE(df,discrete_variable,loan_status):
        """

        This is a function used to calculated the weight of evidence.
        
        Formula: WOE=ln(distribution of good/distribution of bad)
          -Distribution of Goods - % of Good Customers in a particular group
          -Distribution of Bads - % of Bad Customers in a particular group

        """
        df = pd.concat([df[discrete_variable],loan_status],axis=1)
        df = pd.concat([df.groupby(df.columns.values[0], as_index = False)[df.columns.values[1]].count(),
                        df.groupby(df.columns.values[0], as_index = False)[df.columns.values[1]].mean()], axis = 1)
        df = df.iloc[:, [0, 1, 3]] #after merge the column will have the same df,delete one
        df.columns = [df.columns.values[0], 'n_obs', 'prop_good'] #rename columns


        df['prop_n_obs'] = df['n_obs'] / df['n_obs'].sum()

        df['n_good'] = df['prop_good'] * df['n_obs']
        df['n_bad'] = (1 - df['prop_good']) * df['n_obs']

        df['prop_n_good'] = df['n_good'] / df['n_good'].sum()
        df['prop_n_bad'] = df['n_bad'] / df['n_bad'].sum()

        df['WoE'] = np.log(df['prop_n_good'] / df['prop_n_bad'])

        return df

    def IV(df,discrete_variable,loan_status):
        """
        This is a function to calculate the information value.
        
        Formula: IV = ∑ (% of non-events - % of events) * WOE

        Purpose: select important variables in a predictive model

        """
        df['diff_prop_good'] = df['prop_good'].diff().abs()
        df['diff_WoE'] = df['WoE'].diff().abs()
        df['IV'] = (df['prop_n_good'] - df['prop_n_bad']) * df['WoE']
        df['IV'] = df['IV'].sum()
        
        return df
    
    def plot_by_woe(df_WoE, rotation_of_x_axis_labels = 0):
        x = np.array(df_WoE.iloc[:, 0].apply(str))
        # Turns the values of the column with index 0 to strings, makes an array from these strings, and passes it to variable x.
        y = df_WoE['WoE']
        # Selects a column with label 'WoE' and passes it to variable y.
        plt.figure(figsize=(18, 6))
        # Sets the graph size to width 18 x height 6.
        plt.plot(x, y, marker = 'o', linestyle = '--', color = 'k')
        # Plots the datapoints with coordiantes variable x on the x-axis and variable y on the y-axis.
        # Sets the marker for each datapoint to a circle, the style line between the points to dashed, and the color to black.
        plt.xlabel(df_WoE.columns[0])
        # Names the x-axis with the name of the column with index 0.
        plt.ylabel('Weight of Evidence')
        # Names the y-axis 'Weight of Evidence'.
        plt.title(str('Weight of Evidence by ' + df_WoE.columns[0]))
        # Names the grapth 'Weight of Evidence by ' the name of the column with index 0.
        plt.xticks(rotation = rotation_of_x_axis_labels)
        # Rotates the labels of the x-axis a predefined number of degrees.