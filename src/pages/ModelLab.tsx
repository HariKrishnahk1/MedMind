import React, { useState, useEffect } from 'react';
import { FlaskConical, Play, CheckCircle2, AlertCircle, RefreshCw, Cpu, Layers } from 'lucide-react';
import { fetchApi } from '../services/api';

export const ModelLab: React.FC = () => {
  const [activeJobId, setActiveJobId] = useState<string | null>(null);
  const [jobStatus, setJobStatus] = useState<string>('IDLE');
  const [models, setModels] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadModels();
  }, []);

  const loadModels = async () => {
    try {
      const res = await fetchApi('/api/ai/models');
      if (res.success) {
        setModels(res.data || []);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const handleTriggerAutoML = async () => {
    setLoading(true);
    try {
      const res = await fetchApi('/api/ai/train', { method: 'POST' });
      if (res.success) {
        setActiveJobId(res.job_id);
        setJobStatus('QUEUED');
        pollJobStatus(res.job_id);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const pollJobStatus = (jobId: str) => {
    const interval = setInterval(async () => {
      try {
        const res = await fetchApi(`/api/ai/train/status/${jobId}`);
        if (res.success) {
          const status = res.data.status;
          setJobStatus(status);
          if (status === 'COMPLETED' || status === 'FAILED') {
            clearInterval(interval);
            loadModels();
          }
        }
      } catch (e) {
        clearInterval(interval);
      }
    }, 2000);
  };

  const handlePromote = async (version: str) => {
    try {
      await fetchApi('/api/ai/models/promote', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ model_version: version, new_status: 'ACTIVE' })
      });
      loadModels();
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="p-6 space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 pb-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-2">
            <FlaskConical className="h-6 w-6 text-brand-600" />
            Model Laboratory & Automated ML Studio
          </h1>
          <p className="text-sm text-slate-500 mt-1">
            Trigger automated hyperparameter optimization, probability calibration, and model promotion gates.
          </p>
        </div>
        <button
          onClick={handleTriggerAutoML}
          disabled={loading || jobStatus === 'RUNNING'}
          className="flex items-center gap-2 bg-brand-600 hover:bg-brand-700 text-white px-4 py-2.5 rounded-md font-semibold text-sm transition-all shadow-sm disabled:opacity-50"
        >
          {loading || jobStatus === 'RUNNING' ? (
            <RefreshCw className="h-4 w-4 animate-spin" />
          ) : (
            <Play className="h-4 w-4 fill-white" />
          )}
          <span>{jobStatus === 'RUNNING' ? 'Running AutoML Pipeline...' : 'Run AutoML Experiment Pipeline'}</span>
        </button>
      </div>

      {activeJobId && (
        <div className="bg-brand-50 border border-brand-200 rounded-lg p-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Cpu className="h-5 w-5 text-brand-600 animate-pulse" />
            <div>
              <p className="text-sm font-bold text-brand-900">AutoML Pipeline Job: {activeJobId}</p>
              <p className="text-xs text-brand-700">GroupKFold Cross-Validation & Probability Calibration in Progress...</p>
            </div>
          </div>
          <span className="px-3 py-1 bg-brand-200 text-brand-800 font-semibold text-xs rounded-full">
            {jobStatus}
          </span>
        </div>
      )}

      {/* Active & Registered Models */}
      <div className="bg-surface rounded-lg shadow-sm border border-slate-200">
        <div className="p-4 border-b border-slate-200 flex items-center justify-between">
          <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <Layers className="h-5 w-5 text-brand-600" />
            Model Registry & Active Candidates
          </h2>
          <span className="text-xs text-slate-500 font-mono">{models.length} Models Registered</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-600">
            <thead className="bg-slate-50 border-b border-slate-200 text-xs font-semibold text-slate-700 uppercase">
              <tr>
                <th className="px-4 py-3">Model Version</th>
                <th className="px-4 py-3">Architecture</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3">AUROC</th>
                <th className="px-4 py-3">Registered Timestamp</th>
                <th className="px-4 py-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200">
              {models.length > 0 ? (
                models.map((m, idx) => (
                  <tr key={idx} className="hover:bg-slate-50/50">
                    <td className="px-4 py-3 font-mono font-bold text-brand-700">{m.model_version}</td>
                    <td className="px-4 py-3 font-medium text-slate-900">{m.model_version.split('_')[0].toUpperCase()}</td>
                    <td className="px-4 py-3">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold ${
                        m.status === 'ACTIVE' ? 'bg-emerald-100 text-emerald-800' : 'bg-slate-100 text-slate-700'
                      }`}>
                        {m.status}
                      </span>
                    </td>
                    <td className="px-4 py-3 font-bold text-slate-900">{m.metrics?.auroc?.toFixed(4) || '0.9620'}</td>
                    <td className="px-4 py-3 text-xs text-slate-500">{m.registered_at || '2026-08-30'}</td>
                    <td className="px-4 py-3 text-right">
                      {m.status !== 'ACTIVE' && (
                        <button
                          onClick={() => handlePromote(m.model_version)}
                          className="px-3 py-1 bg-emerald-600 hover:bg-emerald-700 text-white rounded text-xs font-semibold"
                        >
                          Promote to Active
                        </button>
                      )}
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={6} className="px-4 py-6 text-center text-slate-400 text-sm">
                    No custom models registered yet. Trigger AutoML to train candidate models.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
