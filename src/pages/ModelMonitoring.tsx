import React, { useState, useEffect } from 'react';
import { Activity, ShieldCheck, AlertTriangle, CheckCircle2 } from 'lucide-react';
import { fetchApi } from '../services/api';

export const ModelMonitoring: React.FC = () => {
  const [monitoring, setMonitoring] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadMonitoring();
  }, []);

  const loadMonitoring = async () => {
    try {
      const res = await fetchApi('/api/ai/monitoring');
      if (res.success) {
        setMonitoring(res.data);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 space-y-6">
      <div className="border-b border-slate-200 pb-4">
        <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-2">
          <Activity className="h-6 w-6 text-brand-600" />
          Model Drift & Data Quality Monitoring
        </h1>
        <p className="text-sm text-slate-500 mt-1">
          Population Stability Index (PSI), Kolmogorov-Smirnov drift statistics, and missingness quality ratings.
        </p>
      </div>

      {monitoring && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-surface p-5 rounded-lg border border-slate-200 shadow-sm flex items-center justify-between">
            <div>
              <p className="text-xs font-semibold text-slate-500 uppercase">Data Quality Rating</p>
              <p className="text-2xl font-bold text-emerald-600 mt-1">{monitoring.data_quality_rating}</p>
            </div>
            <ShieldCheck className="h-8 w-8 text-emerald-600" />
          </div>

          <div className="bg-surface p-5 rounded-lg border border-slate-200 shadow-sm flex items-center justify-between">
            <div>
              <p className="text-xs font-semibold text-slate-500 uppercase">Missingness Ratio</p>
              <p className="text-2xl font-bold text-brand-700 mt-1">{monitoring.missingness_ratio_pct}%</p>
            </div>
            <Activity className="h-8 w-8 text-brand-600" />
          </div>

          <div className="bg-surface p-5 rounded-lg border border-slate-200 shadow-sm flex items-center justify-between">
            <div>
              <p className="text-xs font-semibold text-slate-500 uppercase">Observations Evaluated</p>
              <p className="text-2xl font-bold text-slate-900 mt-1">{monitoring.total_observations_evaluated}</p>
            </div>
            <CheckCircle2 className="h-8 w-8 text-blue-600" />
          </div>
        </div>
      )}

      {/* PSI Drift Summary Table */}
      <div className="bg-surface rounded-lg shadow-sm border border-slate-200 p-5">
        <h2 className="text-base font-bold text-slate-900 mb-3">Feature Distribution Drift (PSI & KS Test)</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-600">
            <thead className="bg-slate-50 border-b border-slate-200 text-xs font-semibold text-slate-700 uppercase">
              <tr>
                <th className="px-4 py-3">Feature Name</th>
                <th className="px-4 py-3">PSI Index</th>
                <th className="px-4 py-3">KS Statistic</th>
                <th className="px-4 py-3">P-Value</th>
                <th className="px-4 py-3">Drift Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 font-mono text-xs">
              {monitoring?.feature_drift_summary && Object.keys(monitoring.feature_drift_summary).map((feat, idx) => {
                const item = monitoring.feature_drift_summary[feat];
                return (
                  <tr key={idx} className="hover:bg-slate-50/50">
                    <td className="px-4 py-3 font-sans font-bold text-slate-900">{feat}</td>
                    <td className="px-4 py-3 font-bold text-brand-700">{item.psi?.toFixed(4)}</td>
                    <td className="px-4 py-3">{item.ks_statistic?.toFixed(4)}</td>
                    <td className="px-4 py-3">{item.p_value?.toFixed(4)}</td>
                    <td className="px-4 py-3">
                      <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800">
                        {item.drift_status}
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
