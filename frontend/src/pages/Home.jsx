import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plane, MapPin, Calendar, DollarSign, Heart, Sparkles } from 'lucide-react';

const CURRENCIES = [
  { code: 'USD', flag: '🇺🇸', name: 'US Dollar' },
  { code: 'EUR', flag: '🇪🇺', name: 'Euro' },
  { code: 'GBP', flag: '🇬🇧', name: 'British Pound' },
  { code: 'JPY', flag: '🇯🇵', name: 'Japanese Yen' },
  { code: 'AUD', flag: '🇦🇺', name: 'Australian Dollar' },
  { code: 'CAD', flag: '🇨🇦', name: 'Canadian Dollar' },
  { code: 'CHF', flag: '🇨🇭', name: 'Swiss Franc' },
  { code: 'CNY', flag: '🇨🇳', name: 'Chinese Yuan' },
  { code: 'INR', flag: '🇮🇳', name: 'Indian Rupee' },
  { code: 'SGD', flag: '🇸🇬', name: 'Singapore Dollar' },
  { code: 'HKD', flag: '🇭🇰', name: 'Hong Kong Dollar' },
  { code: 'NZD', flag: '🇳🇿', name: 'New Zealand Dollar' },
  { code: 'SEK', flag: '🇸🇪', name: 'Swedish Krona' },
  { code: 'KRW', flag: '🇰🇷', name: 'South Korean Won' },
  { code: 'NOK', flag: '🇳🇴', name: 'Norwegian Krone' },
  { code: 'MXN', flag: '🇲🇽', name: 'Mexican Peso' },
  { code: 'BRL', flag: '🇧🇷', name: 'Brazilian Real' },
  { code: 'ZAR', flag: '🇿🇦', name: 'South African Rand' },
  { code: 'RUB', flag: '🇷🇺', name: 'Russian Ruble' },
  { code: 'TRY', flag: '🇹🇷', name: 'Turkish Lira' },
  { code: 'AED', flag: '🇦🇪', name: 'UAE Dirham' },
  { code: 'SAR', flag: '🇸🇦', name: 'Saudi Riyal' },
  { code: 'THB', flag: '🇹🇭', name: 'Thai Baht' },
  { code: 'IDR', flag: '🇮🇩', name: 'Indonesian Rupiah' },
  { code: 'MYR', flag: '🇲🇾', name: 'Malaysian Ringgit' },
  { code: 'PHP', flag: '🇵🇭', name: 'Philippine Peso' },
  { code: 'PLN', flag: '🇵🇱', name: 'Polish Zloty' },
  { code: 'DKK', flag: '🇩🇰', name: 'Danish Krone' },
  { code: 'CZK', flag: '🇨🇿', name: 'Czech Koruna' },
  { code: 'HUF', flag: '🇭🇺', name: 'Hungarian Forint' },
  { code: 'ILS', flag: '🇮🇱', name: 'Israeli Shekel' },
  { code: 'CLP', flag: '🇨🇱', name: 'Chilean Peso' },
  { code: 'ARS', flag: '🇦🇷', name: 'Argentine Peso' },
  { code: 'COP', flag: '🇨🇴', name: 'Colombian Peso' },
  { code: 'EGP', flag: '🇪🇬', name: 'Egyptian Pound' },
  { code: 'PKR', flag: '🇵🇰', name: 'Pakistani Rupee' },
  { code: 'BDT', flag: '🇧🇩', name: 'Bangladeshi Taka' },
  { code: 'VND', flag: '🇻🇳', name: 'Vietnamese Dong' },
  { code: 'NGN', flag: '🇳🇬', name: 'Nigerian Naira' },
  { code: 'UAH', flag: '🇺🇦', name: 'Ukrainian Hryvnia' },
  { code: 'RON', flag: '🇷🇴', name: 'Romanian Leu' },
  { code: 'BGN', flag: '🇧🇬', name: 'Bulgarian Lev' },
  { code: 'HRK', flag: '🇭🇷', name: 'Croatian Kuna' },
  { code: 'ISK', flag: '🇮🇸', name: 'Icelandic Krona' },
  { code: 'QAR', flag: '🇶🇦', name: 'Qatari Riyal' },
  { code: 'KWD', flag: '🇰🇼', name: 'Kuwaiti Dinar' },
  { code: 'OMR', flag: '🇴🇲', name: 'Omani Rial' },
  { code: 'BHD', flag: '🇧🇭', name: 'Bahraini Dinar' },
  { code: 'JOD', flag: '🇯🇴', name: 'Jordanian Dinar' }
];

