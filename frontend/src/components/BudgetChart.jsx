import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function BudgetChart({ days }) {
  const chartData = days.map(day => ({
    day: `Day ${day.day_number}`,
    cost: day.estimated_cost
  }));

  return (
    <div className="bg-white/95 backdrop-blur rounded-2xl p-6 shadow-xl">
      <h3 className="text-2xl font-black mb-4 text-gray-900">💰 Daily Budget Breakdown</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="day" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="cost" fill="#8b5cf6" radius={[8, 8, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
