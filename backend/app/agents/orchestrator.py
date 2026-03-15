"""
Trip Orchestrator - Coordinates all agents to create complete trip
"""
from typing import Dict, Any
import logging

from app.agents.research_agent import research_agent
from app.agents.planning_agent import planning_agent
from app.agents.optimization_agent import optimization_agent
from app.agents.budget_agent import budget_agent
from app.agents.weather_agent import weather_agent
from app.utils.currency_converter import currency_converter
from app.utils.budget_calculator import budget_calculator

logger = logging.getLogger(__name__)


class TripOrchestrator:
    """Orchestrates multiple agents to create a complete trip plan"""
    
    def __init__(self):
        self.research = research_agent
        self.planning = planning_agent
        self.optimization = optimization_agent
        self.budget = budget_agent
        self.weather = weather_agent
    
    async def create_trip(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create complete trip using all agents
        """
        try:
            logger.info("=" * 80)
            logger.info("🗺️ Trip Orchestrator: Creating complete trip")
            logger.info("=" * 80)
            
            destination = request.get('destination')
            interests = request.get('interests', [])
            trip_duration = request.get('trip_duration', 3)
            budget = request.get('budget', 1000)
            start_date = request.get('start_date')

            # Currency conversion setup
            user_currency = request.get("currency", "USD")
            destination_currency = "USD"  # Will be set later
            original_budget = budget

            

            # Detect destination currency
            destination_currency = currency_converter.get_destination_currency(destination)
            logger.info(f"💱 Currency: {user_currency} → {destination_currency}")
            
            # Convert budget to USD for internal calculations
            if budget and user_currency != "USD":
                budget_usd = currency_converter.convert(budget, user_currency, "USD")
                logger.info(f"   Budget in USD: ${budget_usd:.2f}")
            else:
                budget_usd = budget
            
            # Check minimum budget requirement
            if original_budget:
                min_budget_info = budget_calculator.calculate_minimum_budget(
                    destination=destination,
                    trip_duration=trip_duration,
                    user_currency=user_currency
                )
                
                logger.info(f"💰 Budget Check:")
                logger.info(f"   Your budget: {currency_converter.format_currency(original_budget, user_currency)}")
                logger.info(f"   Minimum needed: {currency_converter.format_currency(min_budget_info['minimum_budget_user'], user_currency)}")
                
                if original_budget < min_budget_info['minimum_budget_user'] * 0.95:  # Allow 5% tolerance
                    logger.error(f"❌ Budget too low!")
                    return {
                        'success': False,
                        'error': 'BUDGET_TOO_LOW',
                        'message': f"Budget too low for {trip_duration} days in {destination}",
                        'minimum_budget': min_budget_info['minimum_budget_user'],
                        'user_budget': original_budget,
                        'currency': user_currency,
                        'destination': destination,
                        'trip_duration': trip_duration
                    }
                logger.info(f"   ✅ Budget sufficient")

            # Phase 1: Research
            logger.info("📍 PHASE 1: Research")
            research_result = self.research.research_destination(
                destination=destination,
                interests=interests,
                trip_duration=trip_duration
            )
            
            # Extract attractions - use 'top_attractions' key
            attractions = research_result.get('top_attractions', [])
            logger.info(f"📍 Extracted {len(attractions)} attractions from research")
            
            # Phase 2: Planning
            logger.info("📍 PHASE 2: Planning")
            itinerary = self.planning.create_itinerary(
                destination=destination,
                attractions=attractions,
                trip_duration=trip_duration,
                interests=interests,
                budget=budget_usd
            )
            
            # Convert all costs from USD to user's currency
            logger.info(f"💱 Converting costs: USD → {user_currency}")
            
            # Convert total cost
            itinerary.estimated_total_cost = currency_converter.convert(
                itinerary.estimated_total_cost, "USD", user_currency
            )
            
            # Convert each day's cost
            for day in itinerary.days:
                day.estimated_cost = currency_converter.convert(
                    day.estimated_cost, "USD", user_currency
                )
            
            logger.info(f"   Total cost: {currency_converter.format_currency(itinerary.estimated_total_cost, user_currency)}")

            
            # Phase 3: Optimization
            logger.info("📍 PHASE 3: Route Optimization")
            optimized_itinerary = self.optimization.optimize_itinerary(
                itinerary=itinerary
            )
            
            # Phase 4: Budget Analysis
            logger.info("📍 PHASE 4: Budget Analysis")
            budget_analysis = self.budget.analyze_budget(
                itinerary=itinerary,
                budget=original_budget,
                user_currency=user_currency,
                destination_currency=destination_currency
            )
            
            # Phase 5: Weather Forecast
            logger.info("📍 PHASE 5: Weather Forecast")
            weather_forecast = self.weather.get_seasonal_forecast(
                destination=destination,
                start_date=start_date
            )
            
            # Phase 6: Combine recommendations
            logger.info("📍 PHASE 6: Final Recommendations")
            recommendations = {
                "time_saved_minutes": optimized_itinerary.get('time_saved_minutes', 0),
                "route_efficiency": optimized_itinerary.get('route_efficiency', 'standard')
            }
            
            # Serialize itinerary object to dict
            itinerary_dict = itinerary.dict() if hasattr(itinerary, 'dict') else itinerary
            
            # Add currency information
            currency_info = {
                'user_currency': user_currency,
                'destination_currency': destination_currency,
                'original_budget': original_budget,
                'converted_budget': budget,
                'budget_display': {
                    'user': currency_converter.format_currency(original_budget, user_currency) if original_budget else None,
                    'destination': currency_converter.format_currency(budget, destination_currency) if budget else None
                }
            }
            
            result = {
                'success': True,
                'request': request,
                'itinerary': itinerary_dict,
                'budget_analysis': budget_analysis,
                'weather_forecast': weather_forecast,
                'recommendations': recommendations,
                'currency_info': currency_info
            }
            
            logger.info("✅ Trip Orchestrator: Complete trip created successfully")
            return result
            
        except Exception as e:
            logger.error(f"❌ Trip Orchestrator: Error creating trip - {str(e)}")
            import traceback
            traceback.print_exc()
            raise


# Create singleton instance
trip_orchestrator = TripOrchestrator()
logger.info("🗺️ Trip Orchestrator initialized")
