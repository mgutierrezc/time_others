# visualizes a player's choices for a specific task over a range of rounds
# Author: Eli Pandolfo, epandolf@ucsc.edu

from sys import argv
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.lines import Line2D
style.use('./elip12.mplstyle')

# pulls data for one player from the csv otree spits out,
# and reformats it to have rounds as rows and each round's data in the cols
def format_df(player_id, data):
    
    df1 = data.loc[player_id, 'RiskAndFairness_oTree.1.player.id_in_group':]

    # there are 29 variables that get recorded per round
    cols = [str(index).split('.')[-1] for index in df1[:][:29].index]
    df2 = pd.DataFrame(columns=cols)
    i = 0
    for i in range(0, df1.shape[0], 29):
        row_dict = {'round': i / 29 + 1}
        for j in range(29):
            row_dict[cols[j]] = [df1[i + j]]
        row_df = pd.DataFrame(row_dict)
        df2 = df2.append(row_df)
    
    df2['round'] = df2['round'].astype(int)
    df2.set_index('round', inplace=True)
    
    return df2

# plots a separate graph for each probability round
def plot_prob(csv, player_id, df, show=False):

    for i, row in df.iterrows():
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_aspect(aspect='equal')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.axis([-2, 102, -2, 102])
        plt.xlabel('You', color='#848484')
        plt.ylabel('Partner', color='#848484')
        date, session = csv.split('_')[0], csv.split('_')[1]
        plt.title(date.capitalize() + ' ' + session.capitalize() + ' ' + player_id.capitalize() + ' Probability - Decision ' + str(i % 10))

        size_a = 7 * row['prob_a']
        size_b = 7 * row['prob_b']

        ax.plot([row['ax'], row['bx']], [row['ay'], row['by']], color='#b2b2b2', zorder=3, alpha=1, linewidth=.5)

        ax.scatter([row['ax']], [row['ay']], color='#eb860d', zorder=4, alpha=.75, s=size_a)
        ax.text(row['ax'] + 5, row['ay'] - 5, 'Outcome A: ' + str(row['prob_a']) + '%')
        
        ax.scatter([row['bx']], [row['by']], color='#eb860d', zorder=4, alpha=.75, s=size_b)
        ax.text(row['bx'] + 5, row['by'] + 5, 'Outcome B: ' + str(row['prob_b']) + '%')

        if show == True:
            plt.show()
        else:
            plt.savefig(date.capitalize() + '_' + session.capitalize() + '_'
                + player_id.capitalize() + '_Probability_Decision-' + str(i % 10) + '.png', format='png', dpi=250)

# plots the choices a given player made for a given mode
# for now were doing it with all one color. later we will implement different colors for different probabilities
# also implement multiple graphs for each round of probability
# display: gray (default), color, coded
def plot_data(csv, player_id, data, mode, display='color', show=False):
    
    df = format_df(player_id, data)
    df = df[df['mode'] == mode]

    if mode == 'probability':
        plot_prob(csv, player_id, df, show=show)
    else:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_aspect(aspect='equal')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.axis([-2, 102, -2, 102])
        plt.xlabel('State A', color='#848484')
        plt.ylabel('State B', color='#848484')
        date, session = csv.split('_')[0], csv.split('_')[1]
        plt.title(date.capitalize() + ' ' + session.capitalize() + ' ' + player_id.capitalize() + ' ' + mode.capitalize())

        if display not in ['gray', 'color', 'coded']:
            print("Invalid display argument, defaulting to gray.")
            display = 'gray'

        if display == 'gray':
            lines = ['#b2b2b2']
            dots = ['#eb860d']
        else:
            lines = ['#60d515', '#d22b10', '#1fa8e4', '#e0cc05', '#eb860d', '#b113ef']
            dots = ['#60d515', '#d22b10', '#1fa8e4', '#e0cc05', '#eb860d', '#b113ef']
            if display == 'coded' and mode != 'det_giv':
                probs = {}
                i = 0
                leg_lines = []
                leg_key = []
                for _, row in df.iterrows():
                    if row['prob_a'] not in probs:
                        probs[row['prob_a']] = lines[i % len(lines)]
                        leg_lines.append(Line2D([0], [0], color=probs[row['prob_a']], linewidth=.5))
                        leg_key.append('State A: ' + str(row['prob_a']) + '%')
                        i += 1
                ax.legend(leg_lines, leg_key)


        if mode == 'det_giv':
            for i, row in df.iterrows():
                ax.plot([row['m'] / row['px'], 0], [0, row['m'] / row['py']], color=lines[i % len(lines)], alpha=0.55, zorder=3, linewidth=.5)
                ax.scatter(row['me_a'], row['me_b'], color=dots[i % len(dots)], alpha=.6, zorder=4)
            plt.xlabel('You', color='#848484')
            plt.ylabel('Partner', color='#848484')

        else:
            for i, row in df.iterrows():
                if display != 'coded':
                    line = lines[i % len(lines)]
                    dot = dots[i % len(dots)]
                else:
                    line = probs[row['prob_a']]
                    dot = line
                ax.plot([row['m'] / row['px'], 0], [0, row['m'] / row['py']], color=line, alpha=0.55, zorder=3, linewidth=.5)
                
                if mode == 'sec_2bl_1ch':
                    ax.plot([0, row['m'] / row['py']], [row['m'] / row['px'], 0], color=line, alpha=0.55, zorder=3, linewidth=.5)
                
                if mode != 'sec_otherrisk_ownfixed':
                    ax.scatter(row['me_a'], row['me_b'], color=dot, alpha=.6, zorder=4)
                
                if mode in ['sec_1bl_1ch', 'sec_1bl_2ch', 'sec_2bl_1ch', 'sec_otherrisk_ownfixed']:
                    ax.scatter(row['partner_a'], row['partner_b'], color=dot, marker='s', alpha=.6, zorder=4)

        if show == True:
            plt.show()
        else:
            plt.savefig(date.capitalize() + '_' + session.capitalize() + '_'
                + player_id.capitalize() + '_' + mode.capitalize() + '_' + display + '.png', format='png', dpi=250)

# lets the user specify their input with command line arguments
if len(argv) > 1:
    csv = str(argv[1])
    leeps_id = str(argv[2])
    df = pd.read_csv(csv, index_col='participant.label')
    mode = str(argv[3])
    if len(argv) > 4:
        display = str(argv[4])
        if len(argv) > 5:
            show = bool(argv[5])
    plot_data(csv.split('.')[0], leeps_id, df, mode, display=display, show=show)
else: # for testing purposes
    df = pd.read_csv('data/anna_test.csv', index_col='participant.label')
    plot_data('data/anna_test.csv'.split('.')[0], 'LEEPS_1', df, 'det_giv', display='gray', show=True)




