import { Patient } from '../types/patient';
import { Alert } from '../types/alert';
import { TimelineEvent } from '../types/timeline';
import { Prediction } from '../types/predictions';

export const patientService = {
  async getPatients(): Promise<Patient[]> {
    const res = await fetch('/api/patients');
    if (!res.ok) throw new Error('Failed to fetch patients');
    return res.json();
  },

  async getPatient(id: string): Promise<Patient> {
    const res = await fetch(`/api/patients/${id}`);
    if (!res.ok) throw new Error('Patient not found');
    return res.json();
  },

  async getPatientPredictions(id: string): Promise<Prediction[]> {
    const res = await fetch(`/api/patients/${id}/predictions`);
    if (!res.ok) throw new Error('Failed to fetch predictions');
    return res.json();
  },

  async getPatientTimeline(id: string): Promise<TimelineEvent[]> {
    const res = await fetch(`/api/patients/${id}/timeline`);
    if (!res.ok) throw new Error('Failed to fetch timeline');
    return res.json();
  }
};

export const alertService = {
  async getAlerts(): Promise<Alert[]> {
    const res = await fetch('/api/alerts');
    if (!res.ok) throw new Error('Failed to fetch alerts');
    return res.json();
  },
  
  async acknowledgeAlert(id: string): Promise<void> {
    const res = await fetch(`/api/alerts/${id}/acknowledge`, { method: 'POST' });
    if (!res.ok) throw new Error('Failed to acknowledge alert');
  }
};

