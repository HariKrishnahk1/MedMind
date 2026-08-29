import React, { useEffect, useState } from 'react';
import { patientService, alertService } from '../services/clinicalServices';
import { Patient } from '../types/patient';
import { Alert } from '../types/alert';
import { Users, AlertTriangle, ArrowUpRight, ArrowDownRight, Activity } from 'lucide-react';
import { Link } from 'react-router-dom';

export const Dashboard: React.FC = () => {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [patientsData, alertsData] = await Promise.all([
          patientService.getPatients(),
          alertService.getAlerts()
        ]);
        setPatients(patientsData);
        setAlerts(alertsData);
      } catch (error) {
        console.error("Failed to fetch data:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return <div className="flex items-center justify-center h-full"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-brand-600"></div></div>;
  }

  const criticalPatients = patients.filter(p => p.priority === 'Critical').length;
  const highRiskPatients = patients.filter(p => p.priority === 'High').length;
  const unacknowledgedAlerts = alerts.filter(a => a.status === 'Unacknowledged').length;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Clinical Overview</h1>
          <p className="text-sm text-slate-500 mt-1">Real-time unit status and AI risk assessments.</p>
        </div>
        <div className="text-xs bg-slate-100 text-slate-600 px-3 py-1.5 rounded-md font-medium flex items-center border border-slate-200">
          <span className="w-2 h-2 rounded-full bg-emerald-500 mr-2 animate-pulse"></span>
          Live Monitoring Active
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-surface rounded-xl p-5 border border-slate-200 shadow-sm flex flex-col justify-between">
          <div className="flex justify-between items-start">
            <p className="text-sm font-medium text-slate-500">Total Patients</p>
            <div className="p-2 bg-slate-50 rounded-lg">
              <Users className="h-4 w-4 text-slate-400" />
            </div>
          </div>
          <div className="mt-4 flex items-baseline gap-2">
            <span className="text-3xl font-bold text-slate-900">{patients.length}</span>
          </div>
        </div>

        <div className="bg-surface rounded-xl p-5 border border-slate-200 shadow-sm flex flex-col justify-between relative overflow-hidden">
          <div className="absolute top-0 right-0 w-16 h-16 bg-risk-critical/5 rounded-bl-full -z-0"></div>
          <div className="flex justify-between items-start z-10">
            <p className="text-sm font-medium text-slate-500">Critical Priority</p>
            <div className="p-2 bg-rose-50 rounded-lg border border-rose-100">
              <Activity className="h-4 w-4 text-risk-critical" />
            </div>
          </div>
          <div className="mt-4 flex items-baseline gap-2 z-10">
            <span className="text-3xl font-bold text-slate-900">{criticalPatients}</span>
            <span className="text-sm text-slate-500 font-medium">patient(s)</span>
          </div>
        </div>

        <div className="bg-surface rounded-xl p-5 border border-slate-200 shadow-sm flex flex-col justify-between">
          <div className="flex justify-between items-start">
            <p className="text-sm font-medium text-slate-500">High Risk</p>
            <div className="p-2 bg-orange-50 rounded-lg border border-orange-100">
              <ArrowUpRight className="h-4 w-4 text-risk-high" />
            </div>
          </div>
          <div className="mt-4 flex items-baseline gap-2">
            <span className="text-3xl font-bold text-slate-900">{highRiskPatients}</span>
          </div>
        </div>

        <div className="bg-surface rounded-xl p-5 border border-rose-200 shadow-sm flex flex-col justify-between ring-1 ring-rose-100">
          <div className="flex justify-between items-start">
            <p className="text-sm font-medium text-slate-800">Action Required</p>
            <div className="p-2 bg-rose-100 rounded-lg">
              <AlertTriangle className="h-4 w-4 text-risk-critical" />
            </div>
          </div>
          <div className="mt-4 flex flex-col">
            <span className="text-3xl font-bold text-risk-critical">{unacknowledgedAlerts}</span>
            <span className="text-xs text-rose-600 font-medium mt-1">Unacknowledged Alerts</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Priority Queue List */}
        <div className="lg:col-span-2 bg-surface border border-slate-200 rounded-xl shadow-sm overflow-hidden flex flex-col">
          <div className="px-5 py-4 border-b border-slate-200 flex justify-between items-center bg-slate-50/50">
            <h2 className="text-base font-semibold text-slate-900">Priority Queue</h2>
            <Link to="/patients" className="text-sm text-brand-600 hover:text-brand-700 font-medium">View all</Link>
          </div>
          <div className="flex-1 overflow-x-auto">
            <table className="min-w-full divide-y divide-slate-200">
              <thead className="bg-slate-50">
                <tr>
                  <th scope="col" className="px-5 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Patient</th>
                  <th scope="col" className="px-5 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Location</th>
                  <th scope="col" className="px-5 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Priority</th>
                  <th scope="col" className="px-5 py-3 text-right text-xs font-medium text-slate-500 uppercase tracking-wider">Action</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-slate-200">
                {patients.sort((a, b) => {
                  const priorities = { 'Critical': 4, 'High': 3, 'Moderate': 2, 'Stable': 1 };
                  return priorities[b.priority] - priorities[a.priority];
                }).map((patient) => (
                  <tr key={patient.id} className="hover:bg-slate-50 transition-colors">
                    <td className="px-5 py-4 whitespace-nowrap">
                      <div className="flex flex-col">
                        <span className="text-sm font-medium text-slate-900">{patient.name}</span>
                        <span className="text-xs text-slate-500">{patient.mrn} • {patient.age}y {patient.gender.charAt(0)}</span>
                      </div>
                    </td>
                    <td className="px-5 py-4 whitespace-nowrap text-sm text-slate-600">
                      {patient.room}
                    </td>
                    <td className="px-5 py-4 whitespace-nowrap">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border
                        ${patient.priority === 'Critical' ? 'bg-rose-50 text-risk-critical border-rose-200' : ''}
                        ${patient.priority === 'High' ? 'bg-orange-50 text-risk-high border-orange-200' : ''}
                        ${patient.priority === 'Moderate' ? 'bg-amber-50 text-risk-moderate border-amber-200' : ''}
                        ${patient.priority === 'Stable' ? 'bg-emerald-50 text-risk-low border-emerald-200' : ''}
                      `}>
                        {patient.priority}
                      </span>
                    </td>
                    <td className="px-5 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <Link to={`/patients/${patient.id}`} className="text-brand-600 hover:text-brand-900">Profile</Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Recent Alerts */}
        <div className="bg-surface border border-slate-200 rounded-xl shadow-sm flex flex-col h-[400px]">
          <div className="px-5 py-4 border-b border-slate-200 bg-slate-50/50 flex justify-between items-center">
            <h2 className="text-base font-semibold text-slate-900">Recent Alerts</h2>
          </div>
          <div className="p-4 flex-1 overflow-y-auto space-y-4">
            {alerts.map(alert => (
              <div key={alert.id} className={`p-4 rounded-lg border ${alert.status === 'Unacknowledged' ? 'bg-rose-50 border-rose-100' : 'bg-white border-slate-200'}`}>
                <div className="flex justify-between items-start mb-2">
                  <div className="flex items-center gap-2">
                    {alert.status === 'Unacknowledged' && <div className="w-2 h-2 rounded-full bg-risk-critical animate-pulse"></div>}
                    <span className="text-xs font-bold text-slate-700 uppercase tracking-wider">{alert.type}</span>
                  </div>
                  <span className="text-xs text-slate-500">{new Date(alert.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</span>
                </div>
                <p className="text-sm font-medium text-slate-900">{alert.message}</p>
                <div className="mt-2 text-xs text-slate-600 bg-white/60 p-2 rounded border border-slate-100">
                  Patient: <span className="font-medium text-slate-900">{patients.find(p => p.id === alert.patientId)?.name || alert.patientId}</span>
                </div>
                {alert.status === 'Unacknowledged' && (
                  <button className="mt-3 w-full bg-white border border-slate-300 text-slate-700 text-xs font-medium py-1.5 rounded hover:bg-slate-50 transition-colors shadow-sm">
                    Review Alert
                  </button>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
