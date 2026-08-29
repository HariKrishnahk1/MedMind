import { Priority } from './patient';

export interface TimelineEvent {
  id: string;
  patientId: string;
  timestamp: string;
  type: 'Admission' | 'Vitals Update' | 'Priority Change' | 'Alert' | 'Intervention' | 'Note';
  title: string;
  description: string;
  priorityAtTime: Priority;
  metadata?: any;
}
