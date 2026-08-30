import React, { useState, useEffect } from 'react';
import { BookOpen, Layers, LineChart, ShieldAlert } from 'lucide-react';
import { fetchApi } from '../services/api';

export const Experiments: React.FC = () => {
  const [experiments, setExperiments] = useState<any[]>([]);
  const [ablation, setAblation] = useState<any[]>([]);
  const [robustness, setRobustness] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadExperiments();
  }, []);

  const loadExperiments = async () => {
    try {
      const res = await fetchApi('/api/ai/experiments');
      if (res.success) {
        setExperiments(res.data.experiments || []);
        setAblation(res.data.ablation_study || []);
        setRobustness(res.data.robustness_study || []);
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
          <BookOpen className="h-6 w-6 text-brand-600" />
          Experiment Registry & Research Benchmark Suite
        </h1>
        <p className="text-sm text-slate-500 mt-1">
          Full tracking registry of executed ML experiments, feature ablation studies, and missing-data robustness evaluations.
        </p>
      </div>

      {/* Feature Ablation Study */}
      <div className="bg-surface rounded-lg shadow-sm border border-slate-200 p-5">
        <h2 className="text-base font-bold text-slate-900 flex items-center gap-2 mb-3">
          <Layers className="h-5 w-5 text-brand-600" />
          Feature Ablation Study (Empirical Results)
        </h2>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-600">
            <thead className="bg-slate-50 border-b border-slate-200 text-xs font-semibold text-slate-700 uppercase">
              <tr>
                <th className="px-4 py-3">Feature Configuration</th>
                <th className="px-4 py-3">Feature Count</th>
                <th className="px-4 py-3">AUROC</th>
                <th className="px-4 py-3">F1-Score</th>
                <th className="px-4 py-3">Precision</th>
                <th className="px-4 py-3">Recall</th>
                <th className="px-4 py-3">Brier Score</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 font-mono text-xs">
              {ablation.map((row, idx) => (
                <tr key={idx} className={idx === ablation.length - 1 ? 'bg-brand-50/50 font-bold' : ''}>
                  <td className="px-4 py-3 font-semibold text-slate-900">{row.experiment}</td>
                  <td className="px-4 py-3">{row.feature_count}</td>
                  <td className="px-4 py-3 text-brand-700 font-bold">{row.auroc?.toFixed(4)}</td>
                  <td className="px-4 py-3">{row.f1_score?.toFixed(4)}</td>
                  <td className="px-4 py-3">{row.precision?.toFixed(4)}</td>
                  <td className="px-4 py-3">{row.recall?.toFixed(4)}</td>
                  <td className="px-4 py-3 text-emerald-700 font-bold">{row.brier_score?.toFixed(4)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Missingness Robustness Study */}
      <div className="bg-surface rounded-lg shadow-sm border border-slate-200 p-5">
        <h2 className="text-base font-bold text-slate-900 flex items-center gap-2 mb-3">
          <LineChart className="h-5 w-5 text-brand-600" />
          Missing-Data Robustness Experiment (5% - 30% Missingness)
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
          {robustness.map((row, idx) => (
            <div key={idx} className="bg-slate-50 border border-slate-200 rounded-lg p-3 text-center">
              <p className="text-xs font-semibold text-slate-500">{row.missingness_level_pct}% Missingness</p>
              <p className="text-xl font-bold text-brand-700 mt-1">{row.auroc?.toFixed(4)}</p>
              <p className="text-[11px] text-slate-500 mt-1">Retention: {row.performance_retention_pct}%</p>
            </div>
          ))}
        </div>
      </div>

      {/* Experiment Registry Table */}
      <div className="bg-surface rounded-lg shadow-sm border border-slate-200">
        <div className="p-4 border-b border-slate-200 flex items-center justify-between">
          <h2 className="text-base font-bold text-slate-900">Executed Experiment Registry Log</h2>
          <span className="text-xs font-mono text-slate-500">{experiments.length} Experiments Recorded</span>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-600">
            <thead className="bg-slate-50 border-b border-slate-200 text-xs font-semibold text-slate-700 uppercase">
              <tr>
                <th className="px-4 py-3">Exp ID</th>
                <th className="px-4 py-3">Model</th>
                <th className="px-4 py-3">AUROC</th>
                <th className="px-4 py-3">AUPRC</th>
                <th className="px-4 py-3">F1</th>
                <th className="px-4 py-3">Sensitivity</th>
                <th className="px-4 py-3">Specificity</th>
                <th className="px-4 py-3">Brier Score</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 font-mono text-xs">
              {experiments.map((exp, idx) => (
                <tr key={idx} className="hover:bg-slate-50/50">
                  <td className="px-4 py-3 font-bold text-brand-700">{exp.experiment_id}</td>
                  <td className="px-4 py-3 font-sans font-semibold text-slate-900">{exp.model_name}</td>
                  <td className="px-4 py-3 font-bold text-slate-900">{exp.auroc?.toFixed(4)}</td>
                  <td className="px-4 py-3">{exp.auprc?.toFixed(4)}</td>
                  <td className="px-4 py-3">{exp.f1?.toFixed(4)}</td>
                  <td className="px-4 py-3">{exp.sensitivity?.toFixed(4)}</td>
                  <td className="px-4 py-3">{exp.specificity?.toFixed(4)}</td>
                  <td className="px-4 py-3 text-emerald-700 font-bold">{exp.brier_score?.toFixed(4)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
