import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Users, 
  Activity, 
  BrainCircuit,
  Bell,
  ArrowRightLeft,
  Settings,
  History,
  LineChart
} from 'lucide-react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: (string | undefined | null | false)[]) {
  return twMerge(clsx(inputs));
}

const navItems = [
  { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { name: 'Patient List', href: '/patients', icon: Users },
  { name: 'Monitoring', href: '/monitoring', icon: Activity },
  { name: 'AI Explainability', href: '/ai-explain', icon: BrainCircuit },
  { name: 'Patient Timeline', href: '/timeline', icon: History },
  { name: 'Alert Center', href: '/alerts', icon: Bell },
  { name: 'Handover', href: '/handover', icon: ArrowRightLeft },
  { name: 'Research Analytics', href: '/research', icon: LineChart },
];

export const Sidebar: React.FC = () => {
  return (
    <div className="w-64 bg-surface border-r border-slate-200 flex flex-col shadow-sm z-10 hidden md:flex">
      <div className="h-16 flex items-center px-6 border-b border-slate-200">
        <div className="flex items-center gap-2 text-brand-800">
          <Activity className="h-6 w-6 text-brand-600" />
          <span className="text-lg font-bold tracking-tight">Clinical AI</span>
        </div>
      </div>
      
      <div className="flex-1 overflow-y-auto py-4">
        <nav className="space-y-1 px-3">
          {navItems.map((item) => (
            <NavLink
              key={item.name}
              to={item.href}
              className={({ isActive }) =>
                cn(
                  'group flex items-center px-3 py-2.5 text-sm font-medium rounded-md transition-colors',
                  isActive
                    ? 'bg-brand-50 text-brand-700'
                    : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                )
              }
            >
              <item.icon
                className="mr-3 h-5 w-5 flex-shrink-0"
                aria-hidden="true"
              />
              {item.name}
            </NavLink>
          ))}
        </nav>
      </div>

      <div className="p-4 border-t border-slate-200">
        <NavLink
          to="/settings"
          className={({ isActive }) =>
            cn(
              'group flex items-center px-3 py-2.5 text-sm font-medium rounded-md transition-colors',
              isActive
                ? 'bg-brand-50 text-brand-700'
                : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
            )
          }
        >
          <Settings className="mr-3 h-5 w-5 flex-shrink-0" />
          Settings
        </NavLink>
      </div>
    </div>
  );
};
