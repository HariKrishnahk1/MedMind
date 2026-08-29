import type { Patient } from '../types/patient';
import type { Alert } from '../types/alert';
import type { TimelineEvent } from '../types/timeline';
import type { Prediction } from '../types/predictions';
import { api } from './api';

export const patientService = {
  async getPatients(): Promise<Patient[]> {
    return api.getPatients();
  },

  async getPatient(id: string): Promise<Patient> {
    const p = await api.getPatient(id);
    if (!p) throw new Error('Patient not found');
    return p;
  },

  async getPatientPredictions(id: string): Promise<Prediction[]> {
    return api.getPredictions(id);
  },

  async getPatientTimeline(id: string): Promise<TimelineEvent[]> {
    return api.getTimeline(id);
  }
};

export const alertService = {
  async getAlerts(): Promise<Alert[]> {
    return api.getAlerts();
  },
  
  async acknowledgeAlert(id: string): Promise<void> {
    await api.acknowledgeAlert(id);
  }
};
