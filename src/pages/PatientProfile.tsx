import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { patientService } from '../services/clinicalServices';
import type { Patient } from '../types/patient';
import type { Prediction } from '../types/predictions';
import type { TimelineEvent } from '../types/timeline';
import { Activity, ArrowLeft, BrainCircuit, AlertTriangle, Info } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';

// Mock chart data for vitals
const vitalsData = [
  { time: '08:00', hr: 82, bp: 110, spo2: 98 },
  { time: '09:00', hr: 85, bp: 108, spo2: 97 },
  { time: '10:00', hr: 90, bp: 105, spo2: 96 },
  { time: '11:00', hr: 95, bp: 100, spo2: 95 },
  { time: '12:00', hr: 105, bp: 95, spo2: 92 },
  { time: '13:00', hr: 112, bp: 90, spo2: 90 },
  { time: '14:00', hr: 118, bp: 88, spo2: 89 },
];

export const PatientProfile: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [patient, setPatient] = useState<Patient | null>(null);
  const [predictions, setPredictions] = useState<Prediction[]>([]);
  const [timeline, setTimeline] = useState<TimelineEvent[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      if (!id) return;
      try {
        const [patientData, predictionData, timelineData] = await Promise.all([
          patientService.getPatient(id),
          patientService.getPatientPredictions(id),
          patientService.getPatientTimeline(id)
        ]);
        setPatient(patientData);
        setPredictions(predictionData);
        setTimeline(timelineData);
      } catch (error) {
        console.error("Failed to fetch patient data", error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [id]);

  if (loading) {
    return <div className="flex items-center justify-center h-full"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-brand-600"></div></div>;
  }

  if (!patient) {
    return <div>Patient not found</div>;
  }

  const latestPrediction = predictions.length > 0 ? predictions[0] : null;

  return (
    <div className="space-y-6 pb-10">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div className="flex items-center gap-4">
          <Link to="/dashboard" className="p-2 border border-slate-200 rounded-lg text-slate-500 hover:bg-slate-50 transition-colors">
            <ArrowLeft className="h-4 w-4" />
          </Link>
          <div>
            <h1 className="text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-3">
              {patient.name}
              <span className="text-sm font-medium px-2 py-0.5 rounded bg-slate-100 text-slate-600 border border-slate-200">{patient.mrn}</span>
            </h1>
            <p className="text-sm text-slate-500 mt-1">
              {patient.age} y/o {patient.gender} • Room {patient.room} • {patient.attendingPhysician}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <div className="text-right">
            <p className="text-xs text-slate-500 font-medium">Current Priority</p>
            <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-bold border mt-1
              ${patient.priority === 'Critical' ? 'bg-rose-50 text-risk-critical border-rose-200' : ''}
              ${patient.priority === 'High' ? 'bg-orange-50 text-risk-high border-orange-200' : ''}
              ${patient.priority === 'Moderate' ? 'bg-amber-50 text-risk-moderate border-amber-200' : ''}
              ${patient.priority === 'Stable' ? 'bg-emerald-50 text-risk-low border-emerald-200' : ''}
            `}>
              {patient.priority}
            </span>
          </div>
          <button className="px-4 py-2 bg-brand-600 hover:bg-brand-700 text-white rounded-lg text-sm font-medium shadow-sm transition-colors">
            Clinical Handover
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Left Column: Demographics & AI Explainability */}
        <div className="space-y-6">
          {/* Clinical Overview */}
          <div className="bg-surface border border-slate-200 rounded-xl p-5 shadow-sm">
            <h2 className="text-base font-semibold text-slate-900 mb-4 flex items-center">
              <Activity className="h-5 w-5 mr-2 text-brand-500" />
              Clinical Overview
            </h2>
            <div className="space-y-4">
              <div>
                <p className="text-xs text-slate-500 font-medium">Primary Diagnosis</p>
                <p className="text-sm text-slate-900 font-medium mt-1">{patient.primaryDiagnosis}</p>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-xs text-slate-500 font-medium">Code Status</p>
                  <p className="text-sm text-slate-900 font-medium mt-1">{patient.codeStatus}</p>
                </div>
                <div>
                  <p className="text-xs text-slate-500 font-medium">Allergies</p>
                  <p className="text-sm text-rose-600 font-medium mt-1">{patient.allergies.join(', ')}</p>
                </div>
              </div>
            </div>
          </div>

          {/* AI Explainability */}
          {latestPrediction && (
            <div className="bg-gradient-to-b from-brand-50 to-white border border-brand-200 rounded-xl p-5 shadow-sm relative overflow-hidden">
              <div className="absolute top-0 right-0 bg-brand-100 text-brand-700 text-[10px] font-bold px-2 py-1 rounded-bl-lg uppercase tracking-wider">
                AI Risk Assessment
              </div>
              <h2 className="text-base font-semibold text-slate-900 mb-2 flex items-center">
                <BrainCircuit className="h-5 w-5 mr-2 text-brand-600" />
                Deterioration Risk
              </h2>
              
              <div className="flex items-center gap-4 mt-4">
                <div className="relative w-16 h-16 flex items-center justify-center">
                  <svg className="w-full h-full transform -rotate-90">
                    <circle cx="32" cy="32" r="28" stroke="currentColor" strokeWidth="6" fill="transparent" className="text-slate-200" />
                    <circle cx="32" cy="32" r="28" stroke="currentColor" strokeWidth="6" fill="transparent" 
                      strokeDasharray="175" strokeDashoffset={175 - (175 * latestPrediction.riskScore) / 100}
                      className={latestPrediction.riskLevel === 'Critical' ? 'text-risk-critical' : 'text-risk-high'} 
                    />
                  </svg>
                  <div className="absolute flex flex-col items-center justify-center">
                    <span className="text-lg font-bold text-slate-900">{latestPrediction.riskScore}</span>
                  </div>
                </div>
                <div>
                  <p className="text-sm font-medium text-slate-900">{latestPrediction.riskLevel} Risk of Decompensation</p>
                  <p className="text-xs text-slate-500 mt-0.5">Horizon: {latestPrediction.predictionHorizon}</p>
                </div>
              </div>

              <div className="mt-5 space-y-3">
                <p className="text-xs text-slate-700 font-medium">{latestPrediction.explanationText}</p>
                
                <div className="bg-white rounded-lg border border-slate-200 p-3">
                  <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Top Contributing Factors</p>
                  <ul className="space-y-2">
                    {latestPrediction.contributingFactors.map((factor, idx) => (
                      <li key={idx} className="flex justify-between items-center text-sm">
                        <span className="text-slate-700 flex items-center">
                          {factor.direction === 'decrease' ? <ArrowDownRight className="h-3 w-3 text-rose-500 mr-1" /> : <ArrowUpRight className="h-3 w-3 text-rose-500 mr-1" />}
                          {factor.name}
                        </span>
                        <span className="font-medium text-slate-900 font-mono">{factor.currentValue}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              <div className="mt-4 flex items-start gap-2 bg-yellow-50 p-2.5 rounded border border-yellow-200">
                <Info className="h-4 w-4 text-yellow-600 flex-shrink-0 mt-0.5" />
                <p className="text-[11px] text-yellow-800 leading-tight">
                  <span className="font-semibold">Clinician Review Required:</span> This AI risk assessment is a decision support tool and does not replace clinical judgment.
                </p>
              </div>
            </div>
          )}
        </div>

        {/* Middle & Right Column: Vitals Trends & Timeline */}
        <div className="lg:col-span-2 space-y-6">
          
          {/* Current Vitals */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div className="bg-surface border border-slate-200 rounded-xl p-4 shadow-sm">
              <p className="text-xs text-slate-500 font-medium">Heart Rate</p>
              <p className="text-2xl font-bold text-slate-900 mt-1 font-mono">{patient.vitals.heartRate} <span className="text-sm font-normal text-slate-500">bpm</span></p>
            </div>
            <div className="bg-surface border border-slate-200 rounded-xl p-4 shadow-sm">
              <p className="text-xs text-slate-500 font-medium">Blood Pressure</p>
              <p className="text-2xl font-bold text-slate-900 mt-1 font-mono">{patient.vitals.bloodPressure.systolic}/{patient.vitals.bloodPressure.diastolic} <span className="text-sm font-normal text-slate-500">mmHg</span></p>
            </div>
            <div className="bg-surface border border-slate-200 rounded-xl p-4 shadow-sm">
              <p className="text-xs text-slate-500 font-medium">SpO2</p>
              <p className={`text-2xl font-bold mt-1 font-mono ${patient.vitals.oxygenSaturation < 92 ? 'text-risk-critical' : 'text-slate-900'}`}>
                {patient.vitals.oxygenSaturation}<span className="text-sm font-normal text-slate-500">%</span>
              </p>
            </div>
            <div className="bg-surface border border-slate-200 rounded-xl p-4 shadow-sm">
              <p className="text-xs text-slate-500 font-medium">Resp. Rate</p>
              <p className="text-2xl font-bold text-slate-900 mt-1 font-mono">{patient.vitals.respiratoryRate} <span className="text-sm font-normal text-slate-500">/min</span></p>
            </div>
          </div>

          {/* Vitals Trends Chart */}
          <div className="bg-surface border border-slate-200 rounded-xl p-5 shadow-sm">
            <h2 className="text-base font-semibold text-slate-900 mb-4">Clinical Trends (24h)</h2>
            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={vitalsData} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                  <XAxis dataKey="time" axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#64748b' }} dy={10} />
                  <YAxis yAxisId="left" axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#64748b' }} dx={-10} domain={[60, 140]} />
                  <YAxis yAxisId="right" orientation="right" axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#64748b' }} dx={10} domain={[80, 100]} />
                  <Tooltip 
                    contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                    itemStyle={{ fontSize: '13px', fontWeight: 500 }}
                  />
                  <ReferenceLine yAxisId="right" y={92} stroke="#e11d48" strokeDasharray="3 3" />
                  <Line yAxisId="left" type="monotone" dataKey="hr" name="Heart Rate" stroke="#f59e0b" strokeWidth={2} dot={{ r: 4, strokeWidth: 2 }} activeDot={{ r: 6 }} />
                  <Line yAxisId="left" type="monotone" dataKey="bp" name="Systolic BP" stroke="#3b82f6" strokeWidth={2} dot={{ r: 4, strokeWidth: 2 }} activeDot={{ r: 6 }} />
                  <Line yAxisId="right" type="monotone" dataKey="spo2" name="SpO2 (%)" stroke="#10b981" strokeWidth={2} dot={{ r: 4, strokeWidth: 2 }} activeDot={{ r: 6 }} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
};
