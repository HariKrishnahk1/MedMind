import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  FlaskConical,
  BookOpen,
  Activity, 
  BrainCircuit,
  Users,
  History,
  ShieldCheck,
  PlayCircle
} from 'lucide-react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: (string | undefined | null | false)[]) {
  return twMerge(clsx(inputs));
}

const navItems = [
  { name: 'AI Research Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { name: 'Model Laboratory', href: '/model-lab', icon: FlaskConical },
  { name: 'Experiment Registry', href: '/experiments', icon: BookOpen },
  { name: 'Model Drift & Quality', href: '/model-monitoring', icon: Activity },
  { name: 'Patient Roster & Risk', href: '/patients', icon: Users },
  { name: 'SHAP & Counterfactuals', href: '/ai-explain', icon: BrainCircuit },
  { name: 'Patient Timeline', href: '/timeline', icon: History },
  { name: 'Queue Workflow Simulation', href: '/simulation', icon: PlayCircle },
];

export const Sidebar: React.FC = () => {
  return (
    <div className="w-64 bg-surface border-r border-slate-200 flex flex-col shadow-sm z-10 hidden md:flex">
      <div className="h-16 flex items-center px-6 border-b border-slate-200">
        <div className="flex items-center gap-2 text-brand-800">
          <BrainCircuit className="h-6 w-6 text-brand-600" />
          <div className="flex flex-col">
            <span className="text-base font-bold tracking-tight leading-none">MedMind AI</span>
            <span className="text-[10px] text-slate-500 font-medium mt-0.5">Clinical Intelligence</span>
          </div>
        </div>
      </div>
      
      <div className="flex-1 overflow-y-auto py-4">
        <div className="px-4 mb-2">
          <p className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">AI Platform Views</p>
        </div>
        <nav className="space-y-1 px-3">
          {navItems.map((item) => (
            <NavLink
              key={item.name}
              to={item.href}
              className={({ isActive }) =>
                cn(
                  'group flex items-center px-3 py-2.5 text-xs font-semibold rounded-md transition-colors',
                  isActive
                    ? 'bg-brand-50 text-brand-700'
                    : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                )
              }
            >
              <item.icon
                className="mr-3 h-4 w-4 flex-shrink-0"
                aria-hidden="true"
              />
              {item.name}
            </NavLink>
          ))}
        </nav>
      </div>

      <div className="p-4 border-t border-slate-200 bg-slate-50/50">
        <div className="flex items-center gap-2 text-xs text-slate-500">
          <ShieldCheck className="h-4 w-4 text-emerald-600 flex-shrink-0" />
          <span>GroupKFold Leakage-Free Validation</span>
        </div>
      </div>
    </div>
  );
};
