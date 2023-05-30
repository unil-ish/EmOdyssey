from evalfeel import *
from abox import *

def main():
    """
        Main pipeline for the program
    """
    
    # (1) Import data, process data, find emotions and export them to csv
    ef = EvalFeel()
    ef.make_df_emotions() # emotions for each speech
    ef.make_all_stats() # make statistics
    
    # If needed, one can plot a single diagram for a single emotion
    # ef.make_diagram('joy')
    
    # (2) Re-import data and fill A-Box and export the ontology
    abf = ABoxFiller('csv/emotions_df.csv', 'csv/stats_emotions.csv', 'ontologies/emotions_modif.rdf')
    abf.fill()

if __name__ == '__main__':
    main()
