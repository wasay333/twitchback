from typing import Dict, List, Optional, Tuple
import logging
from .base import TwitchAPIBaseService
from .errors import TwitchAPIError

logger = logging.getLogger(__name__)

class TwitchCategoryService(TwitchAPIBaseService):
    """Service class for Twitch category-related operations"""
    
    def get_top_categories(self, limit: int = 10, cursor: Optional[str] = None) -> Tuple[List[Dict], Optional[str]]:
        """Get top game categories with cursor support"""
        limit = min(max(1, limit), 100)
        
        params = {
            'first': limit
        }
        if cursor:
            params['after'] = cursor
        
        try:
            data = self._make_request('games/top', params)
            categories = data.get('data', [])
            cursor = data.get('pagination', {}).get('cursor')
            
            formatted_categories = []
            for category in categories:
                formatted_category = self._format_category_data(category)
                formatted_categories.append(formatted_category)
            
            return formatted_categories, cursor
            
        except TwitchAPIError:
            raise
        except Exception as e:
            logger.error(f"Error processing categories data: {e}")
            raise TwitchAPIError(f"Error processing categories: {str(e)}", None)
    
    def get_search_games(self, query: str, limit: int = 5, cursor: Optional[str] = None) -> Tuple[List[Dict], Optional[str]]:
        """Search for games matching the query"""
        limit = min(max(1, limit), 100)
        
        params = {
            'query': query,
            'first': limit
        }
        if cursor:
            params['after'] = cursor
        
        try:
            data = self._make_request('search/categories', params)
            games = data.get('data', [])
            cursor = data.get('pagination', {}).get('cursor')
            
            formatted_games = []
            for game in games:
                formatted_game = self._format_category_data(game)
                formatted_games.append(formatted_game)
            
            return formatted_games, cursor
            
        except TwitchAPIError:
            raise
        except Exception as e:
            logger.error(f"Error processing search games: {e}")
            raise TwitchAPIError(f"Error processing search games: {str(e)}", None)
    
    def _format_category_data(self, category: Dict) -> Dict:
        """Format raw category data from Twitch API for consistent output"""
        try:
            return {
                'id': category['id'],
                'name': category['name'],
                'box_art_url': category['box_art_url'],
                'igdb_id': category.get('igdb_id', ''),
                'thumbnail': {
                    'small': category['box_art_url'].replace('{width}', '320').replace('{height}', '180'),
                    'medium': category['box_art_url'].replace('{width}', '640').replace('{height}', '360'),
                    'large': category['box_art_url'].replace('{width}', '1920').replace('{height}', '1080')
                }
            }
        except KeyError as e:
            logger.error(f"Missing required field in category data: {e}")
            raise TwitchAPIError(f"Invalid category data format: missing {e}", None)
