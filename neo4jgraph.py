from py2neo import Graph, Node, Relationship
import spacy
from spacy.lang.en.stop_words import STOP_WORDS

class graphDB:
    def __init__(self, graph):
        self.graph = graph
    def breakQuery(self,query):
        stopwords = list(STOP_WORDS)
        nlp = spacy.load('en_core_web_sm')
        docx = nlp(query)
        word_frequencies = {}
        for word in docx:
            if word.text.lower() not in stopwords:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
        
        retrieved_data = ""
        data=[]
        for i in word_frequencies.keys():
            data.append(i)
        
        return data
    def checkQuery(self,query):
        words_list = [
    # Interrogative Words
                  
                        "which",
                        "how",
                        "how much",
                        "how many",
                        
                        # Comparison Words
                        "more",
                        "less",
                        "better",
                        "worse",
                        "as",
                        "than",
                        
                        # Differentiating Words
                        "different",
                        "difference",
                        "differ",
                        "contrast",
                        "unlike",
                        "distinct",
                        "distinctive",
                        "varies",
                        "variation",
                        "opposite",
                        "versus",
                        "compare",
                        "contradict",
                        "varied",
                        "distinction",
                        "similar",
                        "same",
                        "dissimilar",
                        "between",       # Added word
                        "among",         # Similar word
                        "within",        # Similar word
                        "across",        # Similar word
                        "relative to",   # Similar phrase
                        "in comparison to", # Similar phrase
                        "in contrast to" # Similar phrase
                        
                        # Synonyms
                        "distinct",
                        "unlike",
                        "diverse",
                        "varied",
                        "distinction",
                        "disparity",
                        "variation",
                        "contrast",
                        "differ",
                        "change",
                        "modulates",
                        "reverse",
                        "antithesis",
                        "against",
                        "compared to",
                        "in contrast to",
                        "oppose",
                        "deny",
                        "dispute",
                        "assorted",
                        "identical",
                        "equal",
                        "resembling",
                        "divergent",
                        
                        # Conjunctions
                        "are",
                        "and",
                        "or",
                        "but",
                        "nor",
                        "for",
                        "yet",
                        "so",
                        "although",
                        "because",
                        "since",
                        "unless",
                        "if",
                        "while",
                        "whereas",
                        "as long as",
                        "even though",
                        "provided that",
                        "whether"
                    ]
        count =0
        query=query.lower()
        print(query)
        for i in words_list:
            if i in query:
                count+=query.count(i)

        if (count>2):
            return True
        
        else:
            return False 

    def create_nodes_and_relationships(self, data):
        for item in data:
            node1 = Node("Data", name=item['node'])
            node2 = Node("Data", name=item['chunk'])
            relationship = Relationship(node1, "RELATED_TO", node2, relation=item['edge'])
            self.graph.merge(node1, "Data", "name")
            self.graph.merge(node2, "Data", "name")
            self.graph.merge(relationship)

    def ask_question(self, question):
        query = f"""
            MATCH (a:Data)-[r:RELATED_TO]->(b:Data)
            WHERE toLower(a.name) = toLower('{question}') 
                OR toLower(b.name) = toLower('{question}')
            RETURN a.name AS node_a, b.name AS node_b, r.relation AS relation
        """
        result = self.graph.run(query).data()
        answer = ""
        for relation in result:
            answer += relation['relation'] + " "
        return answer.strip()
    
    def extract_relations(self, text):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        data = []

        for sent in doc.sents:
            chunks = list(sent.noun_chunks)
            if not chunks:
                continue  # Skip sentences with no noun chunks

            node = chunks[0].root.text
            for chunk in chunks[1:]:
                data.append({
                    "node": node,
                    "chunk": chunk.root.text,
                    "edge": sent.text.strip()
                })

        self.create_nodes_and_relationships(data)


    def retrieve_relevant_data_from_graph(self, query):
        stopwords = list(STOP_WORDS)
        nlp = spacy.load('en_core_web_sm')
        docx = nlp(query)
        word_frequencies = {}
        for word in docx:
            if word.text.lower() not in stopwords:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
        
        retrieved_data = ""
        for i in word_frequencies.keys():
            d = self.ask_question(i)
            if d:
                retrieved_data += d + " "
        
        return retrieved_data.strip()

    def query_processor(self, text, query):
        self.extract_relations(text)
        relevant_ans = self.retrieve_relevant_data_from_graph(query)
        self.delete_nodes_and_relationships()
        return relevant_ans

    def delete_nodes_and_relationships(self):
        query = "MATCH (n) DETACH DELETE n"
        self.graph.run(query)
        print("nodes and relationships deleted")
