import { Priority } from './patient';

export interface Alert {
  id: string;
  patientId: string;
  timestamp: string;
  type: 'Deterioration' | 'Vital Sign Anomaly' | 'Lab Result' | 'System';
  message: string;
  previousPriority?: Priority;
  newPriority: Priority;
  status: 'Unacknowledged' | 'Acknowledged' | 'Resolved';
  reason: string;
  clinicalFactors: string[];
}
