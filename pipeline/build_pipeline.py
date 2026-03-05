import sys
import os
sys.path.append(os.getcwd())

from src.data_loader import AnimeDataLoader
from src.vector_store import VectorStoreBuilder
from dotenv import load_dotenv
from utils.custom_exception import CustomException
from utils.logger import get_logger

load_dotenv()

logger = get_logger(__name__)

def main():
    try:
        logger.info("Building Main pipeline")
        
        loader = AnimeDataLoader("data/anime_with_synopsis.csv","data/anime_processed_synopsis.csv")
        processed_csv = loader.load_and_process()
        
        logger.info("Data loaded and processed succesfully")
        
        vector_builder = VectorStoreBuilder(processed_csv)
        vector_builder.build_and_save_vectorstore()
        
        logger.info("Vector Store built succesfully")
        
        logger.info("Pipeline built successfully")
        
    except Exception as e:
        logger.error(f"Failed to build pipeline {e}")
        raise CustomException(f"Error during excuting pipeline {e}")
    
    
if __name__=="__main__":
    main()