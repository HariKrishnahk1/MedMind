import React, { useState, useEffect } from 'react';
import { BrainCircuit, Info, TrendingDown, TrendingUp, HelpCircle } from 'lucide-react';
import { api } from '../services/api';
import type { Patient } from '../types/patient';
import type { Prediction } from '../types/predictions';

export const AIExplainability: React.FC = () => {
  const [patient, setPatient] = useState<Patient | null>(null);
  const [prediction, setPrediction] = useState<Prediction | null>(null);

  useEffect(() => {
    api.getPatient('P-1001').then(p => p && setPatient(p));
    api.getPredictions('P-1001').then(preds => setPrediction(preds[0]));
  }, []);

  if (!patient || !prediction) return <div>Loading...</div>;

  return (
    <div className="p-6 max-w-5xl mx-auto space-y-6">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-2">
            <BrainCircuit className="h-6 w-6 text-brand-600" />
            AI Explainability
          </h1>
          <p className="text-sm text-slate-500">Understand the 'Why' behind AI-driven predictions.</p>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <div className="bg-brand-50 border-b border-brand-100 p-6 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div>
            <h2 className="text-lg font-bold text-slate-900">Risk Assessment: {patient?.name}</h2>
            <p className="text-sm text-slate-600">Trajectory prediction over the next {prediction.predictionHorizon}.</p>
          </div>
          <div className="flex items-center gap-3 bg-white p-3 rounded-lg shadow-sm border border-brand-200">
            <div className="text-center px-3 border-r border-slate-200">
              <div className="text-xs text-slate-500 font-semibold uppercase tracking-wider mb-1">Risk Score</div>
              <div className="text-3xl font-bold text-red-600">{prediction.riskScore}</div>
            </div>
            <div className="text-center px-3">
              <div className="text-xs text-slate-500 font-semibold uppercase tracking-wider mb-1">Level</div>
              <div className="text-lg font-bold text-red-600 uppercase">{prediction.riskLevel}</div>
            </div>
          </div>
        </div>

        <div className="p-6 space-y-8">
          <div className="bg-slate-50 rounded-lg p-5 border border-slate-200">
            <div className="flex items-start gap-3">
              <Info className="h-5 w-5 text-brand-600 shrink-0 mt-0.5" />
              <div>
                <h3 className="font-semibold text-slate-900 mb-1">AI Conclusion</h3>
                <p className="text-slate-700 leading-relaxed">{prediction.explanationText}</p>
              </div>
            </div>
          </div>

          <div>
            <h3 className="font-bold text-slate-900 mb-4 flex items-center gap-2">
              Feature Importance
              <HelpCircle className="h-4 w-4 text-slate-400 cursor-help" />
            </h3>
            
            <div className="space-y-4">
              {prediction.contributingFactors.map((factor, idx) => (
                <div key={idx} className="bg-white border border-slate-200 rounded-lg p-4 flex items-center gap-6">
                  <div className="flex-1">
                    <div className="flex justify-between items-center mb-2">
                      <span className="font-semibold text-slate-800">{factor.name}</span>
                      <span className="text-sm font-medium text-slate-500">Weight: {(factor.impact * 100).toFixed(0)}%</span>
                    </div>
                    <div className="h-2 w-full bg-slate-100 rounded-full overflow-hidden">
                      <div 
                        className={`h-full rounded-full ${factor.impact > 0.3 ? 'bg-red-500' : 'bg-orange-400'}`} 
                        style={{ width: `${factor.impact * 100}%` }}
                      ></div>
                    </div>
                  </div>
                  
                  <div className="w-48 shrink-0 bg-slate-50 rounded-md p-3 text-sm">
                    <div className="flex justify-between mb-1">
                      <span className="text-slate-500">Current:</span>
                      <span className="font-bold flex items-center gap-1">
                        {factor.currentValue}
                        {factor.direction === 'decrease' ? <TrendingDown className="h-4 w-4 text-red-500" /> : <TrendingUp className="h-4 w-4 text-red-500" />}
                      </span>
                    </div>
                    <div className="flex justify-between text-xs">
                      <span className="text-slate-400">Normal Range:</span>
                      <span className="text-slate-600">{factor.normalRange}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
