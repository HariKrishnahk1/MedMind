import React, { useState } from 'react';
import { AlertTriangle, Clock, CheckCircle, Search, Filter, ShieldAlert } from 'lucide-react';
import { mockAlerts, mockPatients } from '../mock-data/db';
import { Alert } from '../types/alert';

export const AlertCenter: React.FC = () => {
  const [alerts, setAlerts] = useState<Alert[]>(mockAlerts);
  const [searchTerm, setSearchTerm] = useState('');

  const acknowledgeAlert = (id: string) => {
    setAlerts(prev => prev.map(a => a.id === id ? { ...a, status: 'Acknowledged' } : a));
  };

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-2">
            <ShieldAlert className="h-6 w-6 text-brand-600" />
            Alert Center
          </h1>
          <p className="text-sm text-slate-500">Triage and manage clinical AI alerts and early warnings.</p>
        </div>
        <div className="flex items-center gap-3 w-full sm:w-auto">
          <div className="relative flex-1 sm:flex-none sm:w-64">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
            <input 
              type="text" 
              placeholder="Search alerts..." 
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-9 pr-4 py-2 bg-white border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500 transition-all shadow-sm"
            />
          </div>
          <button className="flex items-center gap-2 px-4 py-2 bg-white border border-slate-200 rounded-lg text-sm font-medium text-slate-700 hover:bg-slate-50 transition-colors shadow-sm">
            <Filter className="h-4 w-4" />
            Filter
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-4">
        {alerts.map((alert) => {
          const patient = mockPatients.find(p => p.id === alert.patientId);
          const isCritical = alert.newPriority === 'Critical';
          const isAcknowledged = alert.status === 'Acknowledged';

          return (
            <div key={alert.id} className={`bg-white rounded-xl shadow-sm border overflow-hidden ${isCritical && !isAcknowledged ? 'border-red-300 ring-1 ring-red-300' : 'border-slate-200'}`}>
              <div className={`p-4 sm:p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4 ${isCritical && !isAcknowledged ? 'bg-red-50/50' : ''}`}>
                <div className="flex items-start gap-4">
                  <div className={`p-3 rounded-full shrink-0 ${isCritical ? 'bg-red-100 text-red-600' : 'bg-orange-100 text-orange-600'}`}>
                    <AlertTriangle className="h-6 w-6" />
                  </div>
                  <div>
                    <div className="flex flex-wrap items-center gap-2 mb-1">
                      <h3 className="font-bold text-slate-900 text-lg">{alert.type}</h3>
                      <span className={`px-2 py-0.5 rounded text-xs font-semibold ${isCritical ? 'bg-red-100 text-red-700' : 'bg-orange-100 text-orange-700'}`}>
                        {alert.newPriority} Priority
                      </span>
                      {isAcknowledged && (
                        <span className="flex items-center gap-1 px-2 py-0.5 bg-green-100 text-green-700 rounded text-xs font-semibold">
                          <CheckCircle className="h-3 w-3" /> Acknowledged
                        </span>
                      )}
                    </div>
                    <p className="text-slate-600 font-medium mb-1">{alert.message}</p>
                    <p className="text-sm text-slate-500 mb-3">
                      Patient: <span className="font-semibold text-slate-700">{patient?.name} ({patient?.room})</span> • AI Confidence High
                    </p>
                    <div className="bg-white border border-slate-100 rounded p-3 text-sm">
                      <p className="font-semibold text-slate-700 mb-1">Clinical Factors:</p>
                      <ul className="list-disc list-inside text-slate-600 space-y-1">
                        {alert.clinicalFactors.map((factor, idx) => (
                          <li key={idx}>{factor}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>
                
                <div className="flex sm:flex-col items-center sm:items-end justify-between sm:justify-center gap-4 shrink-0 sm:min-w-[140px]">
                  <div className="text-sm text-slate-500 flex items-center gap-1.5">
                    <Clock className="h-4 w-4" />
                    {new Date(alert.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </div>
                  {!isAcknowledged && (
                    <button 
                      onClick={() => acknowledgeAlert(alert.id)}
                      className={`px-4 py-2 rounded-lg text-sm font-semibold shadow-sm transition-all ${isCritical ? 'bg-red-600 hover:bg-red-700 text-white' : 'bg-brand-600 hover:bg-brand-700 text-white'}`}
                    >
                      Acknowledge
                    </button>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
