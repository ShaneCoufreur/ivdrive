
"use client";

import { useState, useEffect } from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";
import { api } from "@/lib/api";

interface CostData {
  total_sessions: number;
  total_kwh_added: number;
  total_base_cost_eur: number;
  total_actual_cost_eur: number;
  markup_paid_eur: number;
}

export function ChargingCostsDashboard({ vehicleId }: { vehicleId: string }) {
  const [data, setData] = useState<CostData | null>(null);

  useEffect(() => {
    const fetchCosts = async () => {
      try {
        const res = await api.getAnalyticsChargingCosts(vehicleId);
        setData(res);
      } catch (err) {
        console.error("Failed to fetch charging costs", err);
      }
    };
    fetchCosts();
  }, [vehicleId]);

  if (!data) return <div className="p-8 text-center text-iv-text-muted">Loading economics...</div>;

  const chartData = [
    {
      name: "Total Spend (€)",
      Base: data.total_base_cost_eur,
      Markup: data.markup_paid_eur,
    }
  ];

  return (
    <div className="glass rounded-2xl border border-iv-border p-6 mt-6">
      <h3 className="text-lg font-bold text-iv-text">Charging Economics</h3>
      <p className="text-sm text-iv-text-muted mb-6">Base Grid Cost vs Public Charger Convenience Fee</p>
      
      <div className="grid grid-cols-2 gap-6 mb-8">
        <div className="bg-iv-surface rounded-xl p-4 border border-iv-border/50">
          <p className="text-sm text-iv-text-muted flex justify-between">
            Total Energy Added <span>{data.total_sessions} Sessions</span>
          </p>
          <p className="text-3xl font-bold text-iv-text mt-2">{data.total_kwh_added} <span className="text-base font-normal text-iv-text-muted">kWh</span></p>
        </div>
        <div className="bg-iv-surface rounded-xl p-4 border border-iv-border/50">
          <p className="text-sm text-iv-text-muted">Markup Paid</p>
          <p className="text-3xl font-bold text-rose-500 mt-2">€ {data.markup_paid_eur}</p>
        </div>
      </div>

      <div className="h-48 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData} layout="vertical" margin={{ top: 0, right: 30, left: 20, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#374151" opacity={0.2} />
            <XAxis type="number" tickFormatter={(v) => `€${v}`} tick={{fill: '#8b8fa3', fontSize: 12}} />
            <YAxis dataKey="name" type="category" hide />
            <Tooltip 
              formatter={(value: number) => [`€ ${value}`, '']}
              contentStyle={{ backgroundColor: '#1C1C2E', borderColor: '#2a2d42', borderRadius: '12px', color: '#fff' }}
              itemStyle={{ color: '#fff' }}
            />
            <Legend wrapperStyle={{ paddingTop: '20px' }} />
            <Bar dataKey="Base" name="NordPool Grid Base" stackId="a" fill="#10B981" radius={[4, 0, 0, 4]} />
            <Bar dataKey="Markup" name="Public Charger Markup" stackId="a" fill="#F43F5E" radius={[0, 4, 4, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
