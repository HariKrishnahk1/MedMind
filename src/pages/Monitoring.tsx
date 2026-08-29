import React, { useState, useEffect } from 'react';
import { Activity, Heart, Wind, Thermometer, Droplet, AlertCircle } from 'lucide-react';
import { api } from '../services/api';
import type { Patient } from '../types/patient';

export const Monitoring: React.FC = () => {
  const [patients, setPatients] = useState<Patient[]>([]);

  // Simulate real-time updates
  useEffect(() => {
    api.getPatients().then(setPatients).catch(console.error);
    const interval = setInterval(() => {
      setPatients(prev => prev.map(p => {
        const hrFluctuation = Math.floor(Math.random() * 5) - 2;
        const spo2Fluctuation = Math.random() > 0.8 ? -1 : (Math.random() > 0.5 ? 1 : 0);
        
        return {
          ...p,
          vitals: {
            ...p.vitals,
            heartRate: Math.max(40, Math.min(180, p.vitals.heartRate + hrFluctuation)),
            oxygenSaturation: Math.max(70, Math.min(100, p.vitals.oxygenSaturation + spo2Fluctuation))
          }
        };
      }));
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  const getStatusColor = (val: number, min: number, max: number) => {
    if (val < min || val > max) return 'text-red-500 bg-red-50 border-red-200';
    return 'text-brand-600 bg-brand-50 border-brand-100';
  };

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Real-Time Monitoring</h1>
          <p className="text-sm text-slate-500">Live telemetry and vital signs for all ICU/Ward patients.</p>
        </div>
        <div className="flex items-center gap-2 text-sm font-medium text-emerald-600 bg-emerald-50 px-3 py-1.5 rounded-full border border-emerald-200">
          <span className="relative flex h-2.5 w-2.5">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
          </span>
          Live Updates Active
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
        {patients.map(patient => (
          <div key={patient.id} className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden flex flex-col">
            <div className="p-4 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-slate-200 flex items-center justify-center text-slate-700 font-bold">
                  {patient.name.split(' ').map(n => n[0]).join('')}
                </div>
                <div>
                  <h3 className="font-semibold text-slate-900">{patient.name}</h3>
                  <p className="text-xs text-slate-500">Room {patient.room} • {patient.mrn}</p>
                </div>
              </div>
              {patient.priority === 'Critical' && (
                <AlertCircle className="w-5 h-5 text-red-500 animate-pulse" />
              )}
            </div>
            
            <div className="p-5 flex-1 grid grid-cols-2 gap-4">
              <div className={`p-3 rounded-lg border ${getStatusColor(patient.vitals.heartRate, 60, 100)}`}>
                <div className="flex items-center gap-2 mb-1">
                  <Heart className="w-4 h-4" />
                  <span className="text-xs font-semibold uppercase tracking-wider">Heart Rate</span>
                </div>
                <div className="flex items-baseline gap-1">
                  <span className="text-2xl font-bold">{patient.vitals.heartRate}</span>
                  <span className="text-xs opacity-75">bpm</span>
                </div>
              </div>

              <div className={`p-3 rounded-lg border ${getStatusColor(patient.vitals.oxygenSaturation, 92, 100)}`}>
                <div className="flex items-center gap-2 mb-1">
                  <Activity className="w-4 h-4" />
                  <span className="text-xs font-semibold uppercase tracking-wider">SpO2</span>
                </div>
                <div className="flex items-baseline gap-1">
                  <span className="text-2xl font-bold">{patient.vitals.oxygenSaturation}</span>
                  <span className="text-xs opacity-75">%</span>
                </div>
              </div>

              <div className={`p-3 rounded-lg border ${getStatusColor(patient.vitals.bloodPressure.systolic, 90, 140)}`}>
                <div className="flex items-center gap-2 mb-1">
                  <Droplet className="w-4 h-4" />
                  <span className="text-xs font-semibold uppercase tracking-wider">NIBP</span>
                </div>
                <div className="flex items-baseline gap-1">
                  <span className="text-2xl font-bold">{patient.vitals.bloodPressure.systolic}/{patient.vitals.bloodPressure.diastolic}</span>
                </div>
              </div>

              <div className={`p-3 rounded-lg border text-brand-600 bg-brand-50 border-brand-100`}>
                <div className="flex items-center gap-2 mb-1">
                  <Wind className="w-4 h-4" />
                  <span className="text-xs font-semibold uppercase tracking-wider">Resp</span>
                </div>
                <div className="flex items-baseline gap-1">
                  <span className="text-2xl font-bold">{patient.vitals.respiratoryRate}</span>
                  <span className="text-xs opacity-75">/min</span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
