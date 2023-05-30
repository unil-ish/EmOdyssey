import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from unidecode import unidecode
from matplotlib_venn import venn3
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from tagtog2df.tagtog2df import allfiles_onedataframe
import senticnet
from pyfeel.pyFeel import Feel


class EvalFeel:
    """
    Class EvalFeel

    Initialization of global variables stopwords and punctuation.
    Creation of an instance of the class senticnet
    """
    stopwords_lst = list(set(stopwords.words('french')))
    stopwords_lst.extend(('l', 'le', 'la', 'd', 'm'))

    punctuation = [',', '.', ':', ';', '(', ')', '[', ']', '!', '?', '+', '-', '*', "'", '"', '/']
    annotation = {
        "e_8": "Fear",
        "e_3": "Joy",
        "e_27": "Calmness",
        "e_7": "Angry",
        "e_14": "Speaker",
        "e_5": "Disgust",
        "e_6": "Sadness",
        "e_4": "Surprise",
        "e_25": "Speech"
    }

    s = senticnet.Senticnet(path='../Odyssey/senticnet/senticnet.py')

    def __init__(self, path="jsons/members"):
        """"
        Load of all the jsons in a directory. Create a dataframe with all the jsons.
        Then clean the df to keep a df with the useful elements.
        """
        self.df = allfiles_onedataframe(path)
        self.make_df_clean()

    def make_df_clean(self):
        """"
        A function who makes a clean up of the base dataframe loaded from the json files.
        """
        df_clean = self.df[['Class ID', 'Text']]
        df_clean = df_clean.rename(columns={"Class ID": "TagTog"})
        df_clean = df_clean[['Text','TagTog']]
        # Remove the rows who contains non desired tags
        df_clean = df_clean.loc[(df_clean["TagTog"] != 'e_14') & (df_clean["TagTog"] != 'e_25') &
                                (df_clean["TagTog"] != 'e_1') & (df_clean["TagTog"] != 'e_2') &
                                (df_clean["TagTog"] != 'e_9')]

        df1 = df_clean.reset_index(drop=True)
        # Remove the rows with emotion tag to only one word
        mask = df1['Text'].str.strip().str.split(' ').str.len().eq(1)
        df1 = df1[~mask]
        df1 = df1.reset_index(drop=True)
        # Replace all the code names with the names of the emotions stocked in the dict annotations
        df1 = df1.replace('e_8', self.annotation['e_8'])
        df1 = df1.replace('e_3', self.annotation['e_3'])
        df1 = df1.replace('e_27', self.annotation['e_27'])
        df1 = df1.replace('e_7', self.annotation['e_7'])
        df1 = df1.replace('e_5', self.annotation['e_5'])
        df1 = df1.replace('e_6', self.annotation['e_6'])
        df1 = df1.replace('e_4', self.annotation['e_4'])
        # Store the dataframe to a new csv file
        df1.to_csv('csv/all_df_clean.csv')
        self.df = df1

    def add_emotions_senticnet(self):
        """"
        Add a new column with the emotion evaluate with the senticnet method
        """
        emotions = []
        # Browse the column Text of the dataframe and normalize the text for the senticnet method
        for t in self.df['Text']:
            token = []
            t = t.lower().strip()
            t = t.replace("'", ' ')
            t = t.replace('-', '_')
            t = word_tokenize(t)
            for w in t:
                if w not in self.stopwords_lst and w not in self.punctuation:
                    token.append(unidecode(w))
            # Use the function averageEmotionsOf of senticnet to obtain an emotion for each tagged text
            emotions.append(self.s.averageEmotionsOf(token)['primary_emotion'])
        # Create a new column in the base dataframe with all the emotions
        self.df['Senticnet'] = emotions

    def add_emotions_pyfeel(self):
        """"
        Add a new column with the emotion evaluate with the PyFeel method
        """
        emotions = []
        # Browse the column Text of the dataframe
        for l in self.df['Text']:
            e = Feel(l)
            em = e.emotions()
            # Add the emotion calmness if all the emotions receive the score 0 and positivity is greater than 0
            if em.get('sadness') == 0 and em.get('disgust') == 0 and em.get('fear') == 0 and em.get(
                    'surprise') == 0 and em.get('angry') == 0 and em.get('joy') == 0:
                emotions.append('calmness')
                continue
            max_em = max(em, key=em.get)
            # If the label positivity is the greatest, choose the second greatest instead.
            if max_em == 'positivity':
                del em['positivity']
                max_em = max(em, key=em.get)
            # Add the the emotion with greates score in the emotions list
            emotions.append(max_em)
        # Create a new column in the base dataframe with all the emotions
        self.df['PyFeel'] = emotions

    def make_df_emotions(self):
        """"
        Create a csv file with the base datafrane and the two columns with emotions

        return the dataframe with the new columns
        """
        self.add_emotions_senticnet()
        self.add_emotions_pyfeel()
        self.df.to_csv('csv/emotions_df.csv')
        return self.df

    def textsPerEmotions(self, m, em):
        """"
        return the number of texts for a given method m, and a given emotion em
        """
        return len(self.df[self.df[m] == em])

    def normalizeEmSenticnet(self):
        """"
        Normalize the dataframe to be able to make a comparison between the emotions
        """
        self.df = self.df.apply(lambda x: x.astype(str).str.lower())
        self.df = self.df.replace('ecstasy', 'joy')
        self.df = self.df.replace('contentment', 'joy')
        self.df = self.df.replace('anxiety', 'fear')
        self.df = self.df.replace('terror', 'fear')
        self.df = self.df.replace('dislike', 'disgust')
        self.df = self.df.replace('loathing', 'disgust')
        self.df = self.df.replace('bliss', 'calmness')
        self.df = self.df.replace('serenity', 'calmness')
        self.df = self.df.replace('grief', 'sadness')
        self.df = self.df.replace('melancholy', 'sadness')
        self.df = self.df.replace('annoyance', 'anger')
        self.df = self.df.replace('rage', 'angry')
        self.df = self.df.replace('angry', 'anger')
        self.df = self.df.replace('acceptance', 'pleasantness')
        self.df = self.df.replace('delight', 'pleasantness')
        self.df = self.df.replace('pleasantness', 'surprise')
        self.df = self.df.replace('enthusiasm', 'eagerness')
        self.df = self.df.replace('responsiveness', 'eagerness')

    def make_diagram(self, em):
        """
        make a Venn diagram and a new dataframe with the similarity between the methods of tag for a given emotion em

        return a dataframe with the similarity stats stored.
        """
        # Calculate the occurrences for the given emotion for each method
        n1 = self.textsPerEmotions('TagTog', em)
        n2 = self.textsPerEmotions('PyFeel', em)
        n3 = self.textsPerEmotions('Senticnet', em)
        # Calculate the intersection between the methods for the given emotion
        inter1 = self.df[(self.df['TagTog'] == em) & (self.df['PyFeel'] == em)]
        inter2 = self.df[(self.df['Senticnet'] == em) & (self.df['PyFeel'] == em)]
        inter3 = self.df[(self.df['Senticnet'] == em) & (self.df['TagTog'] == em)]
        inter4 = self.df[(self.df['Senticnet'] == em) & (self.df['TagTog'] == em) & (self.df['PyFeel'] == em)]
        # Creation of the dataframe with scores
        df_similarity = pd.DataFrame(
            np.array([[em, n1, n2, n3, (len(inter1)), (len(inter3)), (len(inter2)), (len(inter4))]]),
            columns=['Emotion', 'TagTog', 'PyFeel', 'Senticnet', 'T-P', 'T-S', 'P-S', 'T-P-S'])
        # Creation of the Venn diagram
        venn3(subsets=(n1, n2,len(inter1), n3, len(inter3), len(inter2), len(inter4)),
              set_labels=('TagTog', 'PyFeel', 'Senticnet'))
        plt.title(em)
        plt.savefig('png/'+em+'.png')
        plt.show()
        return df_similarity

    def make_all_stats(self,path):
        """
        Make the dataframes and the Venn diagrams for each emotion present in the base dataframe from a given csv who
        a dataframe with the 3 methods and the texts are stored
        """
        self.df = pd.read_csv(path)
        self.normalizeEmSenticnet()
        # Make an emotions list with all the emotions present in the base dataframe
        emotions = (list(self.df.Senticnet.unique()))
        emotions.extend(list(self.df.TagTog.unique()))
        emotions.extend(list(self.df.PyFeel.unique()))
        emotions = list(dict.fromkeys(emotions))
        # Make a dataframe and the Venn diagrams with the function make_diagram for each emotion
        df2 = pd.DataFrame(
            columns=['Emotion', 'TagTog', 'PyFeel', 'Senticnet', 'T-P', 'T-S', 'P-S', 'T-P-S'])
        for e in emotions:
            df1 = self.make_diagram(e)
            df2 = pd.concat([df2, df1], axis=0)
        df2 = df2.reset_index(drop=True)
        # Store the dataframe in a csv file
        df2.to_csv('csv/stats_emotions.csv')
