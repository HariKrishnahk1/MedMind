import React, { useState, useEffect } from 'react';
import { ArrowRightLeft, FileText, CheckCircle, Hospital, Loader2, Download, AlertTriangle } from 'lucide-react';
import { Patient } from '../types/patient';
import { api } from '../services/api';

export const Handover: React.FC = () => {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [selectedPatientId, setSelectedPatientId] = useState<string>('');
  const [receivingFacility, setReceivingFacility] = useState('General Hospital - ICU Step-down');
  const [isGenerating, setIsGenerating] = useState(false);
  const [report, setReport] = useState<string | null>(null);
  const [isApproved, setIsApproved] = useState(false);

  useEffect(() => {
    api.getPatients().then(setPatients);
  }, []);

  const handleGenerate = async () => {
    if (!selectedPatientId) return;
    setIsGenerating(true);
    setReport(null);
    setIsApproved(false);
    try {
      const result = await api.generateHandover(selectedPatientId, receivingFacility);
      setReport(result.report);
    } catch (e) {
      console.error(e);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="p-6 max-w-5xl mx-auto space-y-6">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-2">
            <ArrowRightLeft className="h-6 w-6 text-brand-600" />
            Clinical Handover & Transfer
          </h1>
          <p className="text-sm text-slate-500">AI-assisted handover report generation.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="md:col-span-1 space-y-4">
          <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5">
            <h3 className="font-semibold text-slate-900 mb-4">1. Transfer Details</h3>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Select Patient</label>
                <select 
                  className="w-full border-slate-300 rounded-md shadow-sm focus:ring-brand-500 focus:border-brand-500 sm:text-sm"
                  value={selectedPatientId}
                  onChange={e => setSelectedPatientId(e.target.value)}
                >
                  <option value="">-- Choose Patient --</option>
                  {patients.map(p => (
                    <option key={p.id} value={p.id}>{p.name} ({p.room})</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Receiving Facility/Unit</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Hospital className="h-4 w-4 text-slate-400" />
                  </div>
                  <input 
                    type="text" 
                    value={receivingFacility}
                    onChange={e => setReceivingFacility(e.target.value)}
                    className="pl-9 w-full border-slate-300 rounded-md shadow-sm focus:ring-brand-500 focus:border-brand-500 sm:text-sm"
                  />
                </div>
              </div>

              <button 
                onClick={handleGenerate}
                disabled={!selectedPatientId || isGenerating}
                className="w-full mt-4 flex items-center justify-center gap-2 px-4 py-2 bg-brand-600 text-white rounded-lg text-sm font-medium hover:bg-brand-700 disabled:opacity-50 transition-colors"
              >
                {isGenerating ? <Loader2 className="h-4 w-4 animate-spin" /> : <FileText className="h-4 w-4" />}
                {isGenerating ? 'Generating...' : 'Generate AI Handover'}
              </button>
            </div>
          </div>
        </div>

        <div className="md:col-span-2">
          <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 min-h-[400px] flex flex-col">
            <h3 className="font-semibold text-slate-900 mb-4">2. Review & Approve</h3>
            
            {!report && !isGenerating && (
              <div className="flex-1 flex flex-col items-center justify-center text-slate-400 border-2 border-dashed border-slate-200 rounded-lg p-6">
                <FileText className="h-12 w-12 mb-3 text-slate-300" />
                <p>Select a patient and click generate to create a handover report.</p>
              </div>
            )}

            {isGenerating && (
              <div className="flex-1 flex flex-col items-center justify-center text-slate-500 border-2 border-slate-100 rounded-lg p-6 bg-slate-50">
                <Loader2 className="h-10 w-10 animate-spin text-brand-500 mb-4" />
                <p className="font-medium">Synthesizing clinical notes and vitals...</p>
                <p className="text-xs text-slate-400 mt-2">AI is reviewing the patient timeline</p>
              </div>
            )}

            {report && !isGenerating && (
              <div className="flex-1 flex flex-col">
                <div className="mb-4 bg-amber-50 border border-amber-200 rounded-md p-3 flex items-start gap-3 text-amber-800 text-sm">
                  <AlertTriangle className="h-5 w-5 shrink-0 text-amber-600" />
                  <div>
                    <span className="font-bold">Clinician Review Required.</span> This report is AI-generated. Please carefully review all synthesized information against source records before approving for transfer.
                  </div>
                </div>

                <div className="flex-1 bg-slate-50 border border-slate-200 rounded-md p-4 whitespace-pre-wrap text-sm text-slate-800 font-mono shadow-inner mb-4 overflow-y-auto">
                  {report}
                </div>

                <div className="flex items-center justify-end gap-3 mt-auto pt-4 border-t border-slate-100">
                  {isApproved ? (
                    <button className="flex items-center gap-2 px-4 py-2 bg-emerald-600 text-white rounded-lg text-sm font-medium hover:bg-emerald-700 transition-colors shadow-sm">
                      <Download className="h-4 w-4" />
                      Export to EMR
                    </button>
                  ) : (
                    <button 
                      onClick={() => setIsApproved(true)}
                      className="flex items-center gap-2 px-4 py-2 bg-brand-600 text-white rounded-lg text-sm font-medium hover:bg-brand-700 transition-colors shadow-sm"
                    >
                      <CheckCircle className="h-4 w-4" />
                      Approve Report
                    </button>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
