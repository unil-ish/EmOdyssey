import pandas as pd
import rdflib

class ABoxFiller():
    """
        A class to fill an ontology with data
        once they are saved to a csv file.

        Usage
        -----------
         - Create a ABoxFiller() object and pass it
           the paths to the csv and ontology files
         - Use the fill() method to fill the A-Box

        Return
        ----------
         - Nothing
         - Export filled ontology in the same folder
           than the original one, but with '_filled'
           as suffix
    """

    def __init__(self, data, stats, ont):
        self.onto_path = ont
        self.data_path = data
        self.stats_path = stats

        assert self.onto_path
        assert self.data_path
        assert self.stats_path

        self.new_onto_path = self.onto_path.split('.')[0] + '_filled.' + self.onto_path.split('.')[1]
        self._data = None
        self._graph = None
        self._stats = None

        # Do the job
        self.loadData()
        self.loadStats()
        self.loadOntology()

    def fill(self):
        """
            Fill A-Box with data extracted from
            csv and fill them into the ontology.
            Save the ontology to a new file.
        """

        # Basic URI
        sp_base_uri  = rdflib.URIRef('http://pplws.unil.ch/speech/id/speech_') # for storing speeches
        base_uri     = rdflib.URIRef('http://github.com/dpicca/ontologies/literary_characters_psychologica_profiles.owl#')
        speech       = rdflib.URIRef('http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#String')
        dc_subject   = rdflib.URIRef('http://purl.org/dc/terms/subject')
        hasTagtogEmotion     = rdflib.URIRef('http://github.com/dpicca/ontologies/literary_characters_psychologica_profiles.owl#hasTagtogEmotion') # custom property, for TagTog
        hasSenticnetEmotion  = rdflib.URIRef('http://github.com/dpicca/ontologies/literary_characters_psychologica_profiles.owl#hasSenticnetEmotion') # custom property, for SenticNet
        hasPyfeelEmotion     = rdflib.URIRef('http://github.com/dpicca/ontologies/literary_characters_psychologica_profiles.owl#hasPyfeelEmotion') # custom property, for PyFeel

        # IRI for stats
        com_base_uri = rdflib.URIRef('http://pplws.unil.ch/comparison/id/comparison_') # for storing comparison between systems
        emotion_tagtog_iri    = rdflib.URIRef('http://github.com/dpicca/ontologies/literary_characters_psychologica_profiles.owl#EmotionTagtog')
        emotion_senticnet_iri = rdflib.URIRef('http://github.com/dpicca/ontologies/literary_characters_psychologica_profiles.owl#EmotionSenticnet')
        emotion_pyfeel_iri    = rdflib.URIRef('http://github.com/dpicca/ontologies/literary_characters_psychologica_profiles.owl#EmotionPyfeel')
        emotion_cat_base_uri  = rdflib.URIRef('http://arsemotica.di.unito.it/ontology#')
        hasCommonEmotion      = rdflib.URIRef('http://github.com/dpicca/ontologies/literary_characters_psychologica_profiles.owl#hasCommonEmotion') # hasCommonEmotion with another system
        hasTotalEmotions      = rdflib.URIRef('http://github.com/dpicca/ontologies/literary_characters_psychologica_profiles.owl#hasTotalEmotions') # hasTotalEmotions for one emotion
        hasAllCommonEmotions  = rdflib.URIRef('http://github.com/dpicca/ontologies/literary_characters_psychologica_profiles.owl#hasAllCommonEmotions') # hasAllCommonEmotions between all systems

        # Remove NaN
        self._data  = self._data.dropna()
        self._stats = self._stats.dropna()

        # Fill A-Box with stats
        for index, row in self._stats.iterrows():
            # Class name
            emotion = emotion_cat_base_uri + row['Emotion'].lower().capitalize()
            tt_iri = base_uri + row['Emotion'].lower().capitalize() + 'Tagtog'
            sn_iri = base_uri + row['Emotion'].lower().capitalize() + 'Senticnet'
            pf_iri = base_uri + row['Emotion'].lower().capitalize() + 'Pyfeel'

            # Instances name
            comparison_tp_i = com_base_uri + 'tp_' + row['Emotion']
            comparison_ts_i = com_base_uri + 'ts_' + row['Emotion']
            comparison_ps_i = com_base_uri + 'ps_' + row['Emotion']

            emotion_i = emotion + 'Stats'
            tt_iri_i = tt_iri + 'Stats'
            sn_iri_i = sn_iri + 'Stats'
            pf_iri_i = pf_iri + 'Stats'

            tt_total = int( row['TagTog'] )
            sn_total = int( row['Senticnet'] )
            pf_total = int( row['PyFeel'] )
            
            tp_value = int( row['T-P'] )
            ts_value = int( row['T-S'] )
            ps_value = int( row['P-S'] )
            
            allCommonEmotions = int( row['T-P-S'] )

            # Triplets (type)
            self._graph.add( ( tt_iri_i, rdflib.RDF.type, tt_iri ) )
            self._graph.add( ( sn_iri_i, rdflib.RDF.type, sn_iri ) )
            self._graph.add( ( pf_iri_i, rdflib.RDF.type, pf_iri ) )

            # Triplets (total)
            self._graph.add( ( tt_iri_i, hasTotalEmotions, rdflib.Literal( tt_total ) ) ) # tagtog amount of emotion x
            self._graph.add( ( sn_iri_i, hasTotalEmotions, rdflib.Literal( sn_total ) ) ) # senticnet amount of emotion x
            self._graph.add( ( pf_iri_i, hasTotalEmotions, rdflib.Literal( pf_total ) ) ) # pyfeel amount of emotion x

            # Triplets (intersection between systems)
            # TP
            self._graph.add( ( comparison_tp_i, hasTagtogEmotion, tt_iri_i ) )
            self._graph.add( ( comparison_tp_i, hasPyfeelEmotion, pf_iri_i ) )
            self._graph.add( ( comparison_tp_i, hasCommonEmotion, rdflib.Literal( tp_value ) ) )
            
            # TS
            self._graph.add( ( comparison_ts_i, hasTagtogEmotion, tt_iri_i ) )
            self._graph.add( ( comparison_ts_i, hasSenticnetEmotion, sn_iri_i ) )
            self._graph.add( ( comparison_ts_i, hasCommonEmotion, rdflib.Literal( ts_value ) ) )
            
            # PS
            self._graph.add( ( comparison_ps_i, hasPyfeelEmotion, pf_iri_i ) )
            self._graph.add( ( comparison_ps_i, hasSenticnetEmotion, sn_iri_i ) )
            self._graph.add( ( comparison_ps_i, hasCommonEmotion, rdflib.Literal( ps_value ) ) )

            # Triplets (all common)
            self._graph.add( ( emotion_i, hasAllCommonEmotions, rdflib.Literal( allCommonEmotions ) ) ) # emotion x commonly found

        # Fill A-Box with data
        for index, row in self._data.iterrows():
            # Get variables
            speech_id = sp_base_uri + str( row[0] )
            text = row['Text']
            hu = base_uri + row['TagTog'].lower().capitalize() + 'Tagtog'
            sn = base_uri + row['Senticnet'].lower().capitalize() + 'Senticnet'
            pf = base_uri + row['PyFeel'].lower().capitalize() + 'Pyfeel'

            # Add to graph
            self._graph.add( ( speech_id, rdflib.RDF.type, speech ) )
            self._graph.add( ( speech_id, hasTagtogEmotion, hu ) )   # TagTog / default
            self._graph.add( ( speech_id, hasSenticnetEmotion, sn ) ) # SenticNet
            self._graph.add( ( speech_id, hasPyfeelEmotion, pf ) ) # PyFeel
            self._graph.add( ( speech_id, dc_subject, rdflib.Literal(text) ) )

        # Export graph
        try:
            self._graph.serialize(destination=self.new_onto_path, format='xml')
            print(f'# Successfully exported ontology to {self.new_onto_path}!')

        except:
            print(f'# Ontology export failed!')

    def loadStats(self):
        """
            Load the stats data from a csv file
        """

        try:
            self._stats = pd.read_csv(self.stats_path)
            print(f'# Successfully loaded ontology {self.stats_path}!')

        except FileNotFoundError:
            print('# CSV file was not found!')

    def loadData(self):
        """
            Load the data from a csv file
        """

        try:
            self._data = pd.read_csv(self.data_path)
            print(f'# Successfully loaded data {self.data_path}!')

        except FileNotFoundError:
            print('# CSV file was not found!')

    def loadOntology(self):
        """
            Load the ontology from owl/rdf/xml file
        """

        try:
            self._graph = rdflib.Graph()
            self._graph.parse(self.onto_path)
            print(f'# Successfully loaded ontology {self.onto_path}!')

        except FileNotFoundError:
            print('# Ontology was not found!')


if __name__ == '__main__':
    abf = ABoxFiller('emotions_df.csv', 'stats_emotions.csv', 'ontologies/emotions_modif.rdf')
    abf.fill()
