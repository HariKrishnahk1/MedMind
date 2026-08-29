import { Patient } from '../types/patient';
import { Alert } from '../types/alert';

export const api = {
  // GET /api/patients
  getPatients: async (): Promise<Patient[]> => {
    const res = await fetch('/api/patients');
    if (!res.ok) throw new Error('Failed to fetch patients');
    return res.json();
  },

  // GET /api/patients/{id}
  getPatient: async (id: string): Promise<Patient | undefined> => {
    const res = await fetch(`/api/patients/${id}`);
    if (res.status === 404) return undefined;
    if (!res.ok) throw new Error('Failed to fetch patient');
    return res.json();
  },

  // GET /api/patients/{id}/predictions
  getPredictions: async (id: string) => {
    const res = await fetch(`/api/patients/${id}/predictions`);
    if (!res.ok) throw new Error('Failed to fetch predictions');
    return res.json();
  },

  // GET /api/patients/{id}/timeline
  getTimeline: async (id: string) => {
    const res = await fetch(`/api/patients/${id}/timeline`);
    if (!res.ok) throw new Error('Failed to fetch timeline');
    return res.json();
  },

  // GET /api/alerts
  getAlerts: async (): Promise<Alert[]> => {
    const res = await fetch('/api/alerts');
    if (!res.ok) throw new Error('Failed to fetch alerts');
    return res.json();
  },

  // POST /api/alerts/{id}/acknowledge
  acknowledgeAlert: async (id: string): Promise<boolean> => {
    const res = await fetch(`/api/alerts/${id}/acknowledge`, { method: 'POST' });
    if (!res.ok) return false;
    const data = await res.json();
    return data.success;
  },

  // POST /api/handover
  generateHandover: async (patientId: string, receivingFacility: string) => {
    const res = await fetch('/api/handover', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ patientId, receivingFacility }),
    });
    if (!res.ok) throw new Error('Failed to generate handover');
    return res.json();
  }
};

