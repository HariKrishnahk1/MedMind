export interface PredictionFactor {
  name: string;
  impact: number; // e.g. 0.8 (high impact)
  direction: 'increase' | 'decrease'; // whether the factor is increasing or decreasing the risk
  currentValue: string;
  normalRange: string;
}

export interface Prediction {
  id: string;
  patientId: string;
  timestamp: string;
  riskScore: number; // 0 to 100
  riskLevel: 'Low' | 'Moderate' | 'High' | 'Critical';
  predictionHorizon: '1h' | '4h' | '12h' | '24h';
  contributingFactors: PredictionFactor[];
  explanationText: string;
}
