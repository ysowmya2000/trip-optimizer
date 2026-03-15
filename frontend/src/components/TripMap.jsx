import { GoogleMap, LoadScript, Marker } from '@react-google-maps/api';

const GOOGLE_MAPS_API_KEY = '***REMOVED***';

const mapContainerStyle = {
  width: '100%',
  height: '500px'
};

export default function TripMap({ days }) {
  const center = days?.[0]?.activities?.find(a => a.attraction?.geometry?.location)?.attraction?.geometry?.location || { lat: 48.8566, lng: 2.3522 };

  return (
    <div className="bg-white rounded-2xl p-6 shadow-xl">
      <div className="flex items-center gap-3 mb-4">
        <span className="text-2xl">📍</span>
        <h2 className="text-2xl font-bold text-gray-800">Your Route</h2>
      </div>
      
      <LoadScript googleMapsApiKey={GOOGLE_MAPS_API_KEY}>
        <GoogleMap
          mapContainerStyle={mapContainerStyle}
          center={center}
          zoom={13}
        >
          {days?.map((day) =>
            day.activities
              .filter(activity => activity.attraction?.geometry?.location)
              .map((activity, idx) => (
                <Marker
                  key={`${day.day_number}-${idx}`}
                  position={activity.attraction.geometry.location}
                  title={activity.name}
                />
              ))
          )}
        </GoogleMap>
      </LoadScript>
    </div>
  );
}
