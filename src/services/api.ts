import { mockPatients, mockAlerts, mockPredictions, mockTimelines } from '../mock-data/db';
import type { Patient } from '../types/patient';
import type { Alert } from '../types/alert';

// Utility to simulate network delay
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

export const api = {
  // GET /api/patients
  getPatients: async (): Promise<Patient[]> => {
    await delay(600); // simulate latency
    return [...mockPatients];
  },

  // GET /api/patients/{id}
  getPatient: async (id: string): Promise<Patient | undefined> => {
    await delay(500);
    return mockPatients.find(p => p.id === id);
  },

  // GET /api/patients/{id}/observations
  getObservations: async (id: string) => {
    await delay(300);
    const patient = mockPatients.find(p => p.id === id);
    return patient ? patient.vitals : null;
  },

  // GET /api/patients/{id}/predictions
  getPredictions: async (id: string) => {
    await delay(400);
    return mockPredictions[id] || [];
  },

  // GET /api/patients/{id}/timeline
  getTimeline: async (id: string) => {
    await delay(400);
    return mockTimelines[id] || [];
  },

  // GET /api/alerts
  getAlerts: async (): Promise<Alert[]> => {
    await delay(500);
    return [...mockAlerts];
  },

  // POST /api/alerts/{id}/acknowledge
  acknowledgeAlert: async (id: string): Promise<boolean> => {
    await delay(300);
    // Note: In a real app this would call the backend. Here we just return true.
    return true;
  },

  // POST /api/handover
  generateHandover: async (patientId: string, receivingFacility: string) => {
    await delay(1200); // longer delay to simulate AI generation
    const patient = mockPatients.find(p => p.id === patientId);
    if (!patient) throw new Error('Patient not found');
    
    return {
      success: true,
      report: `HANDOVER SUMMARY: ${patient.name} (${patient.mrn})
Transfer to: ${receivingFacility}
Priority: ${patient.priority}

Patient condition deteriorated during night shift. Sepsis protocol initiated at 02:00. Blood cultures drawn, broad-spectrum IV antibiotics started. SpO2 unstable, currently requires 4L O2. Closely monitor BP and urine output.

PENDING TASKS:
- Check AM Labs
- Follow up on Cultures
- Physical Therapy Assessment

Vitals at Handover: BP ${patient.vitals.bloodPressure.systolic}/${patient.vitals.bloodPressure.diastolic}, HR ${patient.vitals.heartRate} bpm.`
    };
  }
};
