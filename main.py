from evalfeel import *
from abox import *


if __name__ == '__main__':
    # abf = ABoxFiller('csv/emotions_df.csv', 'csv/stats_emotions.csv', 'ontologies/emotions_modif.rdf')
    # abf.fill()
    f = EvalFeel()
    f.make_all_stats('csv/emotions_df.csv')
