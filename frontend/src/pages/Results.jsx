import { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { ArrowLeft, MapPin, DollarSign, Cloud } from 'lucide-react';
import TripMap from '../components/TripMap';
import BudgetChart from '../components/BudgetChart';
import DestinationHero from '../components/DestinationHero';
import ProTips from '../components/ProTips';

export default function Results() {
  const location = useLocation();
  const navigate = useNavigate();
  const [tripData, setTripData] = useState(null);

  useEffect(() => {
    if (location.state?.tripData) {
      setTripData(location.state.tripData);
    } else {
      navigate('/');
    }
  }, [location, navigate]);

  if (!tripData) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-600 via-purple-500 to-pink-500 flex items-center justify-center">
        <div className="text-white text-2xl">Loading...</div>
      </div>
    );
  }

  const { itinerary, weather_forecast, budget_analysis, recommendations } = tripData;
  const weatherForecast = weather_forecast?.forecast || [];


  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-600 via-purple-500 to-pink-500">
      <div className="bg-white/10 backdrop-blur-md border-b border-white/20">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <button
            onClick={() => navigate('/')}
            className="flex items-center gap-2 text-white hover:text-white/80 transition font-semibold"
          >
            <ArrowLeft size={20} />
            Back to Search
          </button>
        </div>
      </div>

      <DestinationHero destination={itinerary.destination} />

      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Overview Cards */}
        <div className="grid md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white/95 backdrop-blur rounded-2xl p-6 shadow-xl">
            <div className="flex items-center gap-3 mb-2">
              <MapPin className="text-purple-600" size={24} />
              <h3 className="font-bold text-gray-700">Destination</h3>
            </div>
            <p className="text-2xl font-black text-gray-900">{itinerary.destination}</p>
            <p className="text-sm text-gray-600">{itinerary.trip_duration} days</p>
          </div>

          <div className="bg-white/95 backdrop-blur rounded-2xl p-6 shadow-xl">
            <div className="flex items-center gap-3 mb-2">
              <DollarSign className="text-green-600" size={24} />
              <h3 className="font-bold text-gray-700">Budget</h3>
            </div>
            
            {budget_analysis.user_currency && budget_analysis.user_currency !== budget_analysis.destination_currency ? (
              <div className="space-y-2">
                <div>
                  <p className="text-xs text-gray-500">Your Budget</p>
                  <p className="text-lg font-bold text-gray-900">
                    {new Intl.NumberFormat('en-US', { 
                      style: 'currency', 
                      currency: budget_analysis.user_currency 
                    }).format(budget_analysis.user_budget)}
                  </p>
                </div>
                
                <div>
                  <p className="text-xs text-gray-500">Trip Cost</p>
                  <p className="text-2xl font-black text-gray-900">
                    {new Intl.NumberFormat('en-US', { 
                      style: 'currency', 
                      currency: budget_analysis.user_currency 
                    }).format(budget_analysis.estimated_cost_user)}
                  </p>
                  <p className="text-xs text-gray-400">
                    ≈ {new Intl.NumberFormat('en-US', { 
                      style: 'currency', 
                      currency: budget_analysis.destination_currency 
                    }).format(budget_analysis.estimated_cost_destination)}
                  </p>
                </div>
              </div>
            ) : (
              <p className="text-2xl font-black text-gray-900">
                ${itinerary.estimated_total_cost.toFixed(2)}
              </p>
            )}
            
            <p className={`text-sm font-semibold mt-3 ${
              budget_analysis.status === 'under_budget' ? 'text-green-600' :
              budget_analysis.status === 'on_budget' ? 'text-blue-600' : 'text-red-600'
            }`}>
              {budget_analysis.status === 'under_budget' ? '✓ Under Budget' :
               budget_analysis.status === 'on_budget' ? '✓ On Budget' : '⚠ Over Budget'}
            </p>
          </div>

          <div className="bg-white/95 backdrop-blur rounded-2xl p-6 shadow-xl">
            <div className="flex items-center gap-3 mb-2">
              <MapPin className="text-blue-600" size={24} />
              <h3 className="font-bold text-gray-700">Attractions</h3>
            </div>
            <p className="text-2xl font-black text-gray-900">{itinerary.total_attractions}</p>
            <p className="text-sm text-gray-600">places to visit</p>
          </div>


        </div>

        {/* Seasonal Weather Forecast */}
        {weather_forecast && (
          <div className="bg-white/95 backdrop-blur rounded-2xl p-8 shadow-xl mb-8">
            <div className="flex items-center gap-3 mb-6">
              <span className="text-4xl">🌤️</span>
              <h2 className="text-3xl font-black text-gray-900">Weather for Your Trip</h2>
            </div>
            <div className="bg-gradient-to-br from-blue-50 to-purple-50 rounded-xl p-6">
              <div className="grid md:grid-cols-3 gap-6">
                <div>
                  <p className="text-sm font-semibold text-gray-600 mb-1">Season</p>
                  <p className="text-2xl font-black text-gray-900">{weather_forecast.season}</p>
                  <p className="text-sm text-gray-600 mt-1">{weather_forecast.month}</p>
                </div>
                <div>
                  <p className="text-sm font-semibold text-gray-600 mb-1">Temperature</p>
                  <p className="text-2xl font-black text-gray-900">{weather_forecast.temperature}</p>
                  <p className="text-sm text-gray-600 mt-1">{weather_forecast.condition}</p>
                </div>
                <div>
                  <p className="text-sm font-semibold text-gray-600 mb-1">What to Pack</p>
                  <p className="text-sm text-gray-700 mt-1">{weather_forecast.advice}</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Map and Chart */}
        <div className="grid lg:grid-cols-2 gap-6 mb-8">
          <TripMap itinerary={itinerary} />
          <BudgetChart days={itinerary.days} />
        </div>

        <ProTips 
          itinerary={itinerary}
          weather={weather_forecast}
          optimization={recommendations}
        />

        {/* Daily Itinerary */}
        <div className="bg-white/95 backdrop-blur rounded-2xl p-8 shadow-xl mb-8">
          <h2 className="text-3xl font-black mb-6 text-gray-900">Your Itinerary</h2>
          
          <div className="space-y-8">
            {itinerary.days.map((day) => (
              <div key={day.day_number} className="border-l-4 border-purple-500 pl-6">
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <h3 className="text-2xl font-black text-gray-900">
                      Day {day.day_number}: {day.title}
                    </h3>
                    <p className="text-gray-600">{day.notes}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm text-gray-600">Estimated Cost</p>
                    {budget_analysis.user_currency && budget_analysis.user_currency !== budget_analysis.destination_currency ? (
                      <>
                        <p className="text-xl font-bold text-green-600">
                          {new Intl.NumberFormat('en-US', { 
                            style: 'currency', 
                            currency: budget_analysis.user_currency 
                          }).format(day.estimated_cost)}
                        </p>
                        <p className="text-xs text-gray-400">
                          ≈ {new Intl.NumberFormat('en-US', { 
                            style: 'currency', 
                            currency: budget_analysis.destination_currency 
                          }).format(
                            (day.estimated_cost / budget_analysis.estimated_cost_user) * budget_analysis.estimated_cost_destination
                          )}
                        </p>
                      </>
                    ) : (
                      <p className="text-2xl font-bold text-green-600">
                        ${day.estimated_cost.toFixed(2)}
                      </p>
                    )}
                  </div>
                </div>

                <div className="space-y-4">
                  {day.activities.map((activity, idx) => (
                    <div key={idx} className="flex gap-4">
                      <div className="flex-shrink-0 w-24">
                        <span className="inline-block bg-purple-100 text-purple-700 px-3 py-1 rounded-lg font-bold text-sm">
                          {activity.time}
                        </span>
                      </div>
                      
                      <div className="flex-1 bg-gray-50 rounded-xl p-4">
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <h4 className="font-bold text-gray-900 text-lg">
                              {activity.name}
                            </h4>
                            <p className="text-gray-600 text-sm mt-1">
                              {activity.description}
                            </p>
                            {activity.notes && (
                              <p className="text-purple-600 text-sm mt-2 font-semibold">
                                💡 {activity.notes}
                              </p>
                            )}
                          </div>
                          
                          {activity.activity_type === 'attraction' && activity.attraction && (
                            <div className="ml-4 text-right flex-shrink-0">
                              <div className="flex items-center gap-1 text-yellow-500">
                                <span>⭐</span>
                                <span className="font-bold">{activity.attraction.rating}</span>
                              </div>
                              {activity.attraction.user_ratings_total && (
                                <p className="text-xs text-gray-500">
                                  ({activity.attraction.user_ratings_total.toLocaleString()} reviews)
                                </p>
                              )}
                            </div>
                          )}
                        </div>
                        
                        {activity.activity_type === 'attraction' && activity.attraction?.address && (
                          <p className="text-xs text-gray-500 mt-2">
                            📍 {activity.attraction.address}
                          </p>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
      </div>

  );
}
