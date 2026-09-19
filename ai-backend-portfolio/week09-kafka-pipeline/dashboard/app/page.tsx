"use client";
import { useEffect, useState } from "react";

type Event = {
  event_id: string;
  event_type: string;
  classified_type: string;
  entities: Record<string, unknown>;
  anomaly_score: number;
  processed_at: string;
};

export default function Home() {
  const [events, setEvents] = useState<Event[]>([]);
  const [stats, setStats] = useState({ total: 0, avgScore: 0, alerts: 0 });

  useEffect(() => {
    const fetchEvents = async () => {
      const res = await fetch("/api/events");
      const data: Event[] = await res.json();
      setEvents(data);
      setStats({
        total: data.length,
        avgScore: data.length
            ? parseFloat((data.reduce((s, e) => s + e.anomaly_score, 0) / data.length).toFixed(2))
            : 0,
        alerts: data.filter((e) => e.anomaly_score >= 0.7).length,
      });
    };
    fetchEvents();
    const interval = setInterval(fetchEvents, 3000);
    return () => clearInterval(interval);
  }, []);

  const scoreColor = (score: number) => {
    if (score >= 0.7) return "text-red-500 font-bold";
    if (score >= 0.4) return "text-yellow-500";
    return "text-green-500";
  };

  return (
      <main className="min-h-screen bg-gray-950 text-white p-8">
        <h1 className="text-3xl font-bold mb-2">AI Event Pipeline</h1>
        <p className="text-gray-400 mb-8">Live Kafka event enrichment dashboard</p>

        <div className="grid grid-cols-3 gap-4 mb-8">
          <div className="bg-gray-800 rounded-xl p-6">
            <p className="text-gray-400 text-sm">Total Events</p>
            <p className="text-4xl font-bold mt-1">{stats.total}</p>
          </div>
          <div className="bg-gray-800 rounded-xl p-6">
            <p className="text-gray-400 text-sm">Avg Anomaly Score</p>
            <p className={`text-4xl font-bold mt-1 ${scoreColor(stats.avgScore)}`}>{stats.avgScore}</p>
          </div>
          <div className="bg-red-950 rounded-xl p-6">
            <p className="text-gray-400 text-sm">High Risk Alerts</p>
            <p className="text-4xl font-bold mt-1 text-red-400">{stats.alerts}</p>
          </div>
        </div>

        <div className="bg-gray-800 rounded-xl overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-gray-700 text-gray-300">
            <tr>
              <th className="text-left p-4">Event ID</th>
              <th className="text-left p-4">Type</th>
              <th className="text-left p-4">Classified</th>
              <th className="text-left p-4">User</th>
              <th className="text-left p-4">Amount</th>
              <th className="text-left p-4">Anomaly Score</th>
            </tr>
            </thead>
            <tbody>
            {events.map((e) => (
                <tr key={e.event_id} className={`border-t border-gray-700 ${e.anomaly_score >= 0.7 ? "bg-red-950/30" : ""}`}>
                  <td className="p-4 font-mono text-xs text-gray-400">{e.event_id.slice(0, 8)}...</td>
                  <td className="p-4">{e.event_type}</td>
                  <td className="p-4 text-blue-400">{e.classified_type}</td>
                  <td className="p-4">{(e.entities as Record<string, string>)?.user_id ?? "—"}</td>
                  <td className="p-4">{(e.entities as Record<string, number>)?.amount ?? "—"}</td>
                  <td className={`p-4 ${scoreColor(e.anomaly_score)}`}>{e.anomaly_score}</td>
                </tr>
            ))}
            </tbody>
          </table>
        </div>
      </main>
  );
}