import React from 'react';
import { Settings as SettingsIcon, User, Bell, Shield, Database } from 'lucide-react';

export const Settings: React.FC = () => {
  return (
    <div className="p-6 max-w-5xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-2">
          <SettingsIcon className="h-6 w-6 text-brand-600" />
          Settings
        </h1>
        <p className="text-sm text-slate-500">Manage your application preferences and configurations.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="md:col-span-1 space-y-1">
          {[
            { id: 'profile', icon: User, label: 'Profile' },
            { id: 'notifications', icon: Bell, label: 'Notifications' },
            { id: 'security', icon: Shield, label: 'Security' },
            { id: 'data', icon: Database, label: 'Data Integrations' },
          ].map((item, idx) => (
            <button
              key={item.id}
              className={`w-full flex items-center gap-3 px-4 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                idx === 0 
                  ? 'bg-brand-50 text-brand-700' 
                  : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
              }`}
            >
              <item.icon className="h-5 w-5" />
              {item.label}
            </button>
          ))}
        </div>

        <div className="md:col-span-3 bg-white rounded-xl shadow-sm border border-slate-200">
          <div className="p-6 border-b border-slate-100">
            <h2 className="text-lg font-bold text-slate-900 mb-1">Profile Information</h2>
            <p className="text-sm text-slate-500">Update your personal details and clinical role.</p>
          </div>
          
          <div className="p-6 space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <label className="block text-sm font-medium text-slate-700">Full Name</label>
                <input type="text" defaultValue="Dr. Sarah Jenkins" className="w-full px-3 py-2 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:ring-brand-500 focus:border-brand-500 sm:text-sm" />
              </div>
              <div className="space-y-2">
                <label className="block text-sm font-medium text-slate-700">Email Address</label>
                <input type="email" defaultValue="s.jenkins@hospital.org" className="w-full px-3 py-2 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:ring-brand-500 focus:border-brand-500 sm:text-sm" />
              </div>
              <div className="space-y-2">
                <label className="block text-sm font-medium text-slate-700">Role</label>
                <input type="text" defaultValue="Attending Physician - ICU" readOnly className="w-full px-3 py-2 border border-slate-200 bg-slate-50 rounded-md shadow-sm text-slate-500 sm:text-sm" />
              </div>
              <div className="space-y-2">
                <label className="block text-sm font-medium text-slate-700">Department</label>
                <input type="text" defaultValue="Critical Care" readOnly className="w-full px-3 py-2 border border-slate-200 bg-slate-50 rounded-md shadow-sm text-slate-500 sm:text-sm" />
              </div>
            </div>

            <div className="pt-4 flex justify-end">
              <button className="px-4 py-2 bg-brand-600 text-white rounded-lg text-sm font-medium hover:bg-brand-700 transition-colors shadow-sm">
                Save Changes
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
