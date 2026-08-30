import React, { useState } from 'react';
import { 
  Activity, 
  Lock, 
  Mail, 
  ShieldAlert, 
  UserCheck, 
  Stethoscope, 
  Building2, 
  Pill, 
  TestTube,
  Sparkles,
  CheckCircle2
} from 'lucide-react';

interface LoginProps {
  onLogin: () => void;
}

interface RoleConfig {
  id: string;
  name: string;
  email: string;
  roleTitle: string;
  icon: React.ComponentType<{ className?: string }>;
  color: string;
  badgeBg: string;
}

const ROLES: RoleConfig[] = [
  {
    id: 'super_admin',
    name: 'Super Admin',
    email: 'admin@medmind.ai',
    roleTitle: 'Full System & MLOps Administrator',
    icon: UserCheck,
    color: 'text-purple-600 border-purple-200 bg-purple-50 hover:bg-purple-100',
    badgeBg: 'bg-purple-100 text-purple-800'
  },
  {
    id: 'doctor',
    name: 'Attending Doctor',
    email: 'doctor@medmind.ai',
    roleTitle: 'ICU / Attending Physician',
    icon: Stethoscope,
    color: 'text-brand-600 border-brand-200 bg-brand-50 hover:bg-brand-100',
    badgeBg: 'bg-brand-100 text-brand-800'
  },
  {
    id: 'department',
    name: 'Department Head',
    email: 'department@medmind.ai',
    roleTitle: 'Clinical Operations & Resource Allocation',
    icon: Building2,
    color: 'text-blue-600 border-blue-200 bg-blue-50 hover:bg-blue-100',
    badgeBg: 'bg-blue-100 text-blue-800'
  },
  {
    id: 'pharmacy',
    name: 'Pharmacy Specialist',
    email: 'pharmacy@medmind.ai',
    roleTitle: 'Medication Inventory & Order Fulfiller',
    icon: Pill,
    color: 'text-emerald-600 border-emerald-200 bg-emerald-50 hover:bg-emerald-100',
    badgeBg: 'bg-emerald-100 text-emerald-800'
  },
  {
    id: 'laboratory',
    name: 'Laboratory Analyst',
    email: 'laboratory@medmind.ai',
    roleTitle: 'Diagnostic Lab Reports & Biomarkers',
    icon: TestTube,
    color: 'text-rose-600 border-rose-200 bg-rose-50 hover:bg-rose-100',
    badgeBg: 'bg-rose-100 text-rose-800'
  }
];

