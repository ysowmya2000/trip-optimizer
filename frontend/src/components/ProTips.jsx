export default function ProTips({ itinerary, weather, optimization }) {
  const tips = [];
  
  if (optimization?.time_saved_minutes) {
    tips.push(`🚀 Route optimized to save ${optimization.time_saved_minutes} minutes of travel time!`);
  }
  
  if (itinerary?.trip_duration) {
    tips.push(`📅 Perfect ${itinerary.trip_duration}-day itinerary with ${itinerary.total_attractions} carefully selected attractions`);
  }
  
  if (weather?.forecast?.[0]?.condition) {
    tips.push(`☀️ Weather looks ${weather.forecast[0].condition.toLowerCase()} - pack accordingly!`);
  }

  if (tips.length === 0) {
    tips.push('✨ Your personalized trip itinerary is ready!');
  }

  return (
    <div className="bg-white/95 backdrop-blur rounded-2xl p-6 shadow-xl mb-8">
      <h3 className="text-2xl font-black mb-4 text-gray-900">💡 Pro Tips</h3>
      <ul className="space-y-2">
        {tips.map((tip, idx) => (
          <li key={idx} className="text-gray-700 text-lg">
            {tip}
          </li>
        ))}
      </ul>
    </div>
  );
}
