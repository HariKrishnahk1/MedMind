export type Priority = 'Stable' | 'Moderate' | 'High' | 'Critical';

export interface Vitals {
  heartRate: number;
  bloodPressure: {
    systolic: number;
    diastolic: number;
  };
  respiratoryRate: number;
  temperature: number;
  oxygenSaturation: number;
}

export interface Patient {
  id: string;
  name: string;
  age: number;
  gender: string;
  mrn: string; // Medical Record Number
  admissionDate: string;
  room: string;
  attendingPhysician: string;
  primaryDiagnosis: string;
  priority: Priority;
  vitals: Vitals;
  codeStatus: 'Full Code' | 'DNR' | 'DNI';
  allergies: string[];
}