export const Login: React.FC<LoginProps> = ({ onLogin }) => {
  const [selectedRole, setSelectedRole] = useState<RoleConfig>(ROLES[1]); // Default Doctor
  const [username, setUsername] = useState<string>(ROLES[1].email);
  const [password, setPassword] = useState<string>('password123');
  const [isLoading, setIsLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const handleSelectRole = (role: RoleConfig) => {
    setSelectedRole(role);
    setUsername(role.email);
    setPassword('password123');
    setErrorMsg(null);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!username.trim() || !password.trim()) {
      setErrorMsg('Please enter valid credentials.');
      return;
    }
    
    setIsLoading(true);
    setErrorMsg(null);
    setTimeout(() => {
      setIsLoading(false);
      onLogin(); // complete login & proceed into platform
    }, 800);
  };

  return (
    <div className="min-h-screen bg-slate-100 flex flex-col justify-center py-10 px-4 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-xl">
        <div className="flex justify-center items-center gap-2 text-brand-800">
          <Activity className="h-10 w-10 text-brand-600 animate-pulse" />
          <span className="text-3xl font-extrabold tracking-tight">MedMind AI</span>
        </div>
        <h2 className="mt-4 text-center text-2xl font-bold tracking-tight text-slate-900">
          Multimodal Clinical Intelligence Platform
        </h2>
        <p className="mt-1 text-center text-xs font-semibold text-slate-500 uppercase tracking-wider">
          Role-Based Access Control & Clinical Decision Support
        </p>
      </div>

      <div className="mt-6 sm:mx-auto sm:w-full sm:max-w-xl">
        <div className="bg-white py-8 px-6 shadow-md border border-slate-200 sm:rounded-xl sm:px-8 space-y-6">
          
          {/* Security Disclaimer Banner */}
          <div className="p-3.5 rounded-lg bg-amber-50 border border-amber-200 flex items-start gap-3">
            <ShieldAlert className="h-5 w-5 text-amber-600 shrink-0 mt-0.5" />
            <div className="text-xs text-amber-800">
              <span className="font-bold">Authorized Clinical Personnel Only: </span>
              Select your role below to populate credentials or enter your clinical account details.
            </div>
          </div>

          {/* Role Selection Grid */}
          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
              1. Select Clinical Access Role
            </label>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
              {ROLES.map((r) => {
                const Icon = r.icon;
                const isSelected = selectedRole.id === r.id;
                return (
                  <button
                    key={r.id}
                    type="button"
                    onClick={() => handleSelectRole(r)}
                    className={`flex items-center gap-3 p-3 rounded-lg border text-left transition-all relative ${
                      isSelected
                        ? 'border-brand-600 bg-brand-50/80 ring-2 ring-brand-500/20 shadow-sm'
                        : 'border-slate-200 hover:border-slate-300 bg-white hover:bg-slate-50/80'
                    }`}
                  >
                    <div className={`p-2 rounded-md ${r.color}`}>
                      <Icon className="h-5 w-5" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-bold text-slate-900 truncate">{r.name}</span>
                        {isSelected && (
                          <CheckCircle2 className="h-4 w-4 text-brand-600 shrink-0 ml-1" />
                        )}
                      </div>
                      <p className="text-[11px] text-slate-500 truncate">{r.roleTitle}</p>
                    </div>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Login Form */}
          <form className="space-y-4 pt-2 border-t border-slate-200" onSubmit={handleSubmit}>
            <div className="flex items-center justify-between">
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider">
                2. Verify Account Credentials
              </label>
              <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${selectedRole.badgeBg}`}>
                Selected: {selectedRole.name}
              </span>
            </div>

            {errorMsg && (
              <div className="p-2.5 rounded bg-red-50 border border-red-200 text-xs text-red-700">
                {errorMsg}
              </div>
            )}

            <div>
              <label htmlFor="username" className="block text-xs font-semibold text-slate-600 mb-1">
                Username / Clinical Email
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Mail className="h-4 w-4 text-slate-400" />
                </div>
                <input
                  id="username"
                  name="username"
                  type="text"
                  required
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="block w-full rounded-md border border-slate-300 py-2 pl-9 pr-3 text-slate-900 text-sm focus:ring-2 focus:ring-brand-500 focus:border-brand-500 bg-slate-50/50"
                  placeholder="name@medmind.ai"
                />
              </div>
            </div>

            <div>
              <label htmlFor="password" className="block text-xs font-semibold text-slate-600 mb-1">
                Password
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Lock className="h-4 w-4 text-slate-400" />
                </div>
                <input
                  id="password"
                  name="password"
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="block w-full rounded-md border border-slate-300 py-2 pl-9 pr-3 text-slate-900 text-sm focus:ring-2 focus:ring-brand-500 focus:border-brand-500 bg-slate-50/50"
                  placeholder="••••••••"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full flex justify-center items-center gap-2 py-2.5 px-4 border border-transparent rounded-md shadow-sm text-sm font-bold text-white bg-brand-600 hover:bg-brand-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-500 transition-colors disabled:opacity-50"
            >
              {isLoading ? (
                <span>Authenticating Credentials...</span>
              ) : (
                <>
                  <Sparkles className="h-4 w-4 fill-white" />
                  <span>Sign In as {selectedRole.name}</span>
                </>
              )}
            </button>
          </form>

        </div>
      </div>
    </div>
  );
};
