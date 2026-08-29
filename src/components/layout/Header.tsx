import React from 'react';
import { Bell, Search, User } from 'lucide-react';

export const Header: React.FC = () => {
  return (
    <header className="h-16 bg-surface border-b border-slate-200 flex items-center justify-between px-6 z-10 shadow-sm">
      <div className="flex items-center flex-1">
        <div className="relative w-full max-w-md hidden sm:block">
          <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
            <Search className="h-4 w-4 text-slate-400" />
          </div>
          <input
            type="text"
            className="block w-full rounded-md border-0 py-1.5 pl-10 pr-3 text-slate-900 ring-1 ring-inset ring-slate-300 placeholder:text-slate-400 focus:ring-2 focus:ring-inset focus:ring-brand-500 sm:text-sm sm:leading-6 bg-slate-50 transition-shadow"
            placeholder="Search patients (MRN, Name)..."
          />
        </div>
      </div>
      
      <div className="flex items-center gap-4">
        <button className="relative p-2 text-slate-400 hover:text-slate-500 transition-colors rounded-full hover:bg-slate-100">
          <span className="sr-only">View notifications</span>
          <Bell className="h-5 w-5" />
          <span className="absolute top-1.5 right-1.5 block h-2 w-2 rounded-full bg-risk-critical ring-2 ring-white" />
        </button>
        
        <div className="flex items-center gap-3 border-l border-slate-200 pl-4 ml-2">
          <div className="flex flex-col items-end hidden sm:flex">
            <span className="text-sm font-medium text-slate-900 leading-none">Dr. Sarah Jenkins</span>
            <span className="text-xs text-slate-500 mt-1">Attending ICU</span>
          </div>
          <div className="h-8 w-8 rounded-full bg-brand-100 flex items-center justify-center text-brand-600 border border-brand-200">
            <User className="h-4 w-4" />
          </div>
        </div>
      </div>
    </header>
  );
};
