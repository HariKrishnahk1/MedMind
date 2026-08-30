import type { Patient } from '../types/patient';
import type { Alert } from '../types/alert';
import type { TimelineEvent } from '../types/timeline';
import type { Prediction } from '../types/predictions';

const API_BASE = 'http://localhost:8000/api';

export const fetchApi = async (endpoint: string, options?: RequestInit) => {
  const url = endpoint.startsWith('http') ? endpoint : `http://localhost:8000${endpoint}`;
  const res = await fetch(url, options);
  return res.json();
};

export const api = {
  getPatients: async (): Promise<Patient[]> => {
    const res = await fetch(`${API_BASE}/patients`);
    return res.json();
  },

  getPatient: async (id: string): Promise<Patient | undefined> => {
    const res = await fetch(`${API_BASE}/patients/${id}`);
    if (!res.ok) return undefined;
    return res.json();
  },

  getPredictions: async (id: string): Promise<Prediction[]> => {
    const res = await fetch(`${API_BASE}/patients/${id}/predictions`);
    return res.json();
  },

  getTimeline: async (id: string): Promise<TimelineEvent[]> => {
    const res = await fetch(`${API_BASE}/patients/${id}/timeline`);
    return res.json();
  },

  getAlerts: async (): Promise<Alert[]> => {
    const res = await fetch(`${API_BASE}/alerts`);
    return res.json();
  },

  acknowledgeAlert: async (id: string): Promise<boolean> => {
    const res = await fetch(`${API_BASE}/alerts/${id}/acknowledge`, { method: 'POST' });
    return res.ok;
  },

  generateHandover: async (patientId: string, receivingFacility: string) => {
    const res = await fetch(`${API_BASE}/patients/${patientId}/handover`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ receivingFacility })
    });
    return res.json();
  }
};
