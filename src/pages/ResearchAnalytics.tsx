import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line } from 'recharts';
import { LineChart as LineChartIcon, Users, Activity, TrendingDown } from 'lucide-react';

const outcomeData = [
  { month: 'Jan', successful: 45, complications: 12 },
  { month: 'Feb', successful: 52, complications: 10 },
  { month: 'Mar', successful: 48, complications: 15 },
  { month: 'Apr', successful: 61, complications: 8 },
  { month: 'May', successful: 59, complications: 9 },
  { month: 'Jun', successful: 67, complications: 7 },
];

const aiAccuracyData = [
  { week: 'W1', accuracy: 88 },
  { week: 'W2', accuracy: 89 },
  { week: 'W3', accuracy: 91 },
  { week: 'W4', accuracy: 93 },
  { week: 'W5', accuracy: 92 },
  { week: 'W6', accuracy: 95 },
];

export const ResearchAnalytics: React.FC = () => {
  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-2">
          <LineChartIcon className="h-6 w-6 text-brand-600" />
          Research & Analytics
        </h1>
        <p className="text-sm text-slate-500">Retrospective analysis of patient outcomes and AI performance metrics.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-blue-50 text-blue-600 rounded-lg"><Users className="h-5 w-5" /></div>
            <h3 className="font-semibold text-slate-700">Total Patients Analyzed</h3>
          </div>
          <p className="text-3xl font-bold text-slate-900">1,248</p>
          <p className="text-sm text-green-600 mt-1 flex items-center gap-1 font-medium">+12% from last month</p>
        </div>
        
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-purple-50 text-purple-600 rounded-lg"><Activity className="h-5 w-5" /></div>
            <h3 className="font-semibold text-slate-700">AI Alert Accuracy</h3>
          </div>
          <p className="text-3xl font-bold text-slate-900">94.2%</p>
          <p className="text-sm text-green-600 mt-1 flex items-center gap-1 font-medium">+2.1% improvement</p>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-green-50 text-green-600 rounded-lg"><TrendingDown className="h-5 w-5" /></div>
            <h3 className="font-semibold text-slate-700">Avg. Length of Stay</h3>
          </div>
          <p className="text-3xl font-bold text-slate-900">4.1 Days</p>
          <p className="text-sm text-green-600 mt-1 flex items-center gap-1 font-medium">-0.8 days vs baseline</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <h2 className="text-lg font-bold text-slate-900 mb-4">Patient Outcomes (6 Months)</h2>
          <div className="h-80 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={outcomeData} margin={{ top: 20, right: 30, left: 0, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                <XAxis dataKey="month" axisLine={false} tickLine={false} />
                <YAxis axisLine={false} tickLine={false} />
                <Tooltip cursor={{ fill: '#f8fafc' }} contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
                <Legend iconType="circle" />
                <Bar dataKey="successful" name="Successful Discharges" fill="#0ea5e9" radius={[4, 4, 0, 0]} />
                <Bar dataKey="complications" name="Complications/Transfers" fill="#f43f5e" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <h2 className="text-lg font-bold text-slate-900 mb-4">AI Prediction Accuracy Trend</h2>
          <div className="h-80 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={aiAccuracyData} margin={{ top: 20, right: 30, left: 0, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                <XAxis dataKey="week" axisLine={false} tickLine={false} />
                <YAxis domain={['dataMin - 2', 'dataMax + 2']} axisLine={false} tickLine={false} />
                <Tooltip contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
                <Line type="monotone" dataKey="accuracy" name="Accuracy (%)" stroke="#8b5cf6" strokeWidth={3} dot={{ r: 4, strokeWidth: 2 }} activeDot={{ r: 6 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};
