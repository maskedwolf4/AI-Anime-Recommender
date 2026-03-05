from src.vector_store import VectorStoreBuilder
from src.recommender import AnimeRecommender
from config.config import GROQ_API_KEY, MODEL
from utils.logger import get_logger
from utils.custom_exception import CustomException

logger = get_logger(__name__)

class AnimeRecommendationPipeline:
    def __init__(self, persist_dir="chroma_db"):
        try:
            logger.info("INitializing Recommendation Pipeline")
                        
            vector_builder = VectorStoreBuilder(csv_path="", persist_dir=persist_dir)
            
            retriever = vector_builder.load_vector_store().as_retriever()
            
            self.recommender = AnimeRecommender(retriever, GROQ_API_KEY,MODEL)
            
            logger.info("Pipeline initialized successfully...")
            
        except Exception as e:
            logger.error("Failed to initialize pipeline ",e)
            raise CustomException("Error during Pipeline initialization",e)
        
    def recommend(self, query:str) -> str:
        try:
            logger.info(f"Recieved a query {query}")
            
            recommendation = self.recommender.get_recommendation(query)
            
            logger.info(f"Recommendation for {query} is {recommendation}")
            
            return recommendation
        
        except Exception as e:
            logger.error("Failed to recommend ",e)
            raise CustomException("Error during Recommendation",e)