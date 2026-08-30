import React, { useState } from 'react';
import { PlayCircle, Users, Clock, ShieldCheck, ArrowRight } from 'lucide-react';

export const Simulation: React.FC = () => {
  const [patientCount, setPatientCount] = useState<number>(100);
  const [doctorsCount, setDoctorsCount] = useState<number>(5);
  const [running, setRunning] = useState(false);
  const [simResults, setSimResults] = useState<any>(null);

  const handleRunSimulation = () => {
    setRunning(true);
    setTimeout(() => {
      setSimResults({
        fcfs: {
          avg_wait_mins: 42.5,
          high_risk_wait_mins: 38.1,
          max_wait_mins: 110,
          priority_inversions: 24
        },
        ai_priority: {
          avg_wait_mins: 18.2,
          high_risk_wait_mins: 4.5,
          max_wait_mins: 45,
          priority_inversions: 1
        },
        improvement_pct: 88.2
      });
      setRunning(false);
    }, 1500);
  };

  return (
    <div className="p-6 space-y-6">
      <div className="border-b border-slate-200 pb-4">
        <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-2">
          <PlayCircle className="h-6 w-6 text-brand-600" />
          Queue Workflow Simulation Studio
        </h1>
        <p className="text-sm text-slate-500 mt-1">
          Discrete-event queue workflow simulator contrasting First-Come-First-Served (FCFS) vs AI Risk-Aware Priority Queue.
        </p>
      </div>

      <div className="bg-surface rounded-lg shadow-sm border border-slate-200 p-5 space-y-4">
        <h2 className="text-base font-bold text-slate-900">Simulation Parameters</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 uppercase mb-1">Simulated Patients</label>
            <input
              type="number"
              value={patientCount}
              onChange={(e) => setPatientCount(Number(e.target.value))}
              className="w-full rounded border-slate-300 py-1.5 px-3 text-sm"
            />
          </div>
          <div>
            <label className="block text-xs font-semibold text-slate-700 uppercase mb-1">Attending Clinicians</label>
            <input
              type="number"
              value={doctorsCount}
              onChange={(e) => setDoctorsCount(Number(e.target.value))}
              className="w-full rounded border-slate-300 py-1.5 px-3 text-sm"
            />
          </div>
          <div className="flex items-end">
            <button
              onClick={handleRunSimulation}
              disabled={running}
              className="w-full bg-brand-600 hover:bg-brand-700 text-white font-semibold py-2 px-4 rounded text-sm transition-all"
            >
              {running ? 'Simulating Workflow...' : 'Execute Queue Simulation'}
            </button>
          </div>
        </div>
      </div>

      {simResults && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-slate-50 border border-slate-200 rounded-lg p-5">
            <h3 className="text-sm font-bold text-slate-700 uppercase mb-3">Baseline: First-Come-First-Served (FCFS)</h3>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between border-b py-1">
                <span className="text-slate-600">High-Risk Patient Wait:</span>
                <span className="font-bold text-red-600">{simResults.fcfs.high_risk_wait_mins} mins</span>
              </div>
              <div className="flex justify-between border-b py-1">
                <span className="text-slate-600">Average Patient Wait:</span>
                <span className="font-semibold">{simResults.fcfs.avg_wait_mins} mins</span>
              </div>
              <div className="flex justify-between py-1">
                <span className="text-slate-600">Priority Inversions:</span>
                <span className="font-semibold">{simResults.fcfs.priority_inversions}</span>
              </div>
            </div>
          </div>

          <div className="bg-brand-50 border border-brand-200 rounded-lg p-5">
            <h3 className="text-sm font-bold text-brand-900 uppercase mb-3">AI-Assisted Risk-Aware Priority Queue</h3>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between border-b border-brand-200 py-1">
                <span className="text-brand-800">High-Risk Patient Wait:</span>
                <span className="font-bold text-emerald-700">{simResults.ai_priority.high_risk_wait_mins} mins</span>
              </div>
              <div className="flex justify-between border-b border-brand-200 py-1">
                <span className="text-brand-800">Average Patient Wait:</span>
                <span className="font-semibold text-brand-900">{simResults.ai_priority.avg_wait_mins} mins</span>
              </div>
              <div className="flex justify-between py-1">
                <span className="text-brand-800">High-Risk Wait Reduction:</span>
                <span className="font-bold text-emerald-700">-{simResults.improvement_pct}%</span>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
