export default function DestinationHero({ destination }) {
  return (
    <div 
      className="relative h-64 overflow-hidden"
      style={{
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
      }}
    >
      <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent flex items-end">
        <div className="max-w-7xl mx-auto px-6 py-8 w-full">
          <h1 className="text-5xl font-black text-white drop-shadow-lg">
            {destination}
          </h1>
        </div>
      </div>
    </div>
  );
}
