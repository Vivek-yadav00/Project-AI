'use client';
import { useState, useEffect, useRef } from 'react';
import { useBroadcastChannel } from '@/hooks/useBroadcastChannel';

type Message = { id: string; text: string; type: 'sent' | 'received' };

export default function Sender() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');
  const [mode, setMode] = useState('mock');
  const [apiUrl, setApiUrl] = useState('http://127.0.0.1:8000');
  const chatEndRef = useRef<HTMLDivElement>(null);

  const { postMessage } = useBroadcastChannel('dadaai_channel', (msg) => {
    if (msg.type === 'CONFIG_CHANGED') loadSettings();
  });

  const loadSettings = () => {
    setMode(localStorage.getItem('dadaai_api_mode') || 'mock');
    setApiUrl(localStorage.getItem('dadaai_backend_url') || 'http://127.0.0.1:8000');
  };

  useEffect(() => {
    loadSettings();
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const addChatBubble = (text: string, type: 'sent' | 'received') => {
    setMessages(prev => [...prev, { id: Math.random().toString(), text, type }]);
  };

  const doSend = async (text: string) => {
    if (!text.trim()) return;
    addChatBubble(text, 'sent');
    postMessage({ type: 'LOG', level: 'info', text: `4G phone sent SMS: "${text}"` });

    if (mode === 'live') {
      postMessage({ type: 'LOG', level: 'info', text: `POST ${apiUrl}/api/v1/sms/incoming ...` });
      try {
        const res = await fetch(`${apiUrl}/api/v1/sms/incoming`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ from_number: '+919876543210', body: text })
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const resData = await res.json();
        postMessage({ type: 'LOG', level: 'success', text: `FastAPI responded. Body: "${resData.body}"` });
        addChatBubble(`🤖 AI (Backend): ${resData.body}`, 'received');
        
        postMessage({ type: 'LIVE_SMS_ARRIVED', original: text, display: resData.body, wasAI: true });
      } catch (err: any) {
        postMessage({ type: 'LOG', level: 'error', text: `Failed live route: ${err.message}` });
        addChatBubble(`⚠️ Error sending live SMS. Is Backend running?`, 'received');
      }
    } else {
      postMessage({ type: 'SMS_SENT', text });
    }
  };

  const handleSendSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    doSend(inputText);
    setInputText('');
  };

  return (
    <div className="bg-[#0f0c29] min-h-screen text-slate-200 flex flex-col items-center justify-center p-6">
      <div className="mb-6 flex flex-col items-center">
        <h2 className="text-sm font-bold text-blue-400 tracking-wider uppercase flex items-center gap-2">
          <i className="fas fa-paper-plane"></i> Caregiver Terminal (4G)
        </h2>
        <div className="text-[10px] text-gray-500 mt-1 flex items-center gap-1.5">
          Mode: {mode === 'live' ? 'Live (FastAPI)' : 'Mock'}
          <span className={`w-1.5 h-1.5 rounded-full ${mode === 'live' ? 'bg-purple-500' : 'bg-gray-500'}`}></span>
        </div>
      </div>

      <div className="w-[320px] h-[650px] bg-[#111] rounded-[40px] p-3 shadow-2xl relative border-4 border-gray-800">
        <div className="absolute top-0 left-1/2 transform -translate-x-1/2 w-32 h-6 bg-gray-800 rounded-b-xl z-20"></div>
        
        <div className="bg-[#0f172a] w-full h-full rounded-[30px] overflow-hidden flex flex-col relative">
          <div className="h-12 bg-[#1e293b] flex items-center px-4 justify-between shrink-0 z-10 border-b border-gray-700/50">
            <div className="text-white font-semibold text-xs mt-1">11:37</div>
            <div className="flex items-center gap-1.5 text-gray-400 mt-1">
              <i className="fas fa-signal text-[10px]"></i>
              <span className="text-[10px] font-bold">5G</span>
              <i className="fas fa-battery-three-quarters text-[10px]"></i>
            </div>
          </div>
          
          <div className="p-3 bg-[#1e293b] flex items-center gap-3 shrink-0 border-b border-gray-700/50 shadow-sm z-10">
            <div className="w-8 h-8 rounded-full bg-pink-500 flex items-center justify-center text-white font-bold text-xs shadow-inner">
              दा
            </div>
            <div className="flex-1">
              <h3 className="text-white text-sm font-bold">Dada Ji</h3>
              <p className="text-green-400 text-[9px] font-medium tracking-wide">Sync Active</p>
            </div>
            <div className="flex gap-3 text-gray-400 text-sm">
              <i className="fas fa-phone"></i>
              <i className="fas fa-ellipsis-v"></i>
            </div>
          </div>

          <div className="flex-1 overflow-y-auto p-3 flex flex-col gap-3 custom-scrollbar" style={{ backgroundImage: "radial-gradient(circle at center, #1e293b 0%, #0f172a 100%)" }}>
            {messages.map((m) => (
              <div key={m.id} className={`max-w-[85%] rounded-2xl p-3 text-xs shadow-sm ${m.type === 'sent' ? 'bg-blue-600 text-white self-end rounded-tr-sm' : 'bg-[#1e293b] text-gray-200 border border-gray-700/50 self-start rounded-tl-sm'}`}>
                {m.text}
              </div>
            ))}
            <div ref={chatEndRef}></div>
          </div>

          <div className="p-3 bg-[#0f172a] border-t border-gray-800 shrink-0 relative z-10">
            <form onSubmit={handleSendSubmit} className="flex gap-2">
              <input type="text" value={inputText} onChange={(e) => setInputText(e.target.value)} placeholder="Type message to Dada Ji..." className="flex-1 bg-[#1e293b] text-white text-xs rounded-full px-4 py-2.5 outline-none border border-gray-700 focus:border-blue-500 transition-colors" />
              <button type="submit" className="w-9 h-9 rounded-full bg-blue-600 text-white flex items-center justify-center hover:bg-blue-700 transition-transform active:scale-95 shadow-md">
                <i className="fas fa-paper-plane text-xs -ml-0.5"></i>
              </button>
            </form>
            
            <div className="mt-3 flex flex-wrap gap-2">
              <button type="button" onClick={() => doSend("Dada ji kal 5 baje ghar aa jana")} className="bg-[#1e293b] hover:bg-blue-900/40 text-blue-300 text-[9px] border border-blue-900/50 px-2.5 py-1.5 rounded-full transition-colors truncate max-w-full">
                Dada ji kal 5 baje ghar aa jana
              </button>
              <button type="button" onClick={() => doSend("Your OTP is 483921")} className="bg-[#1e293b] hover:bg-blue-900/40 text-blue-300 text-[9px] border border-blue-900/50 px-2.5 py-1.5 rounded-full transition-colors truncate max-w-full">
                Your OTP is 483921
              </button>
              <button type="button" onClick={() => doSend("Your electricity bill of Rs 850 is due")} className="bg-[#1e293b] hover:bg-blue-900/40 text-blue-300 text-[9px] border border-blue-900/50 px-2.5 py-1.5 rounded-full transition-colors truncate max-w-full">
                Your electricity bill of Rs 850 is due
              </button>
              <button type="button" onClick={() => doSend("Dawa le lena")} className="bg-[#1e293b] hover:bg-blue-900/40 text-blue-300 text-[9px] border border-blue-900/50 px-2.5 py-1.5 rounded-full transition-colors truncate max-w-full">
                Dawa le lena
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