"""
graph = Graph("neo4j+s://ffb0b9d5.databases.neo4j.io", auth=("neo4j", "v2WNDZxaDwNt9AVjLps6EZLvudLM5OoHPZFIBsGybvw"))
db = graphDB(graph)

text = '''- If you own an orchard, you'd better know the difference.Similarly, there's single-event probability and there's cumulative probability, and if you're looking at data, you need to understand the difference.Probability of a Single EventThe simplest type of probability is the measure of the chance that a single event will occur.For example, let's say we have a fair, six-sided die.The probability that a single throw will be a 4 is 1/6, because only 1 of the six sides is a 4.Simple, right?Similarly, the probability that a single roll of the die will be a 1 is 1/6.The same holds true for 2, and for 3, and for 5, and for 6.The single-event probability that    
-ly related.Understanding one concept allows for the construction or comprehension of the other, facilitating a more streamlined approach to dealing with probabilistic models.Good luck on this path of knowledge!ShareCiteImprove this answer            Follow            edited Mar 23 at 16:16      answered Feb 11, 2022 at 17:41Marine GalantinMarine Galantin33311 silver badge1010 bronze badges$\endgroup$31$\begingroup$@RuiBarradas - a minor point, but the integral of the CDF is bounded if the variate has an upper bound, e.g., a Uniform$(0,1)$ variate.$\endgroup$–jbowmanCommentedFeb 12, 2022 at 19:57$\begingroup$@jbowman Yes, thanks.And that's not a minor point.$\endgroup$–Rui BarradasCommentedFeb 12, 2022 at 22:09$\begingroup$@RuiBarradas - I was thinking it was minor because your statement was based on an oversight, not on a misunderstanding.$\endgroup$–jbowmanCommentedFeb 13, 2022 at 0:04Add a comment|      11    $\begingroup$The concept of a "probability distribution" is an umbrella term that refers to a particular type of object that can be represented uniquely in multiple ways. One way to represent a probability distribution is through its probability measure, another is through its characteristic function, another is through its cumulative distribution function, and another is through its probability density function (including specification of a dominating measure for the density). All of the latter are specific mathematical objects that describe a probability distribution in a different way. The term "probability distribution" does not refer to a specific mathematical object; it can be thought of as an umbrella term that refers holistically to the "thing" that each of these objects is describing.ShareCiteImprove this answer            Follow         
   edited Feb 16, 2022 at 21:17      answered Feb 14, 2022 at 21:28BenBen129k77 gold badges246246 silver badges569569 bronze badges$\endgrou
-The probability density function (PDF) or the probability that you will get exactly 2 will be 16.667%.Whereas, the cumulative distribution function (CDF) of 2 is 33.33% as described above.Probability Density Function (PDF) vs Cumulative Distribution Function (CDF)The CDF is the probability that random variable values less than or equal to x whereas the PDF is a probability that a random variable, say X, will take a value exactly equal to x.This page provides you with more details on when to use the related Norm.Dist and Norm.Dist and Norm.Inv Microsoft Excel functions?Probability Mass Function vs Cumulative Distribution Function for Continuous Distr     
-e less than or equal to 1 and is 16.667%.There is only one possible way to get a 1.The cumulative distribution function (CDF) of 2 is the probability that the next roll will take a value less than or equal to 2. The cumulative distribution function (CDF) of 2 is 33.33% as there are two possible ways to get a 2 or below (the roll giving a 1 or 2).The cumulative distribution function (CDF) of 6 is 100%.The cumulative distribution function (CDF) of 6 is the probability that the next roll will take a value less than or equal to 6 and is equal to 100% as all possible results will be less than or equal to 6.Probability Density Function (PDF)The probability density function (PDF) is the probability that a random variable, say X, will take a value exactly equal to x. Note the difference between the cumulative distribution function (CDF) and the probability density function (PDF) – Here the focus is on one specific value.Whereas, for the cumulative distribution function, we are interested in the probability of taking on a value equal to or less than the specified value.The probability density function is also referred to as the probability mass function.So do not get perturbed if you encounter the probability mass function.For example, if you roll a die, the probability of obtaining 1, 2, 3, 4, 5, or 6 is 16.667% (=1/6).
-What's the Difference Between Probability and Cumulative Probability?EnglishEnglishFrançaisDeutschPortuguêsEspañol日本語한국어中文（简体）PartnersContactMy AccountProductsBackProductsAll ProductsMinitab Statistical SoftwareMinitab ConnectMinitab Model OpsMinitab Education HubMinitab EngageMinitab WorkspaceReal-Time SPCSPMSolutionsBackSolutionsAll SolutionsAnalyticsStatistics & Predictive AnalyticsData Science & Machine LearningBusiness Analytics & IntelligenceStatistical Process Control Quality AnalyticsLive AnalyticsReliability & Life Data AnalysisKey CapabilitiesContinuous ImprovementData Integration & Data PrepDiagramming & Mind Mapping Model Deployment & ML OpsInnovation & Project ManagementFeatured IndustriesAcademicEnergy & Natural ResourcesGovernment & Public SectorHealthcareInsuranceManufacturing & IndustrialServicesSoftware & TechnologyFeaturedTechnologyFeatured RolesEngineeringBusiness AnalysisInformation TechnologySupply ChainCustomer Service & Contact CenterHuman ResourcesMarketingResources & ServicesBackResources & ServicesAll               
               Resources & ServicesResourcesCase StudiesBlogData SetsWebinars & EventsEducation HubServicesTrainingDeploymentConsultingSelf-Paced LearningContinuing EducationSupportBackSupportTechnical SupportLicensing & ActivationMinitab Quick StartTrainingInstallation SupportSupport VideosSupport DocumentationSoftware UpdatesProduct DownloadsSupport PolicyCompanyBackCompanyCompanyAbout UsLeadership TeamPartnersCareersContactNewsTry/BuyStatisticsData AnalysisQuality ImprovementSubscribeTalk To MinitabWhat's the Difference Between Probability and Cumulativeand Cumulative Probability?              Minitab Blog Editor                                        
| 1/13/2012 Topics:                     StatisticsTweetShareShareProbability is the heart and soul of statistics: at a very simple level, we collect data about something we- Probability Basics - Explained.Introduction to Probability | by Trifunovic Uros | Analytics Vidhya | MediumOpen in appSign upSign inWriteSign upSign inProbability Basics - ExplainedTrifunovic UrosFollowPublished inAnalytics Vidhya7 min readFeb 22, 2021--1ListenShareIntroduction to ProbabilityPhoto by Edge2Edge Media on UnsplashBreaking into Data Science without a degree in a quantitative discipline can be intimidating at times.Finance, Marketing, and Management classes Ive taken as part of the BBA program in Finance and Investment help me understand another essential component of the Data Science task s the business logic.However, the curriculum of similar programs often lacks programming, math, and statistics classes, all of which are necessary to take a Data Science project from starting to the ending point.The article focuses on statistics and, specifically, attempts to explain the basics of one of its core components probability.The logical question to start with is What is probability?.Simply put probability tells us how likely is something to happen after many trials, that is, in a long run.Coin tossing is a typical example to explain the concept of probability.There are two sides to most coins heads and tails.Therefore, if you toss a coin there are high chances that it will land either on heads or tails.
-robability Distribution - Cross Validated Skip to main contentStack Exchange Network                Stack Exchange network consists of 183 Q&A communities including Stack Overflow, the largest, most trusted online community for developers to learn, share their knowledge, and build their careers.        Visit Stack ExchangeLoading…                Tour                                  Start here for a quick overview of the site                             
 Help Center                              Detailed answers to any questions you might have            
                      Meta                         
                 Discuss the workings and policies of this site                                      About Us                                      Learn more about Stack Overflow the company, and our products                  current community      Cross Validated    helpchat      Cross Validated Meta    your communities      Sign up or log in to customize your list.        more stack exchange communitiescompany blogLog inSign up Home Questions Tags Users UnansweredTeamsNow available on Stack Overflow for Teams!AI features where you work: search, IDE, and chat.    Learn moreExplore TeamsTeams      Ask questions, find answers and collaborate at work with Stack Overflow for Teams.      Explore TeamsTeamsQ&A for workConnect and share knowledge within a single location that is structured and easy to search.          Learn more about Teams        Difference in Probability Measure vs. Probability Distribution    Ask Question  Asked2 years, 6 months agoModified5 months agoViewed            10k times
-teImprove this answer            Follow           
 edited Dec 6, 2022 at 15:09      answered Dec 5, 2022 at 21:28Maverick MeerkatMaverick Meerkat3,5402828 silver badges4242 bronze badges$\endgroup$Add a comment|Highly active question.Earn 10 reputation (not counting the association bonus) in order to answer this question.The reputation requirement helps protect this question from spam and non-answer activity.                              Not the answer you're looking for?Browse other questions tagged probabilitydistributionsnormal-distributionterminologymeasure-theory or ask your own question.         '''
query = "differentiate between random probability   and cumulative probability distribution"

result=db.query_processor(text,query)
print(result)"""