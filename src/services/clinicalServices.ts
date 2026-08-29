import type { Patient } from '../types/patient';
import type { Alert } from '../types/alert';
import type { TimelineEvent } from '../types/timeline';
import type { Prediction } from '../types/predictions';
import { mockPatients, mockAlerts, mockPredictions, mockTimelines } from '../mock-data/db';

const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

export const patientService = {
  async getPatients(): Promise<Patient[]> {
    await delay(500);
    return mockPatients;
  },

  async getPatient(id: string): Promise<Patient> {
    await delay(300);
    const patient = mockPatients.find(p => p.id === id);
    if (!patient) throw new Error('Patient not found');
    return patient;
  },

  async getPatientPredictions(id: string): Promise<Prediction[]> {
    await delay(400);
    return mockPredictions[id] || [];
  },

  async getPatientTimeline(id: string): Promise<TimelineEvent[]> {
    await delay(400);
    return mockTimelines[id] || [];
  }
};

export const alertService = {
  async getAlerts(): Promise<Alert[]> {
    await delay(400);
    return mockAlerts;
  },
  
  async acknowledgeAlert(id: string): Promise<void> {
    await delay(300);
    const alert = mockAlerts.find(a => a.id === id);
    if (alert) {
      alert.status = 'Acknowledged';
    }
  }
};
