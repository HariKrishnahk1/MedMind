import type { Patient } from '../types/patient';
import type { Alert } from '../types/alert';
import type { TimelineEvent } from '../types/timeline';
import type { Prediction } from '../types/predictions';

export const mockPatients: Patient[] = [
  {
    id: 'P-1001',
    name: 'Sarah Jenkins',
    age: 68,
    gender: 'Female',
    mrn: 'MRN-847291',
    admissionDate: '2026-08-27T08:30:00Z',
    room: 'ICU-04',
    attendingPhysician: 'Dr. Robert Chen',
    primaryDiagnosis: 'Sepsis secondary to pneumonia',
    priority: 'Critical',
    codeStatus: 'Full Code',
    allergies: ['Penicillin'],
    vitals: {
      heartRate: 118,
      bloodPressure: { systolic: 88, diastolic: 54 },
      respiratoryRate: 26,
      temperature: 39.2,
      oxygenSaturation: 89,
    },
  },
  {
    id: 'P-1002',
    name: 'Michael Chang',
    age: 54,
    gender: 'Male',
    mrn: 'MRN-339201',
    admissionDate: '2026-08-28T14:15:00Z',
    room: 'Ward-B-12',
    attendingPhysician: 'Dr. Sarah Jenkins',
    primaryDiagnosis: 'Post-op CABG (Day 2)',
    priority: 'Moderate',
    codeStatus: 'Full Code',
    allergies: ['Latex', 'Sulfa'],
    vitals: {
      heartRate: 88,
      bloodPressure: { systolic: 115, diastolic: 75 },
      respiratoryRate: 16,
      temperature: 37.4,
      oxygenSaturation: 95,
    },
  },
  {
    id: 'P-1003',
    name: 'Emily Davis',
    age: 42,
    gender: 'Female',
    mrn: 'MRN-112349',
    admissionDate: '2026-08-29T09:00:00Z',
    room: 'Ward-A-05',
    attendingPhysician: 'Dr. James Wilson',
    primaryDiagnosis: 'Acute Asthma Exacerbation',
    priority: 'Stable',
    codeStatus: 'Full Code',
    allergies: ['None'],
    vitals: {
      heartRate: 76,
      bloodPressure: { systolic: 120, diastolic: 80 },
      respiratoryRate: 14,
      temperature: 36.8,
      oxygenSaturation: 98,
    },
  },
  {
    id: 'P-1004',
    name: 'Robert Taylor',
    age: 77,
    gender: 'Male',
    mrn: 'MRN-998273',
    admissionDate: '2026-08-25T11:20:00Z',
    room: 'ICU-02',
    attendingPhysician: 'Dr. Emily Stone',
    primaryDiagnosis: 'Congestive Heart Failure',
    priority: 'High',
    codeStatus: 'DNR',
    allergies: ['Aspirin'],
    vitals: {
      heartRate: 105,
      bloodPressure: { systolic: 150, diastolic: 95 },
      respiratoryRate: 22,
      temperature: 37.1,
      oxygenSaturation: 91,
    },
  }
];

export const mockAlerts: Alert[] = [
  {
    id: 'ALT-501',
    patientId: 'P-1001',
    timestamp: '2026-08-29T14:30:00Z',
    type: 'Deterioration',
    message: 'Rapid decline in SpO2 and BP',
    previousPriority: 'High',
    newPriority: 'Critical',
    status: 'Unacknowledged',
    reason: 'Sepsis protocol triggered by AI Risk Assessment',
    clinicalFactors: ['SpO2 dropped from 94% to 89% in 1 hr', 'Systolic BP dropped to 88'],
  },
  {
    id: 'ALT-502',
    patientId: 'P-1004',
    timestamp: '2026-08-29T13:45:00Z',
    type: 'Vital Sign Anomaly',
    message: 'Increased respiratory rate and decreasing SpO2',
    previousPriority: 'Moderate',
    newPriority: 'High',
    status: 'Acknowledged',
    reason: 'Potential fluid overload',
    clinicalFactors: ['Respiratory rate increased to 22', 'SpO2 91%'],
  }
];

export const mockPredictions: Record<string, Prediction[]> = {
  'P-1001': [
    {
      id: 'PRED-991',
      patientId: 'P-1001',
      timestamp: '2026-08-29T14:30:00Z',
      riskScore: 87,
      riskLevel: 'Critical',
      predictionHorizon: '4h',
      contributingFactors: [
        { name: 'Systolic BP', impact: 0.45, direction: 'decrease', currentValue: '88 mmHg', normalRange: '90-120' },
        { name: 'SpO2', impact: 0.35, direction: 'decrease', currentValue: '89%', normalRange: '>92%' },
        { name: 'Heart Rate', impact: 0.20, direction: 'increase', currentValue: '118 bpm', normalRange: '60-100' }
      ],
      explanationText: 'AI Risk Assessment indicates a high probability of further decompensation due to septic shock trajectory.'
    }
  ]
};

export const mockTimelines: Record<string, TimelineEvent[]> = {
  'P-1001': [
    {
      id: 'TL-101',
      patientId: 'P-1001',
      timestamp: '2026-08-27T08:30:00Z',
      type: 'Admission',
      title: 'Admitted to ED',
      description: 'Patient presented with fever and shortness of breath.',
      priorityAtTime: 'Moderate'
    },
    {
      id: 'TL-102',
      patientId: 'P-1001',
      timestamp: '2026-08-28T10:00:00Z',
      type: 'Priority Change',
      title: 'Priority Upgraded to High',
      description: 'Patient transferred to ICU due to worsening respiratory status.',
      priorityAtTime: 'High'
    },
    {
      id: 'TL-103',
      patientId: 'P-1001',
      timestamp: '2026-08-29T14:30:00Z',
      type: 'Alert',
      title: 'Critical Deterioration Alert',
      description: 'AI Risk Assessment triggered Critical alert for sepsis trajectory.',
      priorityAtTime: 'Critical'
    }
  ]
};
