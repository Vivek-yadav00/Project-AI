'use client';

import { useState, useEffect } from 'react';
import { useBackendPing } from '@/hooks/useBackendPing';
import { useBroadcastChannel } from '@/hooks/useBroadcastChannel';
import Link from 'next/link';

export default function Dashboard() {
  const [apiMode, setApiMode] = useState('mock');
  const [apiUrl, setApiUrl] = useState('http://127.0.0.1:8000');
  const [connectionQuality, setConnectionQuality] = useState('full');
  
  const isBackendOnline = useBackendPing(apiUrl);
  
  const { postMessage } = useBroadcastChannel('dadaai_channel', (msg) => {
    // sync
  });

  useEffect(() => {
    const savedMode = localStorage.getItem('dadaai_api_mode');
    if (savedMode) setApiMode(savedMode);
    
    const savedUrl = localStorage.getItem('dadaai_backend_url');
    if (savedUrl) setApiUrl(savedUrl);
    
    const savedQ = localStorage.getItem('dadaai_connection_quality');
    if (savedQ) setConnectionQuality(savedQ);
  }, []);

  const handleModeChange = (mode: string) => {
    setApiMode(mode);
    localStorage.setItem('dadaai_api_mode', mode);
    postMessage({ type: 'CONFIG_CHANGED' });
  };

  const handleUrlChange = (url: string) => {
    setApiUrl(url);
    localStorage.setItem('dadaai_backend_url', url);
  };

  const handleQualityChange = (q: string) => {
    setConnectionQuality(q);
    localStorage.setItem('dadaai_connection_quality', q);
    postMessage({ type: 'CONNECTION_QUALITY', quality: q });
  };

  return (
    <div className="bg-[#0f0c29] min-h-screen text-slate-200">
      <header className="sticky top-0 z-50 px-6 py-3 bg-[#0f0c29]/85 backdrop-blur-md border-b border-purple-500/20">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center">
              <i className="fas fa-microphone-alt text-white text-lg"></i>
            </div>
            <div>
              <h1 className="text-lg font-bold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
                DadaAI <span className="text-xs font-normal text-gray-400">/ VaaniAI</span>
              </h1>
              <p className="text-[10px] text-gray-500 tracking-wider uppercase">Control Dashboard</p>
            </div>
          </div>
          <div className="flex items-center gap-4 text-xs text-gray-400">
            <span className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded-full inline-block" style={{ backgroundColor: isBackendOnline && apiMode === 'live' ? '#22c55e' : '#ef4444' }}></span>
              Backend: <span className={`font-semibold ${isBackendOnline && apiMode === 'live' ? 'text-green-400' : 'text-red-500'}`}>{isBackendOnline && apiMode === 'live' ? 'Online' : 'Offline'}</span>
            </span>
          </div>
        </div>
      </header>

      <main className="relative z-10 max-w-6xl mx-auto px-4 py-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <Link href="/sender" target="_blank" className="p-5 rounded-2xl bg-[#1e1b4b]/50 border border-purple-500/20 hover:border-purple-500/50 transition transform hover:-translate-y-1">
            <div className="flex items-center gap-4">
              <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-blue-500 to-blue-700 flex items-center justify-center shrink-0">
                <i className="fas fa-mobile-alt text-white text-2xl"></i>
              </div>
              <div>
                <h3 className="text-base font-bold text-white">Caregiver Phone (4G)</h3>
                <p className="text-xs text-gray-400 mt-0.5">Open the Caregiver smartphone sender UI in a new tab.</p>
              </div>
            </div>
          </Link>
          <Link href="/receiver" target="_blank" className="p-5 rounded-2xl bg-[#1e1b4b]/50 border border-purple-500/20 hover:border-purple-500/50 transition transform hover:-translate-y-1">
            <div className="flex items-center gap-4">
              <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-purple-500 to-purple-700 flex items-center justify-center shrink-0">
                <i className="fas fa-phone-alt text-white text-2xl"></i>
              </div>
              <div>
                <h3 className="text-base font-bold text-white">Dada Ji Phone (2G)</h3>
                <p className="text-xs text-gray-400 mt-0.5">Open the retro feature phone UI.</p>
              </div>
            </div>
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-[#1e1b4b]/70 backdrop-blur-md border border-purple-500/20 rounded-2xl p-5">
            <h3 className="text-xs font-bold text-purple-300 uppercase tracking-wider mb-4"><i className="fas fa-network-wired mr-1"></i> System Configuration</h3>
            
            <div className="mb-3">
              <label className="text-[10px] text-gray-400 uppercase tracking-wider block mb-1">API Integration Mode</label>
              <select value={apiMode} onChange={(e) => handleModeChange(e.target.value)} className="w-full bg-black/40 text-xs text-white border border-purple-500/30 rounded p-2 outline-none">
                <option value="mock">Local Mock Mode (No backend)</option>
                <option value="live">Live Backend Mode (FastAPI)</option>
              </select>
            </div>

            {apiMode === 'live' && (
              <div className="mb-3">
                <label className="text-[10px] text-gray-400 uppercase tracking-wider block mb-1">Backend Server URL</label>
                <input type="text" value={apiUrl} onChange={(e) => handleUrlChange(e.target.value)} className="w-full bg-black/40 text-xs text-white border border-gray-700 rounded px-2 py-1.5 outline-none" />
              </div>
            )}

            <div className="mb-3 pt-2.5 border-t border-gray-700/30">
              <label className="text-[10px] text-gray-400 uppercase tracking-wider block mb-1">Network/Signal Quality</label>
              <select value={connectionQuality} onChange={(e) => handleQualityChange(e.target.value)} className="w-full bg-black/40 text-xs text-white border border-purple-500/30 rounded p-2 outline-none">
                <option value="full">Full - Voice AI + Screen text</option>
                <option value="low">Low - Screen Text Only (Silent)</option>
                <option value="offline">Offline - Silent Raw SMS Only</option>
              </select>
            </div>
          </div>
          
          <div className="md:col-span-2 bg-[#1e1b4b]/70 backdrop-blur-md border border-purple-500/20 rounded-2xl p-5">
            <h3 className="text-xs font-bold text-purple-300 uppercase tracking-wider mb-4"><i className="fas fa-terminal mr-1"></i> System Log</h3>
            <div className="bg-[#0d1117] border border-purple-500/15 rounded-xl h-[200px] p-3 text-[11px] font-mono text-gray-400">
               Logs are synced via BroadcastChannel across tabs... (For full logs, view browser console).
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