export default function Home() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    destination: '',
    duration: 5,
    budget: '',
    currency: 'USD',
    interests: [],
    start_date: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const interestOptions = [
    { id: 'culture', label: 'Culture', emoji: '🎭', gradient: 'from-purple-400 to-pink-400' },
    { id: 'food', label: 'Food', emoji: '🍜', gradient: 'from-orange-400 to-red-400' },
    { id: 'nature', label: 'Nature', emoji: '🌿', gradient: 'from-green-400 to-emerald-400' },
    { id: 'adventure', label: 'Adventure', emoji: '🏔️', gradient: 'from-blue-400 to-cyan-400' },
    { id: 'relaxation', label: 'Relaxation', emoji: '🧘', gradient: 'from-indigo-400 to-purple-400' },
    { id: 'shopping', label: 'Shopping', emoji: '🛍️', gradient: 'from-pink-400 to-rose-400' },
    { id: 'nightlife', label: 'Nightlife', emoji: '🎉', gradient: 'from-violet-400 to-fuchsia-400' },
    { id: 'history', label: 'History', emoji: '🏛️', gradient: 'from-amber-400 to-orange-400' },
    { id: 'art', label: 'Art', emoji: '🎨', gradient: 'from-teal-400 to-cyan-400' },
    { id: 'sports', label: 'Sports', emoji: '⚽', gradient: 'from-lime-400 to-green-400' }
  ];

  const toggleInterest = (interest) => {
    setFormData(prev => ({
      ...prev,
      interests: prev.interests.includes(interest)
        ? prev.interests.filter(i => i !== interest)
        : [...prev.interests, interest]
    }));
  };

  const incrementDuration = () => {
    setFormData(prev => ({ ...prev, duration: Math.min(prev.duration + 1, 365) }));
  };

  const decrementDuration = () => {
    setFormData(prev => ({ ...prev, duration: Math.max(prev.duration - 1, 1) }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!formData.destination.trim()) {
      setError('Please enter a destination');
      return;
    }

    if (formData.interests.length === 0) {
      setError('Please select at least one interest');
      return;
    }

    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/trips/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          destination: formData.destination,
          trip_duration: formData.duration,
          budget: formData.budget,
          currency: formData.currency,
          interests: formData.interests,
          start_date: formData.start_date,
          start_date: formData.start_date
        })
      });

      if (!response.ok) {
        const error = new Error('Failed to create trip');
        error.response = response;
        throw error;
      }

      const data = await response.json();
      navigate('/results', { state: { tripData: data } });
    } catch (err) {
      // Check if budget too low error
      if (err.response && err.response.status === 400) {
        const errorData = await err.response.json();
        if (errorData.detail && errorData.detail.error === 'BUDGET_TOO_LOW') {
          const detail = errorData.detail;
          setError(`Budget too low! Minimum needed for ${detail.trip_duration} days in ${detail.destination} is ${new Intl.NumberFormat('en-US', { style: 'currency', currency: detail.currency }).format(detail.minimum_budget)}`);
          return;
        }
      }
      setError('Failed to create trip. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-600 via-purple-500 to-pink-500 relative overflow-hidden">
      {/* Glassmorphism Blobs */}
      <div className="absolute top-20 left-10 w-72 h-72 bg-white/20 backdrop-blur-3xl rounded-full border border-white/30 animate-pulse"></div>
      <div className="absolute bottom-20 right-10 w-96 h-96 bg-pink-300/30 backdrop-blur-3xl rounded-full border border-white/20 animate-pulse" style={{ animationDelay: '1s' }}></div>
      <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-purple-400/20 backdrop-blur-3xl rounded-full border border-white/10 animate-pulse" style={{ animationDelay: '0.5s' }}></div>

      <div className="relative z-10 container mx-auto px-6 py-12">
        <div className="text-center mb-12">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Plane className="w-12 h-12 text-white" />
            <h1 className="text-6xl font-black text-white">Trip Optimizer</h1>
          </div>
          <p className="text-xl text-white/90">Your Perfect Trip, Planned in Seconds ✨</p>
        </div>

        <div className="max-w-3xl mx-auto bg-white/95 backdrop-blur-xl rounded-3xl shadow-2xl p-8 border border-white/50">
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Destination */}
            <div>
              <label className="flex items-center gap-2 text-gray-700 font-bold mb-2">
                <MapPin size={20} className="text-purple-600" />
                Where do you want to go?
              </label>
              <input
                type="text"
                value={formData.destination}
                onChange={(e) => setFormData({ ...formData, destination: e.target.value })}
                placeholder="e.g., Paris, Tokyo, New York"
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:outline-none"
              />
            </div>

            {/* Duration */}
            <div>
              <label className="flex items-center gap-2 text-gray-700 font-bold mb-2">
                <Calendar size={20} className="text-purple-600" />
                How long is your trip?
              </label>
              <div className="flex items-center gap-3">
                <button type="button" onClick={decrementDuration} className="w-12 h-12 bg-purple-100 hover:bg-purple-200 rounded-xl font-bold text-purple-700 text-xl">-</button>
                <input
                  type="number"
                  min="1"
                  max="365"
                  value={formData.duration}
                  onChange={(e) => setFormData({ ...formData, duration: parseInt(e.target.value) || 1 })}
                  className="flex-1 px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:outline-none text-center font-bold text-lg"
                />
                <button type="button" onClick={incrementDuration} className="w-12 h-12 bg-purple-100 hover:bg-purple-200 rounded-xl font-bold text-purple-700 text-xl">+</button>
                <span className="text-gray-600 font-semibold">{formData.duration} {formData.duration === 1 ? 'day' : 'days'}</span>
              </div>
            </div>

            {/* Start Date */}
            <div>
              <label className="flex items-center gap-2 text-gray-700 font-bold mb-2">
                <Calendar size={20} className="text-purple-600" />
                When do you want to travel?
              </label>
              <input
                type="date"
                value={formData.start_date}
                onChange={(e) => setFormData({ ...formData, start_date: e.target.value })}
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:outline-none"
                required
              />
            </div>

            {/* Budget */}
            <div>
              <label className="flex items-center gap-2 text-gray-700 font-bold mb-2">
                <DollarSign size={20} className="text-purple-600" />
                What's your budget?
              </label>
              <div className="flex gap-3">
                <input
                  type="number"
                  min="0"
                  value={formData.budget}
                  onChange={(e) => {
                    const value = e.target.value;
                    // Remove leading zeros and allow empty string
                    const cleanValue = value === '' ? '' : parseFloat(value) || '';
                    setFormData({ ...formData, budget: cleanValue });
                  }}
                  className="flex-1 px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:outline-none"
                />
                <select
                  value={formData.currency}
                  onChange={(e) => setFormData({ ...formData, currency: e.target.value })}
                  className="px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:outline-none font-semibold bg-white"
                >
                  {CURRENCIES.map(c => (
                    <option key={c.code} value={c.code}>{c.flag} {c.code}</option>
                  ))}
                </select>
              </div>
            </div>

            {/* Interests */}
            <div>
              <label className="flex items-center gap-2 text-gray-700 font-bold mb-3">
                <Heart size={20} className="text-purple-600" />
                What are your interests?
              </label>
              <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
                {interestOptions.map(interest => (
                  <button
                    key={interest.id}
                    type="button"
                    onClick={() => toggleInterest(interest.id)}
                    className={`py-3 px-4 rounded-xl font-bold transition-all ${
                      formData.interests.includes(interest.id)
                        ? `bg-gradient-to-r ${interest.gradient} text-white shadow-lg scale-105`
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    <div className="text-2xl mb-1">{interest.emoji}</div>
                    <div className="text-sm">{interest.label}</div>
                  </button>
                ))}
              </div>
            </div>

            {/* Error */}
            {error && (
              <div className="bg-red-50 border-2 border-red-200 rounded-xl p-4">
                <p className="text-red-700 font-semibold text-center">{error}</p>
              </div>
            )}

            {/* Submit */}
            <button
              type="submit"
              disabled={loading}
              className={`w-full py-4 rounded-xl font-black text-lg ${
                loading ? 'bg-gray-400' : 'bg-gradient-to-r from-purple-600 to-pink-500 hover:from-purple-700 hover:to-pink-600 shadow-xl hover:shadow-2xl'
              } text-white flex items-center justify-center gap-3`}
            >
              {loading ? (
                <>
                  <div className="w-6 h-6 border-4 border-white/30 border-t-white rounded-full animate-spin"></div>
                  Creating your perfect trip...
                </>
              ) : (
                <>
                  <Sparkles size={24} />
                  Plan My Trip
                </>
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
