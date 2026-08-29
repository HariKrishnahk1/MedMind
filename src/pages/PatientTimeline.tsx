import React, { useState, useEffect } from 'react';
import { History, Activity, AlertTriangle, ArrowRightCircle } from 'lucide-react';
import { api } from '../services/api';
import type { Patient } from '../types/patient';
import type { TimelineEvent } from '../types/timeline';

export const PatientTimeline: React.FC = () => {
  const [patient, setPatient] = useState<Patient | null>(null);
  const [timelineEvents, setTimelineEvents] = useState<TimelineEvent[]>([]);

  useEffect(() => {
    // Assuming P-1001 for demonstration as in original code
    api.getPatient('P-1001').then(p => {
        if (p) setPatient(p);
    });
    api.getTimeline('P-1001').then(setTimelineEvents);
  }, []);

  if (!patient) return <div>Loading...</div>;

  const getEventIcon = (type: string) => {
    switch (type) {
      case 'Admission': return <ArrowRightCircle className="h-5 w-5 text-blue-500" />;
      case 'Alert': return <AlertTriangle className="h-5 w-5 text-red-500" />;
      case 'Priority Change': return <Activity className="h-5 w-5 text-orange-500" />;
      default: return <History className="h-5 w-5 text-slate-500" />;
    }
  };

  return (
    <div className="p-6 max-w-4xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-2">
          <History className="h-6 w-6 text-brand-600" />
          Patient Timeline
        </h1>
        <p className="text-sm text-slate-500">Longitudinal view of clinical events and AI interventions.</p>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <h2 className="text-lg font-bold text-slate-900 mb-6">Timeline for {patient.name}</h2>
        
        <div className="relative border-l-2 border-slate-200 ml-4 space-y-8">
          {timelineEvents.map((event, index) => (
            <div key={event.id} className="relative pl-8">
              <div className="absolute -left-[11px] top-1 bg-white border-2 border-slate-200 rounded-full p-0.5">
                {getEventIcon(event.type)}
              </div>
              
              <div className="bg-slate-50 rounded-lg p-4 border border-slate-100">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="font-bold text-slate-900">{event.title}</h3>
                  <span className="text-xs font-medium text-slate-500">
                    {new Date(event.timestamp).toLocaleString()}
                  </span>
                </div>
                <p className="text-sm text-slate-600 mb-3">{event.description}</p>
                <div className="flex gap-2">
                  <span className="px-2 py-0.5 bg-white border border-slate-200 rounded text-xs font-medium text-slate-600 shadow-sm">
                    {event.type}
                  </span>
                  <span className="px-2 py-0.5 bg-slate-200 rounded text-xs font-medium text-slate-700 shadow-sm">
                    Priority: {event.priorityAtTime}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
